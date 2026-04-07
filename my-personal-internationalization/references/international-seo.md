# International SEO

Use this reference when the international architecture touches crawlability, indexation, or localized acquisition.

## 1. Separate multilingual SEO from generic SEO

International SEO is not just "add translations".

It must coordinate:

- localized URLs
- canonical URLs
- `hreflang`
- `x-default`
- localized sitemaps
- route inventories
- base URL resolution

## 2. Explicit locale URLs are the stable default

When localized acquisition matters, use stable locale-specific URLs for indexable pages.

Examples:

- `/en/...`
- `/fr/...`
- `/pt-br/...`

This supports:

- query-language matching in search
- ad and affiliate landing-page consistency
- shareable locale-specific URLs

## 3. Canonical URLs must be absolute and self-referential

For each localized page:

- canonical points to that exact localized page
- not to another locale
- not to a generic root page

Do not canonicalize French pages to English pages.

## 4. `hreflang` clusters must include self

Every indexable localized page must link to:

- itself
- every valid alternate locale
- `x-default` when applicable

Do not omit the current locale from the cluster.

## 5. `x-default` must point to a real 200 page

If the product has no language selector page:

- point `x-default` to a real default-locale content page
- do not point it to a redirect-only root URL

If the root URL performs locale negotiation and returns a redirect, do not use it for `x-default`.

## 6. Use a metadata factory, not page-by-page repetition

The scalable pattern is:

- central locale registry
- central public-route registry
- shared metadata factory

This reduces:

- missing alternates
- inconsistent canonicals
- stale or partial locale coverage

## 7. Sitemaps should be generated from real route data

Preferred pattern:

- `public routes × supported locales`
- optionally extended by dynamic content sources

Do not hardcode multilingual sitemaps page by page unless the site is tiny and stable.

## 8. Sitemaps must contain real pages, not fragments

Never include:

- `#faq`
- `#pricing`
- anchor-only URLs

Only real indexable localized pages belong in the sitemap.

## 9. Base URL must be centralized

All localized SEO surfaces should derive from the same base-URL resolver:

- canonical
- `hreflang`
- sitemap
- structured data
- redirects

Do not scatter production domains in multiple helpers or pages.

## 10. Incomplete locales need an explicit SEO policy

If a locale exists in routing but is not fully translated, choose explicitly:

- keep it out of public SEO until ready
- or expose it knowingly with a controlled fallback during prelaunch

Do not accidentally index incomplete locales.

## 11. Root redirect behavior is a tradeoff, not a free win

If `/` negotiates locale and redirects:

- it can be acceptable operationally
- but it is not the cleanest SEO surface

Prefer real 200 content pages for canonicalized, `x-default`, and sitemap targets.
