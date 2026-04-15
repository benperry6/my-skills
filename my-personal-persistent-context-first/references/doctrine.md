# Doctrine

This skill operationalizes one simple rule:

For a serious technical project, durable repo context must exist before implementation starts.

The durable context layer has four jobs:

1. Survive session loss, compaction, and agent handoff
2. Replace dependence on one giant transcript
3. Give the next agent a deterministic reading order
4. Prevent premature coding from becoming the de facto plan

It also has to stay shareable:

- reusable with partners
- compatible with stronger local setups
- free of private machine implementation details

## Why transcripts are not enough

A ChatGPT export is useful raw material, but it is not enough on its own because:

- it is long and expensive to reload repeatedly
- priorities, decisions, and open questions are not always separated cleanly
- one transcript is not a stable control plane for multiple future sessions
- implementation can drift if the repo does not contain the latest accepted truth

## Durable layer vs transient layer

Durable layer:

- repo instruction entrypoint
- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/BACKLOG.md`
- `docs/PROJECT_STATE.md`
- ADRs

Transient layer:

- raw transcript exports
- scratch notes in chat
- intermediate agent reasoning
- throwaway experiments

Optional bootstrap-only durable helpers:

- `docs/CONTEXT_SOURCES.md`
- `docs/EVAL_V1.md` when the evaluation protocol is already fixed and still operationally relevant

The job of this skill is to convert from transient to durable, then compact the live layer so it does not stay bloated forever.

## Stop line

The most important behavioral rule is the stop line:

If bootstrap is not approved yet, the agent must not write product code.

That includes:

- `src/`
- `app/`
- `package.json`
- `pyproject.toml`
- migrations
- build output
- tests tied to unfinished code

If any of that already exists from a bad start, the agent must not continue it by inertia.

## Compatibility without disclosure

This doctrine should adapt to the environment without documenting private machine wiring.

The correct pattern is:

- inspect the repo for existing instruction-file and memory conventions
- follow them if they exist
- otherwise create the minimum tool-appropriate entrypoint

The incorrect pattern is:

- dump a private local setup into the shared skill
- make the skill depend on hidden machine-only file paths to make sense

## Subproject-first preference

If a repo contains multiple unrelated concerns, a new product should usually start in a dedicated subproject folder.

That folder should get:

- its own local `AGENTS.md`
- its own `docs/`
- its own backlog and state

This lets deeper instructions override the generic root rules without polluting the whole repo.

## Exit condition

This skill is finished when the project has a durable operating context and a clean handoff to implementation.

It is not finished when the docs skeleton merely exists.

## Small live control plane

The public Antigravity pattern is closer to a few active artifacts than to a large doc tree.

This skill should therefore prefer:

- a small active reading order
- a current plan/task surface
- a current state surface
- a small number of supporting canonical docs

Default interpretation:

- keep at most 6 live markdown files directly under `docs/`
- use the 6th slot only when a bootstrap-only or rollout-critical doc clearly earns it
- move old or finished material out of the live set instead of letting it accumulate
