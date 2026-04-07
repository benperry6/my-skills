# Language and Market Selection

Use this reference when the user asks:

- which languages to translate first
- which markets to prioritize
- whether regional variants should be merged or split
- how to simplify currencies at launch
- how to reuse a multilingual SEO expansion strategy across projects

## 1. Start from business scope, not from translation enthusiasm

First classify the project:

- `local-only`:
  one country, one language, one fulfillment or legal perimeter
- `selective multi-market`:
  several targeted countries or languages, but not broad global intent
- `broad-addressable`:
  the offer can plausibly attract search demand across many countries and languages

Only broad-addressable products should default to an aggressive multilingual SEO rollout.

Examples that are often broad-addressable:

- SaaS
- digital tools
- info products
- broad affiliate content
- non-country-specific marketplaces

Examples that are often not broad-addressable by default:

- highly local ecommerce
- country-specific services
- regulation-bound offers
- logistics-constrained physical products

## 2. Working SEO thesis for multilingual expansion

Operationally, this skill assumes the following:

- correct localized equivalents plus correct `hreflang` help search engines understand that multiple pages are the right language versions of the same underlying topic
- this often helps translated pages gain international visibility faster than if they were launched in total isolation

Treat that as a practical SEO growth heuristic and rollout doctrine.
Do not present it as a guaranteed "authority transfer" promise from Google.

## 3. Default shortlist for broad-addressable products

When a product is broad-addressable and no project-specific research says otherwise, use this as the default launch shortlist of hreflang languages, in priority order:

1. `en`
2. `de`
3. `ja`
4. `pt-BR`
5. `it`
6. `fr`
7. `hi`
8. `es`
9. `pl`
10. `ru`
11. `tr`
12. `th`
13. `ko`
14. `nl`
15. `zh-Hant`
16. `id`
17. `vi`
18. `hu`
19. `el`
20. `pt-PT`

Then add:

- `x-default` for SEO routing logic

This list is:

- a strong default starting point
- not a universal rule
- meant for broad-addressable products
- meant to be adapted when the real audience, logistics, compliance, or offer fit says otherwise

## 4. Merge-vs-split rule for language variants

Default rule:

- merge by default
- split only when the difference materially changes SEO or business outcomes

Use simple language codes unless a regional split is justified.

### Split only if one or more of these are true

- the usual keywords differ enough to change search demand
- the phrasing or conventions materially change SERP relevance
- orthography, script, or register materially affects CTR
- local expectations materially affect conversion
- a different variant is needed for legal, catalog, or market-fit reasons

### Merge if these are true

- main queries are close enough
- intent is effectively the same
- orthography differences are minor
- expected SEO or conversion lift from splitting is negligible

If you are unsure, merge.

## 5. Default business bias for market coupling

Unless the project explicitly says otherwise, assume:

- one market = one language = one currency

This is an operational simplification, not a universal law.

Implications:

- changing language normally changes display currency too
- price symbols, acronyms, decimals, and formatting must follow locale
- market copy and legal phrasing should stay aligned with the selected locale

## 6. Launch-stage currency simplification

If the product does not want multi-currency complexity at launch, the default simplification is:

- support only `USD` and `EUR`

Use this default mapping for the shortlist above unless the project explicitly says otherwise:

- `en` -> `USD`
- `de` -> `EUR`
- `ja` -> `USD`
- `pt-BR` -> `USD`
- `it` -> `EUR`
- `fr` -> `EUR`
- `hi` -> `USD`
- `es` -> `USD`
- `pl` -> `EUR`
- `ru` -> `USD`
- `tr` -> `USD`
- `th` -> `USD`
- `ko` -> `USD`
- `nl` -> `EUR`
- `zh-Hant` -> `USD`
- `id` -> `USD`
- `vi` -> `USD`
- `hu` -> `EUR`
- `el` -> `EUR`
- `pt-PT` -> `EUR`

Why this exists:

- it keeps launch complexity low
- it avoids prematurely supporting many billing currencies
- it still gives a coherent multilingual product experience

Important:

- launch-stage simplification affects display and market defaults
- it must not silently mutate active billing state for already subscribed users

## 7. When not to use the default shortlist

Override the default shortlist when:

- the product is clearly local or regional
- the target market is much narrower than the shortlist
- the product depends on a language not present in the shortlist
- the product has logistics/compliance barriers in most markets
- the economics do not justify translating broadly yet

## 8. Default output for market-selection tasks

When the user asks which languages/markets to prioritize, produce:

- the business-scope classification
- the recommended languages in priority order
- which variants are merged vs split, and why
- the default currency plan
- the reasons to keep or override the defaults
