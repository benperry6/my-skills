#!/usr/bin/env python3
"""Append a structured learning entry to the skill references."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def append_entry(path: Path, entry: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    path.write_text(existing + entry, encoding="utf-8")


def build_entry(args: argparse.Namespace) -> str:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    title_parts = [timestamp]
    if args.provider:
        title_parts.append(args.provider)
    title_parts.append(args.title)
    lines = [f"## {' — '.join(title_parts)}", ""]
    lines.append(f"- Summary: {args.summary}")
    if args.evidence:
        lines.append(f"- Evidence: {args.evidence}")
    if args.command:
        lines.append(f"- Command: `{args.command}`")
    for doc in args.docs:
        lines.append(f"- Docs: {doc}")
    if args.notes:
        lines.append(f"- Notes: {args.notes}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a verified or runtime learning entry.")
    parser.add_argument("--kind", choices=["verified", "runtime"], required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--provider")
    parser.add_argument("--evidence")
    parser.add_argument("--command")
    parser.add_argument("--docs", action="append", default=[])
    parser.add_argument("--notes")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    target = skill_dir / "references" / ("verified-learning.md" if args.kind == "verified" else "runtime-learning.md")
    append_entry(target, build_entry(args))
    print(f"[OK] Appended {args.kind} learning to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
