# Generic Decision Rules for `my-personal-knowledge-source-ingest`

## Mechanics that stay generic

Every domain variant should preserve these mechanics:

- process one source at a time
- extract candidates only after understanding the whole source
- score candidates before keeping them
- avoid duplicate learnings
- enrich when the new source adds useful specificity
- preserve useful but under-evidenced claims as explicit hypotheses when the domain contract allows it
- preserve concrete actionable techniques with a lower-confidence status instead of rejecting them solely for weak proof, when the domain contract allows it
- preserve contradictions explicitly
- reject noise aggressively
- update durable repo artifacts, not just thread memory

## Domain-specific pieces that must be supplied separately

The parent skill does not decide:

- what counts as a high-value learning in a given domain
- which themes should be updated
- what future execution skills the repo is trying to enable
- what non-goals should block retention

## Rejection baseline

Across domains, reject candidates that are:

- vague
- generic
- non-actionable
- purely rhetorical
- duplicated without new value
- too anecdotal to transfer

## Hypothesis baseline

A domain variant may add a hypothesis layer when it needs to preserve pressure-testable claims without promoting them to doctrine.

Use hypotheses only when the candidate is actionable, specific, and testable enough for later corroboration. Do not use them as a parking lot for interesting but vague claims.

## Capture-first baseline

When a domain expert has selected a source as relevant, concrete and repeatable techniques should usually be retained with the appropriate uncertainty label rather than rejected for being anecdotal.

Weak evidence should downgrade confidence or status. It should not delete an actionable candidate unless the candidate is vague, unsafe for the domain, duplicate without enrichment, or outside scope.
