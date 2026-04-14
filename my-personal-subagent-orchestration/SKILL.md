---
name: my-personal-subagent-orchestration
description: "[My Personal Skill] Use when a task delegates work to subagents and must stay recoverable across app restarts, detached UI state, quota interruptions, and long-running parallel work. Defines prompt hygiene, inactivity thresholds, durable run registries, recovery/respawn rules, and provider-specific notes for Codex, Claude Code, and Gemini."
metadata:
  version: 1.0.0
---

# My Personal Subagent Orchestration

## Overview

This skill exists to make delegated agent work resumable and boring instead of fragile and guessy.

Use it when one orchestrator session spawns subagents or parallel workers and the task must survive:

- quiet warm-up periods
- app or terminal closure
- visual detachment from spawned sessions
- quota/rate-limit interruptions
- later recovery in a fresh session

This skill is provider-agnostic by default.

It does not define the business logic of the delegated task.
It defines the orchestration discipline around that task.

## Trigger Conditions

Use this skill when the task needs any variation of:

- "spawn one agent per unit of work"
- "run several agents in parallel and supervise them"
- "resume a delegated run after closing Codex / Claude Code / Gemini / terminal"
- "keep track of spawned agents after the UI link is gone"
- "decide whether a quiet agent is still warming up or actually dead"
- "keep a durable registry of translators / reviewers / fixers / researchers"
- "recover from quota interruptions without losing the state of the run"

Do not use this skill for:

- a single-session task with no delegation
- a business-specific review rubric
- provider-specific CLI debugging that is unrelated to orchestration

## Core Doctrine

1. The orchestrator owns the outcome. Spawning workers does not transfer responsibility.
2. The worker prompt should contain only the worker's job and local constraints. Polling, recovery, retry, and routing rules belong to the orchestrator.
3. By default, give one worker one bounded unit of work.
4. Keep delegated workers on inherited/default conversation settings unless the user explicitly authorizes a model or reasoning override.
5. UI attachment is not a source of truth. Keep a durable run registry outside the UI.
6. Quiet is not death. Less than 10 minutes without visible progress is not, by itself, a failure signal by default.
7. Supervise on a measured cadence. Do not busy-poll every 30 seconds when the death threshold is 10 minutes.
8. On resume, reload the registry first, inspect local artifacts second, and only then decide whether to wait, recover, or respawn.
9. A detached worker is not a dead worker. Detachment only means the current session lost its direct visual link.
10. The orchestrator stays active until every delegated unit reaches an explicit terminal state or an explicit handoff artifact is written for a later session.
11. Terminal states must be explicit. Do not leave stale `running` or `waiting` entries after the real outcome changed.
12. If the environment cannot supply the required separation or agent capacity, stop and report that limitation honestly.

## Reference Map

Read only what the current task needs:

- `references/doctrine.md`
  - The reusable orchestration workflow for spawning, supervising, recovering, and replacing subagents.
- `references/run-registry-contract.md`
  - The durable registry contract and example JSON structure for resumable multi-agent runs.
- `references/provider-notes.md`
  - Current verified notes for Codex, Claude Code, and Gemini session/subagent behavior.
- `references/implementation-checklist.md`
  - The practical checklist before trusting a delegated run in production work.

## Workflow

### 1. Decide whether delegation is warranted

Delegate only when parallel work or context isolation materially helps.

Good fits:

- one worker per locale
- one worker per audit surface
- one worker per hypothesis
- one worker per file/module slice

Bad fits:

- tiny tasks where coordination costs more than execution
- sequential tasks where every step blocks the next
- many workers editing the same file

### 2. Define the bounded unit and acceptance rule

Before spawning, define:

- the unit each worker owns
- the artifact or evidence each worker must produce
- the terminal states the orchestrator will use
- the local verification step required before acceptance

Never accept work from a worker's final message alone when the real source of truth is local state on disk, in git, or in an external system.

### 3. Keep worker prompts narrow

Worker prompts should stay task-focused.

Do not overload them with:

- polling cadence
- inactivity policy
- registry instructions
- respawn logic
- orchestration theory

Those rules belong to the orchestrator.

### 4. Spawn and record immediately

Every spawned worker attempt must be recorded immediately in the durable run registry.

At minimum record:

- unit identifier
- phase
- attempt number
- agent id
- status
- started timestamp
- last observed timestamp

If discoverable, also record:

- provider
- nickname
- transcript/session path
- artifact paths
- replacement_of

### 5. Supervise calmly

Default supervision doctrine:

- check on a measured cadence such as every 2 to 5 minutes
- do not interrupt or recadre quiet workers under the inactivity threshold
- treat more than 10 minutes with no observable progress as the first point where replacement becomes reasonable

If the task-specific skill needs a stricter threshold, that skill may override this one explicitly.

### 6. Recover before respawning

When a session is resumed after the app or terminal was closed:

1. reload the run registry
2. inspect local artifacts and timestamps
3. try recovery or reattachment if the environment supports it
4. only if there is still no progress beyond the inactivity threshold should the orchestrator respawn a replacement worker

Respawns must be recorded as new attempts linked with `replacement_of`.

### 7. Keep the orchestrator alive

The orchestrator must not stop at "all workers spawned".

It remains responsible for:

- observing progress
- updating the registry
- routing follow-up workers such as reviewers or fixers
- applying local verification
- deciding acceptance or rejection
- leaving a durable handoff if the full run cannot finish in the current session

## Output Standard

A well-run delegated workflow should leave behind:

- a durable run registry path
- explicit terminal states for every delegated unit
- enough metadata to recover detached workers later
- a clear acceptance trail tied to local verification, not just chat output

If the run is paused between sessions, the user should be able to reopen the project and resume from the registry instead of reconstructing state from memory.
