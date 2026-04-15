#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


FILES = {
    "AGENTS.md": """# {project_name}

## Local Doctrine

This area follows a `persistent-context first` doctrine.

Until `docs/PROJECT_STATE.md` explicitly says implementation is authorized:

- only `AGENTS.md`, `docs/**`, and `artifacts/runs/**` may be modified
- no product code may be created

## Reading Order

1. `docs/INDEX.md`
2. `docs/PROJECT_BRIEF.md`
3. `docs/ARCHITECTURE.md`
4. `docs/BACKLOG.md`
5. `docs/PROJECT_STATE.md`
6. `docs/DECISIONS/`
""",
    "docs/INDEX.md": """# Index

1. [PROJECT_BRIEF.md](PROJECT_BRIEF.md)
2. [ARCHITECTURE.md](ARCHITECTURE.md)
3. [BACKLOG.md](BACKLOG.md)
4. [PROJECT_STATE.md](PROJECT_STATE.md)
5. [DECISIONS/ADR-0001-initial.md](DECISIONS/ADR-0001-initial.md)
""",
    "docs/PROJECT_BRIEF.md": """# Project Brief

## Goal

[Fill from transcript/export]

## Scope

[Fill]

## Non-goals

[Fill]

## Constraints

[Fill]
""",
    "docs/ARCHITECTURE.md": """# Architecture

## Modules

[Fill]

## Boundaries

[Fill]

## Open Decisions

[Fill]
""",
    "docs/BACKLOG.md": """# Backlog

## P0

- [ ] Validate bootstrap docs
- [ ] Freeze data contracts
- [ ] Freeze eval protocol
- [ ] Define implementation order
""",
    "docs/PROJECT_STATE.md": """# Project State

## Current Status

- Bootstrap created
- No product code authorized yet

## Next Step

- Distill source material into durable docs

## Done When

- Brief, architecture, backlog, and state are approved
""",
    "docs/DECISIONS/ADR-0001-initial.md": """# ADR-0001 — Docs-first bootstrap

## Status

Accepted

## Decision

This project adopts a `persistent-context first` doctrine.

No implementation starts before durable project docs exist.
""",
}


def write_file(path: Path, content: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a docs-first project context tree.")
    parser.add_argument("target", help="Target repo or subproject directory")
    parser.add_argument("--project-name", default="Project", help="Display name for AGENTS.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    for relative_path, template in FILES.items():
        write_file(target / relative_path, template.format(project_name=args.project_name), args.force)

    keep = target / "artifacts" / "runs" / ".gitkeep"
    keep.parent.mkdir(parents=True, exist_ok=True)
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

    print(f"Initialized persistent context in: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
