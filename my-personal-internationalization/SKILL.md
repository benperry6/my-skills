---
name: my-personal-internationalization
description: "[My Personal Skill] Use when a website or web app needs its international architecture designed, audited, fixed, or translated for multilingual SEO. Trigger on requests about i18n, l10n, locale routing, language selectors, language cookies, Accept-Language, mismatch banners, hreflang, x-default, canonical alternates, localized sitemaps, translating locale catalogs (for example `fr.json` -> `en.json`), auditing missing locale keys, scanning hardcoded user-facing strings, post-translation verification, or deciding which languages or language variants to launch first. This skill is doctrine-first, web-focused, and language-first: it turns proven hreflang-driven product decisions into reusable rules for websites and web apps."
metadata:
  version: 1.5.0
---

# My Personal Internationalization

## Overview

This skill exists to avoid rediscovering web international architecture from zero on every project.

It is a language-first, hreflang-driven internationalization skill for websites and web apps.

Its job is to turn already-proven multilingual product decisions into reusable doctrine, then adapt that doctrine to the current project's stack, routes, auth model, optional price-display model, international SEO strategy, and rollout scope.

This is an international architecture skill first.

It also includes a dedicated catalog-translation mode when translation work is part of that architecture.

Optional display-currency logic may be layered on top when the product visibly shows prices.

This skill is not a multi-country commerce architecture skill and must not drift into multi-entity, multi-country, or heavy multi-billing design unless the user explicitly asks for that.

This skill serves two primary use cases:

- design or audit multilingual architecture
- run a multilingual catalog-translation campaign correctly

## Why This Skill Exists

For broad-addressable products, internationalization is not just a UX or content concern.
It is also a growth lever.

The operational thesis behind this skill is:

- if a strong page already performs in one language
- and its localized equivalents are implemented correctly
- and those equivalents are tied together with the right international SEO signals

then those translated pages often gain international search visibility faster than isolated pages launched from zero.

This makes internationalization strategically useful because it can:

- expand reachable search demand without reinventing each page from scratch
- help search engines serve the right language version to the right users
- reduce multilingual duplication confusion
- create a reusable rollout system across multiple businesses

Important:

- treat this as a strong SEO operating doctrine and growth heuristic
- do not present it as a guaranteed Google promise of literal signal transfer

This is why this skill covers both:

- international architecture
- and language / language-variant rollout strategy

Use it both:

- when building a multilingual website or web app from scratch
- when auditing or fixing the international behavior of an existing product

## Trigger Conditions

Use this skill when the user asks any variation of:

- "Set up the international architecture of this website or web app"
- "Audit our i18n / locale behavior"
- "Fix locale routing / language persistence / language switching"
- "Design the language selector"
- "Handle browser language vs explicit locale URLs"
- "Implement or review a locale mismatch banner"
- "Separate language from optional price display rules"
- "Decide which languages or language variants to translate first"
- "Use hreflang strategy to scale SEO internationally"
- "Make emails / API errors / shared pages respect the user's language"
- "Review hreflang / x-default / localized sitemap"
- "Turn our i18n doctrine into a reusable implementation"
- "Translate `fr.json` into `en.json` like a native speaker"
- "Translate a locale catalog naturally, not literally"
- "Audit missing locale keys or hardcoded strings after translation"

Do not use this skill for:

- copywriting in another language
- generic SEO work that is not materially about multilingual behavior
- native mobile app internationalization that is not about web routing, web UX, or multilingual SEO

Pure catalog translation is still valid here when it is coupled to locale architecture, locale rollout, or translation-quality verification.

## Core Doctrine

These are the default rules unless the project has already made an explicit contrary decision:

1. Treat internationalization as product architecture, not as string replacement.
2. Keep `current locale` and `preferred locale` separate.
3. Treat an explicit locale in the URL as sovereign for display.
4. Model language preference in two layers:
   - explicit manual preference
   - auto-detected preference
5. Manual preference always beats auto-detection.
6. Guests need explicit preference handling too, not just authenticated users.
7. Never confuse a technical navigation cookie with an explicit language preference.
8. Locale switching must preserve path, query string, and hash whenever possible.
9. The explicit locale selector should be driven by one central ordered locale registry, not ad hoc page-level lists.
10. Language is the primary axis in this skill. Country or market variants are secondary.
11. Treat `language`, `display currency`, `billing state`, and any optional market metadata as separate layers, even when a launch policy maps some of them 1:1.
12. Default to a `language-only` locale strategy. Split into region variants only when materially justified by SEO relevance, conversion, legal wording, or product fit.
13. Optional locale -> display currency mapping is allowed when the product visibly shows prices.
14. Language changes must not by themselves change active billing currency, subscription price IDs, legal entity, or country-specific business state.
15. Do not expand into multi-country, multi-entity, or heavy multi-billing architecture unless the user explicitly asks for it.
16. Internationalization must cover UI and non-UI surfaces.
17. International SEO must be centralized and generated from shared rules.
18. Language rollout should be strategic, not arbitrary.
19. Locale logic must be tested like business logic.

## Reference Map

Read only what the current task needs:

- `references/doctrine.md`
  - The reusable international product doctrine distilled from prior real-world implementation work.
- `references/locale-decision-tree.md`
  - The decision tree for `current locale`, `preferred locale`, banner logic, and durable preference behavior.
- `references/international-seo.md`
  - The reusable doctrine for canonical, `hreflang`, `x-default`, route registries, and localized sitemaps.
- `references/market-selection.md`
  - The reusable strategy for selecting languages or language variants, deciding when a regional split is justified, and optionally simplifying display-currency rollout.
- `references/catalog-translation.md`
  - The reusable workflow for native, culturally adapted locale-catalog translation, scaling orchestration, and post-translation verification.
- `references/evaluator-rubric.md`
  - The acceptance rule for independent locale evaluators, including what stops or continues the correction loop.
- `references/implementation-checklist.md`
  - The practical build/audit checklist before shipping multilingual behavior.

## Before Recommending Anything

Read the current project's context first.

Prioritize:

- `AGENTS.md` / `CLAUDE.md`
- `PRODUCT_MEMORY.md` or equivalent project memory
- `.claude/notes.md` if it exists
- any i18n, pricing, routing, SEO, or architecture docs
- any document like `docs/i18n-hreflang-seo.md` if present

If the project already contains explicit international decisions, reuse them instead of reopening settled questions.

Before producing a doctrine, audit, or implementation plan, establish these assumptions:

- which locale codes are supported
- which locales are actually translated and production-ready
- whether localized URLs already matter for acquisition
- whether the project is broad-addressable or inherently local/narrow-market
- whether the product has authenticated user state
- whether guest traffic needs language persistence
- whether the product visibly shows prices
- whether locale-aware display currency is needed
- whether launch-stage display-currency simplification is desirable
- whether any region split is materially justified
- which user-facing non-UI surfaces exist
- which multilingual SEO surfaces exist or should exist

If some of these materially affect the recommendation and are still unknown, say so explicitly.

## Workflow

### 1. Classify the international problem

Determine whether the task is primarily about:

- language/language-variant prioritization
- locale routing
- language persistence
- mismatch and suggestion UX
- translation asset structure
- catalog translation execution
- locale vs optional price-display separation
- cross-surface language consistency
- international SEO
- testing and rollout safety

Many projects need several of these at once. Name them explicitly.

### 2. Classify the international growth model

Determine whether the product is:

- single-market and intentionally local
- regional/multi-market but selective
- broad-addressable and a good candidate for international SEO scaling

If the product is broad-addressable, treat language selection as a growth decision, not just a translation task.

If the product is narrow by regulation, fulfillment, language community, or offer fit, say so explicitly and avoid defaulting to unnecessary multilingual expansion.

### 3. Build the international state model

Define at minimum:

- `current locale`
- `preferred locale`
- explicit authenticated preference
- auto-detected authenticated preference
- explicit guest preference
- passive guest signals
- default locale

Never let a project operate on a single vague "locale" variable if those concepts are actually distinct.

### 4. Audit the resolution hierarchy

Check or define the full precedence order.

Default reusable order:

1. explicit locale in the URL
2. explicit manual account preference
3. auto-detected account preference
4. explicit guest preference
5. browser/app language
6. default locale

Use this to drive defaults, redirects when no locale is explicit, and cross-surface delivery.
Do not use it to forcibly override an explicit localized URL.

### 5. Audit or design the suggestion layer

If `preferred locale !== current locale`, the safe default is a non-blocking suggestion banner, not a forced redirect.

For the suggestion layer, ensure:

- it works for authenticated users
- it works for anonymous users
- it is written in the language most likely to be understood
- it uses simple user-facing wording rather than storage jargon
- it distinguishes durable choices from session-only dismissal

Default interpretation:

- `Switch to X` = durable preference for `X`
- `Stay in Y` = durable preference for `Y`
- `Close` = session-only, pair-scoped dismiss

Unless the project already validated a different pattern, reuse the default mismatch-banner doctrine from `references/locale-decision-tree.md`:

- compact title
- short two-sentence subtitle
- language names localized into the banner language
- primary CTA for switching
- secondary ghost CTA for staying
- independent close button
- stacked mobile actions by default

### 6. Audit or design locale-aware navigation

Check that the project preserves locale correctly across:

- internal links
- redirects
- auth entry and return flows
- shared links
- deep links
- programmatic navigation
- language switching

The user should land on the localized equivalent of the same place, not the homepage, unless no equivalent exists.

Also audit or define the explicit locale selector itself:

- where it lives
- how the current locale is displayed
- how locale options are ordered
- whether flags are shown
- whether currency/market labels are shown when relevant
- how the selector persists an explicit choice
- how the selector indicates the currently active locale

### 7. Audit or design translation and optional display-currency layers

Check that the project has:

- one central locale registry
- one central formatting layer
- when prices are visibly exposed, one central locale -> display currency mapping
- explicit translation completeness rules
- explicit fallback behavior for missing translations

If the task is about translating locale catalogs, read `references/catalog-translation.md` and apply that workflow instead of inventing a one-off prompt.

If the product does not expose prices, skip display-currency logic entirely.

If the product exposes prices, keep display formatting separate from billing state.

For new purchases, the current locale may determine the checkout currency when the project explicitly maps locale to currency.

For existing subscriptions, keep the original billing currency stable; add-ons or additional items attached to that subscription should inherit the subscription's existing billing currency rather than switching with the current locale.

Translation content must not become the place where pricing, currency, or subscription invariants are hidden.

This skill may recommend a lightweight locale -> display currency mapping, but it must not expand by default into multi-country, multi-entity, or heavy multi-billing architecture.

### 8. Execute catalog translation when needed

When the task is to translate locale catalogs:

- start from one structurally complete reference locale
- use one orchestrator to define invariants and verification before parallelizing
- validate the workflow on a small pilot batch before full rollout
- do not use programmatic translation services, translation APIs, browser translation, or translation scripts as the source of the translated copy unless the user explicitly authorizes that trade-off
- scale through small parallel batches, not one giant all-at-once run
- in each wave, use one translator subagent per locale
- keep translation subagents on the conversation's inherited/default model settings unless the user explicitly authorizes model or reasoning overrides
- after each translation wave, use one independent evaluator subagent per locale
- never let the same agent/session generate and evaluate the same locale
- translate toward the target locale as a native speaker, not literally
- adapt formulations, references, and cultural codes so they feel natural to the target community
- preserve keys, placeholders, ICU syntax, and structural parity
- distinguish deterministic structure tooling from translation: scripts may scaffold, compare, parse, or verify catalogs, but they must not be the translator unless explicitly authorized
- accept a locale only after direct local verification confirms the file exists and passes structural checks; never accept a locale from a subagent's final message alone
- treat audit scripts as evidence, not authority: investigate any script finding that conflicts with direct runtime-safe ICU/placeholder usage before declaring the locale failed
- if a translation wave times out twice or produces no files, stop the wave, close stale subagents where possible, summarize the partial state, and re-plan before launching another wave
- finish with a verification pass for missing keys, extra keys, placeholder parity, and hardcoded user-facing strings outside the message system
- use the reusable audit scripts from this skill instead of inventing one-off checks
- treat the hardcoded-string scanner as a heuristic review aid, not as a magical blocker-free truth source
- use `references/evaluator-rubric.md` so locale acceptance is explicit rather than subjective

### 9. Audit or design language and language-variant prioritization

If the product is broad-addressable, choose languages or language variants strategically rather than translating randomly.

When doing this:

- use `references/market-selection.md`
- start from search demand and acquisition logic
- merge regional variants by default unless splitting materially improves SEO or conversion
- simplify optional display-currency complexity unless the business case justifies more

### 10. Audit cross-surface international consistency

Verify that locale logic is reused across:

- app UI
- emails
- notifications
- API messages and errors
- cron jobs and background tasks
- shared pages
- chatbot or support surfaces
- SEO metadata
- structured data

Any user-facing surface that ignores locale weakens the architecture.

### 11. Audit or design international SEO

When SEO is in scope, ensure:

- canonical URLs are self-referential and absolute
- `hreflang` clusters include the current page and all valid alternates
- `x-default` points to a real 200 page
- metadata generation is centralized
- sitemap generation is centralized
- the sitemap contains real localized pages, not fragments
- base URL resolution is centralized

Use `references/international-seo.md`.

### 12. Define the rollout and testing strategy

Treat locale behavior like business logic.

At minimum, define or audit tests for:

- locale parsing
- precedence order
- authenticated preference behavior
- anonymous preference behavior
- explicit URL precedence
- mismatch banner triggering
- dismiss behavior
- localized redirects
- fallback behavior

## Default Outputs

Depending on the user's request, produce one or more of:

- a doctrine summary
- a locale decision tree
- an audit of the current architecture
- a reusable implementation plan adapted to the project's stack
- a list of gaps and risks
- a multilingual SEO plan
- a prioritized language / language-variant launch recommendation
- a test plan for locale behavior

## Anti-Patterns

Flag these explicitly when found:

- silently redirecting away from an explicit localized URL
- collapsing display locale and preference locale into one field
- using a routing cookie as if it were an explicit language choice
- coupling translation strings and billing logic
- hardcoding currency symbols or prices in localized surfaces
- translating into many locales without a clear acquisition or market rationale
- splitting regional variants prematurely when a merged language would serve the same demand
- implementing multilingual pages while leaving emails, APIs, or shared pages unlocalized
- hand-writing `hreflang` clusters page by page
- putting `#fragment` URLs in a sitemap
- exposing incomplete locales publicly without an explicit fallback policy
- assuming browser language is the same thing as user preference

## Execution Boundary

When the user asks for analysis, stay at doctrine, audit, and implementation-plan level.

When the user explicitly asks for execution, implement the chosen architecture in the current stack while preserving the doctrine above.
