---
name: my-personal-product-legal-review
description: "[My Personal Skill] Use when a digital product needs a post-build legal/compliance review anchored in the real implemented scope. Trigger on requests about legal review, compliance audit, privacy policy, terms, cookies, cookie banner / CMP review or optimization, GDPR/e-commerce obligations, legal text patching, durable-medium/order confirmation flows, or checking whether the real product flow and features are properly covered by legal surfaces. Best fit for FR/EU B2C digital products by default, while remaining adaptable to other jurisdictions when explicitly scoped."
---

# My Personal Product Legal Review

## Overview

This skill audits the real implemented scope of a digital product, maps the resulting legal obligations, reviews the existing legal and adjacent customer-facing surfaces, and identifies or patches the gaps when explicitly asked to execute.

Its default unit of analysis is the real product scope, not a page-by-page checklist. Start from implemented features and flows, derive the obligations from that scope, then judge whether the current legal and adjacent surfaces cover them.

This is an operational compliance-review skill, not a substitute for licensed legal counsel. Its job is to produce a rigorous, source-backed product/legal review without hallucinating certainty.

## Trigger Conditions

Use this skill when the user asks any variation of:

- "Review the legal compliance of this app / site / SaaS"
- "Audit our privacy policy / terms / cookies against the real product"
- "Review or optimize our cookie banner / CMP against the real product and consent flow"
- "Check whether our legal pages cover the actual flow and features"
- "What legal obligations do we have given this product?"
- "Patch the legal texts"
- "Do we need a post-purchase confirmation email / durable medium?"
- "Re-review the product after launch for legal gaps"
- "Understand the codebase, determine the real features and obligations, then fix the missing legal text"

Do not use this skill for:

- trademark clearance
- company formation / tax structuring
- bespoke litigation strategy
- pure security reviews with no legal-surface question
- generic "what is GDPR?" educational questions detached from a real product

## Core Doctrine

This skill is intentionally strict.

Its default posture is:

1. Inspect the real implemented product first
2. Classify the legal perimeter before concluding anything
3. Use current official sources for anything time-sensitive or jurisdiction-sensitive
4. Separate verified facts from hypotheses
5. Stop when required compliance inputs are missing instead of pretending completeness
6. Treat new customer-facing compliance assets as product/marketing surfaces first, then weave compliance into them
7. Never modify visible UX outside legal pages without explicit before/after approval
8. Do not default to a page-by-page matrix; default to a scope-based review grouped by real behavior and obligation buckets
9. When execution is explicitly requested, carry the work through end-to-end inside the approved scope instead of stopping at diagnosis
10. When a missing compliance surface requires customer-facing value design, scan the full live installed skill inventory before choosing which downstream skills to use
11. For customer-facing assets outside legal pages, switch to collaborative review mode: inspect the surrounding flow first, then review one element at a time with before/after on both form and substance before implementation
12. Never let value-first framing override the primary job of the asset; first prove that the chosen vehicle can actually solve the gap it was introduced to solve
13. Every proposed block or element in a customer-facing asset must have a unique job; if two blocks carry materially the same message, merge or remove one
14. When implementing a recommended asset, verify that it is actually wired into the real product flow and trigger path; never stop at creating dead code, an unused template, or an uncalled helper
15. Treat cookie banners as hybrid compliance + marketing + measurement + performance surfaces; never review only the wording while ignoring the real consent runtime, performance footprint, or choice architecture
16. For cookie-banner optimization, separate what is proved on raw consent from what is proved on net business impact; never present "more coercive = more business" as settled fact without scoped evidence
17. When the evidence for the final business KPI is incomplete, default to the strongest generalizable doctrine and label any more aggressive option as inference-only or test-only

When the user only asks for analysis, stay at advice level.

When the user explicitly asks for execution, patch only what has been requested and only after the audit is grounded enough to act safely.

## Default Scope Bias

Unless the user states otherwise, assume:

- FR / EU legal posture first
- B2C consumer-facing digital product
- website / SaaS / app with possible payments, emails, auth, support, analytics, cookies, and public-sharing surfaces

If the real project differs, state the deviation explicitly and adapt the audit.

Read:

- `references/scope-classification.md`
- `references/legal-surface-matrix.md`
- `references/value-first-compliance-assets.md`
- `references/dynamic-skill-selection.md`
- `references/customer-asset-review-mode.md`

If the request touches cookie banners / CMPs, also read:

- `references/cookie-banner-optimization.md`
- `references/cookie-banner-business-evidence.md`
- `references/cookie-banner-business-deep-research.md`
- `references/cookie-banner-business-chatgpt-export.md`
- `references/cookie-banner-deep-research-report.md`

## Workflow

### Step 1 — Classify the product and legal perimeter

Determine and state explicitly:

- geography / jurisdiction in scope
- B2C vs B2B vs mixed
- product type
- payment / subscription model
- data-processing model
- support model
- public-sharing / community / marketplace / content surfaces
- whether the task is analysis-only or execution

If any of these is unclear and materially changes the audit, flag it as missing.

### Step 2 — Inspect the real implemented scope first

Audit the product from evidence, not from marketing copy.

Prefer:

- codebase and configs
- real routes, API handlers, cron jobs, emails, payment/webhook flows
- live product behavior when needed and when safe
- admin surfaces only when necessary

Never infer a feature merely because the UI suggests it "should" exist.

Use the checklist in `references/scope-classification.md`.

### Step 3 — Research current official legal sources

Before concluding on obligations that may change over time, research current official sources.

Examples:

- Service-Public
- economie.gouv.fr / DGCCRF
- CNIL
- Commission européenne
- other official regulator or government sources for the scoped jurisdiction

For technical/legal questions, prefer primary and official sources over summaries.

State what is:

- verified from source
- inferred from source
- still uncertain

### Step 4 — Build the obligation map from the real product

Map implemented features to legal obligations.

Do not collapse the review into a page inventory too early. The primary lens is:

`real feature / real flow -> legal obligation -> current coverage -> gap -> action`

Typical buckets:

- identity / mandatory legal notices
- contract formation / pre-contractual information
- subscription, renewal, cancellation, durable-medium confirmation
- consumer mediation / complaints channel
- privacy notice / GDPR articles 13-14 style information
- cookies / consent / cookie banner / CMP / measurement / advertising
- support/chatbot/AI disclosures
- public sharing / user-generated or publicly exposed data
- retention / deletion / post-termination behavior
- email communications and preference management

Use `references/legal-surface-matrix.md`.

### Step 5 — Run the assumptions checkpoint before any deliverable

Before producing an audit conclusion or patch proposal, list:

- `✅ verified` assumptions with source
- `❌ not verified` assumptions with what is missing

If a missing input prevents a reliable conclusion, stop and surface the blocker clearly.

Do not quietly fill gaps with "usual" assumptions.

### Step 6 — Review the current legal and adjacent surfaces

Inspect what currently exists:

- terms / CGU / CGV
- privacy policy
- cookies policy
- legal notice / imprint
- checkout / onboarding / upgrade wording
- post-purchase or post-upgrade emails
- support pages / chatbot disclosures
- unsubscribe and consent flows

When the gap touches a customer-facing asset outside legal pages, also inspect the adjacent flow surfaces around that asset instead of reviewing it in isolation.

Separate:

- what is already covered correctly
- what is covered but incomplete or stale
- what is not covered
- what is contradicted by the real product behavior

### Step 6.5 — If cookies / CMP are in scope, inspect the real consent surface end-to-end

Do not stop at "there is a cookie policy" or "there is a banner".

Inspect the real implemented consent surface and runtime:

- whether a banner / CMP actually exists
- where and when it appears
- first-layer controls and whether reject is as visible/actionable as accept
- whether there is a true settings path and where it leads
- category model on the preference center
- whether the banner feels like a modal, bottom sheet, top bar, inline block, or other pattern
- whether it creates layout shift, blocks reading, or risks becoming a performance bottleneck
- whether consent state is initialized before tags that depend on it
- whether consent updates are applied on the real page where the interaction occurs
- whether analytics / ads / measurement firing logic is actually gated by the chosen consent state
- whether the user can re-open and change consent later
- whether the consent funnel itself is instrumented cleanly enough for testing and optimization

For banner creation or revision, use:

- `references/cookie-banner-optimization.md` for the actionable baseline
- `references/cookie-banner-business-evidence.md` for the business-evidence ladder and proof thresholds
- `references/cookie-banner-business-deep-research.md` as the preserved business-focused deep research source
- `references/cookie-banner-business-chatgpt-export.md` as the preserved exploratory decision log
- `references/cookie-banner-deep-research-report.md` as the preserved full research source

When a cookie banner or CMP needs to be created or updated, treat it as a customer-facing asset that must satisfy both:

- the compliance job first
- then the value / friction / measurement / performance goals

When the user asks which cookie-banner direction is "best for business", explicitly classify:

- what the evidence proves on raw consent or interaction
- what the evidence proves on bounce, conversion, revenue, or business health
- what is still only an inference
- whether publisher evidence is being misapplied to a non-publisher business model

If the final KPI is not publicly proved for the scoped model, say so plainly instead of guessing.

### Step 7 — Decide the action lane

Choose one or more lanes explicitly:

- analysis only
- legal-text patching
- adjacent product-surface recommendation
- execution of requested legal-page changes
- specification of a new missing compliance surface

If a gap requires a new customer-facing asset, do not frame it as a cold legal patch.

Follow `references/value-first-compliance-assets.md`.

If autonomous execution was explicitly requested, the default expectation is:

1. understand the real codebase and features first
2. determine the obligations from that real scope
3. review the current legal surfaces against those obligations
4. patch the missing text or legal-page gaps directly inside the requested scope

Do not stop at a diagnosis or a page-by-page matrix unless the user explicitly asked for that format.

### Step 7.4 — Validate the vehicle before any framing work

When a new or revised asset is being considered, state explicitly:

- the primary function the asset is supposed to fulfill
- why this function exists
- whether the proposed vehicle can actually fulfill it
- what the secondary goals are, if any

Examples of primary functions:

- satisfy a durable-medium / post-purchase confirmation obligation
- carry mandatory cancellation information
- provide a visible complaint channel
- explain a support or chatbot disclosure requirement
- reassure and orient the user after a state change

Examples of secondary goals:

- reduce anxiety
- improve perceived value
- reinforce the product story
- increase activation or retention

Functional-fit rule:

- if the asset was introduced primarily to solve a legal/compliance gap, it must be able to satisfy that gap before any value-first framing work begins
- if the proposed vehicle cannot carry the required content or required durable/technical property, reject that vehicle immediately and choose another one
- do not continue into copy review, UX review, or skill orchestration for an unfit vehicle

Value-first is a framing rule, not a permission to choose the wrong vehicle.

### Step 7.5 — Discover relevant installed skills dynamically for value-first assets

Use this step only when the legal gap requires a new or revised customer-facing asset such as:

- post-purchase email
- onboarding disclosure
- upgrade confirmation
- cancellation confirmation
- support or chatbot disclosure surface
- cookie banner / CMP surface
- any other adjacent asset where product value and compliance must coexist

Before choosing any downstream skill, run:

```bash
python3 ~/.agents/skills/my-personal-product-legal-review/scripts/list_installed_skills.py
```

Use that live inventory so the full currently installed skill list is in working context.
Do not choose downstream skills from memory, from a static shortlist, or from only the first few plausible skills.
Do not dump the raw full inventory into the final user-facing answer unless the user explicitly asks for it.

Then read `references/dynamic-skill-selection.md` and decide:

- which currently installed skills are actually relevant to the specific asset
- which one should shape the strategic foundation first
- which ones are execution helpers only
- which ones are not relevant for this task and should be ignored

The selection must be task-specific, not fixed.

### Step 7.6 — Load customer and flow context before reviewing a visible asset

If the gap requires reviewing or creating a customer-facing asset outside legal pages, read `references/customer-asset-review-mode.md`.

Load, if they exist in the repo:

- `.agents/product-marketing-context.md`
- `.agents/business-model.md`
- `.agents/know-your-customer.md`
- `.agents/storytelling.md`
- `.agents/performance-memory.md`

Also load:

- the current asset code
- the current translations for that asset
- the neighboring assets in the same journey

Do not propose changes until the triggering moment, upstream messages, downstream state, and likely emotional context are understood.

This review mode applies only after the proposed vehicle has passed the functional-fit check in Step 7.4.

### Step 7.7 — Review one element at a time before any visible implementation

For visible assets outside legal pages:

- review with the user one element at a time
- compare each element with before/after on both form and substance
- keep the comparison easy to scan; do not use one giant before block and one giant after block
- for review examples, present the content only in French unless the user asked otherwise
- do not omit any part of the element under review
- for each proposed element, state its unique job in the asset
- check whether that job or information is already carried elsewhere in the same asset
- if two elements overlap materially, merge them or remove the weaker one before presenting the review

Only implement after the user has explicitly validated the reviewed element or reviewed bundle.

### Step 8 — Patch only with the requested execution scope

If execution is requested:

- patch legal pages directly when the user asked for it
- do not change visible UX outside legal pages without explicit approval
- if a new customer-facing asset is required, present the before/after and rationale first unless the user has already authorized implementation
- for visible customer-facing assets outside legal pages, get approval on the element-by-element review before patching
- when frontend/UI work is delegated by project convention, follow the repo’s routing rule instead of implementing directly

### Step 8.5 — Verify real integration, not just asset existence

When the execution includes a new or revised asset that is supposed to close a real product gap:

- identify the exact runtime trigger or invocation path that should fire it
- patch that real integration point, not just the asset file
- verify that the upstream flow can actually reach that point with the current code
- verify that the downstream effect is observable through tests, logs, or other concrete evidence
- if the asset exists in code but is not actually triggered, treat the gap as still open

Examples:

- a post-purchase email must be triggered from the real payment / activation flow
- a disclosure surface must be rendered in the actual UI state where the requirement applies
- a durable-medium confirmation must be attached to the real order-confirmation path
- a consent or unsubscribe mechanism must be wired to the actual stored preferences

### Step 9 — Verify before claiming success

For any code/content changes:

- run the relevant validation steps
- show what changed
- distinguish what is now fixed from what remains intentionally unresolved

## Output Contract

Default output should be concise but structured.

Use:

1. `Checkpoint présupposés`
2. `Scope réel vérifié`
3. `Obligations déclenchées`
4. `Ce qui va`
5. `Ce qui ne va pas`
6. `Ce qui manque pour conclure`
7. `Actions ou patches recommandés / exécutés`

When the request is specifically about cookie-banner optimization, also include:

- `Ce qui est prouvé`
- `Ce qui est probable`
- `Ce qui n'est pas démontré`
- `Ce qui reste une hypothèse de test`

For audits, findings come before summary.

Default to grouping findings by obligation bucket or real product behavior, not by page, unless the user explicitly asks for a page-by-page format.

When dynamic skill discovery was used for a value-first asset, also include:

- `Live skills scanned: ...`
- `Relevant skills selected: ...`
- `Why these skills: ...`
- `Deferred / ignored skills: ...`

For execution, distinguish:

- implemented changes
- remaining legal risks
- deliberately accepted business trade-offs

## Hard Guardrails

- Never present unverified legal claims as facts
- Never confuse code inference with behavioral verification
- Never ignore conflicting sources; surface the conflict explicitly
- Never declare the product "fully compliant" if a required input or proof is missing
- Never optimize a new compliance asset for legal completeness alone; preserve reassurance, clarity, and perceived value
- Never choose or keep a customer-facing asset whose vehicle cannot fulfill the primary function that justified its creation
- Never bury important legal gaps behind soft language
- Never keep redundant blocks just because each one sounds individually good

## Anti-Patterns

Actively call out these mistakes when relevant:

- "The page sounds compliant, so the product must be compliant"
- "The UI says X, therefore the backend does X"
- "Everybody in SaaS skips this, so it is probably fine"
- "We can use one scary legal email as a pure compliance patch"
- "Because the user already knows they bought, no confirmation surface is needed at all"
- "A likely answer is good enough for legal review"
- "Because the copy direction is good, the underlying vehicle must be the right one"
- "Value-first means we can ignore whether the asset actually closes the identified gap"
- "If each block sounds good on its own, the full asset must be well structured"

## References

- For classification and evidence capture: `references/scope-classification.md`
- For obligation buckets and surfaces: `references/legal-surface-matrix.md`
- For value-first compliance assets: `references/value-first-compliance-assets.md`
- For cookie banner / CMP optimization: `references/cookie-banner-optimization.md`
- For cookie banner business-evidence framing: `references/cookie-banner-business-evidence.md`
- For the preserved cookie banner business deep research source: `references/cookie-banner-business-deep-research.md`
- For the preserved cookie banner exploratory export: `references/cookie-banner-business-chatgpt-export.md`
- For the preserved cookie banner deep research source: `references/cookie-banner-deep-research-report.md`
