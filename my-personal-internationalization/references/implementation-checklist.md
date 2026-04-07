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
- [ ] default locale is defined in one place
- [ ] display labels and localized language names are centralized
- [ ] market attributes tied to locales are centralized

## Market and Locale Selection

- [ ] the language/market scope is chosen intentionally, not arbitrarily
- [ ] a broad-addressable product uses a prioritized locale shortlist or an explicit alternative
- [ ] regional variants are merged by default unless a split is materially justified
- [ ] any split variants are justified by SEO, conversion, legal, or market-fit reasons
- [ ] the project states whether it follows the default bias `one market = one language = one currency`

## Translation Assets

- [ ] one reference locale is structurally complete
- [ ] other core locales stay iso-structured with the reference locale
- [ ] target catalogs are translated natively for their target language communities, not literally
- [ ] missing keys are auditable
- [ ] placeholder and ICU parity are auditable
- [ ] hardcoded user-facing strings outside the message system are audited
- [ ] declared locales and translation-ready locales are tracked separately

## Preference Modeling

- [ ] authenticated users support manual preference
- [ ] authenticated users support auto-detected preference
- [ ] anonymous users have a dedicated explicit preference mechanism
- [ ] anonymous users do not confuse a technical navigation cookie with explicit preference

## Routing and Navigation

- [ ] localized routes are consistent
- [ ] redirects preserve locale correctly
- [ ] internal links preserve locale
- [ ] programmatic navigation preserves locale
- [ ] language switching preserves path, query string, and hash

## Mismatch Banner

- [ ] mismatch logic works for authenticated users
- [ ] mismatch logic works for anonymous users
- [ ] banner copy is shown in the most understandable locale available
- [ ] primary CTA creates a durable preference
- [ ] secondary CTA creates a durable preference
- [ ] close/X is session-only dismiss
- [ ] dismiss is scoped by locale pair

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
- [ ] currency formatting is centralized
- [ ] localized language-name formatting is centralized

## Pricing and Billing

- [ ] launch-stage display-currency complexity is intentionally scoped
- [ ] if launch simplification is desired, the project explicitly chooses a reduced display-currency set
- [ ] locale changes do not silently mutate active subscription billing currency
- [ ] locale changes do not silently mutate active subscription price IDs
- [ ] localized prices come from verified mappings or source data
- [ ] display formatting is separate from billing state

## Locale Parsing

- [ ] browser locale parsing supports composed tags
- [ ] progressively less specific tags are matched safely
- [ ] unsupported locale values degrade to the default locale

## SEO

- [ ] canonical URLs are self-referential and absolute
- [ ] `hreflang` includes the current page and all valid alternates
- [ ] `x-default` points to a real 200 page
- [ ] metadata generation is centralized
- [ ] sitemap generation is centralized
- [ ] sitemap only contains real indexable localized URLs
- [ ] base URL resolution is centralized

## Testing

- [ ] locale parsing is tested
- [ ] authenticated preference priority is tested
- [ ] anonymous preference priority is tested
- [ ] explicit URL precedence is tested
- [ ] mismatch banner triggering is tested
- [ ] banner dismiss behavior is tested
- [ ] localized redirects are tested
- [ ] fallback behavior is tested
