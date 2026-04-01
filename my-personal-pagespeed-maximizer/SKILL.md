---
name: my-personal-pagespeed-maximizer
description: "[My Personal Skill] Use when a page, page type, or template must be pushed as close as possible to its practical maximum on Google PageSpeed Insights without unauthorized visual regressions. Trigger for new landing pages, new page archetypes, major template or above-the-fold changes, Core Web Vitals regressions, or when deciding whether a new page instance needs a full optimization loop or can inherit a previously validated template."
---

# My Personal PageSpeed Maximizer

## Overview

This skill turns PageSpeed optimization into a repeatable operating model instead of an ad hoc perf sweep.

Its job is to decide whether a page needs a full optimization loop, a lighter targeted re-check, or no full rerun at all, then push the page as close as possible to its practical maximum on Google PageSpeed Insights under the approved product and UX constraints.

## Required Inputs

Before running the optimization loop, make sure these inputs exist or can be verified:

- a real target URL, preview URL, or other directly testable page address
- enough access to load the real page variant that matters
- the current approval boundary for visible vs invisible changes
- enough context to know whether this is a new archetype, a meaningful variant, or a content-only instance

If the page cannot be measured for real, do not pretend to optimize it. Stop at diagnostics about what is missing.

## Use This Skill When

Use this skill when the user wants any variation of:

- "Optimize this page as much as possible for PageSpeed Insights"
- "Push this landing page to the max on performance"
- "Improve Core Web Vitals on this page"
- "Check whether this new page type needs a full perf pass"
- "A template was changed and I want to know if perf needs to be re-validated"
- "We have a PageSpeed regression"

Typical triggers:

- a new landing page, pricing page, blog template, homepage, sales page, or other new page archetype
- a major change to a page shell or above-the-fold composition
- a change to hero media, embeds, scripts, fonts, or first-viewport runtime behavior on an existing template
- a reported PageSpeed / Core Web Vitals regression
- a request to determine whether a content-only page can inherit a previously validated template

Do not use this skill for:

- a broad SEO audit that is not primarily about performance
- a pure visual redesign
- a content-only page instance that clearly inherits an already validated performance fingerprint with no material perf-sensitive differences
- speculative advice about performance without measuring the real page first

## Core Doctrine

This skill is deliberately strict.

Its default doctrine is:

1. Google PageSpeed Insights is the primary scorecard and diagnostic engine.
2. Prefer the dedicated PageSpeed MCP or other programmatic access first. Do not default to browser testing when the PageSpeed programmatic path should work.
3. Optimize for mobile first. Desktop matters, but mobile is the default optimization target.
4. "Green" is not enough. The target is the practical maximum, not mere compliance.
5. Do not change the user-visible design without explicit user approval. Invisible technical changes are fair game; visible changes are approval-gated.
6. Optimize page archetypes, not every URL blindly.
7. Treat PageSpeed recommendations as testable hypotheses, not automatic truths.
8. Keep only changes that improve the observed result. Revert or reject regressions even if the technique sounded correct in theory.
9. Stop only when no material gain remains, the remaining gains require unapproved visual changes, or the remaining opportunities are blocked by hard product constraints.

## Universality Rule

This skill must stay framework-agnostic by default.

It should reason in terms of:

- LCP candidate
- above-the-fold media
- script and style loading
- runtime work in the first viewport
- third-party overhead
- server delay and network path
- layout stability

It should not anchor its reasoning to one framework, one bundler, or one rendering model unless the current repo explicitly requires that translation.

When a framework-specific idea becomes relevant, express the generic performance problem first, then map it to the local implementation details.

## Decision Gate Before The Optimization Loop

Before touching code, classify the page into one of these three modes.

### Mode A - Full Archetype Optimization

Use a full optimization loop when the page introduces a genuinely new performance archetype.

Common signals:

- new page template or route shell
- new above-the-fold component composition
- different first-viewport rendering model or runtime behavior
- different LCP candidate type such as text hero vs image hero vs video hero
- major refactor of layout, data fetching, runtime behavior, or asset loading strategy

### Mode B - Targeted Variant Re-check

Use a lighter targeted re-check when the page reuses an existing archetype but introduces a perf-sensitive delta.

Common signals:

- heavier or different hero media
- new embeds, widgets, ads, consent surfaces, or third-party scripts
- altered font loading or tracking stack
- a changed first-screen component order
- an A/B variant that materially changes the first viewport

### Mode C - Inherit Prior Validation

Skip the full optimization loop when the page is only a content instance of an already validated archetype and its performance fingerprint still matches.

Common signals:

- same shell, same first viewport structure, same scripts, same font path, same LCP candidate type
- only copy, metadata, internal links, taxonomy, or body content changed
- no meaningful change to first-load assets or first-viewport runtime work

If the classification is uncertain, do not blindly skip. Default to at least a targeted re-check.

For the detailed fingerprint rules, read `references/performance-fingerprint.md`.
For the actual skip and inheritance policy, read `references/validation-policy.md`.

## Validation Inheritance Policy

Mode C is allowed only when all of these are true:

1. a prior validated page already exists for the same archetype
2. that prior validation is still relevant to the current shell and asset path
3. the new page does not introduce a meaningful perf-sensitive delta
4. the page is not a critical page that requires a direct guard check by default

If one of these is false or unknown, do not inherit blindly.

### Mandatory Full Re-Run Cases

A full optimization loop is mandatory when at least one of these is true:

- there is no prior validated archetype to inherit from
- the page introduces a new shell, new first-screen composition, or new LCP candidate type
- the route/template changed in a way that likely alters the first-load path
- the page introduces new third-party tooling in or near first load
- the prior validation is too stale or no longer trustworthy after major template evolution
- the page is launch-critical and there is no recent direct evidence on a materially equivalent page

### Mandatory Targeted Re-Check Cases

Do at least a targeted re-check when the archetype seems reusable but one of these is true:

- hero media changed materially in size, type, or delivery path
- the first viewport runtime burden changed
- consent, analytics, widgets, embeds, ads, or experiments changed
- locale, personalization, or audience-specific variants may alter early assets or runtime
- the page is a top-traffic, top-revenue, or launch-critical URL
- confidence in inheritance is moderate rather than high

### Safe Inheritance Cases

Inherited validation is reasonable when all of these are true:

- the shell and first viewport are materially the same
- the likely LCP candidate type is the same
- early assets and third-party footprint are materially the same
- the runtime burden in the first viewport is materially the same
- the prior validation is recent enough to remain credible
- the page is not a critical page that requires a direct guard check by default

### Cheap Guard Check Rule

Even when inheritance is allowed, a cheap guard check is mandatory by default for:

- homepage variants
- money pages
- launch pages
- pages expected to receive meaningful paid or PR traffic
- pages whose failure cost is high even if the archetype looks reused

A cheap guard check is not a full loop. It is a low-cost confirmation that the inherited confidence was justified.

If one of these critical-page conditions is true, do not conclude with pure inherited validation alone. Conclude with inherited validation plus mandatory guard check, or escalate further if the page looks noisy.

## Canonical Optimization Loop

### 1. Establish the Baseline

- run Google PageSpeed Insights on the real target URL
- collect mobile results first, then desktop if helpful
- identify the current LCP candidate, the major diagnostics, and the strongest bottleneck family
- distinguish clearly between observed metrics and inferred causes

Never say a page is optimized without fresh evidence.

### 2. Lock The Constraint Boundary

State what is allowed before optimization begins:

- invisible technical changes: allowed by default
- visible UX or design changes: require explicit approval
- business or product constraints that cannot be broken

If the current bottleneck can only be solved through a visible change, stop and ask before proceeding.

### 3. Translate Diagnostics Into Changes

Prefer interventions in roughly this order:

1. LCP candidate visibility and delivery
2. above-the-fold media and asset loading
3. render-blocking fonts, CSS, and JS
4. first-viewport runtime and bundle pressure
5. third-party scripts and consent/runtime overhead
6. data-fetching waterfalls and server delays
7. CLS sources
8. remaining JavaScript and bundle waste

For common diagnostic-to-action mappings, read `references/diagnostic-playbook.md`.

### 4. Change One Family At A Time

Do not mix five theories into one opaque batch if they cannot be evaluated separately.

Make narrow, explainable changes whenever possible:

- one family of LCP fixes
- one family of third-party deferrals
- one family of bundle reductions
- one family of layout-shift corrections

This preserves attribution and avoids noisy "it got better or worse but we do not know why" results.

### 5. Re-Test After Each Meaningful Batch

After each meaningful change family:

- re-run PageSpeed Insights
- compare the actual metrics
- keep the change only if the evidence justifies it

Important:

- never assume lazy loading, preconnects, font-loading changes, code splitting, or any other common pattern is automatically beneficial
- if the metric worsens, treat that as a failed hypothesis and undo or avoid institutionalizing it

### 6. Continue Until The Residual Opportunity Is Truly Small

The loop continues while there is still a meaningful, technically plausible, evidence-backed gain left to pursue.

The loop ends when:

- the strongest bottlenecks have been addressed
- the remaining improvements are marginal
- the remaining path requires an unapproved visual change
- the page is at its practical ceiling for the current constraints

### 7. Persist Durable Learning Carefully

If the repo already uses a performance memory file such as `.agents/performance-memory.md`, persist only verified learnings.

Good examples of durable learning:

- "Animating or hiding the LCP element delayed first meaningful paint on this archetype"
- "A proposed optimization worsened TBT in real PSI tests and was reverted"
- "This template can inherit validation unless hero media or third-party scripts change"

Do not persist one-off noise, vague intuitions, or techniques that were not proven on a real measured page.

## High-Value Non-Negotiables

These rules should be enforced every time the skill runs:

- never optimize blindly without a real PageSpeed baseline
- never claim "done" without a fresh measured result
- never hide or delay the likely LCP element on first paint without a very strong reason
- never trust a perf trick just because it is fashionable
- never spend a full optimization loop on every CMS page instance if the validated archetype already covers it
- never skip a page that changed its performance fingerprint in a meaningful way

## Output Contract

When this skill finishes, it should provide:

1. the chosen mode: full optimization, targeted re-check, or inherited validation
2. the reason for that classification
3. whether a mandatory guard check applied because the page is critical
4. the baseline metrics and top diagnostics
5. the changes applied or proposed, grouped by bottleneck family
6. the post-change evidence
7. the remaining constraints or residual bottlenecks
8. a final statement of whether the page is at its current practical ceiling

## Adjacent Skills

- For broader technical SEO questions beyond performance, use `seo-audit`.
- For tracking, consent, or vendor-script decisions that materially affect performance, `analytics-tracking` may be relevant as a companion skill.
