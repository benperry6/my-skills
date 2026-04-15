# Doctrine

This skill operationalizes one simple rule:

For a serious technical project, durable repo context must exist before implementation starts.

The durable context layer has four jobs:

1. Survive session loss, compaction, and agent handoff
2. Replace dependence on one giant transcript
3. Give the next agent a deterministic reading order
4. Prevent premature coding from becoming the de facto plan

## Why transcripts are not enough

A ChatGPT export is useful raw material, but it is not enough on its own because:

- it is long and expensive to reload repeatedly
- priorities, decisions, and open questions are not always separated cleanly
- one transcript is not a stable control plane for multiple future sessions
- implementation can drift if the repo does not contain the latest accepted truth

## Durable layer vs transient layer

Durable layer:

- `AGENTS.md`
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

The job of this skill is to convert from transient to durable.

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
