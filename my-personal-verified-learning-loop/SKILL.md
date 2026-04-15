---
name: my-personal-verified-learning-loop
description: "[My Personal Skill] Use when a skill, session, or AI agent needs to learn from real-world behavior without polluting its doctrine with theory. Defines the shared guardrails for runtime learnings, verified learnings, promotion rules, and tightly scoped self-modification based on actual evidence."
metadata:
  version: 1.0.0
---

# My Personal Verified Learning Loop

## Overview

This skill exists to let skills improve themselves without turning into self-rewriting chaos.

Use it when:

- a real workflow broke and had to be repaired
- a command, wrapper, provider path, or vendor flow changed
- a fix worked in real behavior and should become reusable
- an unresolved incident should be recorded without being promoted to canonical doctrine yet
- a run hit an explicit learning trigger and should checkpoint that finding instead of letting it disappear

This skill is about operational learning.

It is not:

- business memory
- project memory
- product strategy memory
- arbitrary self-editing

## Core Doctrine

1. Learning is allowed only from real behavior, not from theory alone.
2. Runtime learning and verified learning are separate layers.
3. Self-modification is allowed, but only with explicit gates.
4. A skill should not rewrite its own canonical doctrine just because one run looked promising.
5. If a finding is still unresolved, mark it as unresolved or runtime-only instead of contaminating the verified base.
6. Update the smallest correct surface: runtime note first, verified note second, `SKILL.md` only if the canonical guidance truly changed.
7. Preserve specialization. Shared learning doctrine should not erase the business-specific logic of downstream skills.
8. Learning should be triggered by explicit runtime checkpoints, not by hoping the model spontaneously self-reports something important from hidden chain-of-thought.
9. Runtime incidents should be stored in a structured machine-readable format, with Markdown as a human-friendly mirror rather than the only source of truth.

## What "Self-Modification" Means Here

Self-modification is allowed.

What is not allowed is ungated self-modification.

Allowed with evidence:

- append a runtime incident after a real failure or repair attempt
- promote a runtime incident into verified learning after repeated or strong real-world proof
- patch `SKILL.md` when the canonical workflow or guardrails materially changed
- patch a helper script when the helper itself was repaired and the repaired path was proven

Not allowed:

- writing doctrine from docs alone
- writing doctrine from "this probably works"
- broad rewrites when only one command or step changed
- mixing project-specific context into reusable skill doctrine

## Reference Map

Read only what the current task needs:

- `references/doctrine.md`
  - Shared doctrine for runtime learnings, verified learnings, and write-back decisions.
- `references/promotion-ladder.md`
  - The exact decision ladder for runtime-only vs verified vs `SKILL.md` updates.
- `references/evidence-contract.md`
  - The minimum proof required before a learning can be promoted.
- `references/triggering-rules.md`
  - The explicit trigger classes and checkpoints that should cause the learning loop to run.
- `references/runtime-incident-schema.md`
  - The structured JSON shape for runtime incidents and how it maps to the Markdown mirror.
- `references/runtime-incident.schema.json`
  - The machine-readable contract for a single runtime incident object.
- `references/skill-extension-contract.md`
  - The contract for skill-specific trigger overlays, extra JSON fields, and promotion overrides.
- `references/runtime-hooks.md`
  - The standard runtime hook names and when they should fire.
- `references/implementation-checklist.md`
  - Practical checklist before claiming a skill has learned something durable.
- `scripts/record_learning.py`
  - Shared helper to append runtime or verified learning entries to a target skill, including structured runtime JSON incidents, extension-schema validation, stable runtime de-duplication, producer-grade batch append behavior, and optional git persist semantics.

## Workflow

### 1. Classify the finding

Determine whether the finding is:

- a runtime incident
- a repaired path now proven in real behavior
- a durable canonical change to the workflow
- still unresolved

If it is unresolved, do not promote it.

### 2. Check whether a learning trigger fired

Do not rely on hidden reasoning to decide whether to learn.

Run the learning loop when at least one explicit trigger fired, for example:

- a documented path failed
- an undocumented path worked
- a repaired path differed from the current canonical guidance
- the user corrected the agent's prior approach
- a non-trivial multi-step workflow was discovered
- a provider, auth mode, wrapper, or environment behavior drifted in a way that changed the real execution path

If no trigger fired, do nothing.

### 3. Gather real evidence

Before any write-back, gather concrete evidence such as:

- command plus exit code
- produced artifact
- structured payload
- API response
- on-disk state change
- before/after behavior

If you only have documentation or reasoning, you do not yet have promotion-grade evidence.

### 4. Record the runtime incident structurally first

When a trigger fired, default to recording a structured runtime incident first.

The structured incident should capture:

- what failed or changed
- what was tried
- what worked or still remains unresolved
- the evidence
- the current confidence tier
- whether the canonical guidance appears to need an update

This turns learning into an explicit runtime action rather than a vague intuition.

### 5. Apply any skill-specific overlay

If the target skill defines an overlay, apply it here.

Typical overlay responsibilities:

- add skill-specific trigger classes
- add skill-specific JSON extension fields
- narrow or strengthen promotion conditions
- define which runtime hooks matter for that skill

The shared loop owns the base doctrine.
The target skill owns its domain-specific overlay.

### 6. Pick the smallest correct write target

Default order:

1. `runtime-learning.md`
2. `verified-learning.md`
3. `SKILL.md`
4. helper scripts or references, but only if they were part of the repaired path

Do not jump straight to `SKILL.md` when a runtime note is enough.

### 7. Apply bounded self-modification

When a write-back is justified:

- change only the files materially affected
- preserve the specialized business logic already present in the target skill
- prefer additive updates and explicit deprecation notes over broad rewrites
- make the evidence trail clear enough that a later session can audit why the skill changed

### 8. Keep unresolved gaps explicit

If the path still is not proven:

- record it as runtime-only if useful
- mark it as unresolved
- leave the verified layer untouched

This is still learning.
It is just not verified learning yet.

## Shared Output Standard

A correct learning loop should leave behind:

- the exact incident or repaired path
- the evidence that justified the write-back
- the confidence layer used (`runtime` or `verified`)
- a structured runtime incident record when the loop was triggered
- a machine-readable runtime incident contract that later adapters or validators can target
- the smallest updated target surface
- no contamination from project-specific or speculative content
