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
- `references/implementation-checklist.md`
  - Practical checklist before claiming a skill has learned something durable.
- `scripts/record_learning.py`
  - Shared helper to append runtime or verified learning entries to a target skill.

## Workflow

### 1. Classify the finding

Determine whether the finding is:

- a runtime incident
- a repaired path now proven in real behavior
- a durable canonical change to the workflow
- still unresolved

If it is unresolved, do not promote it.

### 2. Gather real evidence

Before any write-back, gather concrete evidence such as:

- command plus exit code
- produced artifact
- structured payload
- API response
- on-disk state change
- before/after behavior

If you only have documentation or reasoning, you do not yet have promotion-grade evidence.

### 3. Pick the smallest correct write target

Default order:

1. `runtime-learning.md`
2. `verified-learning.md`
3. `SKILL.md`
4. helper scripts or references, but only if they were part of the repaired path

Do not jump straight to `SKILL.md` when a runtime note is enough.

### 4. Apply bounded self-modification

When a write-back is justified:

- change only the files materially affected
- preserve the specialized business logic already present in the target skill
- prefer additive updates and explicit deprecation notes over broad rewrites
- make the evidence trail clear enough that a later session can audit why the skill changed

### 5. Keep unresolved gaps explicit

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
- the smallest updated target surface
- no contamination from project-specific or speculative content
