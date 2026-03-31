#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


CANONICAL_FILES = {
    ".agents/business-model.md": "# Business Model\n\n## Snapshot\n\n## Open Questions\n- \n",
    ".agents/storytelling.md": "# Storytelling\n\n## Narrative Core\n\n## Open Questions\n- \n",
    ".agents/know-your-customer.md": "# Know Your Customer\n\n## Snapshot\n\n## Voice of Customer\n\n<!-- Save only real audience language or clearly supported synthesis. Founder assumptions belong in search guidance, not in the canonical file as truth. -->\n\n## Open Questions\n- \n",
    ".agents/performance-memory.md": "# Performance Memory\n\n## Rules\n- Only include real observations.\n- Mark unvalidated items as hypotheses.\n\n## Hypotheses To Test\n- \n",
}

VOC_BANK_HEADER = (
    "entry_id,captured_at,source_type,platform,source_label,source_url,date_seen,"
    "quote,quote_language,evidence_kind,capture_method,segment,journey_stage,"
    "theme_tags,friction_type,risk_type,intensity,evidence_notes\n"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize the canonical context tree for my-personal-context-distillation."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to initialize. Defaults to current working directory.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    helper_workspace = root / ".agents" / "customer-research"
    helper_workspace.mkdir(parents=True, exist_ok=True)
    print(f"ok  ensured directory: {helper_workspace}")

    docs_sources = root / "docs" / "context-sources"
    docs_sources.mkdir(parents=True, exist_ok=True)
    print(f"ok  ensured directory: {docs_sources}")

    voc_bank = docs_sources / "voc-bank.csv"
    if voc_bank.exists():
        print(f"skip existing file: {voc_bank}")
    else:
        voc_bank.write_text(VOC_BANK_HEADER, encoding="utf-8")
        print(f"create file: {voc_bank}")

    for relative_path, initial_content in CANONICAL_FILES.items():
        file_path = root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            print(f"skip existing file: {file_path}")
            continue
        file_path.write_text(initial_content, encoding="utf-8")
        print(f"create file: {file_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
