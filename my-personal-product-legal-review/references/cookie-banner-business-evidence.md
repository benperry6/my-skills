# Cookie Banner Business Evidence

Use this file when the user asks a cookie-banner / CMP question in explicitly business-first terms, for example:

- "Will hiding or weakening reject all improve the business?"
- "Does a full-screen modal beat a bottom sheet on net business impact?"
- "Choose the highest-performing banner based on data, not just compliance"

This file does not replace `cookie-banner-optimization.md`.
It adds the missing evidence ladder for business-first decisions.

## The Evidence Ladder

Always separate these questions:

1. What increases raw consent or immediate interaction?
2. What is proved to improve the final business KPI?
3. What is only an inference or test hypothesis?

Do not collapse them into one answer.

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

## Default Doctrine When Evidence Is Incomplete

If the user wants the best generalizable default for business-first cookie optimization and no local experiment exists, use this doctrine:

- bottom sheet / bottom placement first
- short first layer
- `Accept all`, `Reject all`, and `Customize / Settings` visible on the first layer
- category-first preference center
- measurement resilience improved through stack choices, not only through coercive choice architecture

Why this remains the default:

- it is the strongest cross-business doctrine supported by the available public evidence
- it avoids overstating the case for more coercive designs
- it still leaves room for optimization through copy, visual presence, measurement setup, and runtime quality

## Inference-Only Fallback

If the user explicitly asks for the strongest **inference** despite missing proof, you may state it as an inference only.

The current inference from the preserved exploratory discussion is:

- keep the low-friction format (`bottom sheet`, not full-screen by default)
- increase assertiveness more through choice hierarchy than through full-screen blocking
- if the user wants to push acceptance harder, the speculative direction is:
  - `Accept all` as primary button
  - `Customize` as secondary
  - `Reject all` less salient than accept

But label this clearly:

- not proved as best for global business
- only a hypothesis
- test-only, not doctrine

Never present this fallback as the skill's default recommendation.

## Required Output Framing

For business-first cookie-banner questions, classify the answer into:

- `Prouvé`
- `Probable`
- `Non démontré`
- `Hypothèse testable`

If the user asks for a single recommendation anyway, state whether it is:

- a data-backed default doctrine
- or an inference chosen under incomplete evidence

## Preserved Sources

Read alongside:

- `references/cookie-banner-optimization.md`
- `references/cookie-banner-business-deep-research.md`
- `references/cookie-banner-business-chatgpt-export.md`
- `references/cookie-banner-deep-research-report.md`
