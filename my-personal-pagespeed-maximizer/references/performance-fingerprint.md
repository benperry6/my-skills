# Performance Fingerprint

Use this file when deciding whether a page needs:

- a full optimization loop
- a targeted re-check
- or inherited validation from an existing archetype

## What A Performance Fingerprint Is

A performance fingerprint is the set of factors that materially shape the real PageSpeed behavior of a page.

It is not the URL slug.
It is not the CMS entry ID.
It is not the article title.

It is the rendering and delivery profile that actually drives the metrics.

## The Highest-Value Fingerprint Dimensions

When comparing a new page to an already validated page type, inspect these dimensions first:

1. Template or route shell
- same page shell or not
- same layout and first-screen structure or not

2. Above-the-fold component set
- same hero structure or not
- same first-screen component order or not
- same banners, bars, popups, nav treatment, and consent runtime or not

3. Likely LCP candidate
- text block vs image vs video vs carousel vs widget
- same candidate type and delivery path or not

4. Critical media
- same image class, dimensions, compression, formats, and loading behavior or not
- same video, embed, or iframe footprint or not

5. Client/server rendering boundary
- same amount of hydration in the first viewport or not
- same client islands or interactive shells above the fold or not

6. Third-party footprint
- same trackers, consent tools, widgets, chat, ads, embeds, and experiments or not

7. Font path
- same font files, loading strategy, and render behavior or not

8. Data-fetching path
- same server delay, waterfall exposure, personalization, or blocking fetches or not

## Usually Safe To Inherit Validation

In most cases, inherited validation is reasonable when:

- the same template and first viewport structure are reused
- the same LCP candidate type is preserved
- the same scripts and font path are preserved
- the same rendering model is preserved
- only copy, metadata, body text, internal links, taxonomy, or similar content-level fields changed

This is a bias, not a proof.
If the page is strategically important, a quick targeted re-check may still be worthwhile.

## Usually Not Safe To Inherit Validation

Do not blindly inherit validation when any of these changed:

- the hero image became significantly heavier
- a video or embed entered the first viewport
- a chat widget, ad tech, consent layer, experiment framework, or analytics tool changed
- the first viewport moved from server-heavy to client-heavy rendering
- a new carousel, slider, map, or personalization layer was introduced
- the likely LCP element changed type
- the page introduced locale-specific assets or alternate font/runtime behavior

## Classification Rule

Use this rule of thumb:

- same fingerprint -> inherited validation is allowed
- mostly same fingerprint with one or two perf-sensitive deltas -> targeted re-check
- meaningfully different fingerprint -> full optimization loop

If there is real uncertainty, choose the more cautious path.

The anti-pattern is false confidence.
