#!/usr/bin/env python3
"""
Phase 3 — Modify content streams by replacing glyph hex codes.

Takes a PDF and a replacements JSON file describing what to change.
Works at the content stream level to replace glyph codes in TJ/Tj operators.

Usage:
    python3 modify_streams.py <input.pdf> <output.pdf> --replacements replacements.json [--metadata metadata.json]

Replacements JSON format:
    {
        "replacements": [
            {
                "old_hex": "0037002C00140033",
                "new_hex": "0032002C00140033",
                "description": "05Mar -> 12Mar",
                "pages": [0, 1]  // optional, default all pages
            }
        ]
    }

Metadata JSON format (optional):
    {
        "CreationDate": "D:20260311120000+05'30'",
        "ModDate": "D:20260311120000+05'30'"
    }
"""
import argparse
import json
import re
import sys
import zlib
from pathlib import Path

import pikepdf


def find_and_replace_in_stream(stream_bytes: bytes, old_hex: str, new_hex: str) -> tuple[bytes, int]:
    """
    Find and replace hex glyph sequences in a content stream.
    Handles both uppercase and lowercase hex in the PDF.
    Returns (modified_bytes, replacement_count).
    """
    text = stream_bytes.decode("latin-1")
    count = 0

    # Pattern: hex strings appear as <HEXDATA> inside TJ arrays or after Tj
    # We need to find the old_hex sequence within hex strings
    old_upper = old_hex.upper()
    old_lower = old_hex.lower()

    # Try direct replacement in hex strings
    # PDF hex strings: <4865...>
    def replace_in_hex_strings(match):
        nonlocal count
        hex_content = match.group(1)
        # Check if old_hex appears in this hex string (case-insensitive)
        idx = hex_content.upper().find(old_upper)
        if idx >= 0:
            # Replace preserving the case of surrounding content
            new_content = hex_content[:idx] + new_hex.upper() + hex_content[idx + len(old_upper):]
            count += 1
            return f"<{new_content}>"
        return match.group(0)

    result = re.sub(r"<([0-9A-Fa-f]+)>", replace_in_hex_strings, text)

    return result.encode("latin-1"), count


def modify_pdf(input_path: Path, output_path: Path, replacements: list, metadata: dict = None):
    """Apply glyph replacements to PDF content streams and optionally update metadata."""
    pdf = pikepdf.open(str(input_path))
    total_replacements = 0

    for repl in replacements:
        old_hex = repl["old_hex"]
        new_hex = repl["new_hex"]
        target_pages = repl.get("pages")  # None = all pages
        desc = repl.get("description", f"{old_hex} -> {new_hex}")

        for page_num, page in enumerate(pdf.pages):
            if target_pages is not None and page_num not in target_pages:
                continue

            contents = page.get("/Contents")
            if contents is None:
                continue

            # Contents can be a single stream or an array
            if isinstance(contents, pikepdf.Array):
                content_refs = list(contents)
            else:
                content_refs = [contents]

            for ref in content_refs:
                try:
                    stream_data = ref.read_bytes()
                    modified_data, count = find_and_replace_in_stream(stream_data, old_hex, new_hex)

                    if count > 0:
                        # Write back with same compression
                        ref.write(modified_data, filter=ref.get("/Filter"))
                        total_replacements += count
                        print(f"  Page {page_num}: {count}x {desc}", file=sys.stderr)
                except Exception as e:
                    print(f"  Page {page_num}: Error processing stream: {e}", file=sys.stderr)

    # Update metadata if provided
    if metadata:
        with pdf.open_metadata() as meta:
            pass  # pikepdf metadata API is XMP-based

        # Use the Info dictionary directly for PDF metadata
        info = pdf.trailer.get("/Info")
        if info:
            info_obj = pdf.get_object(info)
            for key, value in metadata.items():
                info_obj[pikepdf.Name(f"/{key}")] = pikepdf.String(value)
                print(f"  Metadata: {key} = {value}", file=sys.stderr)

    pdf.save(str(output_path))
    pdf.close()

    print(f"\nTotal replacements: {total_replacements}", file=sys.stderr)
    print(f"Output saved to: {output_path}", file=sys.stderr)
    return total_replacements


def main():
    parser = argparse.ArgumentParser(description="Modify PDF content streams")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--replacements", "-r", required=True, help="Replacements JSON file")
    parser.add_argument("--metadata", "-m", help="Metadata JSON file (optional)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    # Load replacements
    repl_data = json.loads(Path(args.replacements).read_text())
    replacements = repl_data.get("replacements", repl_data if isinstance(repl_data, list) else [])

    # Load metadata if provided
    metadata = None
    if args.metadata:
        metadata = json.loads(Path(args.metadata).read_text())

    print(f"Modifying {input_path} with {len(replacements)} replacement(s)...", file=sys.stderr)
    modify_pdf(input_path, output_path, replacements, metadata)


if __name__ == "__main__":
    main()
