# Validation Policy

Use this file when deciding whether a page can inherit prior performance validation or must be measured again.

Its role is to stop two bad behaviors:

- wasting time on a full loop for every page instance
- skipping pages that only look similar but are no longer safe to inherit

## The Priority Order

Always apply the decision rules in this order:

1. Full optimization required
2. Targeted re-check required
3. Inherited validation allowed

Do not start from "can I skip?" and work backward.
Start from the strictest gate and relax only when the evidence justifies it.

## Rule 1 - Full Optimization Required

A full optimization loop is required when any of these is true:

- no trustworthy prior validated archetype exists
- the current page introduces a new shell or new first-screen composition
- the likely LCP candidate changed type
- the first-load asset path changed materially
- the third-party footprint changed materially
- the runtime burden of the first viewport changed materially
- a major template refactor happened after the last trusted validation
- the current page is strategically important and there is no recent evidence on an equivalent page

This is the anti-false-confidence rule.

## Rule 2 - Targeted Re-Check Required

Use a targeted re-check when inheritance looks plausible but confidence is not high enough for a clean skip.

Common triggers:

- different hero image size, format, or delivery path
- a video, embed, map, widget, or experiment touches the first viewport
- locale or audience variants may change assets, runtime, or personalization
- tracking, consent, chat, or ads changed
- the template is shared but one part of the first viewport changed in a meaningful way
- the page is top-traffic, high-intent, launch-critical, or revenue-critical

The targeted re-check exists to validate the risky delta without paying for a full exploration loop unless needed.

## Rule 3 - Inherited Validation Allowed

Inherited validation is allowed only when all of these are true:

- the page belongs to a previously validated archetype
- the current shell and first viewport materially match the trusted reference page
- the likely LCP candidate type is unchanged
- early assets and third-party footprint are materially unchanged
- first-viewport runtime burden is materially unchanged
- the prior validation is still recent enough to remain credible
- the page is not a critical page that requires direct confirmation by default

If one of these is weak or unknown, fall back to a targeted re-check.

## What "Recent Enough" Means

This skill should not hardcode a universal number of days.

Instead, evaluate recency by change exposure:

- if the shared template, shell, asset path, or third-party layer changed since the last validation, the old validation is no longer recent enough
- if the archetype remained materially stable, the last validation stays credible for longer

Recency here is structural, not just calendar-based.

## Critical Page Definitions

Apply these definitions literally unless the user explicitly overrides them.

### Critical Page

A page is critical if at least one of these is true:

- it is a homepage or main market entry page
- it is a money page
- it is a launch page
- it is expected to absorb meaningful paid, PR, partner, or campaign traffic soon
- its failure would create a high business cost relative to an ordinary content page

If there is real doubt, bias toward classifying the page as critical until clarified.

### Money Page

A money page is any page whose primary purpose is to create, capture, or accelerate revenue.

Typical examples:

- pricing pages
- sales pages
- signup or trial-start pages
- checkout or payment pages
- lead-capture pages tied to revenue intent
- demo request pages
- upgrade, paywall, or plan-selection pages
- high-intent comparison or product pages that sit close to conversion

Not every product page is automatically a money page.
The test is whether the page is materially part of the revenue path, not whether it merely mentions the product.

### Homepage

A homepage is the main default entry page for the site, product, or market segment being optimized.

This usually includes:

- the root homepage
- a locale homepage that functions as a primary market entry page
- a campaign-specific replacement homepage if it temporarily becomes the main entry experience

### Launch Page

A launch page is any page expected to receive concentrated attention in a bounded launch window.

Typical examples:

- a page tied to a product launch
- a page tied to a PR push
- a page tied to an email blast
- a page tied to a paid campaign rollout
- a page tied to a partnership or affiliate push

The test is not the URL name.
The test is whether the page is about to receive concentrated important traffic where a missed regression would be costly.

### High Failure Cost

A page has high failure cost when a performance regression would cause outsized business harm compared with an ordinary informational page.

Typical examples:

- revenue loss
- lead loss
- launch underperformance
- wasted paid spend
- broken first impression on a flagship entry page

When high failure cost is plausible, default toward guard checking rather than pure inheritance.

## Critical Pages And Cheap Guard Check

Even when inherited validation is otherwise allowed, a cheap guard check is mandatory by default for:

- homepage variants
- launch pages
- key commercial pages
- URLs expected to absorb meaningful traffic quickly
- URLs whose failure cost is high even if the archetype looks reused

A cheap guard check is intentionally small:

- confirm the target page loads correctly
- run a lightweight PageSpeed confirmation on the real page
- verify that no obvious diagnostic family regressed

If the guard check looks noisy or suspicious, escalate to a targeted re-check.

For the detailed execution protocol, read `cheap-guard-check.md`.

Important:

- critical pages may inherit an archetype, but they do not inherit the right to skip direct confirmation
- on these pages, the minimum acceptable outcome is `inherited validation allowed` plus a passed cheap guard check
- if the cheap guard check cannot be run, do not pretend the inheritance is enough

## Decision Output

Every decision should end with one of these explicit statements:

- `full optimization required`
- `targeted re-check required`
- `inherited validation allowed`
- `inherited validation allowed, mandatory guard check required`

And it should always state why.
