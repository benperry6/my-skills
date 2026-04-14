# Promotion Ladder

Use this ladder every time a skill is about to "learn" from a run.

## Step 1 — Runtime-only

Use `runtime-learning.md` when:

- a path failed
- a repair was attempted
- a fix seems promising but is not yet clearly durable
- the incident is worth remembering across sessions

This is the default first landing zone.

## Step 2 — Verified learning

Use `verified-learning.md` when:

- the repaired or discovered path worked in real behavior
- the evidence is concrete
- the learning is reusable across future runs
- the learning is concise enough to become durable guidance

Do not promote every runtime note.
Promote only the stable subset.

## Step 3 — Canonical skill update

Update `SKILL.md` only when:

- the canonical guidance actually changed
- the default decision path changed
- an old instruction became misleading or obsolete
- the skill would otherwise keep steering future runs incorrectly

If `verified-learning.md` is enough, do not edit `SKILL.md`.

## Step 4 — Helper or reference patch

Patch scripts or detailed references only when:

- the helper or reference was part of the broken path
- the repaired path is now proven
- the patch is the smallest correct way to prevent recurrence

## Refusal rule

Do not promote anything when:

- evidence is weak
- the path is still unresolved
- the learning is actually project-specific
- the update would be broad and speculative
