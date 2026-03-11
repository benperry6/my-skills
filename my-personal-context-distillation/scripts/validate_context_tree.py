#!/usr/bin/env python3

from __future__ import annotations

import argparse
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
        header = voc_bank.read_text(encoding="utf-8").splitlines()
        first_line = header[0].strip() if header else ""
        if first_line != VOC_BANK_HEADER:
            failures.append(
                f"invalid voc bank header: {voc_bank} -> expected exact schema"
            )
        else:
            print(f"ok  {voc_bank} -> {first_line}")

    for relative_path in REQUIRED_FILES:
        file_path = root / relative_path
        if not file_path.exists():
            failures.append(f"missing canonical file: {file_path}")
            continue

        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            failures.append(f"empty canonical file: {file_path}")
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
