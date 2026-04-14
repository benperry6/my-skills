# Evidence Contract

Before promoting a learning, be able to answer:

## 1. What failed?

State the concrete failing path:

- command
- API flow
- wrapper invocation
- browser fallback path
- helper script

## 2. What changed?

State the repaired or alternative path that was tested.

## 3. What proves success?

At least one of these should exist:

- exit code aligned with success
- expected artifact created on disk
- structured response produced and usable
- provider object created or updated as expected
- local verification step passed

Prefer more than one when the environment is flaky.

## 4. What confidence tier applies?

Use:

- `runtime` when the incident is real but the learning is still provisional
- `verified` when the path is reusable enough to guide future runs by default

## 5. What should be updated?

Choose the smallest correct write target:

- `runtime-learning.md`
- `verified-learning.md`
- `SKILL.md`
- helper/reference file

If you cannot justify the target, you should not write it.
