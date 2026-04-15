#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = [
    "AGENTS.md",
    "docs/INDEX.md",
    "docs/PROJECT_BRIEF.md",
    "docs/ARCHITECTURE.md",
    "docs/BACKLOG.md",
    "docs/PROJECT_STATE.md",
    "docs/DECISIONS/ADR-0001-initial.md",
    "artifacts/runs/.gitkeep",
]

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a docs-first persistent-context bootstrap.")
    parser.add_argument("target", help="Target repo or subproject directory")
    parser.add_argument(
        "--docs-only",
        action="store_true",
        help="Fail if common product-code paths exist",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    missing = [item for item in REQUIRED if not (target / item).exists()]

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

    if missing or unexpected:
        return 1

    print(f"Persistent context bootstrap looks valid: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
