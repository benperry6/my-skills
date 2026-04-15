# Lifecycle

## Purpose

This file defines how the docs-first control plane should shrink and stay healthy over time.

The goal is not only to bootstrap a project.
The goal is to keep the live project surface small enough that a future agent can reload it quickly.

## The four states

### `active`

Use for files that are still part of the normal reading order and current operating context.

Default examples:

- `docs/INDEX.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/BACKLOG.md`
- `docs/PROJECT_STATE.md`
- at most one flex-slot file such as `docs/EVAL_V1.md`

### `completed`

Use for execution notes, implementation plans, mismatch reviews, or migration notes that were useful during delivery but no longer drive current work.

Store them under:

- `docs/completed/`

### `archive`

Use for historical source material or old operational notes that might still be useful for forensic context but should not stay in the main reading order.

Store them under:

- `docs/archive/`

### `deprecated`

Use for formerly canonical docs that were replaced by a better source of truth.

Store them under:

- `docs/deprecated/`

Best practice:

- leave a short pointer to the replacement file
- or delete the file if Git history already preserves enough traceability

## File-count discipline

Hard default:

- keep at most 6 live markdown files directly under `docs/`

Interpretation:

- 5 files are the normal operating core
- the 6th file is the flex slot

If a 7th file seems necessary, first ask:

1. can its content be merged into `PROJECT_STATE.md`, `BACKLOG.md`, or `ARCHITECTURE.md`?
2. is it only needed during a short phase and therefore better placed in `completed/` or `archive/`?
3. is it replacing an older canonical file that should move to `deprecated/`?

## Lifecycle by project phase

### `bootstrap`

Allowed:

- the 5-file core
- one bootstrap-only helper file in the flex slot if it clearly helps the handoff

Examples:

- `docs/CONTEXT_SOURCES.md`
- `docs/EVAL_V1.md`

Do not keep both live by reflex.

### `implementation`

Expected:

- bootstrap helper files are either merged into the core docs, moved out of the live set, or deleted
- only rollout-critical helper docs should keep the flex slot

Example:

- `EVAL_V1.md` may stay live if it still gates autonomy rollout
- `CONTEXT_SOURCES.md` usually should not remain live once durable truth is absorbed

### `mature`

Expected:

- only the smallest operational live set remains
- bootstrap-only files are gone from the live root
- completed plans and old notes live outside the active reading order

## Maintenance rhythm

Apply a quick doc-gardening pass:

- after bootstrap approval
- after each major implementation milestone
- before calling a project mature
- whenever the live set hits the cap

Checklist:

1. remove completed work from the active backlog
2. keep `PROJECT_STATE.md` focused on the present, not a diary
3. move finished plans to `completed/`
4. move historical context to `archive/`
5. move replaced canonical docs to `deprecated/`
6. confirm the live set is still 6 files or fewer
