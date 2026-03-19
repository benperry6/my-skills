#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)


def parse_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    frontmatter = match.group(1) if match else ""

    def get_field(name: str) -> str:
        pattern = re.compile(rf"^{re.escape(name)}:\s*(.+)$", re.M)
        field_match = pattern.search(frontmatter)
        if not field_match:
            return ""
        value = field_match.group(1).strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            value = value[1:-1]
        return " ".join(value.split())

    return get_field("name"), get_field("description")


def compact_description(description: str, max_len: int = 140) -> str:
    text = description.replace("[My Personal Skill] ", "").strip()
    for marker in (
        " Also use when",
        " Also triggers",
        " Triggers on",
        " Trigger for",
        " Use this whenever",
        " This skill should be used when",
        " Works with ",
    ):
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    text = text.rstrip(" .")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def iter_skills(root: Path):
    for skill_file in sorted(root.glob("*/SKILL.md")):
        name, description = parse_frontmatter(skill_file)
        yield {
            "folder": skill_file.parent.name,
            "name": name or skill_file.parent.name,
            "description": description or "(no description found)",
        }


def render_markdown(root: Path) -> str:
    skills = list(iter_skills(root))
    lines = [
        f"Installed skills scanned: {len(skills)}",
        "",
        "Full installed skill inventory:",
    ]
    for skill in skills:
        lines.append(f"- {skill['folder']}: {compact_description(skill['description'])}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="List installed skills from the live skills directory.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Directory containing sibling skill folders. Defaults to the current installed skills root.",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"skills root does not exist: {root}")

    print(render_markdown(root))


if __name__ == "__main__":
    main()
