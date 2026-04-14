# Internationalization Implementation Checklist

Use this before shipping multilingual behavior.

## Product Rules

- [ ] `current locale` and `preferred locale` are modeled separately
- [ ] explicit localized URL is never silently overridden
- [ ] locale resolution hierarchy is documented
- [ ] the business scope is classified as local-only, selective multi-market, or broad-addressable
- [ ] fallback policy for missing translations is explicit
- [ ] public SEO policy for incomplete locales is explicit

## Locale Registry

- [ ] one central locale registry exists
- [ ] supported locale codes are defined in one place
- [ ] planned locale codes and published locale codes are distinguished explicitly
- [ ] default locale is defined in one place
- [ ] display labels and localized language names are centralized
- [ ] any optional display-currency attributes tied to locales are centralized when used
- [ ] one source of truth defines which locale set drives routing, selectors, metadata, sitemap, mismatch UX, auth helpers, and tests

## Language and Locale Selection

- [ ] the language scope is chosen intentionally, not arbitrarily
- [ ] a broad-addressable product uses a prioritized locale shortlist or an explicit alternative
- [ ] locale strategy defaults to language-only unless a split is materially justified
- [ ] any split variants are justified by SEO, conversion, legal, or market-fit reasons
- [ ] if the product shows prices, the project states whether it uses a lightweight locale -> display currency mapping

## Translation Assets

- [ ] one reference locale is structurally complete
- [ ] other core locales stay iso-structured with the reference locale
- [ ] target catalogs are translated natively for their target language communities, not literally
- [ ] translator prompts stay minimal and task-only rather than carrying orchestration or verification boilerplate
- [ ] the default translator prompt follows the proven direct pattern, with only the target language/community and self-translation warning adapted
- [ ] large multi-locale rollout uses one orchestrator, not isolated ad hoc runs
- [ ] all requested locales are spawned in parallel by default, with one translator subagent per locale
- [ ] each translator subagent handles exactly one locale
- [ ] translator subagents inherit the parent conversation settings with no model or reasoning override unless explicitly authorized
- [ ] long-running translation waves are supervised on a measured cadence (for example every 2 to 5 minutes), not busy-polled every 30 seconds
- [ ] inactivity under 10 minutes is not treated as translator death by default
- [ ] a translator is only treated as potentially dead after more than 10 minutes with no observable activity or task progression
- [ ] missing keys are auditable
- [ ] placeholder and ICU parity are auditable
- [ ] reusable structural audit scripts are available to compare source and target catalogs
- [ ] catalog review is done by an independent evaluator agent, not by the generator itself
- [ ] each evaluator subagent reviews exactly one locale
- [ ] evaluators report findings but do not directly fix the locale they reviewed
- [ ] failed locales go through a separate correction loop before acceptance
- [ ] every corrected locale is re-evaluated before acceptance
- [ ] locale acceptance uses an explicit pass/fail rubric rather than ad hoc judgment
- [ ] locale acceptance is based on local file verification, not on a subagent final message
- [ ] the translation run records every translator/evaluator/fixer attempt with locale, phase, attempt number, agent id, status, started_at, last_observed_at, and any discoverable session/transcript path
- [ ] the run registry is updated after every spawn, recovery attempt, respawn, verification result, evaluator decision, and final acceptance
- [ ] a resumed session reloads the run registry and checks local file state before any detached subagent is treated as dead or respawned
- [ ] a resumed session applies the same 10-minute inactivity threshold to recorded observation/progress timestamps before replacing a detached agent
- [ ] the run registry reaches explicit terminal states instead of being left with stale `running` markers after the real outcome changed
- [ ] the orchestrator stays active until all translation, evaluation, and correction loops are complete
- [ ] hardcoded user-facing strings outside the message system are audited
- [ ] declared locales and translation-ready locales are tracked separately

## Preference Modeling

- [ ] authenticated users support manual preference
- [ ] authenticated users support auto-detected preference
- [ ] anonymous users have a dedicated explicit preference mechanism
- [ ] anonymous users do not confuse a technical navigation cookie with explicit preference

## Routing and Navigation

- [ ] public indexable URLs follow one explicit locale-routing doctrine
- [ ] the project states whether the default locale is prefixed or intentionally left unprefixed
- [ ] the root URL policy is explicit (`200` page, selector page, or redirect)
- [ ] localized routes are consistent
- [ ] redirects preserve locale correctly
- [ ] internal links preserve locale
- [ ] programmatic navigation preserves locale
- [ ] language switching preserves path, query string, and hash
- [ ] stale locale-prefixed URLs from unpublished or paused locales are normalized server-side to a valid published locale path
- [ ] stale locale-prefixed URLs do not produce doubled paths like `/{published-locale}/{old-locale}/...`
- [ ] one explicit locale selector exists if the product needs manual language control
- [ ] the selector is driven by a central locale registry, not a page-level hardcoded list
- [ ] the selector exposes published locales only unless the project explicitly wants to surface prelaunch locales
- [ ] selector option ordering is intentional (business/acquisition/rollout priority or an explicit alternative), not accidental
- [ ] native language names are used in the selector unless the project explicitly chooses otherwise
- [ ] flags/language markers are used only when they materially improve scanning
- [ ] currency or market labels are shown next to locale labels when locale and market are materially linked and that context helps users
- [ ] current locale is clearly identifiable in the selector trigger and menu/list
- [ ] selector clicks persist a durable explicit preference
- [ ] private or non-indexable app surfaces are excluded from sitemap targets even if they reuse localized routing

## Mismatch Banner

- [ ] mismatch logic works for authenticated users
- [ ] mismatch logic works for anonymous users
- [ ] banner copy is shown in the most understandable locale available
- [ ] title is compact and user-simple
- [ ] subtitle explicitly names both the current page language and the preferred-language signal
- [ ] language names are localized into the banner's own display language
- [ ] primary CTA creates a durable preference
- [ ] secondary CTA creates a durable preference
- [ ] secondary CTA is visually button-like, not just a plain text link, when it creates a durable preference
- [ ] visual hierarchy is primary filled CTA + secondary ghost CTA + independent close button
- [ ] close/X is session-only dismiss
- [ ] dismiss is scoped by locale pair
- [ ] mobile layout stacks actions vertically by default

## Cross-Surface Coverage

- [ ] emails use effective locale
- [ ] API messages/errors use effective locale
- [ ] background jobs use effective locale
- [ ] outbound user-facing communication uses effective locale
- [ ] shared/public pages use effective locale
- [ ] chatbot/help/support surfaces reuse central locale and formatting helpers

## Formatting

- [ ] date formatting is centralized
- [ ] number formatting is centralized
- [ ] currency formatting is centralized when prices are visibly shown
- [ ] localized language-name formatting is centralized

## Optional Pricing Display and Billing Safeguards

- [ ] if the product shows prices, launch-stage display-currency complexity is intentionally scoped
- [ ] if launch simplification is desired, the project explicitly chooses a reduced display-currency set
- [ ] locale changes do not silently mutate active subscription billing currency
- [ ] locale changes do not silently mutate active subscription price IDs
- [ ] new checkout currency selection and existing-subscription currency persistence are both explicit
- [ ] localized prices come from verified mappings or source data
- [ ] display formatting is separate from billing state

## Locale Parsing

- [ ] browser locale parsing supports composed tags
- [ ] progressively less specific tags are matched safely
- [ ] unsupported locale values degrade to the default locale

## Web Guardrails

- [ ] `<html lang>` reflects the effective locale on every localized page
- [ ] if any supported locale is RTL, `dir` is derived from the locale registry and applied correctly
- [ ] cache or CDN behavior cannot serve one locale's HTML to another locale

## SEO

- [ ] canonical URLs are self-referential and absolute
- [ ] `hreflang` includes the current page and all valid published alternates
- [ ] `x-default` points to a real 200 page
- [ ] metadata generation is centralized
- [ ] sitemap generation is centralized
- [ ] sitemap only contains real indexable localized URLs
- [ ] sitemap and alternates are generated from published locales only, not planned-but-unpublished locales
- [ ] base URL resolution is centralized
- [ ] base URL/env writes are re-read and verified after mutation
- [ ] app-production host validation and public-domain validation are run separately when a domain cutover is in scope

## Testing

- [ ] locale parsing is tested
- [ ] authenticated preference priority is tested
- [ ] anonymous preference priority is tested
- [ ] explicit URL precedence is tested
- [ ] mismatch banner triggering is tested
- [ ] banner dismiss behavior is tested
- [ ] localized redirects are tested
- [ ] fallback behavior is tested
- [ ] negative tests cover stale locale-prefixed URLs such as `/de/...` when `de` is no longer published

## Suggested commands

- `python3 ~/.agents/skills/my-personal-internationalization/scripts/verify_catalog.py --source path/to/fr.json --target path/to/en.json`
- `python3 ~/.agents/skills/my-personal-internationalization/scripts/scan_hardcoded_strings.py --root path/to/app/src`
- `python3 ~/.agents/skills/my-personal-internationalization/scripts/run_catalog_audit.py --source path/to/fr.json --target path/to/en.json --code-root path/to/app/src`
