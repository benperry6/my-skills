---
name: my-personal-persistent-context-first
description: "[My Personal Skill] Use when a new technical product starts from a ChatGPT export, brainstorming transcript, founder dump, or other long-form context and must be turned into durable repo context before any implementation begins. This skill owns the technical implementation control plane: repo instruction entrypoint, docs-first bootstrap, project brief, architecture, backlog, project state, ADRs, and the stop line before code. Not for `.agents/business-model.md`, `.agents/storytelling.md`, `.agents/know-your-customer.md`, `.agents/performance-memory.md`, or VoC/context distillation work."
---

# Persistent Context First

## Purpose

This skill exists to stop code-first thrash on serious projects.

Its job is to turn raw planning material into durable repo context first, then hold the line until that context is good enough to guide implementation across sessions and agents.

This skill is not a code generator.
It is a bootstrap, restart, and governance skill.

## Compatibility Contract

This skill must stay infrastructure-agnostic in its visible content.

That means:

- do not embed one machine's private paths
- do not hardcode one team's MCP layout
- do not describe private wrapper scripts, local browser ports, or secret bootstrap internals

At the same time, it must remain compatible with stronger local setups by convention.

So always:

- inspect the target repo for an existing instruction-file convention before creating anything
- preserve an existing convention if one already exists
- use a tool-native or repo-native instruction entrypoint instead of forcing one filename everywhere
- keep the durable docs contract tool-agnostic even if the instruction entrypoint differs

Practical rule:

- if the repo already has a canonical instruction file pattern, keep it
- if the repo has no convention yet, create the current tool's native instruction file or the explicitly requested one
- do not expose a private machine setup just to stay compatible with it

## What This Skill Owns

This skill owns the transition from:

- "we have a long ChatGPT or brainstorm transcript"
- "the repo or subproject has little or no durable context"
- "someone already started coding too early"

to:

- a local repo instruction entrypoint that routes work correctly
- a durable `docs/` contract for the project or subproject
- a prioritized backlog
- a current state file that says what happens next
- an explicit stop line: no product code until bootstrap is approved

## What This Skill Does Not Own

This skill does not own:

- implementing the product itself
- deciding frontend aesthetics
- inventing business scope from thin air
- pretending public platform docs define the exact doctrine already
- canonical business, narrative, customer, or performance context for marketing and communication work
- `.agents/business-model.md`, `.agents/storytelling.md`, `.agents/know-your-customer.md`, or `.agents/performance-memory.md`

It can summarize and operationalize platform primitives.
It must not overclaim that Antigravity, Claude Code, or Codex publicly document this exact doctrine end to end.

If the primary need is to turn messy founder/business/customer/performance material into durable marketing or communication context, use `my-personal-context-distillation` instead.

## Hard Reroute Gate

Do not start this skill if the user's real target is the canonical business-context layer instead of the technical implementation control plane.

Immediate reroute to `my-personal-context-distillation` when the request is mainly about:

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`
- `docs/context-sources/voc-bank.csv`
- business context bootstrap
- founder/business/customer/performance context distillation
- voice-of-customer research or evidence-bank maintenance

Practical rule:

- if the durable output should govern coding work, repo structure, and implementation sequencing, this skill owns it
- if the durable output should govern messaging, audience understanding, customer truth, or marketing reasoning, reroute to `my-personal-context-distillation`
- if both layers are needed, bootstrap the technical control plane first, then hand off to `my-personal-context-distillation`

## Boundary Against Context Distillation

This skill and `my-personal-context-distillation` both operate on context, but they do not own the same layer.

- `my-personal-persistent-context-first` owns the technical project control plane before implementation:
  - repo instruction entrypoint
  - docs-first bootstrap
  - project brief
  - architecture
  - backlog
  - current state
  - ADRs
  - explicit stop line before code
- `my-personal-context-distillation` owns the canonical business/marketing/customer/performance truth used by downstream messaging, CRO, SEO, and communication work.

Practical rule:

- if the context must become durable so a technical product can be implemented safely across sessions and agents, this skill owns it
- if the context must become durable so AI can reason better about the business, audience, positioning, or performance of a product/site/brand, `my-personal-context-distillation` owns it
- when both are needed, run this skill first for the implementation control plane, then run `my-personal-context-distillation` for the business/marketing context layer

## Core Doctrine

1. Persistent context beats chat memory.
2. A transcript export is source material, not the operating system of the project.
3. For a serious project, bootstrap docs are a prerequisite, not a nice-to-have.
4. If coding started too early, stop, reset, and rebuild the context layer first.
5. The context layer must live in repo files that survive compaction, thread changes, and agent handoffs.
6. The repo instruction entrypoint should stay short and route to durable docs; the spec should live in `docs/`.
7. No product code resumes until the bootstrap is explicitly approved.
8. Reusable doctrine belongs in a reusable skill; project-specific truth belongs in the repo.

## Trigger Conditions

Use this skill when:

- the user says they plan in ChatGPT and then hand off to Codex or another coding agent for implementation
- the user wants "persistent context first"
- a repo needs a clean docs-first restart
- a subproject needs its own `AGENTS.md` and `docs/` before coding
- the agent must transform a long export into brief, architecture, backlog, state, and ADR files
- the user wants to delete premature scratch code and restart properly
- the user wants a reusable doctrine for future repos, not just one-off instructions
- a technical product, SaaS, app, system, or engineering-heavy subproject is about to move from transcript/planning material into real implementation
- the next reliable step depends on turning long-form chat/transcript context into durable implementation guidance first

Strong trigger phrases include:

- ChatGPT export
- docs-first
- persistent context
- bootstrap this repo
- restart cleanly
- stop coding and re-plan
- create AGENTS and docs first
- Antigravity-style planning
- planning mode before code
- voici l'export ChatGPT
- lis cette conversation et bootstrap le projet
- transforme ce transcript en contexte persistant
- ne code pas, prepare d'abord le projet

Do not trigger this skill just because the input is long-form context.

The trigger is not "there is a transcript."
The trigger is "this transcript is about to function as the operating context for technical implementation, and that context is not yet durably materialized."

If the transcript's main job is instead to update business context, audience understanding, narrative, or performance learnings for marketing/site/communication work, use `my-personal-context-distillation` instead.

## Source-of-Truth Hierarchy

When this skill runs, use this order:

1. Explicit user instructions in the current conversation
2. Existing durable repo truth already accepted by the user
3. The provided transcript/export/source dump
4. Official platform primitives and local verified environment behavior
5. Agent inference only where clearly marked as inference

Never invert this order.

## Preflight

Before producing the bootstrap, explicitly classify the inputs:

- verified and durable
- verified but non-durable
- ambiguous
- missing

If critical material is missing, stop and ask for it.
Do not compensate by inventing scope or architecture.

## Default Deliverables

Unless the user explicitly wants a different file contract, bootstrap the target repo or subproject with this default live set:

- one repo instruction entrypoint (`AGENTS.md`, `CLAUDE.md`, or equivalent existing convention)
- `docs/INDEX.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/BACKLOG.md`
- `docs/PROJECT_STATE.md`
- `docs/DECISIONS/ADR-0001-initial.md`
- `artifacts/runs/.gitkeep`

Optional bootstrap-only live files:

- `docs/CONTEXT_SOURCES.md`
- `docs/EVAL_V1.md`

But do not create both by reflex.
The default rule is: keep the live `docs/` root as small as possible and add at most one extra bootstrap-only file unless the user explicitly wants a richer contract.

If the project already has a stronger equivalent contract, adapt to it rather than duplicating it.

## Live File Budget

This skill should stay close to the spirit of Antigravity's public artifacts:

- one active planning surface
- one active task surface
- one current-state surface
- a small number of supporting canonical docs

So the hard default is:

- at most 6 live markdown files directly under `docs/`
- the repo instruction entrypoint does not count toward that cap
- `docs/DECISIONS/`, `docs/completed/`, `docs/archive/`, and `docs/deprecated/` do not count toward that cap

Interpretation:

- 5 core live docs are normal
- the 6th slot is the flex slot
- if a 7th live doc seems necessary, consolidate first instead of adding another file

## File Lifecycle

Every durable doc must belong to one of these states:

- `active`
  - currently part of the reading order and still operational
- `completed`
  - useful record of finished implementation work or finished plans, but no longer part of the live control plane
- `archive`
  - historical material worth keeping for future forensic context, but not needed in normal operation
- `deprecated`
  - formerly canonical material replaced by a newer source of truth

Default mapping:

- live root docs in `docs/*.md` are `active`
- finished execution notes and finished plans move to `docs/completed/`
- old but still useful historical material moves to `docs/archive/`
- replaced canonical docs move to `docs/deprecated/`

## Maintenance Rules

This skill is not only for bootstrap. It must also enforce doc gardening during the project.

Rules:

1. `docs/BACKLOG.md` keeps only active and upcoming work.
2. Completed items should be removed from the active backlog once their outcome is folded back into durable truth.
3. `docs/PROJECT_STATE.md` is the current status file, not a full project diary.
4. Bootstrap-only files must either be absorbed into the permanent docs, moved out of the live set, or deleted once they no longer earn their keep.
5. If a file is no longer in the normal reading order, it should not stay live at `docs/`.
6. If a canonical file is replaced, move the old one to `docs/deprecated/` with a pointer to the replacement or delete it if the repo history already preserves enough traceability.
7. Do not let live docs accumulate just because they were once useful during bootstrap.

Lifecycle expectations by phase:

- `bootstrap`
  - the project may use the flex slot for one bootstrap-only helper file
- `implementation`
  - `CONTEXT_SOURCES.md` should usually be gone from the live set
  - `EVAL_V1.md` may stay live only if it still drives rollout decisions
- `mature`
  - keep only the smallest operational live set
  - bootstrap-only files should be archived, deprecated, merged, or deleted

## Transcript Handoff Mode

When the only input is a ChatGPT export or similar long transcript, this skill should still be sufficient to launch the project cleanly.

In that mode, the job is:

1. read the transcript fully enough to extract durable truth
2. separate stable decisions from open questions and discarded brainstorming
3. bootstrap the repo instruction entrypoint and durable docs
4. write the stop line into the state file
5. stop before product code

This means the user should not have to add a second long ad hoc instruction just to get the docs-first layer.

The first implementation-ready bootstrap is not the end state of the docs.
As the repo matures, the live set should shrink, not grow.

## Workflow

### 1. Decide the target scope

Determine whether the bootstrap belongs at:

- repo root
- a dedicated subproject folder
- a new subfolder that will later contain the product

If the repo already mixes multiple concerns, prefer a dedicated subproject folder with its own deeper `AGENTS.md`.

Also determine the instruction-file strategy:

- preserve existing repo convention if present
- otherwise choose the instruction entrypoint appropriate for the active tool or the user's explicit preference

### 2. Decide the reset policy

If premature code already exists, ask whether the user wants:

- preserve and curate
- snapshot then reset
- hard delete

Never hard delete without explicit user approval.

If hard delete is explicitly requested, do not argue for preserving scratch code.

See [references/reset-policy.md](references/reset-policy.md).

### 3. Initialize the bootstrap tree

Use [scripts/init_persistent_context.py](scripts/init_persistent_context.py) to create the file skeleton.

The script only creates the durable structure and placeholder content.
It does not decide the project truth for you.
By default it creates only the core live set plus the repo instruction entrypoint.
Optional bootstrap-only files must be requested explicitly.

### 4. Distill the source material into durable docs

Populate the docs from the transcript/export and accepted repo truth:

- `PROJECT_BRIEF.md`
  - goal
  - scope
  - non-goals
  - constraints
  - business rules already fixed
- `ARCHITECTURE.md`
  - modules
  - boundaries
  - data flow
  - open architectural decisions
- `CONTEXT_SOURCES.md`
  - what source material was used
  - what became durable repo truth
  - what remains only historical source material
- `EVAL_V1.md`
  - if the source material already fixed the evaluation doctrine, capture it now instead of leaving it trapped in the transcript
- `BACKLOG.md`
  - prioritized tasks
  - dependencies
  - "done when" criteria
- `PROJECT_STATE.md`
  - current status
  - what changed
  - what happens next
- `ADR-0001-initial.md`
  - why the docs-first doctrine applies here

When optional bootstrap-only files are created, they must later be merged, archived, deprecated, or deleted according to the lifecycle rules above.

### 5. Freeze the stop line

Until the user validates the bootstrap:

- do not create product code
- do not recreate `src/`, `package.json`, `migrations`, or equivalent product files
- do not continue old implementation tickets

Use [scripts/validate_persistent_context.py](scripts/validate_persistent_context.py) with `--docs-only` when the target must remain code-free during bootstrap.

### 6. Hand off to implementation only after approval

Once the bootstrap is approved:

- update `PROJECT_STATE.md` to say implementation is authorized
- keep the backlog as the execution queue
- keep the architecture and ADRs updated as the project evolves
- keep the live-file budget under control as the project evolves

This skill ends at the handoff.
It should not silently slide into implementation mode.

## Reference Map

Read only what the current task needs:

- [references/doctrine.md](references/doctrine.md)
  - The durable doctrine and how to translate transcript context into repo truth.
- [references/file-contract.md](references/file-contract.md)
  - The default file contract and what each file is responsible for.
- [references/lifecycle.md](references/lifecycle.md)
  - The active/completed/archive/deprecated lifecycle and the live-file budget.
- [references/platform-primitives.md](references/platform-primitives.md)
  - Official and locally verified primitives from Codex, Claude Code, and Antigravity.
- [references/reset-policy.md](references/reset-policy.md)
  - How to choose between curate, snapshot-reset, and hard delete.

## Practical Rules

- Prefer a short routing instruction entrypoint plus durable docs over a giant instruction dump.
- Prefer docs at the target subproject level when the repo contains multiple unrelated domains.
- Capture project truth in the repo, not in the skill.
- Capture reusable doctrine in the skill, not in one repo's docs.
- When public docs are partial, say what is official and what is your transposition.
- If the repo drifts again into code-first work, re-run this skill before resuming implementation.
- The skill should be shareable with partners without leaking private machine setup.
- The skill should leave behind a small live control plane, not a pile of bootstrap files.
