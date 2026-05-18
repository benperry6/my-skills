# Default QA Rubric

Use this as the default evaluator rubric.

Adapt it when the task has unusual constraints, but do not remove the core distinction between fulfillment and evidence.

## Default weighted criteria

- `Contract fulfillment` — 35%
  - Did the delivered work actually implement what was requested?
  - Check every meaningful requested behavior, not just the headline.

- `Behavioral evidence` — 25%
  - What was proven in real execution?
  - Prefer tests, browser behavior, API responses, or produced outputs over code reading.

- `Regression / collateral damage` — 15%
  - Did the change break nearby behavior, create scope drift, or add unrequested complexity?

- `Constraint adherence` — 10%
  - Did the implementation respect explicit technical or product constraints?
  - Examples: no new library, specific API contract, required styling approach, budget limit.

- `UX / operability sanity` — 10%
  - Even if technically working, is the flow understandable and usable enough for the intended user?

- `Test adequacy` — 5%
  - Are the executed tests meaningful for the risky behaviors, or is there still a verification gap?

## Optional conditional criterion

Add only when relevant:

- `Memory / durable truth integrity`
  - If the implementation changes durable product truth, verify that the relevant memory surface was updated correctly.

## Scoring guidance

Use `PASS / CONCERN / FAIL` per criterion, then derive the overall verdict using `references/verdict-policy.md`.

Do not pretend the weighted score replaces judgment.
One critical unproven behavior can still force `REWORK` or `BLOCK`.
