# Loop Stop Rule

Use this file to decide whether the optimization loop should continue or stop.

Its purpose is to stop two opposite errors:

- stopping too early because a page is merely "green enough"
- continuing too long because tiny noisy gains look like real progress

## Core Question

At the end of each meaningful batch, ask:

> "Is there still a material, evidence-backed gain left to pursue under the current constraints?"

If yes, continue.
If not, stop.

## What A Material Gain Is

A gain is material when it improves the page in a way that is both:

1. real enough to exceed likely noise or guesswork
2. meaningful enough to justify another optimization step

In practice, a gain is material when at least one of these is true:

- a dominant bottleneck family is reduced, removed, or clearly demoted
- a critical user-facing metric meaningfully improves in a way consistent with the change
- the page becomes meaningfully more resilient on a critical surface such as LCP, responsiveness, or layout stability
- a critical-page guard check or optimization step removes a business-relevant regression risk
- the change produces a cleaner and more trustworthy performance profile without causing offsetting regressions

## What Is Usually Not A Material Gain

Treat these as usually non-material unless stronger evidence exists:

- tiny PSI score movement with no supporting diagnostic improvement
- single-run metric wiggles that look like normal variance
- gains that exist only on a weak secondary metric while a more important metric stays flat
- gains that are offset by a regression elsewhere
- deep complexity added for a barely measurable result

The loop should not continue just because "the number moved a bit."

## Noise Rule

Do not treat every score or metric fluctuation as real progress.

Bias toward noise when:

- the result changed only slightly
- the diagnostic families look the same
- the page is known to have run-to-run variance
- a second confirmation would likely be needed before making a strong claim

If the result smells like noise, do not institutionalize it as a win.

## Continue The Loop When

Continue when all of these are true:

- there is a plausible next hypothesis
- the hypothesis targets a material remaining bottleneck
- the expected upside is still meaningful
- the path does not require an unapproved visual change
- the prior batch produced signal rather than pure noise

Prefer continuing with one narrow next hypothesis rather than reopening the whole search space.

## Stop The Loop When

Stop when any of these is true:

- the strongest bottleneck families have already been addressed
- the remaining opportunities look marginal or speculative
- the next moves are likely noise-chasing
- the remaining path requires an unapproved visual or UX change
- further work would create disproportionate complexity for little likely benefit
- repeated passes no longer produce credible material gains

This is the practical-ceiling rule.

## Stop Blocked By Constraint

There is a special stop case:

- a real opportunity still exists
- but it is blocked by an explicit constraint such as visual approval, product behavior, or business requirements

In that case, do not say the page is absolutely maxed out.
Say the loop is stopping at the current approved ceiling.

## Critical Pages

On critical pages, keep the same discipline.

Critical pages do not justify noise-chasing forever.
They justify a lower tolerance for unverified inheritance and a higher willingness to confirm risk.

But once the remaining path becomes marginal, blocked, or speculative, the loop should still stop.

## Output Contract

Every stop decision should say which of these applies:

- `continue: material gain still plausible`
- `stop: practical ceiling reached`
- `stop: blocked by approval or constraint`
- `stop: remaining opportunity too marginal or too noisy`

And it should explain why in plain language.
