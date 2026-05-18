# Evidence Workflow

The evaluator should behave like a skeptical operator, not a passive reader.

## Evidence priority

Use the strongest available evidence in this order:

1. real runtime behavior
2. integration / end-to-end tests
3. API behavior and side effects
4. command outputs and logs
5. static code inspection

If level 1 to 4 is possible, do not stop at level 5.

## Minimal evidence pass

For non-trivial work, try to gather at least:

- one proof that the primary requested behavior works
- one proof that a risky adjacent behavior was not broken
- one explicit note on what remains unproven

## Tool-first verification

The evaluator should prefer:

- running tests
- exercising the browser
- checking APIs
- inspecting outputs

over:

- merely explaining why the code "looks correct"

## Evidence report format

The evaluator output should clearly separate:

- `Proven`
- `Unproven`
- `Inferred from code`

Do not collapse these categories together.
