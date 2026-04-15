---
name: my-personal-persistent-context-first
description: "[My Personal Skill] Use when a new technical product starts from a ChatGPT export, brainstorming transcript, founder dump, or other long-form context and must be turned into durable repo context before any implementation begins. Also use when a repo drifted into premature coding, when the user wants a docs-first restart, when a subproject needs local AGENTS/docs bootstrap, or when an agent must stop coding and rebuild persistent project state first."
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

It can summarize and operationalize platform primitives.
It must not overclaim that Antigravity, Claude Code, or Codex publicly document this exact doctrine end to end.

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

- the user says they plan in ChatGPT and then hand off to Codex
- the user wants "persistent context first"
- a repo needs a clean docs-first restart
- a subproject needs its own `AGENTS.md` and `docs/` before coding
- the agent must transform a long export into brief, architecture, backlog, state, and ADR files
- the user wants to delete premature scratch code and restart properly
- the user wants a reusable doctrine for future repos, not just one-off instructions

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

Unless the user explicitly wants a different file contract, bootstrap the target repo or subproject with:

- one repo instruction entrypoint (`AGENTS.md`, `CLAUDE.md`, or equivalent existing convention)
- `docs/INDEX.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTEXT_SOURCES.md`
- `docs/EVAL_V1.md` if the source material already fixes an eval protocol
- `docs/BACKLOG.md`
- `docs/PROJECT_STATE.md`
- `docs/DECISIONS/ADR-0001-initial.md`
- `artifacts/runs/.gitkeep`

If the project already has a stronger equivalent contract, adapt to it rather than duplicating it.

## Transcript Handoff Mode

When the only input is a ChatGPT export or similar long transcript, this skill should still be sufficient to launch the project cleanly.

In that mode, the job is:

1. read the transcript fully enough to extract durable truth
2. separate stable decisions from open questions and discarded brainstorming
3. bootstrap the repo instruction entrypoint and durable docs
4. write the stop line into the state file
5. stop before product code

This means the user should not have to add a second long ad hoc instruction just to get the docs-first layer.

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

This skill ends at the handoff.
It should not silently slide into implementation mode.

## Reference Map

Read only what the current task needs:

- [references/doctrine.md](references/doctrine.md)
  - The durable doctrine and how to translate transcript context into repo truth.
- [references/file-contract.md](references/file-contract.md)
  - The default file contract and what each file is responsible for.
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
