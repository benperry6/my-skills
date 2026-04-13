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

Treat `planned locales` and `published locales` as separate concepts:

- planned locales = known or intended locale codes for future rollout
- published locales = locales that are truly translated and ready to be exposed in runtime and SEO

Only published locales should feed public SEO surfaces.

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

For SEO-oriented websites and web apps, the default routing doctrine is:

- explicit locale-prefixed public URLs
- the default locale is also prefixed unless the project explicitly chooses otherwise
- `/` may negotiate and redirect, but if it does, `x-default` must point to a real 200 page rather than to `/`
- public indexable pages use centralized metadata generation and centralized sitemap generation
- private or non-indexable app surfaces are not sitemap targets, even if they reuse the same locale-prefixed routing pattern

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

It also prevents a real-world failure mode:

- routing or SEO code reading from the full planned locale list while the product is only ready to expose a smaller published subset

## 7. Sitemaps should be generated from real route data

Preferred pattern:

- `public routes × supported locales`
- optionally extended by dynamic content sources

In partial rollouts, read `supported locales` here as the published locale set, not the full planned locale set.

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

For partial launches, make this operationally concrete:

- selectors expose published locales only
- `hreflang` enumerates published locales only
- sitemap enumerates published locales only
- metadata factories derive alternates from published locales only

## 11. Root redirect behavior is a tradeoff, not a free win

If `/` negotiates locale and redirects:

- it can be acceptable operationally
- but it is not the cleanest SEO surface

Prefer real 200 content pages for canonicalized, `x-default`, and sitemap targets.

## 12. Stale locale URLs from earlier rollout states need deliberate handling

If a locale was previously exposed, linked, tested publicly, or simply existed in a broader planned-locale registry, stale URLs such as `/de/...` may survive in bookmarks, crawlers, logs, emails, or internal links.

Do not leave these to accidental router behavior.

Handle them deliberately:

- detect known-but-unpublished locale prefixes
- strip the stale locale prefix first
- rebuild the path under the best published locale
- do this server-side before the i18n router creates further redirects

The failure mode to avoid is a malformed redirect like `/{published-locale}/{old-locale}/...`.

## 13. Localized HTML attributes should be explicit

Set `<html lang>` from the effective locale on every localized page.

If any supported locale is RTL, derive `dir` from the locale registry and apply `rtl` only for those locales.

## 14. Cache behavior must not leak locales

Do not let a cache or CDN serve one locale's HTML to another locale.

If locale negotiation depends on request signals, ensure the cache strategy preserves locale correctness instead of collapsing multiple locales into one cached HTML response.

## 15. App-production verification and public-domain verification are separate

When a project uses both a deployment host and a public custom domain, verify both independently.

Do not assume that:

- a successful production deployment
- or a successful alias operation

means the public domain already serves the same origin.

Check separately:

- the app/deployment host behavior
- the public custom-domain behavior
- the real DNS/origin path when a cutover is involved

Likewise, after changing a base-URL environment variable, re-read the effective value instead of trusting the write command alone.
