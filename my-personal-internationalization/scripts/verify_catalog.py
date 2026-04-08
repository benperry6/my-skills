#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from i18n_audit_utils import compare_catalogs


def render_text(findings: dict) -> str:
    lines: list[str] = [
        f"Source: {findings['source']}",
        f"Target: {findings['target']}",
    ]

    if not findings["has_findings"]:
        lines.append("Result: OK - structural parity checks passed.")
        return "\n".join(lines)

    lines.append("Result: FAIL - structural parity issues found.")

    if findings["missing_keys"]:
        lines.append("")
        lines.append("Missing keys in target:")
        lines.extend(f"- {path}" for path in findings["missing_keys"])

    if findings["extra_keys"]:
        lines.append("")
        lines.append("Extra keys in target:")
        lines.extend(f"- {path}" for path in findings["extra_keys"])

    if findings["type_mismatches"]:
        lines.append("")
        lines.append("Type mismatches:")
        for item in findings["type_mismatches"]:
            lines.append(
                f"- {item['path']}: source={item['source_type']} target={item['target_type']}"
            )

    if findings["placeholder_mismatches"]:
        lines.append("")
        lines.append("Placeholder mismatches:")
        for item in findings["placeholder_mismatches"]:
            lines.append(
                f"- {item['path']}: source={item['source']} target={item['target']}"
            )

    if findings["icu_mismatches"]:
        lines.append("")
        lines.append("ICU mismatches:")
        for item in findings["icu_mismatches"]:
            lines.append(
                f"- {item['path']}: source={item['source']} target={item['target']}"
            )

    if findings["markup_mismatches"]:
        lines.append("")
        lines.append("Markup tag mismatches:")
        for item in findings["markup_mismatches"]:
            lines.append(
                f"- {item['path']}: source={item['source']} target={item['target']}"
            )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify structural parity between a source locale catalog and a target locale catalog."
    )
    parser.add_argument("--source", required=True, type=Path, help="Reference locale catalog path.")
    parser.add_argument("--target", required=True, type=Path, help="Target locale catalog path.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    args = parser.parse_args()

    findings = compare_catalogs(args.source.expanduser().resolve(), args.target.expanduser().resolve())

    if args.format == "json":
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        print(render_text(findings))

    raise SystemExit(1 if findings["has_findings"] else 0)


if __name__ == "__main__":
    main()

