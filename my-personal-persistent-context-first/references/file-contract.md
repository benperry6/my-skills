# File Contract

## Repo instruction entrypoint

Purpose:

- short local routing file
- defines the bootstrap discipline
- points to the durable docs

It should not become the full spec.

Possible filenames depend on the tool or existing repo convention:

- `AGENTS.md`
- `CLAUDE.md`
- another already-established local convention

## `docs/INDEX.md`

Purpose:

- define the reading order
- point to canonical files
- tell the next session where to start

## `docs/PROJECT_BRIEF.md`

Purpose:

- define the product goal
- define scope and non-goals
- define business constraints already fixed

## `docs/ARCHITECTURE.md`

Purpose:

- describe modules and boundaries
- show how work should be decomposed later
- record what is still open architecturally

## `docs/BACKLOG.md`

Purpose:

- order the work
- make dependencies explicit
- keep "done when" visible

## `docs/PROJECT_STATE.md`

Purpose:

- tell any future session what changed
- say whether the project is still in bootstrap or may resume implementation
- define the immediate next action
- declare the lifecycle phase (`bootstrap`, `implementation`, or `mature`)

## `docs/DECISIONS/ADR-0001-initial.md`

Purpose:

- explain why the docs-first doctrine applies here
- make the restart rationale durable

## `artifacts/runs/.gitkeep`

Purpose:

- reserve a deterministic place for future run manifests and other reproducible execution artifacts

## Optional later files

Common later additions:

- `docs/CONTEXT_SOURCES.md`
- `docs/EVAL_V1.md`
- `docs/DATA_CONTRACTS.md`
- `docs/IMPLEMENTATION_ORDER.md`
- `docs/DECISIONS/ADR-0002-*.md`

These should be added only when the project truth needs them, not by reflex.

## Active file budget

Default live-set policy:

- only markdown files directly under `docs/` count as live control-plane docs
- keep that live set at 6 files or fewer
- the instruction entrypoint and ADR folders do not count toward that cap
- `docs/completed/`, `docs/archive/`, and `docs/deprecated/` are explicitly outside the live set

Practical interpretation:

- `INDEX`, `PROJECT_BRIEF`, `ARCHITECTURE`, `BACKLOG`, and `PROJECT_STATE` form the normal core
- one additional live doc may exist when it clearly earns the flex slot
- if another file seems necessary, consolidate before adding
