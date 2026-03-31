# Cookie Banner Business Evidence

Use this file when the user asks a cookie-banner / CMP question in explicitly business-first terms, for example:

- "Will hiding or weakening reject all improve the business?"
- "Does a full-screen modal beat a bottom sheet on net business impact?"
- "Choose the highest-performing banner based on data, not just compliance"

This file does not replace `cookie-banner-optimization.md`.
It adds the missing evidence ladder for business-first decisions.

## How To Use This File

For explicit business-first cookie-banner questions, answer in this order:

1. `Ce qui est prouvé`
2. `Ce qui a été inféré`
3. `Ce qui reste non démontré`
4. `Comment relancer cette recherche`

If the user still wants one practical direction despite the missing proof, default to section 2, but say clearly that it is inferred and not proved.

## What Is Proved

The public evidence reviewed here robustly supports:

- weakening or removing `Reject all` from the first layer increases raw consent materially
- adding extra effort to refuse can crush the refusal rate
- barrier / intrusive formats reduce banner ignorance and force more immediate action
- bottom placement performs well on interaction and is a strong default on mobile

Representative quantitative anchors from the preserved research:

- removing first-layer reject can lift consent by roughly `+22 to +23 percentage points`
- an extra-click-to-refuse pattern can move refusal from about `16%` to about `4%`
- a banner can be ignored about `3.6x` more often than a barrier
- a bottom-left placement reached about `37.1%` interaction in one field study

These are strong signals for:

- raw acceptance
- refusal difficulty
- interaction / forced action

They are not automatic proof of higher profit.

## What Is Not Proved Publicly

The public evidence reviewed here does **not** robustly prove, in a generalizable way, that:

- more coercive cookie banners maximize global business for product / SaaS / ecommerce / lead-gen sites
- weakening reject all improves the final KPI once bounce, friction, trust, and conversion are accounted for together
- a full-screen / barrier modal beats a bottom sheet on net revenue or conversion for non-publisher businesses

When that proof is missing, say so explicitly.

Do not turn:

- a proved lift on raw consent

into:

- a claimed lift on revenue, conversion, or business health

unless the evidence actually reaches that KPI.

## Business-Model Split

Do not generalize publisher evidence to product businesses.

Keep these models separate:

- `publisher / ad-supported`:
  public evidence can exist for revenue effects of stronger tracking or pay-or-tracking walls
- `product / SaaS / ecommerce / lead-gen`:
  public evidence is much weaker on the final business KPI, even when consent effects are well documented

If the scoped business is not ad-supported, do not use publisher revenue results as if they settled the question.

## What Has Been Inferred From The Available Evidence

If the user forces a single business-first recommendation under incomplete public proof, the current inferred best synthesis is:

- bottom sheet / sticky bottom sheet
- short and compact first layer
- no full-screen modal by default
- `Accept all` as the primary button
- `Customize` as the secondary button
- `Reject all` as a less salient text link on the first layer rather than an equivalent primary button

Why this is the current inference:

- the format stays low-friction to avoid the known downside risk of more intrusive barriers
- the choice hierarchy is where the available evidence most clearly supports a raw-consent lift
- it is the best synthesis the preserved discussion reached once it tried to optimize for acceptance while still accounting for bounce risk

But label this clearly:

- inferred, not proved
- current best synthesis under incomplete public evidence
- valid only when the user explicitly wants the strongest business-first direction despite missing proof

Do not rebrand this as "data-proved" or "universally best".

## What Still Remains Unanswered

The unresolved question that the preserved research still failed to settle is:

`For non-publisher product / SaaS / ecommerce / lead-gen sites, which cookie-banner configuration maximizes net business once both raw acceptance and bounce / abandonment / downstream conversion are jointly accounted for?`

More specifically, public evidence is still missing or insufficient on:

- bottom-sheet vs more intrusive modal on the final composite KPI
- visible reject vs weakened reject on the final composite KPI
- revenue/session or conversion impact for non-publisher businesses under these exact banner choices
- whether the raw-consent gain from weaker reject salience survives once extra bounce or friction is included

Keep this gap alive in the skill instead of pretending it has been solved.

## How To Re-Run The Missing Research Later

When the user wants to retry this search from zero, use a prompt with these constraints:

- the target KPI is not raw consent alone
- the target KPI is net business impact, including both acceptance and bounce / abandonment
- distinguish publisher evidence from product / SaaS / ecommerce / lead-gen evidence
- prioritize public quantitative studies, A/B tests, field experiments, or case studies that measure both acceptance and downstream business effects
- if the public proof still does not exist, say so plainly

Minimum rerun question:

`Find public quantitative evidence that jointly measures cookie-banner design, consent lift, bounce or abandonment, and downstream business KPIs for non-publisher product / SaaS / ecommerce / lead-gen sites. Compare bottom-sheet vs intrusive modal, and visible reject vs weakened reject.`

## Operational Split

When writing the final answer, keep the split explicit:

- `Prouvé` = only what the public evidence actually demonstrates
- `Inféré` = the current best synthesis when the user still wants one directional answer
- `Non démontré` = the exact missing proof
- `Recherche à relancer` = the preserved missing question and how to ask it again

## Preserved Sources

Read alongside:

- `references/cookie-banner-optimization.md`
- `references/cookie-banner-business-deep-research.md`
- `references/cookie-banner-business-chatgpt-export.md`
- `references/cookie-banner-deep-research-report.md`
