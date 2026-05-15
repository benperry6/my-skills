# Repo Contract for `source-ingest`

## Required reading before use

- `docs/PROJECT_BRIEF.md`
- `docs/ARCHITECTURE.md`
- `docs/PROJECT_STATE.md`
- `PRODUCT_MEMORY.md`

For short social sources, `SKILL.md` defines a file-backed fast path: the full control-plane read is still required at the start of a work session, after control-plane or skill edits, or whenever state is uncertain. For later short social sources in the same active work session, a file-backed freshness check plus targeted re-read of changed/current files may replace re-opening every full artifact. This exception must never rely on chat memory alone.

## Directory responsibilities

- `sources/inbox/`: optional landing zone for raw source files that have not been processed yet.
- `sources/processed/`: one markdown file per processed source.
- `learnings/atomic/`: one markdown file per canonical learning.
- `learnings/hypotheses/`: one markdown file per pressure-testable non-canonical hypothesis or technique candidate.
- `learnings/syntheses/`: one markdown file per synthesis theme that gets updated over time.
- `drafts/skill-specs/`: draft specs for future execution skills when evidence becomes stable.

## File naming

- Processed source: `SRC-####-short-slug.md`
- Atomic learning: `LRN-####-short-slug.md`
- Hypothesis: `HYP-####-short-slug.md`
- Synthesis: `theme-short-name.md`
- Skill spec: `skill-short-name.md`

Use the next available zero-padded numeric ID by scanning existing files.

## Processed source template

```md
---
id: SRC-0001
title: "Source title"
source_type: blog-article
url: https://example.com/article
author: Example Author
captured_at: 2026-04-17
processed_at: 2026-04-17
language: fr
themes:
  - geo-answerability
status: processed
---

## Source Summary

Two to six bullets on what the source actually says.

## Retained Learnings

- `LRN-0001` new
- `LRN-0002` enriched

## Retained Hypotheses

- `HYP-0001` new

## Retained Technique Candidates

- `HYP-0002` technique candidate

## Rejected Candidates

- Candidate text — rejected because too vague

## Evidence Notes

- Main evidence profile(s) used for retained claims.
- Explicitly note when a retained mechanism is source-stated vs inferred.

## Raw Content

Normalized raw content or a faithful extract.
```

## Hypothesis or technique-candidate template

```md
---
id: HYP-0001
title: "Short hypothesis title"
tentative_statement: "Single sentence framed as a possibility, not doctrine."
mechanism_type: source_stated
pressure_test_action: "What to observe, test, or corroborate next."
review_trigger: "What future source, test, or signal should trigger review."
retirement_trigger: "What would cause this record to be merged, narrowed, archived, or dropped."
scope: "Where it might apply."
theme: geo-answerability
tags:
  - llm
  - retrieval
status: active
confidence: low
source_ids:
  - SRC-0001
promotion_criteria:
  - "What evidence would justify promotion to canonical learning."
rejection_criteria:
  - "What evidence or failure mode would retire the hypothesis."
decision_status: hypothesis
---

## Why It Might Matter

One concise paragraph.

## Mechanism

- Why this might work.
- If inferred rather than directly stated by the source, say so explicitly.

## Current Evidence

- Source-backed proof point or practitioner observation.

## Boundaries

- Caveats and contexts where this should not be applied.
```

For technique candidates, use the same non-canonical template but set `decision_status: technique_candidate` and explain what detail or evidence is needed before promotion.

## Atomic learning template

```md
---
id: LRN-0001
title: "Short learning title"
canonical_statement: "Single sentence that states the learning clearly."
action: "What to do in practice."
scope: "Where it applies."
mechanism_type: mixed
theme: geo-answerability
tags:
  - llm
  - answer-structure
confidence: medium
source_ids:
  - SRC-0001
operator_validation:
  date: 2026-04-20
  evidence_type: user-reported first-party tests
  note: "Only include when the operator explicitly validates the scoped technique."
conflicts_with: []
scores:
  actionability: 3
  specificity: 3
  novelty: 2
  transferability: 2
  solidity: 2
decision_status: active
---

## Why It Matters

One concise paragraph.

## Mechanism

- Operational explanation for why this learning may hold.
- Distinguish source-stated vs inferred reasoning when relevant.

## Evidence

- Source-backed proof point

## Exceptions

- Important boundary or caveat

## Disconfirmation Risks

- What future evidence, failure mode, or contextual shift would weaken, narrow, or demote this learning.

## Examples

- Optional example if it adds operational clarity
```

Use `decision_status: operator_verified` when the operator reports first-party tests validating a scoped technique.

## Synthesis update rule

Only update the synthesis files for impacted themes. Do not touch unrelated syntheses.

## Skill-spec update rule

Only update `drafts/skill-specs/` when a source materially reinforces a stable operational pattern. Do not create final execution skills from one isolated source.
