# Evaluator Calibration Loop

Evaluator quality is not automatic.

If the evaluator is too soft, too noisy, or too shallow, calibrate it explicitly.

## When calibration is needed

Typical signals:

- it keeps approving weak work
- it repeatedly misses edge cases
- it over-focuses on style while missing fulfillment
- it produces too many low-value complaints

## Calibration method

1. Save concrete examples of bad evaluator judgments.
2. Classify the failure:
   - too lenient
   - too shallow
   - wrong criterion weight
   - wrong verdict threshold
3. Update the rubric or verdict policy at the smallest correct surface.
4. Reuse `my-personal-verified-learning-loop` to promote only what was validated by real runs.

## Important discipline

Do not recalibrate from one random impression.

Calibrate from repeated or high-signal evaluator failures with explicit evidence.
