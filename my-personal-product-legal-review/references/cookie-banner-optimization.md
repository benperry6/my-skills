# Cookie Banner Optimization

Use this file when the legal review touches a cookie banner, CMP, consent layer, or tracking-choice surface.

This is the concise operational layer.
The preserved long-form research source lives in:

- `references/cookie-banner-deep-research-report.md`

## What this surface is

A cookie banner is not just a legal notice.

It is simultaneously:

- a compliance surface
- a conversion-friction surface
- a measurement gate
- a performance risk surface
- a mobile and accessibility surface

Review it end-to-end, not as isolated copy.

## The baseline recommendation

Unless the real product context strongly suggests otherwise, the default baseline is:

- bottom placement first
- short first layer
- three visible choices on the first layer:
  - accept all
  - reject all
  - settings / manage choices
- category-first preference center
- symmetric primary choices
- persistent re-open path later

This is the default optimization starting point, not a universal law.

## Primary goals

Optimize for all of these together:

1. valid and understandable consent
2. maximum useful consent without manipulative steering
3. minimum friction at entry
4. measurement quality that reflects the real consent state
5. minimal performance damage
6. strong mobile usability and accessibility

## First-layer review checklist

Check:

- Does the banner actually appear in the real product?
- Does it show immediately enough for the real tracking flow?
- Are accept and reject equally visible and equally easy to click?
- Is settings visible without hunting?
- Is the copy short enough to scan quickly on mobile?
- Does the layout avoid covering essential UI or blocking reading more than necessary?
- Does it avoid fake urgency, fake recommendations, or asymmetric visual emphasis?

## Preference-center review checklist

Check:

- categories are understandable
- necessary is clearly distinguished from optional
- settings are not buried behind an excessive number of layers
- vendor details are progressive, not dumped by default if that hurts usability
- save / confirm behavior is obvious
- the user can later reopen and revise choices

## Runtime review checklist

Check:

- default consent state is initialized before dependent tags run
- accept / reject / save settings actually update the real runtime state
- analytics, ads, and other optional tags are gated by the chosen state
- denied flows still behave coherently for measurement where the stack supports it
- the consent event pipeline is observable enough to debug or test

Do not declare the banner "done" because the UI exists if the runtime is wrong.

## Performance review checklist

Check:

- banner does not create CLS when it appears
- banner is not large enough to risk becoming the LCP element unnecessarily
- clicking accept does not trigger an avoidable INP spike from loading everything at once
- banner scripts and assets are loaded with an intentional strategy
- mobile viewport and safe-area behavior are acceptable

## Accessibility review checklist

Check:

- full keyboard navigation
- predictable focus order
- proper dialog semantics if modal
- readable contrast and tap targets
- toggles and buttons are labeled clearly

## Creation / update rule

If the banner is missing or materially weak:

1. inspect the real stack first
2. verify the vehicle can do the runtime job
3. review or propose the banner one element at a time
4. show before / after on form and substance before visible implementation
5. when implementation is approved, wire the banner into the real consent flow and verify it is not dead code

## Anti-patterns

Call these out explicitly:

- accept visible, reject hidden
- reject only accessible through a second layer without strong reason
- misleading color contrast or button hierarchy
- banner copy optimized in isolation from the real tracking runtime
- a legally "present" banner that is technically disconnected from the real consent logic
- a banner that destroys mobile UX or Core Web Vitals while claiming to be optimized
