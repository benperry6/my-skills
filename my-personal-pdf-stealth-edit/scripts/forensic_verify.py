#!/usr/bin/env python3
"""
Phase 5 — Full verification of a modified PDF against the original.

Runs three verification layers:
1. 13-point forensic binary check
2. Deep stream analysis (operator sequence comparison)
3. Visual pixel-by-pixel comparison (Phase 6) — confirms diffs exist
   ONLY where modifications were requested, nowhere else

Usage:
    python3 forensic_verify.py <modified.pdf> <original.pdf> [--deep] [--visual] [--expected-changes changes.json] [--output-dir ./diffs]
"""
import argparse
import re
import sys
from pathlib import Path


# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def check_pass(num, name, detail=""):
    print(f"  {GREEN}[PASS]{RESET} #{num:02d} {name}" + (f" — {detail}" if detail else ""))
    return True


def check_fail(num, name, detail=""):
    print(f"  {RED}[FAIL]{RESET} #{num:02d} {name}" + (f" — {detail}" if detail else ""))
    return False


def check_warn(num, name, detail=""):
    print(f"  {YELLOW}[WARN]{RESET} #{num:02d} {name}" + (f" — {detail}" if detail else ""))
    return True  # Warnings don't fail the check


def run_checks(modified_path: Path, original_path: Path) -> bool:
    mod_data = modified_path.read_bytes()
    orig_data = original_path.read_bytes()
    mod_text = mod_data.decode("latin-1")
    orig_text = orig_data.decode("latin-1")

    passed = 0
    failed = 0
    total = 13

    print(f"\n{BOLD}Forensic Verification: {modified_path.name} vs {original_path.name}{RESET}\n")

    # --- Check 1: Binary marker bytes ---
    def get_marker(data):
        lines = data.split(b"\n", 3)
        if len(lines) >= 2 and lines[1].startswith(b"%") and len(lines[1]) >= 5:
            return lines[1][1:5]
        return None

    mod_marker = get_marker(mod_data)
    orig_marker = get_marker(orig_data)
    if mod_marker == orig_marker:
        if check_pass(1, "Binary marker bytes", f"both {orig_marker.hex() if orig_marker else 'none'}"):
            passed += 1
    else:
        if not check_fail(1, "Binary marker bytes",
                          f"modified={mod_marker.hex() if mod_marker else 'none'}, "
                          f"original={orig_marker.hex() if orig_marker else 'none'}"):
            failed += 1

    # --- Check 2: PDF version header ---
    mod_ver = re.search(r"%PDF-(\d+\.\d+)", mod_text[:50])
    orig_ver = re.search(r"%PDF-(\d+\.\d+)", orig_text[:50])
    mod_v = mod_ver.group(1) if mod_ver else "?"
    orig_v = orig_ver.group(1) if orig_ver else "?"
    if mod_v == orig_v:
        if check_pass(2, "PDF version", f"both {orig_v}"):
            passed += 1
    else:
        if not check_fail(2, "PDF version", f"modified={mod_v}, original={orig_v}"):
            failed += 1

    # --- Check 3: %%EOF count ---
    mod_eof = mod_text.count("%%EOF")
    orig_eof = orig_text.count("%%EOF")
    if mod_eof == orig_eof:
        if check_pass(3, "%%EOF count", f"both {orig_eof}"):
            passed += 1
    else:
        if not check_fail(3, "%%EOF count", f"modified={mod_eof}, original={orig_eof}"):
            failed += 1

    # --- Check 4: xref section count ---
    mod_xref = len(re.findall(r"^xref\s*$", mod_text, re.MULTILINE))
    orig_xref = len(re.findall(r"^xref\s*$", orig_text, re.MULTILINE))
    if mod_xref == orig_xref:
        if check_pass(4, "xref section count", f"both {orig_xref}"):
            passed += 1
    else:
        if not check_fail(4, "xref section count", f"modified={mod_xref}, original={orig_xref}"):
            failed += 1

    # --- Check 5: Tool string scan ---
    tool_strings = [
        (b"qpdf", "qpdf"), (b"pikepdf", "pikepdf"), (b"pypdf", "pypdf"),
        (b"pyPdf", "pyPdf"), (b"ReportLab", "ReportLab"), (b"reportlab", "reportlab"),
        (b"pdftk", "pdftk"), (b"iText", "iText"), (b"Ghostscript", "Ghostscript"),
        (b"mutool", "mutool"), (b"MuPDF", "MuPDF"), (b"cairo", "cairo"),
    ]
    found_tools = []
    for sig, name in tool_strings:
        if sig in mod_data and sig not in orig_data:
            found_tools.append(name)
    if not found_tools:
        if check_pass(5, "Tool string scan", "no foreign tool signatures"):
            passed += 1
    else:
        if not check_fail(5, "Tool string scan", f"found: {', '.join(found_tools)}"):
            failed += 1

    # --- Check 6: /ID field in trailer ---
    mod_trailer = re.search(r"trailer\s*<<(.*?)>>", mod_text, re.DOTALL)
    orig_trailer = re.search(r"trailer\s*<<(.*?)>>", orig_text, re.DOTALL)
    mod_has_id = "/ID" in mod_trailer.group(1) if mod_trailer else False
    orig_has_id = "/ID" in orig_trailer.group(1) if orig_trailer else False
    if mod_has_id == orig_has_id:
        if check_pass(6, "/ID field", f"both {'present' if orig_has_id else 'absent'}"):
            passed += 1
    else:
        if not check_fail(6, "/ID field",
                          f"modified={'present' if mod_has_id else 'absent'}, "
                          f"original={'present' if orig_has_id else 'absent'}"):
            failed += 1

    # --- Check 7: Trailer padding ---
    if mod_trailer:
        trailer_text = mod_trailer.group(1)
        # Check for suspicious whitespace blocks (>= 10 consecutive spaces)
        padding = re.findall(r" {10,}", trailer_text)
        if not padding:
            if check_pass(7, "Trailer padding", "no suspicious whitespace"):
                passed += 1
        else:
            if not check_fail(7, "Trailer padding", f"found {len(padding)} padding block(s)"):
                failed += 1
    else:
        if check_warn(7, "Trailer padding", "no trailer found"):
            passed += 1

    # --- Check 8: Object count ---
    mod_objs = len(re.findall(r"\d+\s+\d+\s+obj", mod_text))
    orig_objs = len(re.findall(r"\d+\s+\d+\s+obj", orig_text))
    if mod_objs == orig_objs:
        if check_pass(8, "Object count", f"both {orig_objs}"):
            passed += 1
    else:
        diff = mod_objs - orig_objs
        if abs(diff) <= 1:
            if check_warn(8, "Object count", f"modified={mod_objs}, original={orig_objs} (delta={diff})"):
                passed += 1
        else:
            if not check_fail(8, "Object count", f"modified={mod_objs}, original={orig_objs}"):
                failed += 1

    # --- Check 9: Producer/Author metadata ---
    from pypdf import PdfReader
    mod_reader = PdfReader(str(modified_path))
    orig_reader = PdfReader(str(original_path))
    mod_meta = mod_reader.metadata or {}
    orig_meta = orig_reader.metadata or {}

    meta_match = True
    meta_issues = []
    for key in ["/Producer", "/Author", "/Creator"]:
        mod_val = str(mod_meta.get(key, "")) if mod_meta.get(key) else ""
        orig_val = str(orig_meta.get(key, "")) if orig_meta.get(key) else ""
        if mod_val != orig_val:
            meta_match = False
            meta_issues.append(f"{key}: '{mod_val}' vs '{orig_val}'")

    if meta_match:
        producer = orig_meta.get("/Producer", "unknown")
        if check_pass(9, "Producer/Author metadata", f"Producer={producer}"):
            passed += 1
    else:
        if not check_fail(9, "Producer/Author metadata", "; ".join(meta_issues)):
            failed += 1

    # --- Check 10: BT/ET text block count ---
    mod_bt = len(re.findall(r"\bBT\b", mod_text))
    orig_bt = len(re.findall(r"\bBT\b", orig_text))
    mod_et = len(re.findall(r"\bET\b", mod_text))
    orig_et = len(re.findall(r"\bET\b", orig_text))
    if mod_bt == orig_bt and mod_et == orig_et:
        if check_pass(10, "BT/ET text block count", f"BT={orig_bt}, ET={orig_et}"):
            passed += 1
    else:
        if not check_fail(10, "BT/ET text block count",
                          f"modified BT={mod_bt}/ET={mod_et}, original BT={orig_bt}/ET={orig_et}"):
            failed += 1

    # --- Check 11: White fill operators ---
    mod_white = len(re.findall(r"1\s+1\s+1\s+rg", mod_text))
    orig_white = len(re.findall(r"1\s+1\s+1\s+rg", orig_text))
    if mod_white == orig_white:
        if check_pass(11, "White fill operators", f"both {orig_white}"):
            passed += 1
    else:
        if not check_fail(11, "White fill operators",
                          f"modified={mod_white}, original={orig_white}"):
            failed += 1

    # --- Check 12: File size delta ---
    mod_size = len(mod_data)
    orig_size = len(orig_data)
    delta = abs(mod_size - orig_size)
    delta_pct = (delta / orig_size) * 100
    if delta_pct < 1.0:
        if check_pass(12, "File size delta", f"{delta:,} bytes ({delta_pct:.2f}%)"):
            passed += 1
    else:
        if not check_fail(12, "File size delta",
                          f"{delta:,} bytes ({delta_pct:.2f}%) — exceeds 1% threshold"):
            failed += 1

    # --- Check 13: CreationDate == ModDate ---
    mod_creation = str(mod_meta.get("/CreationDate", ""))
    mod_moddate = str(mod_meta.get("/ModDate", ""))
    if mod_creation == mod_moddate:
        if check_pass(13, "CreationDate == ModDate", f"{mod_creation}"):
            passed += 1
    else:
        if not check_fail(13, "CreationDate == ModDate",
                          f"Creation={mod_creation}, Mod={mod_moddate}"):
            failed += 1

    # --- Summary ---
    print(f"\n{BOLD}Results: {passed}/{total} passed, {failed} failed{RESET}")

    if failed == 0:
        print(f"\n{GREEN}{BOLD}ALL CHECKS PASSED — file appears forensically clean{RESET}")
    else:
        print(f"\n{RED}{BOLD}{failed} CHECK(S) FAILED — file has detectable traces{RESET}")

    return failed == 0


def deep_stream_analysis(modified_path: Path, original_path: Path):
    """Additional deep analysis comparing content streams."""
    import pikepdf

    print(f"\n{BOLD}Deep Stream Analysis{RESET}\n")

    mod_pdf = pikepdf.open(str(modified_path))
    orig_pdf = pikepdf.open(str(original_path))

    issues = []

    # Compare page count
    if len(mod_pdf.pages) != len(orig_pdf.pages):
        issues.append(f"Page count differs: {len(mod_pdf.pages)} vs {len(orig_pdf.pages)}")

    # Compare content streams per page
    for page_num in range(min(len(mod_pdf.pages), len(orig_pdf.pages))):
        mod_page = mod_pdf.pages[page_num]
        orig_page = orig_pdf.pages[page_num]

        mod_contents = mod_page.get("/Contents")
        orig_contents = orig_page.get("/Contents")

        if mod_contents is None and orig_contents is None:
            continue

        # Get stream data
        def get_streams(contents):
            if contents is None:
                return []
            if isinstance(contents, pikepdf.Array):
                refs = list(contents)
            else:
                refs = [contents]
            result = []
            for ref in refs:
                try:
                    result.append(ref.read_bytes())
                except Exception:
                    result.append(b"")
            return result

        mod_streams = get_streams(mod_contents)
        orig_streams = get_streams(orig_contents)

        if len(mod_streams) != len(orig_streams):
            issues.append(f"Page {page_num}: stream count differs ({len(mod_streams)} vs {len(orig_streams)})")
            continue

        for idx in range(len(mod_streams)):
            mod_stream = mod_streams[idx]
            orig_stream = orig_streams[idx]

            # Compare operators (everything except hex data)
            mod_ops = re.findall(r"\b(BT|ET|Tf|Td|Tm|TJ|Tj|re|rg|RG|cm|Do|q|Q|w|J|j|M|d|gs|f|S|n)\b",
                                 mod_stream.decode("latin-1", errors="replace"))
            orig_ops = re.findall(r"\b(BT|ET|Tf|Td|Tm|TJ|Tj|re|rg|RG|cm|Do|q|Q|w|J|j|M|d|gs|f|S|n)\b",
                                  orig_stream.decode("latin-1", errors="replace"))

            if mod_ops != orig_ops:
                issues.append(f"Page {page_num}, stream {idx}: operator sequence differs")

    mod_pdf.close()
    orig_pdf.close()

    if not issues:
        print(f"  {GREEN}[OK]{RESET} No structural differences in content streams")
        print(f"  {GREEN}[OK]{RESET} Operator sequences match across all pages")
    else:
        for issue in issues:
            print(f"  {RED}[ISSUE]{RESET} {issue}")

    return len(issues) == 0


def main():
    parser = argparse.ArgumentParser(description="Full verification of modified PDF")
    parser.add_argument("modified", help="Modified/cleaned PDF")
    parser.add_argument("original", help="Original unmodified PDF")
    parser.add_argument("--deep", action="store_true", help="Also run deep stream analysis")
    parser.add_argument("--visual", action="store_true", help="Also run visual pixel-by-pixel verification")
    parser.add_argument("--expected-changes", "-e", help="JSON file with expected text changes (for visual verify)")
    parser.add_argument("--output-dir", "-o", help="Directory to save visual diff images")
    parser.add_argument("--full", action="store_true", help="Run all checks: forensic + deep + visual")
    args = parser.parse_args()

    modified_path = Path(args.modified)
    original_path = Path(args.original)

    if not modified_path.exists():
        print(f"Error: {modified_path} not found", file=sys.stderr)
        sys.exit(1)
    if not original_path.exists():
        print(f"Error: {original_path} not found", file=sys.stderr)
        sys.exit(1)

    run_deep = args.deep or args.full
    run_visual = args.visual or args.full

    # Phase 5a: 13-point forensic check
    checks_ok = run_checks(modified_path, original_path)

    # Phase 5b: Deep stream analysis
    deep_ok = True
    if run_deep:
        deep_ok = deep_stream_analysis(modified_path, original_path)

    # Phase 6: Visual pixel-by-pixel verification
    visual_ok = True
    if run_visual:
        from visual_verify import run_visual_verification
        import json

        expected_changes = None
        if args.expected_changes:
            data = json.loads(Path(args.expected_changes).read_text())
            expected_changes = data.get("changes", data if isinstance(data, list) else [])

        output_dir = Path(args.output_dir) if args.output_dir else None
        visual_ok = run_visual_verification(modified_path, original_path, expected_changes, output_dir)

    # Final verdict
    all_ok = checks_ok and deep_ok and visual_ok
    print(f"\n{'=' * 60}")
    if all_ok:
        print(f"{GREEN}{BOLD}FINAL VERDICT: ALL VERIFICATIONS PASSED{RESET}")
    else:
        parts = []
        if not checks_ok:
            parts.append("forensic")
        if not deep_ok:
            parts.append("deep stream")
        if not visual_ok:
            parts.append("visual")
        print(f"{RED}{BOLD}FINAL VERDICT: FAILED — {', '.join(parts)} verification(s){RESET}")
    print(f"{'=' * 60}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
