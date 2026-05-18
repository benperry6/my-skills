# Codex-era solution porting guard

Use this reference when ingesting older Codex, Claude Code, or agent-session exports into current Hermes.

## Core rule

Do not copy old implemented solutions just because the source session converged on them. Extract:

1. the underlying failure mode;
2. the constraints the old solution was trying to satisfy;
3. the evidence available in the source;
4. the current Hermes-native mechanisms that could satisfy the same need;
5. whether the old artifact is still useful as-is, needs adaptation, should be retired, or should be quarantined out of active skill discovery.

## Why this matters

Older Codex-era workflows often used personal skills as the only durable mechanism available to that agent. Hermes has different affordances: native toolsets, delegation, cron jobs, profiles, Telegram gateway workflows, vault/QMD retrieval, memory, and skill packaging. A skill that was optimal in Codex may be unnecessary ceremony or the wrong abstraction in Hermes.

## When old skills risk biasing Hermes

If a Codex-era skill is itself steering implementation toward an old solution before Hermes-native design has happened, quarantine it:

1. move it out of the active skill path or into a non-discoverable archive directory;
2. rename `SKILL.md` to `SKILL.archived.md` so the loader cannot treat it as an active skill;
3. keep references and supporting files intact as cold source material;
4. write a vault decision note explaining why it is reference-only;
5. update backlog wording so future work starts from Hermes-native mechanisms, not from loading the archived skill.

Example active archive pattern:

```text
/home/hermes/.agents/skills/legacy-codex-skill-archive/active/<old-skill>/SKILL.archived.md
```

## Classification language

Prefer these labels when writing source records and backlog items:

- `concept valid; vehicle unproven`
- `candidate adapter`
- `Hermes-native alternative needed`
- `test before promoting`
- `load-bearing in real Hermes run`
- `ceremonial / retire or narrow`

Avoid these unless verified by current Hermes behavior:

- `use this skill`
- `require this evaluator`
- `current separation is correct`
- `already operationalized`
- `default policy`

## Backlog wording pattern

Bad:

- `Use my-personal-harness-engineering at the start of the next ProStrike task.`
- `Require my-personal-qa-evaluator before acceptance.`

Good:

- `On the next substantial Hermes/ProStrike task, test whether the Codex-era harness doctrine or a simpler Hermes-native checkpoint is useful.`
- `For the next non-trivial implementation, test whether a separate QA/evaluator gate improves acceptance quality and whether the old evaluator skill is the right vehicle.`

## Verification standard

Before promoting an old Codex-era artifact to Hermes doctrine, gather real Hermes evidence:

- command/test/browser/API/log evidence where applicable;
- what Hermes-native alternative was considered;
- whether the old skill changed the outcome;
- whether the added structure was load-bearing or ceremony;
- whether thresholds should be patched, replaced, or retired.

## Final report standard

When Ben challenges an ingestion, answer directly:

- whether the ingestion over-ported old solutions;
- what remains valid at the level of findings/constraints;
- which durable artifacts were corrected;
- whether the old skills are now treated as candidates rather than defaults.
