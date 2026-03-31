# Cookie Banner Optimization

Use this file when the legal review touches a cookie banner, CMP, consent layer, or tracking-choice surface.

This is the concise operational layer.
The preserved long-form research source lives in:

- `references/cookie-banner-deep-research-report.md`
- `references/cookie-banner-business-deep-research.md`
- `references/cookie-banner-business-chatgpt-export.md`

The distilled business-evidence layer lives in:

- `references/cookie-banner-business-evidence.md`

## What this surface is

A cookie banner is not just a legal notice.

It is simultaneously:

- a compliance surface
- a conversion-friction surface
- a measurement gate
- a performance risk surface
- a mobile and accessibility surface

Review it end-to-end, not as isolated copy.

## The baseline recommendation

Unless the real product context strongly suggests otherwise, the default baseline is:

- bottom placement first
- short first layer
- three visible choices on the first layer:
  - a primary accept action
  - an explicit reject action
  - settings / manage choices
- labels can be softened when the scope is already obvious from the cookie context, e.g. `Accept` / `Refuse` or `Accepter` / `Refuser`, as long as the meaning stays clear
- category-first preference center
- symmetric primary choices
- persistent re-open path later, preferably via a visible footer link on product-like sites rather than a floating chip unless the product context really benefits from the chip pattern

This is the default optimization starting point, not a universal law.

## Copy / CRO Lessons

Once the banner is structurally sound and the real runtime is verified, do not overfit the skill to one fixed label set.

For copy and tonality, prefer reusable lessons over rigid wording rules.

Explicitly use:

- `copywriting`
- `popup-cro`

when the user wants to make the banner feel softer, clearer, more persuasive, or less anxiety-inducing without changing its core structure.

The current lessons to preserve are:

- improve by tone, hierarchy, compacity, and anxiety reduction more than by legalese
- make the body more user-first
- explain what the user gains
- explain what improves in the user's experience
- make it feel that accepting helps the service be more useful or more relevant for the user, not merely better tracked for the company
- make categories more positive and concrete
- reduce jargon such as `advertising`, `publicité`, `campaigns`, `campagnes`, `conversions`, and tracking-stack language when it is not needed for clarity
- if the optional ads-related category needs a softer presentation, prefer a context-adapted, more desirable framing over a cold `Advertising` / `Publicité` label, as long as the function stays honest and understandable
- keep all derived copy coherent with that framing, including help text and strict-notice text, so harsher ad language does not reappear elsewhere in the same banner

These are lessons, not hardcoded strings.
Adapt the final wording to the product context, audience stress level, and honesty constraints.

## Business-Evidence Guardrail

Do not answer a cookie-banner business question with a single blurred conclusion.

Always separate:

- what is proved on raw consent
- what is proved on interaction or banner ignorance
- what is proved on the final business KPI
- what is only an inference or a test hypothesis

Current default evidence posture:

- stronger asymmetry or weaker reject visibility is proved to increase raw consent
- intrusive barrier formats are proved to force more action and reduce ignored banners
- neither of those facts is sufficient, by itself, to prove higher global business for product / SaaS / ecommerce / lead-gen sites
- for those scoped businesses, the strongest generalizable default remains a bottom-sheet style first layer with three visible choices

If the business model is `publisher / ad-supported`, keep that evidence separate.
Do not transfer publisher revenue findings to non-publisher products as if they were universal.

## Primary goals

Optimize for all of these together:

1. valid and understandable consent
2. maximum useful consent without manipulative steering
3. minimum friction at entry
4. measurement quality that reflects the real consent state
5. minimal performance damage
6. strong mobile usability and accessibility

## First-layer review checklist

Check:

- Does the banner actually appear in the real product?
- Does it show immediately enough for the real tracking flow?
- Are accept and reject equally visible and equally easy to click?
- Is settings visible without hunting?
- Is the copy short enough to scan quickly on mobile?
- Does the layout avoid covering essential UI or blocking reading more than necessary?
- Does it avoid fake urgency, fake recommendations, or asymmetric visual emphasis?

## Preference-center review checklist

Check:

- categories are understandable
- necessary is clearly distinguished from optional
- settings are not buried behind an excessive number of layers
- vendor details are progressive, not dumped by default if that hurts usability
- save / confirm behavior is obvious
- the user can later reopen and revise choices

## Runtime review checklist

Check:

- default consent state is initialized before dependent tags run
- accept / reject / save settings actually update the real runtime state
- analytics, ads, and other optional tags are gated by the chosen state
- denied flows still behave coherently for measurement where the stack supports it
- the consent event pipeline is observable enough to debug or test

Do not declare the banner "done" because the UI exists if the runtime is wrong.

## Recommendation Ladder

Use this ladder when the user asks "what should we do?".

### 1. Data-backed default doctrine

Recommend by default:

- bottom placement
- short first layer
- visible `Accept`, `Refuse`, and `Customize` when the cookie scope is obvious enough for shorter labels
- keep `Refuse` explicit and immediately clickable, but it may be visually weaker than the primary accept action if the user explicitly chooses the business-first inferred direction
- category-first preferences
- improved measurement through runtime quality and stack choices
- a persistent footer link such as `Cookie preferences` / `Préférences cookies` to reopen preferences later on product-like sites

This is still the safest operational baseline for compliance-first or mixed compliance/business review.

### 2. Business-first inferred direction

If the user explicitly asks for the strongest business-first direction despite incomplete proof on the final KPI, do not stop at the conservative baseline.

You may state the current inferred direction:

- low-friction format
- stronger accept hierarchy than reject
- weaker reject salience on the first layer
- softer button labels when the meaning stays obvious
- footer-link reopen path preferred over a floating chip for cleaner product UI
- copy refinement should bias toward perceived usefulness, relevance, and reduced anxiety rather than internal campaign language

But always label it as:

- inferred rather than proved
- not settled on the final business KPI
- the current best synthesis under incomplete public evidence

## Performance review checklist

Check:

- banner does not create CLS when it appears
- banner is not large enough to risk becoming the LCP element unnecessarily
- clicking accept does not trigger an avoidable INP spike from loading everything at once
- banner scripts and assets are loaded with an intentional strategy
- mobile viewport and safe-area behavior are acceptable

## Accessibility review checklist

Check:

- full keyboard navigation
- predictable focus order
- proper dialog semantics if modal
- readable contrast and tap targets
- toggles and buttons are labeled clearly

## Creation / update rule

If the banner is missing or materially weak:

1. inspect the real stack first
2. verify the vehicle can do the runtime job
3. review or propose the banner one element at a time
4. show before / after on form and substance before visible implementation
5. when implementation is approved, wire the banner into the real consent flow and verify it is not dead code

## Anti-patterns

Call these out explicitly:

- accept visible, reject hidden
- reject only accessible through a second layer without strong reason
- reject buried inside the body copy or confused with the information paragraph
- misleading color contrast or button hierarchy
- banner copy optimized in isolation from the real tracking runtime
- a legally "present" banner that is technically disconnected from the real consent logic
- a banner that destroys mobile UX or Core Web Vitals while claiming to be optimized
- a proved lift on raw consent being presented as if it proved higher global business
- publisher-only revenue evidence being used to settle a product / SaaS / ecommerce question
