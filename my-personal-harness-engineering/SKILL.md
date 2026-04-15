---
name: my-personal-harness-engineering
description: "[My Personal Skill] Use when a non-trivial build, refactor, or long-running coding task needs an explicit harness instead of naive single-agent execution. Distills Anthropic's harness-design findings into a level-0 orchestration doctrine: when to stay solo, when to add planner / generator / evaluator roles, when to use sprint contracts or end-of-run QA, when to reset context, and how to simplify the harness as models improve."
metadata:
  version: 0.1.0
---

# My Personal Harness Engineering

## Overview

This skill is the level-0 doctrine for deciding what harness structure to use before or during serious coding work.

It exists to answer:

- should this run stay solo?
- does it need a planner?
- does it need an evaluator?
- does it need sprint contracts or other handoff artifacts?
- does it need hard context resets?
- has the harness become heavier than the current model actually needs?

This skill does not execute the harness itself.
It defines the decision framework and the required artifacts.

Status:

- `v0.1.0`
- treat this as a provisional operating doctrine
- after 3 to 5 real uses, run `my-personal-verified-learning-loop` on the results and tighten the rules

## Trigger Conditions

Use this skill when the task has one or more of these traits:

- the build is likely long enough that coherence drift matters
- the prompt is under-scoped and likely to produce a weak or incomplete implementation
- runtime correctness matters enough that self-evaluation is not trustworthy
- the work spans several files, modules, or phases
- the run may need browser, API, or behavior-level QA
- you are deciding whether to stay single-agent or introduce role separation

Good fits:

- a new feature with both product and engineering ambiguity
- a large refactor with meaningful regression risk
- a long-running application build
- a prototype where feature completeness matters
- any task near the model's reliability frontier

Do not use this skill for:

- tiny fixes with obvious acceptance criteria
- rote edits where coordination costs more than execution
- pure cross-engine review or post-implementation audit by itself; use `my-personal-second-opinion`
- provider/session supervision and recovery mechanics; use `my-personal-subagent-orchestration`

## Core Doctrine

1. Start with the smallest harness that can plausibly work.
2. Add roles only when a concrete failure mode justifies them.
3. Planner and generator are different jobs.
4. Generator and evaluator are different jobs.
5. Evaluate against explicit criteria, not vibes.
6. Handoffs should be artifact-based, not memory-based.
7. Context resets are a tool, not a ritual.
8. Evaluator overhead is justified near the capability frontier, not on every task.
9. As models improve, remove scaffolding that is no longer load-bearing.
10. A harness is successful only if it improves real output quality enough to justify added cost and latency.

## Quick Decision Tree

Use this as the default mental model:

1. If the task is short, clear, and easy to verify, stay `solo`.
2. If it is still modest but omission risk is real, use `solo + explicit checkpoints`.
3. If the prompt is under-scoped and completeness matters, add a `planner`.
4. If self-evaluation is not trustworthy, add an `evaluator`.
5. If the run must survive long duration, parallel workers, or session loss, add durable orchestration.

Before choosing Mode 3 or Mode 4, do a quick overhead check:

- is the likely quality gain worth the added latency?
- is the likely quality gain worth the added token cost?
- is the task actually near the model's current reliability frontier?

## Reference Map

Read only what the current task needs:

- `references/article-findings.md`
  - faithful paraphrase of the Anthropic article's main findings, constraints, and trade-offs
- `references/decision-ladder.md`
  - the practical ladder for choosing solo vs checkpoints vs planner / generator / evaluator
- `references/artifact-contracts.md`
  - the minimum artifact contracts for plan, sprint, handoff, and QA
- `references/integration-boundaries.md`
  - how this skill composes with `my-personal-second-opinion`, `my-personal-subagent-orchestration`, and `my-personal-verified-learning-loop`

## Workflow

### 1. Classify the task

Decide:

- how ambiguous the goal is
- how risky the runtime behavior is
- how verifiable success is
- how long the work is likely to run
- whether parallelism or fresh-context handoffs are actually needed

Then use `references/decision-ladder.md`.

### 2. Choose the minimum viable harness

Default harness modes:

- `solo`
- `solo + explicit checkpoints`
- `planner + generator`
- `planner + generator + evaluator`
- `planner + generator + evaluator + durable worker orchestration`

Do not jump to the heaviest mode by default.

### 3. Define the required artifacts before building

For non-trivial harnesses, define the artifacts up front:

- the plan/spec artifact
- the sprint or build contract
- the progress or handoff artifact
- the QA report artifact

Use `references/artifact-contracts.md`.

### 4. Choose the evaluator type explicitly

There are at least two evaluator shapes:

- code-level evaluator
  - use `my-personal-second-opinion` when you need independent technical review, plan challenge, or post-implementation audit
- behavior-level evaluator
  - use tests, browser automation, API checks, or product interaction when code review alone is not enough

Do not assume one evaluator shape covers both.

### 5. Decide context policy

Use compaction alone when the run is still coherent.

Introduce hard context resets only when:

- the model starts wrapping up early
- the run becomes incoherent
- the handoff artifact is strong enough for a fresh session to resume cleanly

If recoverability across sessions or detached workers matters, also load `my-personal-subagent-orchestration`.

### 6. Run with a simplify-first bias

The harness should stay under constant suspicion.

Ask after real runs:

- which component was actually load-bearing?
- which component was ceremony?
- would the current model now succeed with less scaffolding?

If the answer is yes, remove complexity.

### 7. Learn only from real runs

If the harness failed, over-performed, or needed a changed threshold:

- gather real evidence
- record the smallest correct learning
- use `my-personal-verified-learning-loop` instead of silently rewriting doctrine

## Output Standard

A correct use of this skill should leave behind:

- an explicit harness choice
- explicit role boundaries when more than one role is used
- explicit artifacts for planning, execution, and QA
- a stated reason for any evaluator overhead
- a stated reason for any hard context reset policy
- a simplification opportunity list after the run, if overhead was too high
