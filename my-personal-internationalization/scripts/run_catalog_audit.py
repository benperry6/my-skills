#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from i18n_audit_utils import compare_catalogs
from scan_hardcoded_strings import DEFAULT_EXCLUDE_DIRS, collect_findings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the full reusable locale-catalog audit workflow: parity checks plus hardcoded-string scan."
    )
    parser.add_argument("--source", required=True, type=Path, help="Reference locale catalog path.")
    parser.add_argument(
        "--target",
        required=True,
        action="append",
        type=Path,
        help="Target locale catalog path. Pass multiple times for multiple locales.",
    )
    parser.add_argument(
        "--code-root",
        required=True,
        type=Path,
        help="Code root to scan for hardcoded user-facing string candidates.",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude from the hardcoded-string scan. Can be passed multiple times.",
    )
    parser.add_argument(
        "--hardcoded-limit",
        type=int,
        default=200,
        help="Maximum hardcoded-string findings to print. Defaults to 200.",
    )
    parser.add_argument(
        "--strict-hardcoded",
        action="store_true",
        help="Exit non-zero when hardcoded-string candidates are found.",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    targets = [path.expanduser().resolve() for path in args.target]
    code_root = args.code_root.expanduser().resolve()
    exclude_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude_dir)

    parity_failed = False
    for target in targets:
        findings = compare_catalogs(source, target)
        status = "FAIL" if findings["has_findings"] else "OK"
        print(f"[catalog] {target.name}: {status}")
        if findings["missing_keys"]:
            print(f"  missing keys: {len(findings['missing_keys'])}")
        if findings["extra_keys"]:
            print(f"  extra keys: {len(findings['extra_keys'])}")
        if findings["type_mismatches"]:
            print(f"  type mismatches: {len(findings['type_mismatches'])}")
        if findings["placeholder_mismatches"]:
            print(f"  placeholder mismatches: {len(findings['placeholder_mismatches'])}")
        if findings["icu_mismatches"]:
            print(f"  ICU mismatches: {len(findings['icu_mismatches'])}")
        if findings["markup_mismatches"]:
            print(f"  markup mismatches: {len(findings['markup_mismatches'])}")
        parity_failed = parity_failed or findings["has_findings"]

    hardcoded_findings = collect_findings(code_root, exclude_dirs, max(1, args.hardcoded_limit))
    print(f"[hardcoded-scan] candidates: {len(hardcoded_findings)}")
    for item in hardcoded_findings[:20]:
        print(f"  - {item['path']}:{item['line']} [{item['kind']}] {item['text']}")
    if len(hardcoded_findings) > 20:
        print(f"  ... {len(hardcoded_findings) - 20} more candidates omitted")

    should_fail = parity_failed or (args.strict_hardcoded and bool(hardcoded_findings))
    raise SystemExit(1 if should_fail else 0)


if __name__ == "__main__":
    main()
