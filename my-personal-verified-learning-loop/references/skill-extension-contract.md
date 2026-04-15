# Skill Extension Contract

Use this contract when a downstream skill wants to reuse the shared verified-learning loop without losing its specialization.

## Rule

The shared skill defines:

- the learning layers
- the trigger model
- the runtime hook model
- the promotion ladder
- the base runtime incident schema

The downstream skill may extend:

- trigger classes
- required evidence
- promotion thresholds
- runtime incident JSON fields
- hook usage

## Overlay responsibilities

A skill-specific overlay may define:

### 1. Additional triggers

Examples:

- "new vendor not documented"
- "documented vendor flow drifted"
- "browser fallback identity mismatch was discovered"

### 2. Additional runtime incident fields

Use the `extensions` object for skill-specific fields.

Examples:

- `vendor`
- `operation`
- `phase`
- `auth_surface`
- `approved_account`
- `verification_surface`

### 3. Promotion overrides

A skill may say:

- "do not promote this class of incident to verified until phase 4 proof exists"
- "this kind of bootstrap learning becomes verified after phase 2 proof because bootstrap itself is the learned surface"

### 4. Hook map

A skill may say which hooks are active and what they should capture.

## What an overlay must not do

An overlay must not:

- erase the runtime vs verified split
- permit theory-only promotion
- remove the smallest-correct-write-target rule
- mix project-specific memory into reusable doctrine

## Recommended file shape

The simplest form is a single reference file inside the downstream skill, for example:

- `references/learning-overlay.md`

That file should define:

- skill-specific triggers
- runtime incident `extensions`
- promotion overrides
- hook usage notes
