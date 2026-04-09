# Language and Locale Selection

Use this reference when the user asks:

- which languages to translate first
- whether regional variants should be merged or split
- whether locale-aware display currency should be simplified at launch
- how to reuse a multilingual SEO expansion strategy across projects

Default to language-only locale targeting.

Do not create country-specific hreflang variants just because multiple countries share the same language.

Split into region variants only when the regional language variant is materially different in a way that changes SEO relevance, CTR, conversion, legal wording, or product fit.

Example that is often justified:

- `pt-BR` vs `pt-PT`

Examples that are often not justified by default:

- `fr` split into `fr-FR`, `fr-BE`, `fr-CA`, `fr-LU`

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

Why this matters:

- it gives multilingual rollout a business reason beyond "being translated"
- it lets a business reuse strong pages across more markets
- it can accelerate international discovery relative to launching unrelated pages from zero
- it helps search engines show the correct language version rather than the wrong locale
- it reduces duplicate-content ambiguity across translated equivalents

Treat that as a practical SEO growth heuristic and rollout doctrine.
Do not present it as a guaranteed "authority transfer" promise from Google.

## 3. Default shortlist for broad-addressable products

When a product is broad-addressable and no better business-specific data exists yet, treat this as a heuristic launch shortlist rather than as product doctrine.

Use this heuristic launch shortlist of hreflang languages, in priority order:

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

## 5. Optional lightweight display-currency mapping

If the product visibly shows prices and the project explicitly wants locale-aware price display, a lightweight locale -> display currency mapping is acceptable.

This is a display-layer convenience, not a multi-country architecture.

Unless the project explicitly says otherwise:

Implications:

- changing language may change display currency too
- price symbols, acronyms, decimals, and formatting should follow locale
- active billing state must stay separate from visible price display

## 6. Launch-stage currency simplification

If the product shows prices but does not want extra display-currency complexity at launch, the default simplification is:

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
- it avoids prematurely supporting many visible currencies
- it still gives a coherent multilingual product experience

Important:

- launch-stage simplification affects display defaults only
- it must not silently mutate active billing state for already subscribed users

## 7. When not to use the default shortlist

Override the default shortlist when:

- the product is clearly local or regional
- the target market is much narrower than the shortlist
- the product depends on a language not present in the shortlist
- the product has logistics/compliance barriers in most markets
- the economics do not justify translating broadly yet

## 8. Default output for language-selection tasks

When the user asks which languages or language variants to prioritize, produce:

- the business-scope classification
- the recommended languages in priority order
- which variants are merged vs split, and why
- the optional display-currency plan when the product visibly shows prices
- the reasons to keep or override the defaults
