# File Contract

## `AGENTS.md`

Purpose:

- short local routing file
- defines the bootstrap discipline
- points to the durable docs

It should not become the full spec.

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

## `docs/DECISIONS/ADR-0001-initial.md`

Purpose:

- explain why the docs-first doctrine applies here
- make the restart rationale durable

## `artifacts/runs/.gitkeep`

Purpose:

- reserve a deterministic place for future run manifests and other reproducible execution artifacts

## Optional later files

Common later additions:

- `docs/EVAL_V1.md`
- `docs/DATA_CONTRACTS.md`
- `docs/IMPLEMENTATION_ORDER.md`
- `docs/DECISIONS/ADR-0002-*.md`

These should be added only when the project truth needs them, not by reflex.
