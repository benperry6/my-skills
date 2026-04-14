#!/usr/bin/env python3
"""Append a structured runtime or verified learning entry to a target skill."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_entry(target: Path, heading: str, lines: list[str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    block = "\n".join([heading, "", *lines, ""])
    target.write_text(existing + block, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a runtime or verified learning entry.")
    parser.add_argument("--skill-dir", required=True, help="Absolute path to the target skill directory.")
    parser.add_argument("--kind", choices=("runtime", "verified"), required=True)
    parser.add_argument("--topic", required=True, help="Short topic label for the entry heading.")
    parser.add_argument("--summary", required=True, help="One-line summary of the learning.")
    parser.add_argument("--failed-path", help="Concrete failing path that was observed.")
    parser.add_argument("--repaired-path", help="Concrete repaired path that was validated.")
    parser.add_argument("--evidence", action="append", default=[], help="Concrete evidence line. Repeatable.")
    parser.add_argument("--notes", action="append", default=[], help="Extra note line. Repeatable.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    references_dir = skill_dir / "references"
    target = references_dir / ("runtime-learning.md" if args.kind == "runtime" else "verified-learning.md")

    heading = f"## {utc_now()} - {args.topic}"
    lines = [f"- Summary: {args.summary}"]
    if args.failed_path:
        lines.append(f"- Failed path: `{args.failed_path}`")
    if args.repaired_path:
        lines.append(f"- Repaired path: `{args.repaired_path}`")
    for item in args.evidence:
        lines.append(f"- Evidence: {item}")
    for item in args.notes:
        lines.append(f"- Note: {item}")

    append_entry(target, heading, lines)
    print(f"[OK] Appended {args.kind} learning to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
