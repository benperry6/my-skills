#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


CORE_FILES = {
    "__INSTRUCTION_FILE__": """# {project_name}

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

## Out Of The Live Set

- `docs/completed/`
- `docs/archive/`
- `docs/deprecated/`
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

## Lifecycle Stage

- bootstrap

## Current Status

- Bootstrap created
- No product code authorized yet

## Next Step

- Distill source material into durable docs

## Done When

- Brief, architecture, backlog, and state are approved

## Live File Policy

- Keep `docs/` root at 6 live markdown files or fewer
- Move finished plans to `docs/completed/`
- Move historical context to `docs/archive/`
- Move replaced canonical docs to `docs/deprecated/`
""",
    "docs/DECISIONS/ADR-0001-initial.md": """# ADR-0001 — Docs-first bootstrap

## Status

Accepted

## Decision

This project adopts a `persistent-context first` doctrine.

No implementation starts before durable project docs exist.
""",
}

OPTIONAL_FILES = {
    "context-sources": (
        "docs/CONTEXT_SOURCES.md",
        """# Context Sources

## Input Sources

- [Fill]

## Durable Truth Created From These Sources

- [Fill]

## Exit Rule

- Once durable truth is absorbed into the core docs, move this file out of the live set or delete it.
""",
    ),
    "eval-v1": (
        "docs/EVAL_V1.md",
        """# Eval v1

## Status

- [Fill if the source material already fixes an eval protocol]

## Exit Rule

- Keep this file live only while it still gates rollout or autonomy decisions.
""",
    ),
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
    parser.add_argument(
        "--instruction-file",
        default="AGENTS.md",
        help="Repo instruction entrypoint filename to create (for example AGENTS.md or CLAUDE.md)",
    )
    parser.add_argument(
        "--with-context-sources",
        action="store_true",
        help="Create docs/CONTEXT_SOURCES.md as the single optional flex-slot live doc",
    )
    parser.add_argument(
        "--with-eval-v1",
        action="store_true",
        help="Create docs/EVAL_V1.md as the single optional flex-slot live doc",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    optional_selections = [flag for flag in ("context-sources", "eval-v1") if getattr(args, f"with_{flag.replace('-', '_')}")]
    if len(optional_selections) > 1:
        parser.error(
            "The default live-file budget allows only one optional flex-slot file. "
            "Choose either --with-context-sources or --with-eval-v1."
        )

    for relative_path, template in CORE_FILES.items():
        resolved_path = args.instruction_file if relative_path == "__INSTRUCTION_FILE__" else relative_path
        write_file(target / resolved_path, template.format(project_name=args.project_name), args.force)

    for selection in optional_selections:
        relative_path, template = OPTIONAL_FILES[selection]
        write_file(target / relative_path, template, args.force)

    keep = target / "artifacts" / "runs" / ".gitkeep"
    keep.parent.mkdir(parents=True, exist_ok=True)
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

    print(f"Initialized persistent context in: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
