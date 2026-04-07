# Internationalization Doctrine

This reference distills reusable multilingual product doctrine from prior real-world implementation work.

Use it when the goal is to stop rediscovering the same international architecture decisions on every new project.

## 1. Localized acquisition makes explicit URLs important

In real products, localized URLs often already encode acquisition intent:

- SEO results should land on the locale matching the query language
- ads should land on the locale matching the creative
- shared links should preserve the sender's explicit page locale

Because of that:

- explicit localized URL wins for display
- mismatch is handled with suggestion UX, not forced redirect

## 2. `current locale` and `preferred locale` are different

Do not reduce locale to one variable.

- `current locale` = the locale currently displayed in the URL/page
- `preferred locale` = the best-known language the product should suggest or use by default

This distinction is essential for mismatch handling, routing safety, and cross-surface consistency.

## 3. Preference has at least two layers

For authenticated users:

- manual preference
- auto-detected preference

Manual preference always wins.

For anonymous users, keep the same distinction conceptually:

- explicit guest preference
- passive signals such as browser language

## 4. Anonymous users need real preference handling

Guests can also arrive on the "wrong" locale through:

- shared links
- copied URLs
- search engine oddities
- ad mistakes

Therefore:

- guests also need `preferred locale` logic
- guests also need durable preference persistence
- guests also need mismatch suggestions

## 5. One cookie is not enough

There are two different concerns:

- technical navigation memory
- explicit user language preference

Do not conflate them.

A cookie written automatically because a user visited `/fr/...` is not the same as a cookie written because the user explicitly chose French.

## 6. Locale resolution needs a stable hierarchy

Reusable default order:

1. explicit locale in the URL
2. manual authenticated preference
3. auto-detected authenticated preference
4. explicit guest preference
5. browser/app language
6. default locale

Important:

- this hierarchy is for defaults, no-locale redirects, and cross-surface delivery
- it is not permission to override an explicit localized URL

## 7. The mismatch banner is a suggestion layer

The banner reconciles:

- explicit URL locale
- best-known user preference

It should be:

- non-blocking
- shown to authenticated and anonymous users
- written in the language most likely to be understood
- dismissed by locale pair and session when closed

Interpret the actions like this:

- `Switch to X` = durable preference for `X`
- `Stay in Y` = durable preference for `Y`
- `Close` = not now

## 8. Banner wording should stay user-simple

Prefer wording about the language experience, not storage mechanics.

Better:

- `Switch to Italian`
- `Stay in French`

Worse:

- `Change my profile locale`
- `Persist this device preference`

The user-facing wording should be simple even if the underlying persistence differs by auth state.

## 9. Reuse one validated mismatch-banner UX pattern by default

Unless a project already validated a better alternative, reuse the same core mismatch-banner pattern across projects instead of redesigning it from zero each time.

### Copy structure

Use:

- a compact title
- then a short two-sentence subtitle

The subtitle should always do both:

- say what language the current page is in
- say why the product suggests another language

Recommended reusable wording shape:

- title: `Switch to {preferredLanguageName}?`
- browser subtitle: `This page is in {currentLanguageName}. Your browser prefers {preferredLanguageName}.`
- account subtitle: `This page is in {currentLanguageName}. Your account is set to {preferredLanguageName}.`
- guest-preference subtitle: `This page is in {currentLanguageName}. You usually browse in {preferredLanguageName}.`
- fallback subtitle: `This page is in {currentLanguageName}. Also available in {preferredLanguageName}.`
- primary CTA: `Switch to {preferredLanguageName}`
- secondary CTA: `Stay in {currentLanguageName}`

Important:

- localize `currentLanguageName` and `preferredLanguageName` into the banner's own display language
- prefer short, direct wording over explanatory prose
- do not expose storage jargon such as profile, cookie, localStorage, or device preference in the CTA labels unless the project explicitly wants that

### Visual hierarchy

Default reusable hierarchy:

- primary filled CTA = switch to suggested language
- secondary ghost/outline CTA = stay in current language
- close/X = independent dismiss control

Do not style the secondary action like a plain text link if it creates a durable preference.
If both main actions are product-significant, both should read as buttons, even if only one is visually dominant.

### Responsive layout

Default reusable layout:

- close button at top-right, independent from action row
- text block first
- action block second
- mobile: stack actions vertically
- desktop: horizontal layout is acceptable if space allows

### Visual restraint

Use language markers, such as flag emojis or locale chips, with restraint.

Recommended default:

- allowed inside CTA labels
- optional in subtitle
- avoid repeating them in title, subtitle, and buttons all at once

The goal is immediate comprehension, not decorative multilingual noise.

## 10. Language and market are separate layers

Translation is one layer.
Market behavior is another.

Locale-dependent market behavior may include:

- currency
- number/date formatting
- legal wording
- price IDs
- subscription or catalog availability

Keep these rules in central helpers/configuration, not buried inside translation strings.

## 11. Translation catalogs are infrastructure

Reusable rules:

- maintain one structurally complete reference locale
- keep other key locales iso-structured with that reference
- translate target catalogs natively for the target language community, not literally
- audit missing keys
- audit placeholder and ICU parity
- eliminate hardcoded user-facing strings outside the message system

Hardcoded strings often survive in:

- legal pages
- onboarding edge cases
- emails
- shared pages
- chatbot flows

When the task is to translate catalogs, treat it as architecture work, not as standalone copywriting.
The translation pass should always be followed by a codebase audit for remaining hardcoded user-facing strings.
For multi-locale translation campaigns, separate generator and evaluator responsibilities so the same agent does not grade its own output.

## 12. Locale support and translation readiness are separate

A product may declare many locale codes for routing and future growth while only a subset is translation-ready today.

Track those separately.

This enables:

- explicit fallback policy
- safe prelaunch development
- clean public SEO exposure decisions

## 13. Fallback behavior must be deliberate

If a locale exists in routing but its content is not fully translated, the product must choose deliberately between:

- strict/public mode: do not expose it publicly yet
- development/prelaunch mode: keep the locale in the URL but load a controlled fallback

Do not let this happen accidentally.

## 14. Formatting must be centralized

Use shared helpers for:

- prices
- currency symbols
- dates
- numbers
- localized language names

Do not let every surface improvise its own formatting logic.

## 15. Billing invariants survive language changes

Critical rule for subscription products:

- a user may switch language freely
- that must not silently rewrite active billing currency
- that must not silently rewrite active subscription price IDs

Localized display and billing state are related, but they are not interchangeable.

## 16. Price display must come from verified sources

Do not infer localized pricing from:

- locale suffixes
- string naming conventions
- duplicated hardcoded values

Use:

- verified source mappings
- central locale -> market -> formatting helpers
- tests or verification scripts when billing complexity grows

## 17. Composite locale parsing is not optional

Locale negotiation must handle tags like:

- `pt-BR`
- `pt-PT`
- `zh-Hant-TW`

Use progressive fallback from the most specific tag to less specific supported tags.

## 18. Internationalization is not UI-only

Every user-facing surface should reuse effective-locale logic:

- app UI
- shared/public pages
- API errors
- emails
- background jobs
- chatbot/help surfaces
- structured data
- SEO metadata

If one of these surfaces is still hardcoded, the architecture is incomplete.

## 19. International SEO needs factories, not repetition

The scalable pattern is:

- central locale registry
- central public-route registry
- metadata factory
- dynamic sitemap generation

This guarantees:

- self-referential canonical URLs
- full `hreflang` clusters including self
- a valid `x-default`
- real localized sitemap entries

## 20. Base URL must be centralized

Do not scatter the production domain across:

- metadata
- `hreflang`
- sitemap
- emails
- structured data
- redirects

Resolve the base URL centrally from configuration or runtime context.

## 20. Default business bias: one market = one language = one currency

Unless the project explicitly says otherwise, assume:

- one market
- one language
- one currency

This means language switching normally also changes:

- display currency
- symbol or acronym
- decimal formatting
- localized market wording

This is an operational default, not a universal law.

## 21. Broad-addressable products should choose locales strategically

For products with broad international demand, language coverage should be chosen from:

- real search-demand logic
- acquisition logic
- business fit

Do not translate randomly.

Use a prioritized launch shortlist and adapt it when the business is narrower or different.

## 22. Merge variants by default, split only when justified

Regional language variants should be merged by default unless a split materially improves:

- search demand coverage
- SERP relevance
- CTR
- conversion
- legal or market fit

If in doubt, merge.

## 23. Launch-stage currency complexity should stay low by default

If the project does not explicitly require many billing currencies at launch, prefer a simplified display-currency strategy first.

The reusable default is:

- keep launch display currencies to a minimal set
- centralize locale -> market -> currency mapping
- defer extra billing-currency complexity until there is a proven business reason

## 24. Locale logic must be tested as business logic

At minimum, test:

- locale parsing
- precedence order
- authenticated preference behavior
- anonymous preference behavior
- explicit URL precedence
- mismatch banner logic
- dismiss behavior
- localized redirects
- fallback behavior
