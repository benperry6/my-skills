#!/usr/bin/env python3
"""
Phase 1 — Analyze a PDF for stealth editing.

Extracts metadata, structural baseline, font CMap mappings, text content,
and content stream inventory. Outputs a JSON report used by subsequent phases.

Usage:
    python3 analyze_pdf.py <input.pdf> [--output analysis.json]
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path


def extract_metadata(pdf_path: Path) -> dict:
    """Extract PDF metadata using pypdf."""
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    meta = reader.metadata or {}
    result = {}
    for key in ["/Producer", "/Author", "/Creator", "/Title", "/Subject",
                "/Keywords", "/CreationDate", "/ModDate"]:
        val = meta.get(key)
        if val:
            result[key.lstrip("/")] = str(val)
    return result


def extract_structural_baseline(pdf_path: Path) -> dict:
    """Analyze binary structure of the PDF."""
    data = pdf_path.read_bytes()
    text_data = data.decode("latin-1")

    # Binary marker bytes at offsets 10-13 (the comment line after %PDF-x.y)
    # Typically the second line is a binary comment like %âãÏÓ
    binary_marker = None
    lines = data.split(b"\n", 3)
    if len(lines) >= 2:
        line2 = lines[1]
        if line2.startswith(b"%") and len(line2) >= 5:
            binary_marker = line2[1:5].hex()

    # PDF version from header
    version_match = re.search(r"%PDF-(\d+\.\d+)", text_data[:100])
    pdf_version = version_match.group(1) if version_match else "unknown"

    # Count %%EOF markers
    eof_count = text_data.count("%%EOF")

    # Count xref sections
    xref_count = len(re.findall(r"^xref\s*$", text_data, re.MULTILINE))

    # Count objects
    obj_count = len(re.findall(r"\d+\s+\d+\s+obj", text_data))

    # Check for /ID field in trailer
    trailer_match = re.search(r"trailer\s*<<(.*?)>>", text_data, re.DOTALL)
    has_id = False
    trailer_content = ""
    if trailer_match:
        trailer_content = trailer_match.group(1)
        has_id = "/ID" in trailer_content

    # File size
    file_size = len(data)

    # Scan for known tool signatures in binary
    tool_signatures = {
        "qpdf": [b"qpdf", b"\xbf\xf7\xa2\xfe"],
        "pikepdf": [b"pikepdf"],
        "pypdf": [b"pypdf", b"pyPdf"],
        "reportlab": [b"ReportLab", b"reportlab"],
        "pdftk": [b"pdftk", b"iText"],
        "ghostscript": [b"Ghostscript", b"GPL Ghostscript"],
        "mutool": [b"mutool", b"MuPDF"],
        "cairo": [b"cairo"],
    }
    detected_tools = []
    for tool, sigs in tool_signatures.items():
        for sig in sigs:
            if sig in data:
                offset = data.index(sig)
                detected_tools.append({
                    "tool": tool,
                    "signature": sig.hex() if not sig.isascii() else sig.decode("ascii", errors="replace"),
                    "offset": offset
                })

    # Count BT/ET text blocks
    bt_count = len(re.findall(r"\bBT\b", text_data))
    et_count = len(re.findall(r"\bET\b", text_data))

    # Check for white fill operators (overlay indicator)
    white_fills = len(re.findall(r"1\s+1\s+1\s+rg", text_data))

    return {
        "pdf_version": pdf_version,
        "file_size": file_size,
        "binary_marker_hex": binary_marker,
        "eof_count": eof_count,
        "xref_count": xref_count,
        "object_count": obj_count,
        "has_id_field": has_id,
        "trailer_snippet": trailer_content.strip()[:200],
        "bt_count": bt_count,
        "et_count": et_count,
        "white_fill_count": white_fills,
        "detected_tools": detected_tools,
    }


def extract_font_cmaps(pdf_path: Path) -> dict:
    """Extract font CMap mappings (character → glyph hex code) for each font."""
    import pikepdf

    fonts_info = {}
    pdf = pikepdf.open(str(pdf_path))

    for page_num, page in enumerate(pdf.pages):
        resources = page.get("/Resources", {})
        font_dict = resources.get("/Font", {})

        for font_name, font_ref in font_dict.items():
            font_obj = font_ref
            if isinstance(font_ref, pikepdf.Object):
                try:
                    font_obj = pdf.get_object(font_ref.objgen) if hasattr(font_ref, "objgen") else font_ref
                except Exception:
                    pass

            font_key = f"page{page_num}_{font_name}"
            info = {"name": str(font_name), "page": page_num}

            # Get encoding
            encoding = font_obj.get("/Encoding")
            if encoding:
                info["encoding"] = str(encoding)

            # Get BaseFont
            base_font = font_obj.get("/BaseFont")
            if base_font:
                info["base_font"] = str(base_font)

            # Extract ToUnicode CMap if present
            to_unicode = font_obj.get("/ToUnicode")
            if to_unicode:
                try:
                    stream = to_unicode.read_bytes()
                    cmap_text = stream.decode("latin-1", errors="replace")
                    # Parse beginbfchar / beginbfrange sections
                    char_map = {}

                    # bfchar: <src> <dst>
                    bfchar_blocks = re.findall(
                        r"beginbfchar\s*(.*?)\s*endbfchar",
                        cmap_text, re.DOTALL
                    )
                    for block in bfchar_blocks:
                        pairs = re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block)
                        for src, dst in pairs:
                            try:
                                unicode_char = bytes.fromhex(dst).decode("utf-16-be")
                                char_map[unicode_char] = src.upper()
                            except Exception:
                                char_map[f"U+{dst}"] = src.upper()

                    # bfrange: <start> <end> <dst>
                    bfrange_blocks = re.findall(
                        r"beginbfrange\s*(.*?)\s*endbfrange",
                        cmap_text, re.DOTALL
                    )
                    for block in bfrange_blocks:
                        ranges = re.findall(
                            r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>",
                            block
                        )
                        for start_hex, end_hex, dst_hex in ranges:
                            start = int(start_hex, 16)
                            end = int(end_hex, 16)
                            dst_start = int(dst_hex, 16)
                            for i in range(end - start + 1):
                                try:
                                    unicode_char = chr(dst_start + i)
                                    glyph_hex = format(start + i, f"0{len(start_hex)}X")
                                    char_map[unicode_char] = glyph_hex
                                except Exception:
                                    pass

                    info["cmap"] = char_map
                    info["cmap_size"] = len(char_map)
                except Exception as e:
                    info["cmap_error"] = str(e)

            fonts_info[font_key] = info

    pdf.close()
    return fonts_info


def extract_text(pdf_path: Path) -> list:
    """Extract text content per page using pdfplumber."""
    import pdfplumber

    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            # Also get character-level data for precise positioning
            chars = []
            for char in (page.chars or []):
                chars.append({
                    "text": char.get("text", ""),
                    "x0": round(char.get("x0", 0), 2),
                    "y0": round(char.get("top", 0), 2),
                    "fontname": char.get("fontname", ""),
                    "size": round(char.get("size", 0), 2),
                })
            pages.append({
                "page": i,
                "text": text,
                "char_count": len(chars),
                "chars_sample": chars[:50],  # First 50 chars for reference
            })
    return pages


def extract_content_streams(pdf_path: Path) -> list:
    """Inventory content streams: count, sizes, compression."""
    import pikepdf

    streams = []
    pdf = pikepdf.open(str(pdf_path))

    for page_num, page in enumerate(pdf.pages):
        contents = page.get("/Contents")
        if contents is None:
            continue

        # Contents can be a single stream or an array
        if isinstance(contents, pikepdf.Array):
            content_refs = list(contents)
        else:
            content_refs = [contents]

        for idx, ref in enumerate(content_refs):
            try:
                obj = ref
                raw_size = len(bytes(obj.read_raw_bytes()))
                decoded_size = len(bytes(obj.read_bytes()))
                filters = obj.get("/Filter")
                filter_name = str(filters) if filters else "none"
                streams.append({
                    "page": page_num,
                    "index": idx,
                    "raw_size": raw_size,
                    "decoded_size": decoded_size,
                    "filter": filter_name,
                })
            except Exception as e:
                streams.append({
                    "page": page_num,
                    "index": idx,
                    "error": str(e),
                })

    pdf.close()
    return streams


def main():
    parser = argparse.ArgumentParser(description="Analyze PDF for stealth editing")
    parser.add_argument("input", help="Path to the PDF file")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    pdf_path = Path(args.input)
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing {pdf_path}...", file=sys.stderr)

    report = {
        "file": str(pdf_path),
        "metadata": extract_metadata(pdf_path),
        "structure": extract_structural_baseline(pdf_path),
        "fonts": extract_font_cmaps(pdf_path),
        "text": extract_text(pdf_path),
        "content_streams": extract_content_streams(pdf_path),
    }

    output = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Analysis saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
