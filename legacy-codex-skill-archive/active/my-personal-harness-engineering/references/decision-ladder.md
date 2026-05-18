# Harness Decision Ladder

Use this ladder to choose the lightest harness that still protects quality.

## Default question

What is the smallest harness that gives a trustworthy result for this task?

## Mode 0 — Solo

Use solo when all of the following are true:

- the task is short
- the acceptance criteria are clear
- the implementation is easy to verify
- under-scoping risk is low
- self-evaluation risk is low

Typical examples:

- obvious bug fix
- narrow refactor
- small, well-specified component change

## Mode 1 — Solo + explicit checkpoints

Use this when:

- the task is still modest
- but drift or omission risk is no longer trivial

Add:

- a short plan
- a local verification checkpoint
- a final check against stated acceptance criteria

## Mode 2 — Planner + Generator

Use this when:

- the raw prompt is likely to under-scope the product
- the task has meaningful product ambiguity
- completeness matters more than just code correctness

Planner is justified when the run needs a richer spec before coding starts.

## Mode 3 — Planner + Generator + Evaluator

Use this when one or more of these are true:

- the generator is likely to self-approve weak work
- runtime behavior matters enough that code alone is not trustworthy
- the task is close to the model's reliability frontier
- there is meaningful risk of feature incompleteness or hidden stubs

Evaluator overhead is justified here.

## Mode 4 — Full harness with durable orchestration

Use this only when the run also needs:

- parallel workers
- multi-session recoverability
- detached worker supervision
- explicit restart / recovery behavior

At this point, also load:

- `my-personal-subagent-orchestration`

## Starting heuristics

These are provisional heuristics, not laws:

- if the task looks comfortably under `~45 minutes` and under `~3 files`, do not default to the full harness
- if the task is larger, riskier, or more ambiguous than that, explicitly justify staying light

Use real evidence later to tighten these thresholds.

## Context policy decision

### Use compaction only

When:

- the run is still coherent
- the model is not showing wrap-up anxiety
- the session is still handling retrieval well

### Introduce hard context resets

When:

- the model starts ending work prematurely
- the run becomes incoherent
- a clean handoff artifact can carry the state forward

Do not add resets only because an older model needed them in a paper.

## Evaluator choice

### Code-level evaluator

Use when you need:

- technical critique
- plan challenge
- independent code review
- post-implementation audit

Load:

- `my-personal-second-opinion`

### Behavior-level evaluator

Use when you need:

- browser interaction
- API verification
- database state checks
- user-like QA

This may be separate from cross-engine review.
