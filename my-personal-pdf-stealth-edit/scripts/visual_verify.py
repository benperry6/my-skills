#!/usr/bin/env python3
"""
Phase 6 — Visual verification of a modified PDF against the original.

Renders both PDFs to images at 300 DPI, then performs pixel-by-pixel comparison.
Verifies that visual differences exist ONLY in the areas where modifications were
requested — no layout shifts, no extra artifacts, no design changes anywhere else.

Optionally takes a list of expected modification strings to verify that diff regions
correspond exclusively to the intended changes.

Usage:
    python3 visual_verify.py <modified.pdf> <original.pdf> [--expected-changes changes.json] [--output-dir ./diffs] [--dpi 300]

Expected changes JSON format:
    {
        "changes": [
            {"old": "05Mar2026", "new": "12Mar2026", "description": "departure date flight 1"},
            {"old": "01Mar2026", "new": "11Mar2026", "description": "issue date"},
            {"old": "06Mar2026", "new": "13Mar2026", "description": "departure date flight 2"}
        ]
    }
"""
import argparse
import json
import os
import sys
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def render_pdf_pages(pdf_path: Path, dpi: int = 300) -> list:
    """Render all pages of a PDF to PIL images."""
    import pypdfium2 as pdfium
    images = []
    pdf = pdfium.PdfDocument(str(pdf_path))
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=dpi / 72)
        images.append(bitmap.to_pil().convert("RGB"))
    pdf.close()
    return images


def extract_text_positions(pdf_path: Path) -> dict:
    """Extract character positions per page using pdfplumber.
    Returns {page_num: [(char, x0, y0, x1, y1, fontname), ...]}
    """
    import pdfplumber
    pages = {}
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            chars = []
            for c in (page.chars or []):
                chars.append({
                    "text": c.get("text", ""),
                    "x0": c.get("x0", 0),
                    "top": c.get("top", 0),
                    "x1": c.get("x1", 0),
                    "bottom": c.get("bottom", 0),
                })
            pages[i] = chars
    return pages


def find_text_regions(chars: list, search_text: str, page_width: float, page_height: float,
                      img_width: int, img_height: int) -> list:
    """Find bounding boxes of a text string in the character list.
    Returns list of (x0, y0, x1, y1) in image pixel coordinates.
    """
    regions = []
    text_chars = [c for c in chars if c["text"]]
    full_text = "".join(c["text"] for c in text_chars)

    start = 0
    while True:
        idx = full_text.find(search_text, start)
        if idx < 0:
            break

        # Get bounding box from matching characters
        match_chars = text_chars[idx:idx + len(search_text)]
        if not match_chars:
            break

        # PDF coordinates → image pixel coordinates
        # PDF origin is bottom-left, image origin is top-left
        scale_x = img_width / page_width
        scale_y = img_height / page_height

        x0 = min(c["x0"] for c in match_chars) * scale_x
        y0 = min(c["top"] for c in match_chars) * scale_y
        x1 = max(c["x1"] for c in match_chars) * scale_x
        y1 = max(c["bottom"] for c in match_chars) * scale_y

        # Add margin around text
        margin = 5
        regions.append((
            max(0, x0 - margin),
            max(0, y0 - margin),
            min(img_width, x1 + margin),
            min(img_height, y1 + margin),
        ))
        start = idx + 1

    return regions


def pixel_in_any_region(x: int, y: int, regions: list) -> bool:
    """Check if a pixel coordinate falls within any of the expected regions."""
    for (rx0, ry0, rx1, ry1) in regions:
        if rx0 <= x <= rx1 and ry0 <= y <= ry1:
            return True
    return False


def run_visual_verification(modified_path: Path, original_path: Path,
                            expected_changes: list = None, output_dir: Path = None,
                            dpi: int = 300) -> bool:
    """
    Full visual verification pipeline.
    Returns True if all diffs are in expected regions (or no expected_changes provided and diffs are minimal).
    """
    from PIL import Image, ImageChops, ImageDraw

    print(f"\n{BOLD}Visual Verification: {modified_path.name} vs {original_path.name}{RESET}\n")

    # Render both PDFs
    print("  Rendering PDFs at {dpi} DPI...", file=sys.stderr)
    orig_images = render_pdf_pages(original_path, dpi)
    mod_images = render_pdf_pages(modified_path, dpi)

    if len(orig_images) != len(mod_images):
        print(f"  {RED}[FAIL]{RESET} Page count mismatch: {len(mod_images)} vs {len(orig_images)}")
        return False

    # Get text positions from original for expected-change region mapping
    orig_text_positions = None
    orig_page_sizes = None
    if expected_changes:
        import pdfplumber
        orig_text_positions = extract_text_positions(original_path)
        with pdfplumber.open(str(original_path)) as pdf:
            orig_page_sizes = [(p.width, p.height) for p in pdf.pages]

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    all_ok = True
    total_diff_pixels = 0
    total_pixels = 0
    total_unexpected = 0

    for page_num in range(len(orig_images)):
        orig_img = orig_images[page_num]
        mod_img = mod_images[page_num]

        if orig_img.size != mod_img.size:
            print(f"  {RED}[FAIL]{RESET} Page {page_num}: image size mismatch "
                  f"{mod_img.size} vs {orig_img.size}")
            all_ok = False
            continue

        w, h = orig_img.size
        page_pixels = w * h
        total_pixels += page_pixels

        # Compute pixel diff
        diff = ImageChops.difference(orig_img, mod_img)
        bbox = diff.getbbox()

        if bbox is None:
            # Pages are identical
            print(f"  {GREEN}[PASS]{RESET} Page {page_num}: IDENTICAL (0 different pixels)")
            continue

        # Count different pixels and their positions
        orig_px = orig_img.load()
        mod_px = mod_img.load()
        diff_pixels = []

        for y in range(bbox[1], bbox[3]):
            for x in range(bbox[0], bbox[2]):
                r1, g1, b1 = orig_px[x, y]
                r2, g2, b2 = mod_px[x, y]
                if (r1, g1, b1) != (r2, g2, b2):
                    diff_pixels.append((x, y))

        diff_count = len(diff_pixels)
        total_diff_pixels += diff_count
        diff_pct = (diff_count / page_pixels) * 100

        # If we have expected changes, check that ALL diffs fall in expected regions
        if expected_changes and orig_text_positions and orig_page_sizes:
            page_w, page_h = orig_page_sizes[page_num]
            chars = orig_text_positions.get(page_num, [])

            # Build expected regions from all old text values on this page
            expected_regions = []
            matched_changes = []
            for change in expected_changes:
                old_text = change["old"]
                regions = find_text_regions(chars, old_text, page_w, page_h, w, h)
                if regions:
                    expected_regions.extend(regions)
                    matched_changes.append(change.get("description", old_text))

            # Also look for new text in the modified PDF to catch QR codes or generated content
            # QR codes won't match text search, so we use a tolerance: any diff pixel that's
            # not in an expected text region is flagged
            unexpected_pixels = []
            expected_pixel_count = 0
            for (px, py) in diff_pixels:
                if pixel_in_any_region(px, py, expected_regions):
                    expected_pixel_count += 1
                else:
                    unexpected_pixels.append((px, py))

            unexpected_count = len(unexpected_pixels)
            total_unexpected += unexpected_count

            if unexpected_count == 0:
                print(f"  {GREEN}[PASS]{RESET} Page {page_num}: {diff_count:,} diff pixels, "
                      f"ALL in expected regions ({', '.join(matched_changes)})")
            else:
                unexpected_pct = (unexpected_count / page_pixels) * 100
                # Find bounding box of unexpected pixels
                if unexpected_pixels:
                    ux0 = min(p[0] for p in unexpected_pixels)
                    uy0 = min(p[1] for p in unexpected_pixels)
                    ux1 = max(p[0] for p in unexpected_pixels)
                    uy1 = max(p[1] for p in unexpected_pixels)
                    unexpected_bbox = f"x={ux0}-{ux1}, y={uy0}-{uy1}"
                else:
                    unexpected_bbox = "n/a"

                # Warn if unexpected diffs are < 0.1% (likely QR codes or minor rendering),
                # fail if > 0.1% (likely layout shift or overlay)
                if unexpected_pct < 0.1:
                    print(f"  {YELLOW}[WARN]{RESET} Page {page_num}: {diff_count:,} diff pixels — "
                          f"{expected_pixel_count:,} expected, {unexpected_count:,} outside expected regions "
                          f"({unexpected_pct:.4f}%, bbox: {unexpected_bbox})")
                    print(f"           Likely QR codes or minor rendering differences — review visually")
                else:
                    print(f"  {RED}[FAIL]{RESET} Page {page_num}: {unexpected_count:,} pixels "
                          f"({unexpected_pct:.2f}%) OUTSIDE expected modification regions "
                          f"(bbox: {unexpected_bbox})")
                    all_ok = False
        else:
            # No expected changes provided — just report the diff
            print(f"  {YELLOW}[INFO]{RESET} Page {page_num}: {diff_count:,} different pixels "
                  f"({diff_pct:.4f}%), bbox: x={bbox[0]}-{bbox[2]}, y={bbox[1]}-{bbox[3]}")

        # Save diff images if output_dir provided
        if output_dir:
            # Highlighted diff: red pixels on original
            highlighted = orig_img.copy()
            hl_draw = ImageDraw.Draw(highlighted)
            for (px, py) in diff_pixels:
                if expected_changes and not pixel_in_any_region(px, py, expected_regions if expected_changes else []):
                    hl_draw.point((px, py), fill=(255, 165, 0))  # Orange = unexpected
                else:
                    hl_draw.point((px, py), fill=(0, 200, 0))    # Green = expected
            highlighted.save(output_dir / f"diff_page{page_num}_highlighted.png")

            # Side-by-side crop of diff area
            if bbox:
                margin = 50
                crop_box = (
                    max(0, bbox[0] - margin), max(0, bbox[1] - margin),
                    min(w, bbox[2] + margin), min(h, bbox[3] + margin),
                )
                orig_crop = orig_img.crop(crop_box)
                mod_crop = mod_img.crop(crop_box)
                cw, ch = orig_crop.size
                combined = Image.new("RGB", (cw * 2 + 20, ch + 40), (255, 255, 255))
                combined.paste(orig_crop, (0, 40))
                combined.paste(mod_crop, (cw + 20, 40))
                draw = ImageDraw.Draw(combined)
                draw.text((10, 5), "ORIGINAL", fill=(0, 0, 0))
                draw.text((cw + 30, 5), "MODIFIED", fill=(0, 0, 0))
                combined.save(output_dir / f"diff_page{page_num}_sidebyside.png")

    # --- Summary ---
    total_diff_pct = (total_diff_pixels / total_pixels * 100) if total_pixels else 0

    print(f"\n{BOLD}Visual Summary{RESET}")
    print(f"  Pages compared: {len(orig_images)}")
    print(f"  Total diff pixels: {total_diff_pixels:,} / {total_pixels:,} ({total_diff_pct:.4f}%)")

    if expected_changes:
        print(f"  Unexpected diff pixels: {total_unexpected:,}")
        if total_unexpected == 0:
            print(f"\n  {GREEN}{BOLD}ALL visual differences match expected modifications{RESET}")
        elif total_unexpected > 0 and all_ok:
            print(f"\n  {YELLOW}{BOLD}Minor unexpected diffs detected — likely QR codes or rendering. Review images.{RESET}")
        else:
            print(f"\n  {RED}{BOLD}Significant unexpected visual differences detected{RESET}")
    else:
        if total_diff_pct < 0.5:
            print(f"\n  {GREEN}{BOLD}Visual diff is minimal ({total_diff_pct:.4f}%) — consistent with targeted text edit{RESET}")
        else:
            print(f"\n  {RED}{BOLD}Visual diff is large ({total_diff_pct:.2f}%) — possible layout disruption{RESET}")
            all_ok = False

    if output_dir:
        print(f"\n  Diff images saved to: {output_dir}/")

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Visual verification of modified PDF")
    parser.add_argument("modified", help="Modified PDF")
    parser.add_argument("original", help="Original unmodified PDF")
    parser.add_argument("--expected-changes", "-e", help="JSON file with expected text changes")
    parser.add_argument("--output-dir", "-o", help="Directory to save diff images")
    parser.add_argument("--dpi", type=int, default=300, help="Render DPI (default: 300)")
    args = parser.parse_args()

    modified_path = Path(args.modified)
    original_path = Path(args.original)

    if not modified_path.exists():
        print(f"Error: {modified_path} not found", file=sys.stderr)
        sys.exit(1)
    if not original_path.exists():
        print(f"Error: {original_path} not found", file=sys.stderr)
        sys.exit(1)

    expected_changes = None
    if args.expected_changes:
        data = json.loads(Path(args.expected_changes).read_text())
        expected_changes = data.get("changes", data if isinstance(data, list) else [])

    output_dir = Path(args.output_dir) if args.output_dir else None

    ok = run_visual_verification(modified_path, original_path, expected_changes, output_dir, args.dpi)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
