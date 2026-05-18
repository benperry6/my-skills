# Artifact Contracts

This file defines the minimum artifacts that make a harness recoverable and auditable.

## 1. Plan / Spec artifact

Purpose:

- create a shared target before implementation begins

Minimum fields:

- goal
- user-visible outcome
- non-goals
- success criteria
- key risks
- major constraints

Recommended filenames:

- `PLAN.md`
- `SPEC.md`

## 2. Sprint / Build contract

Purpose:

- translate the high-level plan into a bounded unit of work
- define done before coding begins

Minimum fields:

- scope for this sprint
- explicit out-of-scope items
- required implementation surfaces
- exact verification steps
- artifacts expected at the end

Recommended filenames:

- `SPRINT-01.md`
- `BUILD-CONTRACT.md`

## 3. Progress / Handoff artifact

Purpose:

- allow a fresh session or fresh agent to resume without relying on memory

Minimum fields:

- what was completed
- what remains
- current blockers
- known risks
- next recommended step
- files/modules touched

Recommended filenames:

- `PROGRESS.md`
- `HANDOFF.md`

Treat updating this artifact as a blocking completion step for long runs.

## 4. QA report artifact

Purpose:

- separate implementation from judgment
- preserve evaluator findings as durable evidence

Minimum fields:

- what was tested
- what passed
- what failed
- severity-ordered findings
- confidence level
- recommended fixes
- remaining verification gaps

Recommended filenames:

- `QA-REPORT.md`
- `EVALUATION.md`

## 5. Artifact discipline

Rules:

1. Artifacts are not optional memory aids on serious runs; they are control surfaces.
2. If a fresh session cannot resume cleanly from the artifacts, the harness is too implicit.
3. If artifacts take longer to maintain than the harness benefit they provide, simplify the harness.
