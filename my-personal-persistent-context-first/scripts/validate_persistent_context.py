#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = [
    "docs/INDEX.md",
    "docs/PROJECT_BRIEF.md",
    "docs/ARCHITECTURE.md",
    "docs/BACKLOG.md",
    "docs/PROJECT_STATE.md",
    "docs/DECISIONS/ADR-0001-initial.md",
    "artifacts/runs/.gitkeep",
]

OPTIONAL_LIVE = {
    "docs/CONTEXT_SOURCES.md",
    "docs/EVAL_V1.md",
}

ALLOWED_LIVE = {item for item in REQUIRED if item.startswith("docs/") and item.endswith(".md")} | OPTIONAL_LIVE

MAX_LIVE_DOCS = 6

UNEXPECTED_WHEN_DOCS_ONLY = [
    "src",
    "app",
    "migrations",
    "dist",
    "node_modules",
    "package.json",
    "package-lock.json",
    "pyproject.toml",
    "Cargo.toml",
]


def detect_lifecycle_stage(project_state: Path) -> str | None:
    if not project_state.exists():
        return None

    text = project_state.read_text(encoding="utf-8")
    in_stage_section = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            in_stage_section = line.lower() == "## lifecycle stage"
            continue
        if not in_stage_section:
            continue
        if line.startswith("- "):
            value = line[2:].strip().lower()
            if value in {"bootstrap", "implementation", "mature"}:
                return value
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a docs-first persistent-context bootstrap.")
    parser.add_argument("target", help="Target repo or subproject directory")
    parser.add_argument(
        "--instruction-file",
        default="auto",
        help="Instruction entrypoint filename. Use 'auto' to detect AGENTS.md or CLAUDE.md if present.",
    )
    parser.add_argument(
        "--docs-only",
        action="store_true",
        help="Fail if common product-code paths exist",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if args.instruction_file == "auto":
        detected = None
        for candidate in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            if (target / candidate).exists():
                detected = candidate
                break
        if detected is None:
            print("Missing instruction entrypoint: none of AGENTS.md, CLAUDE.md, or GEMINI.md found.")
            return 1
        instruction_file = detected
    else:
        instruction_file = args.instruction_file

    required = [instruction_file, *REQUIRED]
    missing = [item for item in required if not (target / item).exists()]

    live_docs = sorted(
        path.relative_to(target).as_posix()
        for path in (target / "docs").glob("*.md")
        if path.is_file()
    )
    unexpected_live = [item for item in live_docs if item not in ALLOWED_LIVE]
    live_doc_overflow = len(live_docs) > MAX_LIVE_DOCS

    lifecycle_stage = detect_lifecycle_stage(target / "docs" / "PROJECT_STATE.md")
    lifecycle_violations = []
    if lifecycle_stage in {"implementation", "mature"} and "docs/CONTEXT_SOURCES.md" in live_docs:
        lifecycle_violations.append(
            "docs/CONTEXT_SOURCES.md should not remain live once the project leaves bootstrap."
        )
    if lifecycle_stage == "mature" and "docs/EVAL_V1.md" in live_docs:
        lifecycle_violations.append(
            "docs/EVAL_V1.md should usually be archived, deprecated, merged, or deleted in mature phase."
        )

    unexpected = []
    if args.docs_only:
        unexpected = [item for item in UNEXPECTED_WHEN_DOCS_ONLY if (target / item).exists()]

    if missing:
        print("Missing required files:")
        for item in missing:
            print(f"- {item}")

    if unexpected:
        print("Unexpected code/product paths present in docs-only mode:")
        for item in unexpected:
            print(f"- {item}")

    if unexpected_live:
        print("Unexpected live docs in docs/ root:")
        for item in unexpected_live:
            print(f"- {item}")

    if live_doc_overflow:
        print(f"Live docs exceed the default cap of {MAX_LIVE_DOCS}:")
        for item in live_docs:
            print(f"- {item}")

    if lifecycle_stage is None:
        print("Missing or invalid lifecycle stage in docs/PROJECT_STATE.md (expected bootstrap, implementation, or mature).")

    if lifecycle_violations:
        print("Lifecycle violations:")
        for item in lifecycle_violations:
            print(f"- {item}")

    if missing or unexpected or unexpected_live or live_doc_overflow or lifecycle_stage is None or lifecycle_violations:
        return 1

    print(f"Persistent context bootstrap looks valid: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
