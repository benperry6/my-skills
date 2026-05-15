---
name: my-personal-context-distillation
description: "[My Personal Skill] Distill founder dumps, voice memo transcripts, speech-to-text notes, raw context docs, repo docs, public market research, and performance learnings into canonical business context files. Use when the user wants to bootstrap or update `.agents/business-model.md`, `.agents/storytelling.md`, `.agents/know-your-customer.md`, `.agents/performance-memory.md`, or the VoC evidence bank. Not for `AGENTS.md`, `CLAUDE.md`, docs-first repo bootstrap, `docs/PROJECT_BRIEF.md`, `docs/ARCHITECTURE.md`, `docs/BACKLOG.md`, `docs/PROJECT_STATE.md`, ADRs, or the stop line before code."
---

# Context Distillation

## Purpose

This skill maintains the canonical business-context layer for a repo.

It turns messy source material into durable source-of-truth files:

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

When customer research is in scope, it also maintains:

- `docs/context-sources/voc-bank.csv`

This skill does not own the technical implementation control plane. For `AGENTS.md`, `CLAUDE.md`, docs-first bootstrap, project architecture, backlog, state docs, ADRs, or repo restart before coding, reroute to `my-personal-persistent-context-first`.

## Reference Map

Use the detailed references when the task needs more than the entrypoint rules:

- [references/full-operating-manual.md](references/full-operating-manual.md) - complete doctrine preserved from the long-form skill
- [references/file-contracts.md](references/file-contracts.md) - canonical file responsibilities and boundaries
- [references/voc-bank-schema.md](references/voc-bank-schema.md) - durable voice-of-customer evidence schema
- [references/kyc-research.md](references/kyc-research.md) - research rules for `know-your-customer.md`
- [references/post-distillation-handoff.md](references/post-distillation-handoff.md) - handoff to `product-marketing-context`

## Hard Reroute Gate

Before doing anything else, inspect the request for technical control-plane signals.

Reroute to `my-personal-persistent-context-first` when the request is mainly about:

- `AGENTS.md` or `CLAUDE.md`
- docs-first bootstrap before coding
- `docs/PROJECT_BRIEF.md`, `docs/ARCHITECTURE.md`, `docs/BACKLOG.md`, or `docs/PROJECT_STATE.md`
- ADRs or implementation-agent memory
- converting transcript/export material into durable implementation guidance for coding agents

Reroute behavior:

1. State that the request targets the technical implementation control plane, not the canonical business-context layer.
2. Name `my-personal-persistent-context-first` explicitly.
3. Do not create, edit, or propose the `.agents/` business-context files as the first move.

## Handoff Contract

This skill edits the canonical source files. It does not impersonate downstream skills.

If the user asks to run `product-marketing-context` after distillation:

1. finish the canonical files and evidence bank first
2. read `product-marketing-context/SKILL.md`
3. explicitly state that the downstream skill is now being used
4. let that skill own `.agents/product-marketing-context.md`

If deeper public research is needed for `know-your-customer.md`, `customer-research` may be used as a helper. Its output belongs in `.agents/customer-research/` as scratch material until normalized into `docs/context-sources/voc-bank.csv`.

## When To Use

Use this skill when the user wants to:

- bootstrap canonical business context files for a new repo
- update context files from a founder dump, speech-to-text transcript, or voice memo transcript
- merge new business, customer, narrative, sales, ads, SEO, or performance learning into canonical context
- build or refresh a persistent voice-of-customer bank
- clean up messy context notes into durable files
- prepare a repo for downstream marketing, CRO, or sales skills
- turn early audience assumptions into market-backed customer context

Do not use this skill to write final marketing assets such as ads, pages, articles, or emails.

## Modes

Infer the mode from the request if the user does not specify one.

`bootstrap`: create the canonical files when they do not exist or are too weak to trust. Create `docs/context-sources/voc-bank.csv` when needed, preserve uncertainty in `Open Questions`, and propose `product-marketing-context` after canonical work is complete.

`update`: merge new information into existing canonical files. Preserve existing validated truths, add new evidence precisely, and do not rewrite sections that are not affected.

`performance-update`: add observed outcomes, campaign results, conversion data, or experiment learnings to `.agents/performance-memory.md` and update other context files only when the learning changes business truth.

`audit`: inspect current context files for missing, stale, contradictory, or unsupported claims. Report gaps before editing when source material is insufficient.

`maturity-audit`: evaluate whether the context layer is strong enough to support downstream execution skills without hallucinating product, customer, or offer facts.

## Source Priority

Use sources in this order:

1. explicit user-provided current source material
2. durable project files already in the repo
3. observed performance data or customer evidence
4. public research, only when the task requires it and source quality is adequate
5. hypotheses, clearly marked as such

Never upgrade an assumption into a fact. Keep direct quotes and raw customer language in the evidence layer when wording matters.

## Sufficiency Gate

Before producing or updating a canonical section, verify that the needed evidence exists.

If a section would be generic, ask for the missing input first. Critical missing inputs commonly include:

- what the product is and who it serves
- business model or monetization
- target customer and buying trigger
- proof, examples, or performance data
- founder/customer language to preserve
- explicit decisions about positioning, offer, pricing, or constraints

## Working Rules

- Preserve truth over neatness.
- Standardize anchors, not thinking.
- Separate facts, interpretation, hypotheses, and open questions.
- Keep the evidence layer separate from canonical synthesis.
- Treat `know-your-customer.md` as research-led, not founder-led.
- Touch the minimum necessary files.
- Handle contradictions explicitly.
- Add custom sections when the business needs them.
- Do not treat `.agents/product-marketing-context.md` as source of truth.

## Workflow

1. Inspect current state: existing `.agents/` files, `docs/context-sources/`, project rules, and source material.
2. Classify the requested mode and identify affected files.
3. Run the sufficiency gate before drafting weak sections.
4. Normalize durable customer evidence into `docs/context-sources/voc-bank.csv` before synthesizing KYC claims.
5. Update canonical files carefully, preserving uncertainty and provenance.
6. Validate the context layer for contradictions, unsupported claims, and stale assumptions.
7. Report exactly what changed and what remains unresolved.
8. Propose the `product-marketing-context` handoff when canonical work is complete.

## Output Quality Bar

Canonical context should be specific enough that a downstream skill can act without inventing product facts.

A good output names:

- verified truths
- hypotheses
- open questions
- source files touched
- evidence added or changed
- downstream handoff recommendation

## Validation

After edits, verify the relevant files exist and are internally consistent.

Use the local scripts when helpful:

```bash
python3 SKILL_DIR/scripts/init_context_tree.py <repo>
python3 SKILL_DIR/scripts/validate_context_tree.py <repo>
```

Validation must check the right thing: a file existing is not enough if the content is generic, unsupported, or contradicted by stronger evidence.

## Final Rule

Do not let the repo's business context become a polished pile of guesses. If the evidence is missing, preserve the gap and ask for the source material.
