# Cheap Guard Check

Use this file when a page is allowed to inherit prior validation but still requires direct confirmation because it is critical.

This protocol exists to answer one narrow question:

> "Does this real page still look safe enough to inherit the trusted archetype without opening a full optimization loop?"

It is not a mini full audit.
It is not a broad optimization sprint.
It is not permission to skip real measurement.

## When To Run It

Run a cheap guard check when both conditions are true:

1. inherited validation is otherwise plausible
2. the page is critical enough that direct confirmation is mandatory

Typical examples:

- homepage variants
- money pages
- launch pages
- high-traffic campaign destinations
- pages with high failure cost

## Required Inputs

Before running the guard check, make sure these exist:

- a real target URL or preview URL for the exact page to be checked
- a known trusted reference archetype or prior validated page
- enough context to compare the current page against that trusted reference

If these do not exist, do not pretend the guard check passed.
Escalate.

## What The Guard Check Must Do

The minimum protocol is:

### 1. Confirm The Real Page Variant

- confirm that the page you are about to test is the real variant that matters
- confirm that the page loads successfully and is not obviously broken

If the real page variant cannot be reached, escalate.

### 2. Run A Lightweight Real Measurement

- run Google PageSpeed Insights on the real page
- mobile first by default
- a single lightweight confirmation pass is enough unless the result looks noisy or suspicious

The purpose is not to optimize yet.
The purpose is to verify that inherited confidence still holds on the real page.

### 3. Compare Against The Trusted Reference

Compare the current page against the trusted archetype or prior validated page.

Inspect at least:

- whether the likely LCP candidate still looks equivalent
- whether the dominant bottleneck family stayed broadly similar
- whether an obvious new regression family appeared
- whether the result still looks consistent with inherited trust

Do not require perfect score parity.
Require consistency good enough to justify inheritance.

### 4. Classify The Outcome

The guard check must end in one of these outcomes:

- `passed`
- `escalate to targeted re-check`
- `escalate to full optimization`

Do not stop at vague language like "looks okay".

## Pass Conditions

The cheap guard check may pass when all of these are true:

- the page loaded correctly
- the measurement ran successfully
- no obvious new critical regression family appeared
- the result still looks broadly consistent with the trusted archetype
- there is no strong signal that the page deserves deeper investigation

If these are true, the acceptable conclusion is:

- `inherited validation allowed, mandatory guard check required`
- and the guard check passed

## Escalate To Targeted Re-Check When

Escalate to a targeted re-check when any of these is true:

- the measurement is noisy, ambiguous, or suspicious
- a new bottleneck family appears but does not yet justify a full rerun
- the page looks mostly similar but not similar enough for confident inheritance
- the metrics look weaker than expected in a way that may be caused by a localized delta
- the page is important enough that uncertainty is not acceptable

## Escalate To Full Optimization When

Escalate to a full optimization loop when any of these is true:

- the measured page clearly no longer behaves like the trusted archetype
- a strong regression is visible
- the likely LCP candidate changed materially
- the first viewport or first-load path looks materially different
- there is no longer a trustworthy basis for inheritance

## What A Cheap Guard Check Must Not Do

Do not let this mode silently expand into a full optimization loop.

A cheap guard check must not:

- chase marginal wins
- open multiple broad optimization families
- perform a long revert/iterate cycle
- rewrite the page architecture
- pretend to certify a page that could not be measured directly

If deeper work is needed, escalate instead of smuggling a full optimization loop into guard-check mode.

## Output Contract

A cheap guard check should explicitly report:

1. the tested URL
2. the trusted reference page or archetype
3. whether the real page loaded correctly
4. whether PSI was run successfully
5. whether the guard check passed or escalated
6. why that outcome was chosen
