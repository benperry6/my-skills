#!/usr/bin/env python3
"""
Phase 4 — Forensic cleanup of a modified PDF.

Removes all traces of modification tools (qpdf, pikepdf, etc.) by:
1. Flattening with qpdf (2-pass: --qdf then clean)
2. Patching the binary marker bytes to match the original
3. Removing /ID field from trailer if original didn't have it
4. Rebuilding trailer cleanly (no padding artifacts)
5. Ensuring metadata coherence (CreationDate == ModDate)

Usage:
    python3 forensic_clean.py <input.pdf> <output.pdf> --original <original.pdf>
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def get_binary_marker(pdf_path: Path) -> bytes:
    """Extract the binary marker bytes from the second line of a PDF."""
    data = pdf_path.read_bytes()
    lines = data.split(b"\n", 3)
    if len(lines) >= 2 and lines[1].startswith(b"%"):
        # Return the bytes after the % sign (typically 4 bytes)
        marker_line = lines[1]
        if len(marker_line) >= 5:
            return marker_line[1:5]
    return None


def get_trailer_info(pdf_path: Path) -> dict:
    """Extract trailer information from a PDF."""
    data = pdf_path.read_bytes()
    text = data.decode("latin-1")

    # Find the last trailer
    trailer_matches = list(re.finditer(r"trailer\s*<<(.*?)>>", text, re.DOTALL))
    if not trailer_matches:
        return {"has_trailer": False}

    last_trailer = trailer_matches[-1]
    content = last_trailer.group(1)

    return {
        "has_trailer": True,
        "has_id": "/ID" in content,
        "content": content.strip(),
        "offset": last_trailer.start(),
        "end_offset": last_trailer.end(),
    }


def flatten_with_qpdf(input_path: Path, output_path: Path):
    """Two-pass qpdf flattening to remove incremental update traces."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        intermediate = Path(tmp.name)

    try:
        # Pass 1: --qdf fully decomposes object structure
        result = subprocess.run(
            ["qpdf", "--qdf", str(input_path), str(intermediate)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  qpdf --qdf warning: {result.stderr.strip()}", file=sys.stderr)

        # Pass 2: clean rebuild
        result = subprocess.run(
            ["qpdf", str(intermediate), str(output_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  qpdf clean warning: {result.stderr.strip()}", file=sys.stderr)

    finally:
        intermediate.unlink(missing_ok=True)

    print("  Step 1: qpdf 2-pass flatten complete", file=sys.stderr)


def patch_binary_marker(pdf_path: Path, original_marker: bytes):
    """Replace the binary marker bytes with the original's marker."""
    data = bytearray(pdf_path.read_bytes())
    lines = bytes(data).split(b"\n", 3)

    if len(lines) < 2:
        print("  Step 2: SKIP — can't find binary marker line", file=sys.stderr)
        return

    marker_line = lines[1]
    if not marker_line.startswith(b"%") or len(marker_line) < 5:
        print("  Step 2: SKIP — unexpected marker line format", file=sys.stderr)
        return

    # Find the offset of the marker bytes
    first_line_len = len(lines[0]) + 1  # +1 for \n
    marker_offset = first_line_len + 1  # +1 for % sign

    current_marker = data[marker_offset:marker_offset + 4]
    if bytes(current_marker) == original_marker:
        print(f"  Step 2: Binary marker already matches original ({original_marker.hex()})", file=sys.stderr)
        return

    # Patch
    data[marker_offset:marker_offset + 4] = original_marker
    pdf_path.write_bytes(bytes(data))
    print(f"  Step 2: Binary marker patched: {current_marker.hex()} → {original_marker.hex()}", file=sys.stderr)


def remove_id_and_rebuild_trailer(pdf_path: Path, original_trailer_info: dict):
    """Remove /ID field and rebuild trailer to match original format."""
    data = pdf_path.read_bytes()
    text = data.decode("latin-1")

    # Find the last trailer
    trailer_matches = list(re.finditer(r"trailer\s*<<(.*?)>>", text, re.DOTALL))
    if not trailer_matches:
        print("  Step 3-4: SKIP — no trailer found", file=sys.stderr)
        return

    last_trailer = trailer_matches[-1]
    trailer_content = last_trailer.group(1)

    modified = False

    # Remove /ID field if present and original didn't have it
    if "/ID" in trailer_content and not original_trailer_info.get("has_id", False):
        # Remove /ID [...] pattern
        trailer_content = re.sub(r"\s*/ID\s*\[.*?\]", "", trailer_content, flags=re.DOTALL)
        modified = True
        print("  Step 3: /ID field removed", file=sys.stderr)
    else:
        print("  Step 3: No /ID removal needed", file=sys.stderr)

    if not modified:
        print("  Step 4: No trailer rebuild needed", file=sys.stderr)
        return

    # Clean up trailing whitespace/padding in trailer content
    trailer_content = trailer_content.strip()
    # Normalize whitespace
    trailer_content = re.sub(r"\s+", " ", trailer_content)

    # Find startxref value (the xref table offset)
    startxref_match = re.search(r"startxref\s*(\d+)", text)
    if not startxref_match:
        print("  Step 4: WARNING — can't find startxref", file=sys.stderr)
        return

    xref_offset = startxref_match.group(1)

    # Find the byte offset where trailer begins
    trailer_byte_offset = last_trailer.start()

    # Truncate file at trailer start and rebuild
    truncated = data[:trailer_byte_offset]

    # Build clean trailer
    new_trailer = f"trailer\n<< {trailer_content} >>\nstartxref\n{xref_offset}\n%%EOF\n"
    new_trailer_bytes = new_trailer.encode("latin-1")

    result = truncated + new_trailer_bytes
    pdf_path.write_bytes(result)
    print(f"  Step 4: Trailer rebuilt cleanly ({len(new_trailer_bytes)} bytes)", file=sys.stderr)


def verify_metadata_coherence(pdf_path: Path, target_dates: dict = None):
    """Ensure CreationDate == ModDate and they're coherent."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(pdf_path))
    meta = reader.metadata or {}
    creation = meta.get("/CreationDate", "")
    mod = meta.get("/ModDate", "")

    if creation == mod:
        print(f"  Step 5: Metadata coherent (CreationDate == ModDate: {creation})", file=sys.stderr)
        return

    # If they differ, set ModDate = CreationDate (or use target_dates)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.add_metadata(reader.metadata)

    target_creation = target_dates.get("CreationDate", creation) if target_dates else creation
    target_mod = target_dates.get("ModDate", target_creation) if target_dates else target_creation

    writer.add_metadata({
        "/CreationDate": target_creation,
        "/ModDate": target_mod,
    })

    # Save to temp then replace
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        writer.write(tmp)
        tmp_path = Path(tmp.name)

    # Replace original
    pdf_path.write_bytes(tmp_path.read_bytes())
    tmp_path.unlink()
    print(f"  Step 5: Metadata synchronized: {target_creation}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Forensic cleanup of modified PDF")
    parser.add_argument("input", help="Modified PDF to clean")
    parser.add_argument("output", help="Output cleaned PDF")
    parser.add_argument("--original", "-o", required=True, help="Original unmodified PDF (for reference)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    original_path = Path(args.original)

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)
    if not original_path.exists():
        print(f"Error: {original_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Forensic cleanup of {input_path}...", file=sys.stderr)
    print(f"Reference original: {original_path}", file=sys.stderr)

    # Get original's fingerprint
    original_marker = get_binary_marker(original_path)
    original_trailer = get_trailer_info(original_path)

    print(f"  Original binary marker: {original_marker.hex() if original_marker else 'none'}", file=sys.stderr)
    print(f"  Original has /ID: {original_trailer.get('has_id', 'unknown')}", file=sys.stderr)

    # Work on a copy
    import shutil
    shutil.copy2(str(input_path), str(output_path))

    # Step 1: Flatten with qpdf
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        flattened = Path(tmp.name)
    flatten_with_qpdf(output_path, flattened)
    shutil.copy2(str(flattened), str(output_path))
    flattened.unlink(missing_ok=True)

    # Step 2: Patch binary marker
    if original_marker:
        patch_binary_marker(output_path, original_marker)

    # Step 3-4: Remove /ID and rebuild trailer
    remove_id_and_rebuild_trailer(output_path, original_trailer)

    # Step 5: Metadata coherence
    verify_metadata_coherence(output_path)

    final_size = output_path.stat().st_size
    original_size = original_path.stat().st_size
    delta = abs(final_size - original_size)
    delta_pct = (delta / original_size) * 100

    print(f"\nCleanup complete:", file=sys.stderr)
    print(f"  Original size: {original_size:,} bytes", file=sys.stderr)
    print(f"  Cleaned size:  {final_size:,} bytes", file=sys.stderr)
    print(f"  Delta: {delta:,} bytes ({delta_pct:.2f}%)", file=sys.stderr)
    print(f"  Output: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
