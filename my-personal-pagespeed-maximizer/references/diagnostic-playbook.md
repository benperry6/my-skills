# Diagnostic Playbook

Use this file after collecting a real PageSpeed baseline.

Its purpose is not to replace measurement.
Its purpose is to convert common PSI diagnostics into disciplined investigation paths.

## Important Rule

Every item in this file is a hypothesis generator.

Do not blindly apply a fix because it appears here.
Apply, re-measure, and keep only what improves the observed result.

## LCP Problems

When LCP is the main bottleneck, inspect:

- whether the likely LCP element is hidden, animated late, faded in, or delayed on first paint
- whether the hero image or hero media is oversized, badly compressed, badly prioritized, or served through a slow path
- whether the first viewport depends on too much runtime work before the hero is really visible
- whether data waterfalls delay the hero
- whether render-blocking fonts, CSS, or JS postpone the first meaningful render

High-value suspicion:

- an element that is visually the hero but does not paint immediately

Strong anti-pattern:

- hiding or delaying the likely LCP element as part of an entrance animation

## TBT / INP / Main-Thread Pressure

When responsiveness or blocking time is weak, inspect:

- heavy client bundles
- too much JavaScript above the fold
- unnecessary first-viewport runtime work
- large third-party scripts loading too early
- analytics, chat, consent, ads, or widgets competing for main-thread time
- expensive synchronous work during first load

Useful actions often include:

- reducing client-side work in the first viewport
- deferring non-critical third parties
- narrowing imports
- removing or isolating heavy interactive logic from the first screen

## CLS Problems

When CLS is weak, inspect:

- unsized images, embeds, and iframes
- injected banners, cookie surfaces, or dynamic bars
- layout changes caused by late font swaps
- components that change height after runtime initialization
- placeholders that do not match final dimensions

## Render-Blocking / Unused JavaScript / Network Choke Points

When PSI highlights render-blocking or wasted JS, inspect:

- fonts loaded too early or in the wrong way
- large barrel imports or broad client bundles
- scripts that could wait until after first paint or after consent
- components imported eagerly even though they are below the fold or conditionally used
- route-level waterfalls

Important caution:

- techniques such as preconnects, framework-level font changes, component code splitting, or lazy loading are not universally positive
- a supposed best practice can improve one metric while degrading another

## Third-Party Overhead

When a page is script-heavy, inspect:

- analytics and tracking tags
- consent managers
- chat
- A/B testing tools
- embedded media
- social widgets
- maps
- ads

The default bias should be:

- if it is not required for the first useful paint, move it later
- if it can wait until consent or interaction, do not let it compete with first load

## Revert Discipline

This playbook only works if failed ideas are rejected quickly.

If a technique worsens:

- LCP
- TBT
- INP
- CLS
- or the overall PSI result without a strong compensating gain

then it is a failed hypothesis for this page archetype and should not be turned into doctrine.
