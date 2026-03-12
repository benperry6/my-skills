---
name: "my-personal-context-distillation"
description: "[My Personal Skill] Distill founder dumps, voice memo transcripts, speech-to-text notes, raw context docs, repo docs, public market research, and performance learnings into canonical business context files. Also build and maintain a persistent voice-of-customer evidence bank for customer research. Use when the user wants to bootstrap or update `.agents/business-model.md`, `.agents/storytelling.md`, `.agents/know-your-customer.md`, or `.agents/performance-memory.md`, especially before generating `.agents/product-marketing-context.md` for downstream marketing skills. Also use when the user mentions 'context distillation,' 'business context bootstrap,' or 'voice-of-customer research' for a repo."
---

# Context Distillation

## Purpose

This skill is the editor of the canonical business context for a repo.

Its job is to turn messy source material into four durable source-of-truth files:

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

And, when customer research is in scope, one durable evidence-layer file:

- `docs/context-sources/voc-bank.csv`

After that work is complete, it should always propose running the separate `product-marketing-context` skill, whose job is to compile those source files into:

- `.agents/product-marketing-context.md`

Do not blur these two jobs.

- `my-personal-context-distillation` = edit and maintain the true source of truth
- `my-personal-context-distillation` = build and maintain the evidence bank that supports customer truth
- `product-marketing-context` = compile a derivative context file for downstream skills

## Why This Skill Exists

General-purpose LLMs and execution agents can produce a lot, but they drift when they do not have strong business context.

The goal of this skill is to preserve what human teams used to carry implicitly:

- business logic
- founder intent
- customer understanding
- accumulated performance learnings

Important distinction:

- `business-model.md` and `storytelling.md` are primarily grounded in founder/business input
- `know-your-customer.md` must be grounded in real market voice, not guessed audience beliefs
- `docs/context-sources/voc-bank.csv` stores the supporting raw/semi-raw audience evidence behind that customer understanding
- `performance-memory.md` must be grounded in observed behavior and outcomes

This skill exists because better output depends not only on what is requested, but also on why it is requested. The "why" helps interpret the real objective, priorities, tradeoffs, constraints, and expected quality bar. Use it whenever it changes decisions or output quality. Ignore it when it is decorative, redundant, or operationally irrelevant.

## Default File Layout

Canonical files live at the root of `.agents/`:

```text
.agents/
  business-model.md
  storytelling.md
  know-your-customer.md
  performance-memory.md
  product-marketing-context.md
```

Human-maintained source materials live under `docs/`:

```text
docs/
  context-sources/
    2026-03-11-founder-dump.md
    2026-03-12-ads-review-notes.md
    voc-bank.csv
```

The canonical files are agent-maintained.
The `docs/context-sources/` materials are human-originated or transcript-originated.
`voc-bank.csv` is the persistent evidence layer for customer research. It is agent-maintained, but should remain human-readable and spreadsheet-friendly.
It must follow the schema defined in [references/voc-bank-schema.md](references/voc-bank-schema.md).

## When To Use

Use this skill when the user wants to:

- bootstrap context files for a new repo
- update context files from a founder dump or speech-to-text transcript
- process a voice memo transcript into durable business context
- merge new business, customer, or narrative information into the canonical files
- build or refresh a persistent voice-of-customer bank
- ingest learnings from ads, SEO, email, sales calls, or experiments
- clean up messy context notes into durable files
- prepare a repo for downstream marketing or CRO skills
- turn early audience assumptions into real market-backed customer context
- do web-backed voice-of-customer research for `know-your-customer.md`

Do not use this skill to write final marketing assets such as ads, pages, articles, or emails.

Strong trigger phrases include:

- founder dump
- founder memo
- voice memo transcript
- speech-to-text transcript
- business context bootstrap
- customer context update
- narrative distillation
- voice-of-customer research
- market research for customer context
- ingest performance learnings
- update the canonical context files
- create the source-of-truth context for this repo

## Modes

Infer the mode from the request if the user does not specify one.

### `bootstrap`

Use when the canonical files do not exist yet, or are too weak to be trusted.

Output:
- create the four canonical files
- create `docs/context-sources/voc-bank.csv` if missing
- preserve uncertainty in `Open Questions`
- propose running `product-marketing-context`

Important clarification:

- the initial absence of `docs/context-sources/voc-bank.csv`
- the initial absence of pre-collected public VoC in the repo

are not blockers for launching `bootstrap`.

In `bootstrap`, this skill is expected to go build that customer evidence layer during the run when KYC is in scope.

### `update`

Use when the canonical files already exist and the user provides new source material.

Output:
- update the canonical files without flattening nuance
- update `docs/context-sources/voc-bank.csv` when customer research is in scope
- preserve prior useful information
- surface contradictions explicitly
- propose running `product-marketing-context`
- do not mark KYC work complete unless it clears the completion gate in [references/kyc-research.md](references/kyc-research.md)

### `performance-update`

Use when the new material is primarily behavioral or performance evidence.

Output:
- update `.agents/performance-memory.md`
- touch other canonical files only if a learning clearly changes business, narrative, or customer understanding
- propose running `product-marketing-context` if the learning materially changes positioning or messaging

### `audit`

Use when the user wants to know whether the context system is strong enough.

Output:
- no major rewrites by default
- report missing sections, contradictions, weak areas, and stale learnings
- propose the next best source material to ingest
- for KYC, evaluate against the checklist in [references/kyc-research.md](references/kyc-research.md)

## Source Priority

When multiple sources exist, use this order:

1. Existing canonical files in `.agents/`
2. New user-provided transcript or raw notes
3. Files in `docs/context-sources/`
4. Other relevant docs under `docs/`
5. Marketing pages, README, pricing pages, and repo copy as fallback only
6. `.agents/product-marketing-context.md` only as migration fallback when canonical files are missing and the user did not provide better sources

Never let a fallback source silently override a stronger source.

For `know-your-customer.md`, use a stricter rule:

1. Existing canonical `know-your-customer.md`
2. Existing `docs/context-sources/voc-bank.csv`
3. Real public voice-of-customer evidence found on the web
4. New user-provided customer research or interview material
5. User-supplied audience assumptions only as search guidance, never as saved truth

Do not save audience assumptions as facts just because the founder believes them.

## Sufficiency Threshold

Do not pretend the inputs are strong when they are weak.

Minimum acceptable source quality for `bootstrap`:

- at least one substantial founder-originated source, or
- multiple smaller sources that together cover business, customer, and offer logic

If founder/business input is too thin to support a credible `business-model.md` or `storytelling.md`, do not push forward as if the context is sufficient. Write only what is actually supported, move the missing pieces into `Open Questions`, and say explicitly that more founder context is required before high-quality downstream work should continue.

Minimum acceptable source quality for a meaningful `know-your-customer.md` update:

- real public user voice from the web, or
- real interview/survey/test material supplied by the user, or
- both

If you do not have enough real audience language, do not fill the gaps by inference. Save only what is supported and push the rest into `Open Questions`.

Do not confuse these two states:

- enough founder/business context to start a repo bootstrap
- enough audience evidence to declare KYC complete

The first can be true even when the second is not.

If the source material is too thin:

- initialize the files if needed
- write only what is genuinely supported
- put the rest in `Open Questions`
- say clearly that the repo is not ready for high-quality downstream context compilation yet

For customer research specifically, prefer this sequence:

1. build or extend `voc-bank.csv`
2. synthesize the bank into `know-your-customer.md`

Do not synthesize straight from a loose pile of web findings when you can persist the evidence first.
Do not declare the KYC "done" until it clears the completion gate in [references/kyc-research.md](references/kyc-research.md), unless a real blocker is reached and stated explicitly.

## Working Rules

### Preserve truth, do not optimize for neatness

Do not compress away important nuance just to make the files cleaner.

### Standardize anchors, not thinking

Use stable top-level sections so humans and LLMs can navigate the files reliably.
Do not force rigid form-style answers. Free paragraphs, bullets, verbatim quotes, and custom sections are all allowed.

### Separate fact, interpretation, and hypothesis

- facts belong as stated facts
- interpretations should be framed as interpretations
- uncertain points belong in `Open Questions`
- unvalidated patterns belong in `performance-memory.md` as hypotheses until supported

### Preserve verbatim language when it matters

Customer phrases, founder phrases, objection wording, and converting messages should be captured as-is whenever possible.

### Keep the evidence layer separate from the canonical layer

`docs/context-sources/voc-bank.csv` is not the same thing as `.agents/know-your-customer.md`.

- `voc-bank.csv` = evidence bank, quote store, research cache
- `know-your-customer.md` = synthesized customer truth based on that evidence

Do not turn `know-your-customer.md` into a dump of raw quotes.
Do not skip the evidence bank when customer research is extensive enough to justify persistence.

### `know-your-customer.md` is research-led, not founder-led

Treat founder input about the customer as a starting hypothesis, not as truth.

Use it to guide search direction:

- who to look for
- where to look
- what products, competitors, or use cases are relevant

Do not save it as customer truth unless it is supported by real audience evidence.

### `voc-bank.csv` is the persistence layer for customer research

When KYC research is in scope, store the collected audience evidence in `docs/context-sources/voc-bank.csv` so the repo does not have to redo the same market research later.

The purpose of the bank is to:

- avoid rerunning the same research repeatedly
- preserve nuance that might be lost in direct synthesis
- give future agents and humans a traceable evidence base
- let `know-your-customer.md` be re-synthesized later without starting from zero
- preserve not just quotes, but also how strong or weak each proof item is

Treat raw quote fields as evidence.
Treat tags and labels as analytical metadata, not ground truth.
Treat evidence quality fields as completion-critical, not optional decoration.

Populate the evidence quality columns consistently:

- `evidence_kind`
- `capture_method`

Use the controlled values in [references/voc-bank-schema.md](references/voc-bank-schema.md).
Do not leave those fields blank on newly added rows.

### KYC work is completion-gated

When `know-your-customer.md` is in scope, the job is not complete just because one research/synthesis cycle ran.

Keep iterating until either:

- the KYC is strong enough for downstream work, based on the completion gate in [references/kyc-research.md](references/kyc-research.md), or
- a real blocker is reached and reported explicitly

Do not stop on a weak result if further credible research passes are still available.
Do not mark KYC complete if the evidence bank and the synthesized KYC disagree.

### Use the "why" when it changes the outcome

Use the user's explanation of why this context matters when it helps interpret:

- the real objective
- the success criteria
- the quality bar
- the tradeoffs
- the constraints

Ignore it when it is only emotional decoration, repetition, or commentary with no operational consequence.

### Keep the four files distinct

- `business-model.md` = commercial and operational truth
- `storytelling.md` = origin, mission, worldview, voice, and emotional framing
- `know-your-customer.md` = segments, current situation, JTBD, alternatives, pains, desires, objections, search behavior, trust signals, and voice of customer
- `performance-memory.md` = real-world learnings from observed behavior and outcomes
- `voc-bank.csv` = quote-level audience evidence with source metadata, evidence quality metadata, and lightweight analytical tags

Do not dump everything into every file.

### Do not treat `product-marketing-context.md` as source of truth

It is a downstream compiled artifact for other skills. It can help recover context only when no better source exists, but it should not become the canonical memory of the business.

### Touch the minimum necessary files

Do not update all four files by reflex.

- If the new source only changes narrative framing, prefer `storytelling.md`
- If it only adds customer detail, prefer `know-your-customer.md`
- If it only adds behavioral learnings, prefer `performance-memory.md`
- Update multiple files only when the source clearly changes multiple domains

### Handle contradictions explicitly

When a new source conflicts with prior context:

- do not silently overwrite
- do not blend conflicting claims into vague language
- preserve the stronger prior claim unless the new source is clearly more authoritative
- add an explicit note in the relevant file when the contradiction matters
- mention the contradiction in the change report

For customer context specifically:

- if founder belief conflicts with real audience language, preserve the audience language
- if public audience evidence is mixed, preserve the conflict instead of forcing one conclusion
- if a synthesized KYC claim cannot be reconciled with the actual bank rows, downgrade or remove the claim

### Add custom sections when the business needs them

The stable anchors are navigation aids, not a prison.

Add business-specific sections when needed, for example:

- affiliate economics
- editorial review policy
- channel-specific customer segments
- founder mythology
- market timing
- compliance constraints

Do not force a business to look generic just to preserve symmetry.

## Workflow

### 1. Initialize if needed

If the repo does not yet have the expected tree, run:

```bash
python3 ~/.agents/skills/my-personal-context-distillation/scripts/init_context_tree.py
```

This creates:

- `.agents/`
- `docs/context-sources/`
- the four canonical files, if missing
- `docs/context-sources/voc-bank.csv`, if missing

If `voc-bank.csv` already exists but does not match the current schema in [references/voc-bank-schema.md](references/voc-bank-schema.md), migrate it before adding new rows.

### 2. Inspect current state

Read:

- `.agents/business-model.md`
- `.agents/storytelling.md`
- `.agents/know-your-customer.md`
- `.agents/performance-memory.md`

If source files exist, inspect:

- `docs/context-sources/*.md`
- `docs/context-sources/voc-bank.csv`
- any user-provided transcript in the request

Only inspect wider repo docs when the direct sources are insufficient.

Before reading the wider repo, ask:

- what is still missing?
- which missing field would materially improve the canonical files?
- is repo-wide scraping actually necessary, or would it only create noise?

If `voc-bank.csv` exists, verify early that its header matches the current schema before using it as proof.

### 2b. If `know-your-customer.md` is in scope, do real market research

For `know-your-customer.md`, do not stop at the founder transcript.

Use the founder's description of the audience only as a directional seed, then do real voice-of-customer research on the web. Search as much as needed until the major customer sections are supported by actual public evidence.

Persist what you find in `docs/context-sources/voc-bank.csv` before or while synthesizing.

Acceptable public sources include:

- forums
- Reddit threads
- product reviews
- app reviews
- Amazon reviews
- Google reviews
- YouTube comments
- blog comments
- niche communities
- competitor FAQs when they expose recurring objections

Rules:

- never guess the audience's pains, desires, or wording
- never save invented customer motivations
- do not stop after a few lazy searches and backfill the rest mentally
- quote useful customer language as directly as possible
- append or update the evidence bank instead of discarding useful findings after synthesis
- deduplicate obvious repeats when they add no new signal
- classify each row using the evidence-quality fields from [references/voc-bank-schema.md](references/voc-bank-schema.md)
- keep source notes in the update report

Evidence quality rules:

- prefer `direct_user_voice` captured via `direct_fetch`
- `search_snippet` rows are provisional and should trigger deeper fetching when plausible
- `official_product_statement` and `third_party_summary` can support context, but should not carry core customer-truth claims alone
- `founder_seed` is directional only and should not be treated as proof

Required loop:

1. research
2. persist evidence in `voc-bank.csv`
3. synthesize or update `know-your-customer.md`
4. check that the synthesis is consistent with the actual evidence bank
5. evaluate against the KYC checklist and completion gate
6. if too weak and more plausible evidence sources remain, repeat

Do not stop after synthesis if the consistency check or the completion gate still fails.

For the full method and CSV schema, see:

- [references/kyc-research.md](references/kyc-research.md)
- [references/voc-bank-schema.md](references/voc-bank-schema.md)

### 3. Classify the new information

Before editing, decide where each important statement belongs:

- pricing, offer logic, funnel mechanics, monetization -> `business-model.md`
- mission, origin, beliefs, tone, narrative framing -> `storytelling.md`
- persona details, current situation, JTBD, alternatives, pains, triggers, objections, buying criteria, trust signals, exact phrasing, and real market voice -> `know-your-customer.md`
- winners, losers, experiments, message learnings, performance evidence -> `performance-memory.md`
- raw quotes, URLs, source platforms, access dates, evidence quality fields, and lightweight tags -> `docs/context-sources/voc-bank.csv`

### 4. Update carefully

When editing:

- preserve useful prior detail
- add missing nuance from new source material
- flag contradictions explicitly
- keep short paragraphs and readable bullets
- allow file-specific custom sections where the business needs them
- keep emotionally important phrasing where it clarifies intent
- prefer a short precise paragraph over five vague bullets
- prefer bullets over long prose for rules, mechanics, and distinctions

For the expected structure and section intent of each file, see [references/file-contracts.md](references/file-contracts.md).

#### Editing standard by file

- `business-model.md`: highest precision, lowest fluff
- `storytelling.md`: most narrative freedom, but still well-sectioned
- `know-your-customer.md`: strongest preference for web-backed verbatim language and zero guessing
- `performance-memory.md`: strongest preference for evidence, dates, and explicit uncertainty
- `voc-bank.csv`: strongest preference for faithful quote capture, traceable sources, explicit evidence quality, and consistent row structure

#### What good updates look like

- specific
- repo-specific
- grounded in the provided sources
- easy to diff and review

#### What bad updates look like

- consultant language
- flattened summaries
- generic startup phrasing
- neat but uninformative structure
- removing nuance to make the doc shorter
- customer psychology invented from founder intuition
- audience sections filled without real evidence
- one-off web findings used for synthesis but never persisted in the evidence bank
- KYC files that claim stronger validation than the bank can support
- polished composite personas that outrun the evidence
- pricing sensitivity or urgency claims presented as truth without direct support

### 5. Report what changed

After updating, provide a concise report with these exact headings, in this exact order:

- `Sources used`
- `Files updated`
- `Key additions`
- `Contradictions or unresolved conflicts`
- `Open questions`
- `Recommended next step`
- `Completion status`

If `know-your-customer.md` was updated, also include:

- `Public audience sources reviewed`
- `VoC bank status`
- `Evidence quality mix`
- `Bank/KYC consistency check`
- `KYC checklist status`
- `What remains unsupported by real evidence`

If `know-your-customer.md` was audited, also include:

- `KYC checklist status`

Do not omit required sections.
If a required section is empty, write `- none`.
If KYC was in scope, the report is not complete until every KYC-specific heading appears.

When KYC is still below threshold, `Completion status` must say so plainly.
Do not describe the work as finished if it is only partially supported.
If the report cites quote counts, validated themes, or coverage ratios, derive them from the actual rows in `voc-bank.csv`.

Keep it short, but concrete.

### 6. Always propose the handoff

At the end of a successful `bootstrap`, `update`, or meaningful `performance-update`, always propose running the `product-marketing-context` skill next so downstream marketing skills get an updated compiled context file.

Be explicit:

- say that the canonical files are now updated
- say that `product-marketing-context` is the next compilation step
- say this under `Recommended next step`, not only as a trailing aside
- do not imply that compilation already happened unless it actually did

## Output Quality Bar

The resulting files should be:

- precise enough for agents to act on
- readable enough for a human to review quickly
- rich enough to preserve business-specific nuance
- stable enough to survive repeated updates
- specific enough that downstream skills will not default back to generic output

Use this practical quality test:

- Could a strong copywriter infer the offer, audience, and angle from these files?
- Could an agent produce differentiated content without guessing?
- Could a reviewer see where a claim came from?

Avoid these failure modes:

- transcript dumped almost raw
- over-compressed summaries that lose the founder's real intent
- generic consultant language
- rigid questionnaire style with thin answers
- contradictions rewritten away instead of surfaced

## Validation

To check whether the repo has the expected files, run:

```bash
python3 ~/.agents/skills/my-personal-context-distillation/scripts/validate_context_tree.py
```

Use this before and after updates when you want a quick sanity check.

## Examples

### Example request: bootstrap

"Take this founder transcript and create the canonical context files for this repo."

### Example request: update

"Merge this new voice note transcript into the existing business context."

### Example request: performance update

"Add these Meta ads learnings and loser angles into performance-memory.md."

### Example request: audit

"Audit whether this repo has enough context for high-quality marketing output."

## Final Rule

This skill should leave the repo with stronger source-of-truth context than before.

If a cleaner file would become less truthful, choose truth.
If a more detailed file would become unreadable, reorganize it instead of flattening it.
