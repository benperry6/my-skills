#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FILES = [
    ".agents/business-model.md",
    ".agents/storytelling.md",
    ".agents/know-your-customer.md",
    ".agents/performance-memory.md",
]

VOC_BANK_HEADER = (
    "entry_id,captured_at,source_type,platform,source_label,source_url,date_seen,"
    "quote,quote_language,evidence_kind,capture_method,segment,journey_stage,"
    "theme_tags,friction_type,risk_type,intensity,evidence_notes"
)

MIN_MEANINGFUL_LINES = {
    ".agents/business-model.md": 5,
    ".agents/storytelling.md": 4,
    ".agents/know-your-customer.md": 5,
    ".agents/performance-memory.md": 3,
}

SECTION_REQUIREMENTS = {
    ".agents/business-model.md": {"## Snapshot": 2},
    ".agents/storytelling.md": {"## Narrative Core": 2},
    ".agents/know-your-customer.md": {"## Snapshot": 2, "## Voice of Customer": 1},
    ".agents/performance-memory.md": {"## Rules": 2},
}

ALTERNATIVE_SECTION_PREFIXES = {
    ".agents/know-your-customer.md": [("## Snapshot", "## Segment Card:")],
}


def meaningful_content_lines(lines: list[str]) -> list[str]:
    meaningful: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("<!--") or line.endswith("-->"):
            continue
        if line.startswith("```"):
            continue

        line = re.sub(r"^[-*]\s*", "", line).strip()
        if not line:
            continue
        if line == "...":
            continue
        if not re.search(r"[A-Za-z0-9]", line):
            continue

        meaningful.append(line)
    return meaningful


def split_sections(content: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "__root__"
    sections[current] = []

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped
            sections.setdefault(current, [])
            continue

        sections.setdefault(current, []).append(line)

    return sections


def has_dangling_placeholder_bullets(content: str) -> bool:
    return any(line.strip() == "-" for line in content.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the canonical context tree for my-personal-context-distillation."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to validate. Defaults to current working directory.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    docs_sources = root / "docs" / "context-sources"
    failures: list[str] = []

    if docs_sources.exists():
        print(f"ok  found source directory: {docs_sources}")
    else:
        failures.append(f"missing source directory: {docs_sources}")

    voc_bank = docs_sources / "voc-bank.csv"
    if not voc_bank.exists():
        failures.append(f"missing voc bank: {voc_bank}")
    else:
        rows = voc_bank.read_text(encoding="utf-8").splitlines()
        first_line = rows[0].strip() if rows else ""
        if first_line != VOC_BANK_HEADER:
            failures.append(
                f"invalid voc bank header: {voc_bank} -> expected exact schema"
            )
        else:
            print(f"ok  {voc_bank} -> {first_line}")
            if len(rows) < 2:
                failures.append(f"voc bank has no evidence rows: {voc_bank}")

    for relative_path in REQUIRED_FILES:
        file_path = root / relative_path
        if not file_path.exists():
            failures.append(f"missing canonical file: {file_path}")
            continue

        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            failures.append(f"empty canonical file: {file_path}")
            continue

        if has_dangling_placeholder_bullets(content):
            failures.append(f"placeholder bullet left in canonical file: {file_path}")
            continue

        sections = split_sections(content)
        all_meaningful = meaningful_content_lines(content.splitlines())
        minimum = MIN_MEANINGFUL_LINES.get(relative_path, 1)
        if len(all_meaningful) < minimum:
            failures.append(
                f"canonical file too thin: {file_path} -> found {len(all_meaningful)} meaningful lines, need at least {minimum}"
            )
            continue

        requirements = dict(SECTION_REQUIREMENTS.get(relative_path, {}))
        for primary, alternative in ALTERNATIVE_SECTION_PREFIXES.get(relative_path, []):
            if primary in requirements and primary not in sections:
                if any(section.startswith(alternative) for section in sections):
                    requirements.pop(primary, None)

        section_failures: list[str] = []
        for heading, minimum_lines in requirements.items():
            if heading not in sections:
                section_failures.append(f"missing required section {heading}")
                continue

            section_meaningful = meaningful_content_lines(sections[heading])
            if len(section_meaningful) < minimum_lines:
                section_failures.append(
                    f"section {heading} is too thin ({len(section_meaningful)} meaningful lines, need at least {minimum_lines})"
                )

        if section_failures:
            failures.append(
                f"canonical file content check failed: {file_path} -> " + "; ".join(section_failures)
            )
            continue

        first_line = content.splitlines()[0]
        print(f"ok  {file_path} -> {first_line}")

    if failures:
        print("\nvalidation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nvalidation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
