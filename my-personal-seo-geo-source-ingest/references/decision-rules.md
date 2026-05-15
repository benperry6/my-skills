# Decision Rules for `source-ingest`

## User-curation rule

For this repo, user-selected SEO/GEO sources are pre-curated by an experienced operator and should be treated as high-signal inputs.

This changes the retention posture, not the truth standard:

- assume the source probably contains something worth retaining, enriching, or downgrading
- do not assume every claim in it is true
- when in doubt between `reject` and a useful non-canonical status, prefer the non-canonical status if the candidate is actionable and bounded

## Candidate scoring

Score every candidate learning from `0` to `3` on:

- actionability
- specificity
- novelty
- transferability
- solidity

Use scoring in two layers:

- Canonical baseline: a candidate can become `new learning` only if:
  - total score is at least `9/15`
  - actionability is at least `2`
  - specificity is at least `2`
- Non-canonical retention baseline: a candidate may still be retained below the canonical baseline when it is:
  - actionable enough to matter
  - bounded enough to revisit
  - useful enough to test, combine, or pressure-test later

For user-curated high-signal sources, use the score as a calibration aid rather than as a blind gate. If a candidate is operationally useful but under-supported for canon, downgrade it into `hypothesis` or `technique_candidate` instead of rejecting it solely on score.

## Capture-first technique rule

The user's source selection is a relevance signal. When a user-selected SEO/GEO source contains a concrete, repeatable, plausible technique, do not reject it solely because the source evidence is anecdotal, practitioner-reported, or not fully isolated.

Low proof should affect confidence, scope, caveats, decision status, and whether the candidate is canonical, operator-verified, a hypothesis, or a technique candidate. Low proof alone must not erase an actionable technique.

Reject a technique only when it is non-actionable, genuinely out of SEO/GEO scope, duplicate without enrichment, unsafe/exploit-only for this repo, or too vague to test or apply.

## Bounded-salvage rule

When a source states a tactic in a hacky, unsafe, hidden, or over-broad way, split the candidate before deciding:

1. Reject the naive or abusive version.
2. Extract the bounded version that is visible to users, aligned with page reality, compliant with known feature/page-role constraints, and testable.
3. Retain that bounded version as an enrichment, hypothesis, or technique candidate when it has operational value.

Examples:

- Reject `inject invisible Product/AggregateRating schema on a category to force stars`.
- Retain `test a visible rating/review package on a commerce collection, with real ratings shown on-page and structured data aligned to page role and feature eligibility`.
- Reject `manufacture engagement with decorative widgets`.
- Retain `add task-fit interaction paths such as filters, comparison helpers, product clicks, internal next steps, or useful FAQ toggles when they reduce user uncertainty`.

If no bounded version exists, the processed source must say so explicitly. Do not let a rejected overclaim erase a useful, safer tactic.

Use the hypothesis layer when a candidate is below the canonical learning bar but still useful enough to pressure-test:

- total score is at least `8/15`
- actionability is at least `2`
- specificity is at least `2`
- the candidate has a clear pressure-test path
- the hypothesis record can state explicit promotion and rejection criteria

Do not use hypotheses as weak learnings. They are not canonical doctrine.

## Evidence-type rule

Do not reject a source just because it is not an official Google document.

Instead classify its evidence profile:

- official guidance
- operator-reported first-party test
- first-party experiment
- large observational dataset
- practitioner workflow report
- reasoned hypothesis
- unsupported assertion

Use that evidence profile to calibrate `solidity`, confidence, wording strength, and whether the output should be framed as a robust learning or as a hypothesis that needs corroboration.

If the operator explicitly confirms a scoped technique from first-party tests, mark the retained record as `operator_verified` or promote the matching hypothesis into a scoped learning. Keep attribution to the operator validation and avoid turning a scoped test result into a universal rule.

## Consensus signal-family rule

Some SEO/GEO mechanisms are rarely confirmed cleanly by platform owners but may still be supported by strong practitioner consensus, repeated field reports, operator tests, and leak-derived system clues.

For signal families such as user interactions, clicks, engagement, NavBoost-like systems, Chrome-like traffic, satisfaction, and SERP return behavior:

- do not frame the whole family as low-confidence solely because Google does not state the exact ranking formula
- retain the family as a strong operational, non-canonical hypothesis when multiple independent sources converge
- keep uncertainty on exact inputs, collection sources, weighting, query classes, time windows, and abuse resistance
- separate real user satisfaction and task completion from synthetic or low-quality manipulation

Wording should look like:

`User-interaction signals are operationally important enough to optimize for, but the exact collection source, weighting, and SERP-specific mechanics remain uncertain.`

Not:

`There is no proof this matters, so reject it.`

## Visual-evidence rule

If the source includes images, charts, screenshots, diagrams, or other attached visuals:

- inspect them as part of the source
- use them when they add distinct evidence, structure, or nuance beyond the text
- do not create separate learnings from visuals if they only restate the same claim with numbers or design polish
- mention in the processed source when visuals were used as supporting evidence

## Duplicate rule

Treat a candidate as a duplicate when these three conditions are already present in the base:

1. same underlying principle
2. same concrete action
3. same scope or context of application

If duplicate:

- do not create a new learning
- add the new source ID to the existing learning
- enrich only if the source adds useful detail

Apply the same rule to hypotheses: do not create a new hypothesis when an active one already covers the same tentative principle, action, and scope. Add the source ID or refine the existing hypothesis instead.

## Enrichment rule

Treat a candidate as enrichment when the principle already exists but the new source adds:

- an implementation detail
- a prioritization signal
- a useful example
- an exception
- a contextual boundary
- a more precise wording

## Hypothesis rule

Treat a candidate as a hypothesis when it is:

- specific enough to test
- operationally relevant to SEO/GEO
- under-evidenced for a canonical learning
- not already covered by an existing learning
- not merely interesting trivia, rhetoric, or exploit detail

Every retained hypothesis must include:

- a tentative statement
- a pressure-test action
- scope boundaries
- promotion criteria
- rejection criteria

Promote a hypothesis only when later evidence makes it meet the canonical learning bar, typically through two independent sources, one stronger source, or first-party test evidence.

Reject or retire a hypothesis when later evidence contradicts it, it remains too vague to test, or it stops matching the repo's SEO/GEO scope.

## Technique-candidate rule

Use a technique candidate when the source gives a concrete SEO/GEO tactic that may work, but the available detail is still too thin for either a canonical learning or a well-formed hypothesis.

Minimum bar:

- clear action
- clear intended SEO/GEO outcome
- plausible mechanism or practitioner context
- enough specificity to revisit later

Store technique candidates in the non-canonical hypothesis layer with `decision_status: technique_candidate` until a later source, test, or operator validation upgrades or retires them.

## Technique-candidate lifecycle rule

Every technique candidate must carry an explicit review path.

At minimum, define:

- what new evidence would promote it
- what contradiction or failure would retire it
- what overlap would justify merging it into another hypothesis or learning

Review a technique candidate when:

- a new source materially reinforces or weakens it
- the operator reports first-party validation
- another retained record now covers the same principle, action, and scope

Retire, merge, or narrow a technique candidate when:

- it is superseded by a better-formed hypothesis or learning
- it remains idle and uncorroborated through multiple later passes
- it becomes clearly obsolete, contradicted, or too vague to revisit

## Canonical promotion bar

Use `new learning` only when the candidate has all of the following:

- actionable enough to guide real work
- specific enough to survive paraphrase
- plausible mechanism
- explicit boundary or failure condition
- reusable beyond one anecdote

And at least one of:

- two materially independent supporting sources
- one stronger source plus one supporting source
- explicit operator first-party validation for a scoped version

If the candidate is useful but does not meet this bar:

- use `operator_verified` for scoped first-party validation
- use `hypothesis` for pressure-testable patterns
- use `technique_candidate` for concrete tactics that are valuable but still thin

## Mechanism-extraction rule

Whenever a source gives a tactic, recommendation, or repeated pattern, try to extract the mechanism behind it.

Capture one or more of:

- source-stated mechanism
- source-implied mechanism
- operator-validated mechanism
- unresolved but plausible mechanism

If the mechanism is inferred rather than directly stated, preserve that distinction in wording. Do not present a reconstruction as if the source proved it.

Reject a candidate faster when it has:

- no plausible mechanism
- no bounded context
- no operational value even as a testable tactic

Downgrade rather than reject when the mechanism is still incomplete but the tactic is concrete and useful enough to revisit.

## Canonical asymmetry rule

Retain broadly, canonize slowly.

In this repo:

- `new learning` should be relatively hard to earn
- `hypothesis`, `technique_candidate`, and `operator_verified` should absorb most uncertain but valuable patterns
- promotion to canon should require more than mere repetition inside the same practitioner discourse

## Canonical anti-confirmation rule

Every canonical learning must state at least one realistic disconfirmation path.

A canonical learning is weaker if:

- it has no plausible failure mode
- it has no stated boundary
- it only survives by broad wording
- it cannot explain what would make it narrower, weaker, or false

If those conditions are missing, prefer `hypothesis`, `technique_candidate`, or `operator_verified` instead of `new learning`.

## Conflict rule

When the new source materially contradicts an existing learning:

- do not merge blindly
- preserve both claims
- update `conflicts_with`
- note the apparent conditions under which each claim might hold

## Rejection rule

Reject a candidate when it is:

- vague
- generic
- non-actionable
- obvious with no new angle
- rhetorical or motivational
- anecdotal without a reusable operational takeaway
- too source-specific to generalize
- unsupported assertion with no operational value even as a hypothesis

Do not reject solely because:

- it is not official
- it comes from a podcast, thread, or interview
- it is black-hat or gray-hat
- it lacks perfect proof
- it is currently better framed as a non-canonical pattern than as doctrine

## Noise rule

Do not extract proportionally to source length.

A short source can yield many retained learnings.
A long source can yield none.

Judge only by durable operational value.
