# Evaluator Acceptance Rubric

Use this reference when an independent evaluator reviews one translated locale catalog.

This rubric exists to stop the correction loop from becoming subjective.

## 1. Scope

One evaluator reviews one locale at a time.

The evaluator does not edit that locale.
The evaluator decides whether the locale:

- passes
- or fails and returns to correction

## 2. Output shape

Every evaluation should produce:

- locale reviewed
- decision: `PASS` or `FAIL`
- structural findings
- meaning/accuracy findings
- naturalness/cultural findings
- terminology/tone findings
- concrete correction instructions

Do not stop at vague comments like "sounds a bit off".
Every failure should point to concrete keys and concrete rewrite guidance.

## 3. Structural checks are gating

If any structural check fails, the locale automatically fails.

Gating failures include:

- missing keys
- extra keys that should not exist
- type mismatches
- placeholder mismatches
- ICU mismatches
- broken markup needed at runtime

These checks should be run with the reusable scripts before or alongside qualitative review.

However, the evaluator must adjudicate script findings before failing the locale:

- a script finding is a candidate blocker, not automatically the final truth
- hybrid source patterns that combine a rendered variable with a plural suffix helper may be legitimately translated into a single ICU plural message in the target locale
- locale-specific plural categories may be legitimate if the compiled target message preserves the same user-facing meaning and runtime variables
- when a finding is accepted as a false positive or locale-specific adaptation, the evaluator must say so explicitly and include the direct key-level evidence

## 4. Meaning checks are gating

If product meaning drift is found on any important key, the locale fails.

Examples:

- a billing or pricing sentence changes intent
- a CTA changes what action the user is taking
- legal or support copy weakens or changes a promise
- onboarding or auth copy changes the product behavior implied by the source

## 5. Naturalness checks are gating when they affect immediacy

A locale fails if it still reads like a translation instead of native product copy in ways a real user would notice.

Examples:

- literal wording that feels foreign or clumsy
- phrasing that a native user would not naturally use in a UI
- register that is wrong for the product
- culturally odd references left unadapted when they should have been localized

Minor stylistic nits do not require failure on their own.
But recurring awkwardness across the locale is a fail.

## 6. Terminology consistency checks are gating when they create confusion

A locale fails if terminology is inconsistent in ways that can confuse the user.

Examples:

- the same product object translated three different ways
- inconsistent naming of plans, status labels, or support actions
- switching between formal and informal address when the locale strategy expects one

## 7. Acceptance rule

Only `PASS` stops the loop.

`PASS` requires all of the following:

1. no structural blockers
2. no meaning drift on important keys
3. no native-reader awkwardness that materially hurts immediacy or trust
4. no terminology inconsistency likely to confuse users
5. at most a handful of optional nits that do not justify another full correction pass

If those conditions are not met, the locale is `FAIL`.

There is no separate accepted state like "pass with minor issues" for the correction loop.
If the locale still needs edits before release confidence, it fails and goes back to correction.

## 8. Correction loop

If the evaluator returns `FAIL`:

1. the orchestrator records the findings
2. a translator/fixer subagent applies the corrections
3. the locale returns to evaluation
4. the loop continues until the evaluator returns `PASS`

Every corrected locale must be re-evaluated.
Do not skip re-evaluation after edits.
