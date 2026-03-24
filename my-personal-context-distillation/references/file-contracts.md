# File Contracts

These are not rigid templates. They are stable navigation anchors.

Use them to keep the files legible for humans and LLMs, while preserving the freedom to add business-specific sections.

## `.agents/business-model.md`

Preferred anchors:

- `# Business Model`
- `## Snapshot`
- `## What We Sell`
- `## Who Pays`
- `## Pricing & Monetization`
- `## Acquisition Model`
- `## Conversion Model`
- `## Retention & Expansion`
- `## Business Rules & Constraints`
- `## Special Cases`
- `## Open Questions`

`## Snapshot` contract:

- keep it compact and fast to scan
- make it answer, in plain language:
  - what the business is
  - what it sells
  - who pays or buys
  - what kind of business model it is
  - how monetization works
  - pricing status or pricing shape if known
  - the primary conversion action
- use it as a quick-read layer, not as a duplicate of the detailed sections below
- include technical or credibility signals only when they materially affect positioning, trust, constraints, or messaging

Allowed extras:

- unit economics
- channel mix
- marketplace logic
- affiliate monetization logic
- operational workflows

## `.agents/storytelling.md`

Preferred anchors:

- `# Storytelling`
- `## Narrative Core`
- `## Origin Story`
- `## Founder Truth`
- `## Mission, Vision, Enemy`
- `## Beliefs`
- `## Transformation Promise`
- `## Brand Voice`
- `## Narrative Assets`
- `## Red Lines`
- `## Verbatim Founder Lines`
- `## Special Cases`
- `## Open Questions`

Allowed extras:

- myth vs reality
- why now
- emotional stakes
- strategic worldview

## `.agents/know-your-customer.md`

Preferred anchors:

- `# Know Your Customer`
- `## Snapshot`
- `## Segment Card: ...`
- `## Voice of Customer`
- `## Buying Psychology`
- `## Anti-Personas`
- `## Special Cases`
- `## Open Questions`

Research contract:

- treat founder assumptions as search guidance, not saved truth
- use `docs/context-sources/voc-bank.csv` as the proof layer behind core KYC claims
- prefer direct public audience language over polished synthesis
- do not let search snippets or official docs fully stand in for direct user voice on core KYC claims
- do not write composite persona traits, pricing sensitivity, or confidence claims unless the evidence clearly supports them
- if `decision criteria`, `trust signals`, `search behavior`, or `anti-personas` are only partially supported, phrase them as provisional or move the unsupported specifics to `Open Questions`
- if the file cites counts, validated themes, or category coverage, those claims must reconcile with the current bank rows
- leave unsupported claims in `Open Questions`

Research-backed subfields worth covering inside `Segment Card`:

- who they are
- current situation
- trigger event
- main job to be done
- current substitute or alternatives
- pains
- desired outcomes
- fears
- objections
- decision criteria
- trust signals
- where they search or learn

Allowed extras:

- search behavior
- content preferences
- channel trust patterns
- segmentation by traffic source

## `docs/context-sources/voc-bank.csv`

Purpose:

- persistent evidence bank for customer research
- quote-level traceability behind `know-your-customer.md`
- reusable source layer so research does not need to be rerun from zero

Contract:

- store raw or tightly excerpted audience language
- store source metadata with each quote
- keep analytical tags lightweight and explicit
- do not confuse tags with facts
- do not replace the bank with a prose summary

## `.agents/performance-memory.md`

Preferred anchors:

- `# Performance Memory`
- `## Rules`
- `## Messaging Winners`
- `## Messaging Losers`
- `## Audience Learnings`
- `## Offer Learnings`
- `## SEO / AI Search Learnings`
- `## Paid Learnings`
- `## Email / Social Learnings`
- `## Objections Actually Observed`
- `## Hypotheses To Test`

Required rule:

- only record real observations, or clearly marked hypotheses

Allowed extras:

- sales call learnings
- landing page learnings
- regional differences
- seasonality patterns

## General Writing Contract

- Prefer short paragraphs over walls of text.
- Use bullets for rules, lists, mechanics, or distinctions.
- Preserve verbatim quotes when they matter.
- Add custom sections when the business requires them.
- Never force empty sections to stay if they genuinely do not apply.
- Use `Open Questions` instead of inventing missing context.
