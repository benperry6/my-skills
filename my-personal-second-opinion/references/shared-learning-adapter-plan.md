# Shared Learning Adapter Plan — Second Opinion

This document defines the current convergence plan between:

- `my-personal-second-opinion`
- `my-personal-verified-learning-loop`

It is a phased plan, not a claim that convergence is already complete.

## Verified current state

What is already true in local evidence:

- `second_opinion_runner.py` already owns routing, repair, post-implementation audit mode, runtime persistence, de-duplication, and git persist
- `my-personal-verified-learning-loop` already owns the shared doctrine for triggers, hooks, confidence tiers, promotion rules, and structured incident vocabulary
- `my-personal-paid-tracking-foundation` already proved that the shared loop works well as a doctrinal consumer with a local overlay

## Decision

`my-personal-second-opinion` remains a temporary special implementation on the path to convergence.

That means:

- do not replace the runner with the shared helper right now
- do not leave `second-opinion` permanently outside the shared learning doctrine either
- converge through an adapter layer first

## Why the runner stays special for now

The runner currently provides real capabilities that the shared helper does not yet match:

- engine-specific retry chains
- fallback ordering
- repair-time structured capture
- post-implementation audit mode
- native de-duplication
- native git-persist behavior
- automatic resume semantics after repair

Replacing the runner now would be a regression.

## Adapter strategy

The near-term integration is an adapter and bridge layer, not a replacement.

Target behavior:

- the runner keeps its native storage and persistence logic
- the runner aligns its terminology with the shared trigger and hook doctrine
- the runner emits a shared-compatible incident mirror immediately after accepting a native incident
- the shared mirror preserves runner-specific richness through `extensions`, not through schema flattening

## Current machine-readable contract state

The shared loop now exposes:

- `my-personal-verified-learning-loop/references/runtime-incident.schema.json`

Therefore:

- adapter output can now target a real machine-readable contract
- the next hardening step is to add an explicit compatibility smoke test for the adapter output

## Phase plan

### Phase 1 — Semantic alignment

Goal: align concepts without changing runner behavior.

Deliverables:

- `references/learning-overlay.md` for second-opinion
- explicit mapping from native runner fields to the shared incident shape
- explicit mapping from runner fire-points to shared hook names
- explicit statement that the runner remains the authoritative persistence layer during incubation

Exit criteria:

- no ambiguity remains about how a native incident maps to the shared doctrine

### Phase 2 — Adapter and mandatory shared-compatible mirror

Goal: prevent learning fragmentation.

Deliverables:

- a `to_shared_incident(native_record)` translation function or equivalent
- a mandatory shared-compatible mirror write after each accepted native runtime incident
- no downgrade of native runner capture or persistence behavior

Preferred transitional shape:

- keep the native runtime store untouched
- add a shared-compatible export/mirror as a transition layer until one canonical storage shape becomes safe

Exit criteria:

- second-opinion learnings are no longer trapped in a bespoke format only

Current status:

- the adapter bridge is implemented when the runner accepts a native runtime incident
- the emitted bridge artifacts are:
  - `references/runtime-learning.shared.json`
  - `references/runtime-learning.shared.md`

### Phase 3 — Machine validation

Goal: guard against silent schema drift.

Deliverables:

- a machine-readable incident contract for the shared loop
- a smoke test that validates second-opinion adapter output against that contract

Exit criteria:

- adapter breakage becomes observable during maintenance instead of months later

### Phase 4 — Upstreaming

Goal: move stable producer-grade patterns from the runner into the shared loop.

Candidate upstream targets:

- de-duplication strategy
- richer extension handling
- git-persist semantics
- producer-grade batch append behavior

Exit criteria:

- at least one currently runner-only persistence feature becomes shared infrastructure

### Phase 5 — Convergence decision

Only after phases 2 to 4 should we decide whether:

- the runner keeps a permanent special persistence path
- the runner consumes a matured shared helper
- or both collapse into one canonical implementation

## Non-goals

This plan does **not** do any of the following yet:

- replace `second_opinion_runner.py`
- rewrite runtime-learning history
- claim that second-opinion is already a doctrinal consumer like paid-tracking
- force shared-helper writes that drop runner-only fields

## Regression guardrails

The main risk is silent fragmentation: the runner keeps learning, but the shared ecosystem cannot see those learnings.

Guardrails:

- the shared-compatible mirror must be mandatory once phase 2 starts
- the mirror must preserve runner-only details through `extensions`
- no convergence claim is valid without automated compatibility checks

## Graduation criteria

Reconsider deeper convergence only when the shared loop supports, at minimum:

- batch append without subprocess-per-record
- machine-validated `extensions`
- native git-persist semantics
- producer-grade incident capture without flattening runner-specific detail
