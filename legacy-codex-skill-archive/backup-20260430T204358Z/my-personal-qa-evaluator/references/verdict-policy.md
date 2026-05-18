# Verdict Policy

This skill uses exactly three verdicts.

## PASS

Use `PASS` only when:

- all critical contract items are satisfied
- the important risky behaviors were proven in real behavior
- no meaningful regression or scope failure remains
- remaining issues are truly minor nits

If critical behavior is still inferred rather than proven, do not use `PASS`.

## REWORK

Use `REWORK` when:

- the implementation is close
- the misses are bounded
- the next correction loop is small and clear
- the builder can probably fix it in one or two focused turns

Typical `REWORK` triggers:

- one or two missing contract items
- incomplete runtime proof
- small but real UX or API gaps
- regression risk that still needs one more check

## BLOCK

Use `BLOCK` when:

- the implementation materially misses the contract
- the architecture is wrong for the requested job
- the evaluator lacks enough evidence to trust the result at all
- the change created serious collateral damage
- acceptance would be misleading

Typical `BLOCK` triggers:

- major spec deviation
- critical flow does not actually work
- the implementation is mostly stubbed or display-only
- the proof is absent on a critical surface

## Rule of thumb

- small fix set = `REWORK`
- fundamental mismatch or no trustworthy proof = `BLOCK`
