# Know Your Customer Research

`know-your-customer.md` is the one canonical file that should not rely mainly on founder belief.

Founder input is useful, but only as a search seed.

## Core Rule

Do not guess what the audience thinks, wants, fears, or says.

Only save customer claims that are supported by:

- real public voice-of-customer evidence from the web, or
- real interview, survey, support, or test material provided by the user

If support is weak, preserve the uncertainty.

Persist the evidence in `docs/context-sources/voc-bank.csv` so later synthesis does not depend on memory alone.

## Acceptable Evidence Sources

Use any relevant public source where real people express real experience:

- forums
- Reddit
- product review pages
- app stores
- Google reviews
- Amazon reviews
- YouTube comments
- blog comments
- niche communities
- public competitor FAQ or Q&A pages when they surface recurring objections

Use primary voice whenever possible.

Evidence quality matters.

Prefer direct fetched user voice over:

- search result snippets
- official product copy
- third-party summaries
- founder assumptions

If weaker evidence is all you have, keep it clearly labeled and do not let it masquerade as strong proof.

## What Founder Input Is For

Founder input about the customer should help you decide:

- who to search for
- which competitors or alternatives matter
- what use cases are relevant
- which keywords and communities are worth checking first

Founder input should not be saved as customer truth unless later supported by evidence.

## Search Standard

Do not stop after a few searches and fill the rest from intuition.

Keep researching until the important sections of `know-your-customer.md` are supported by real user language:

- who they are
- current situation
- what they do today instead
- trigger moments
- job to be done
- pains
- desired outcomes
- objections
- buying criteria
- trust signals
- useful phrasing

If that support does not exist, say so explicitly in `Open Questions`.

Do not count official docs, tool landing pages, or generic SEO content as substitutes for real user voice on these core sections.

## Research Stop Conditions

KYC research should be persistent, but not mechanical.

Stop the current research pass and synthesize what you have when one of these is true:

1. the current pass has already produced enough evidence to clear the completion gate
2. two consecutive research passes produce no net-new meaningful evidence, only duplicates, or only weaker evidence than what is already in the bank
3. the remaining plausible public sources are clearly low-yield for this niche

Stop the current run and state an explicit blocker when one of these is true:

- a critical tool or model is rate-limited, unavailable, or repeatedly timing out
- transport or session failures keep interrupting the same step
- the research sources needed for the next pass are inaccessible

When that happens:

- do not keep hammering the same failing tool call
- record the exact blocker
- preserve the evidence already captured
- synthesize only what is supportable now
- put the unresolved gaps in `Open Questions`
- recommend the next best source or the condition needed to resume

## Extraction Standard

Prefer direct language over polished synthesis.

Good:

- quoted phrases
- recurring words
- repeated objections
- repeated trigger moments
- repeated desired outcomes

Bad:

- invented personas
- generic pain points
- soft consultant paraphrase that loses the original wording

## Persistence Standard

Do not let useful audience evidence disappear after one synthesis pass.

When you collect meaningful customer voice:

- add it to `voc-bank.csv`
- preserve source metadata
- preserve evidence quality metadata
- add lightweight tags only if useful
- deduplicate obvious repeats when they add no new signal

Then synthesize from the bank into `know-your-customer.md`.

## Interpretation Rules

Allowed:

- grouping similar quotes under a clear theme
- tagging quotes by source type, friction type, journey stage, or risk type
- noting that evidence appears mixed or contradictory

Not allowed:

- claiming a universal truth from a thin sample
- turning a weak pattern into a strong conclusion
- rewriting audience emotion into abstract marketing language
- writing a polished composite persona that is not directly supported by the evidence
- asserting price sensitivity, urgency, or sophistication levels unless the evidence actually shows them

## Suggested KYC Building Blocks

Use these lenses when building or updating `know-your-customer.md`:

- `Snapshot`
- `Segment Card`
- `Voice of Customer`
- `Buying Psychology`
- `Anti-Personas`
- `Special Cases`
- `Open Questions`

Within `Segment Card`, make sure the research can answer:

- what situation they are in now
- what they are trying to get done
- what they use instead today
- what would make them switch

These are stable anchors, not rigid forms.

## KYC Quality Checklist

Use this checklist when deciding whether `know-your-customer.md` is strong enough.

Mark each item as:

- `supported`
- `partially supported`
- `unsupported`

Minimum checklist:

- clear target segments
- current situation is described
- trigger moments are evidenced
- job to be done is evidenced
- current substitute or alternatives are evidenced
- pains or frustrations are evidenced
- desired outcomes are evidenced
- objections or fears are evidenced
- decision criteria are evidenced
- trust signals are evidenced
- real voice-of-customer quotes are present
- search or learning behavior is at least partially evidenced
- anti-personas or bad-fit users are identified when possible
- unresolved uncertainty is pushed into `Open Questions`

Fast quality test:

- could a strong copywriter write differentiated copy without guessing?
- could another agent understand the customer without redoing the research?
- does the document still hold up if you remove founder intuition from it?

Failure test:

If removing the quotes and evidence would make the file read like a generic persona, the KYC is too weak.

Consistency test:

If `know-your-customer.md` claims a number of validated themes, quotes, or categories, those counts must reconcile with the rows currently stored in `voc-bank.csv`.

## Completion Gate

Do not treat KYC work as finished just because one research pass was completed.

If `know-your-customer.md` is in scope, keep iterating until one of these is true:

1. the KYC is strong enough to support downstream marketing work without obvious guessing, or
2. a real blocker has been reached and is stated explicitly

### Minimum "strong enough" threshold

For a KYC to count as strong enough, all of the following should be true:

- target segments are at least `supported`
- current situation is at least `supported`
- trigger moments are at least `supported`
- job to be done is at least `supported`
- current substitute or alternatives are at least `supported`
- pains or frustrations are at least `supported`
- desired outcomes are at least `supported`
- objections or fears are at least `supported`
- decision criteria are at least `partially supported`
- trust signals are at least `partially supported`
- real voice-of-customer quotes are present
- unresolved uncertainty is isolated in `Open Questions`, not hidden inside the main sections
- any explicit coverage counts or validation claims reconcile with `voc-bank.csv`

Search or learning behavior and anti-personas can remain `partially supported` if the rest of the file is strong and the remaining gaps are explicit.

Evidence quality rule:

- `direct_user_voice` can fully support a core KYC claim
- `official_product_statement` and `third_party_summary` can support context, but should only partially support a core KYC claim unless backed by direct user voice
- `search_snippet` should be treated as provisional and should not fully validate a core KYC claim by itself
- `founder_seed` does not validate a core KYC claim

Partial-support phrasing rule:

- if a field is only `partially supported`, do not write it as a flat validated fact inside a segment card
- use explicit qualifiers such as `partially supported`, `early evidence suggests`, or `some evidence points to`
- if only part of a field is supported, keep the supported core and move the unsupported specificity to `Open Questions`
- `decision criteria`, `trust signals`, `search behavior`, and `anti-personas` are common overreach fields; handle them conservatively
- when in doubt, under-claim and isolate the gap rather than smoothing it over

### Iteration rule

If the threshold is not met:

- do another research pass
- expand the evidence bank
- re-synthesize the weak sections
- re-check against the checklist

Do not stop after a weak first pass if more plausible public evidence sources still exist.

If the bank is populated but the evidence quality is still too weak, continue upgrading the bank rather than just reshuffling the synthesis.

Do not confuse "more searches are technically possible" with "another pass is likely to change the result."

If repeated passes are no longer improving the bank in a meaningful way, treat that as a real low-yield limit and move the remaining uncertainty into `Open Questions`.

### Acceptable blockers

Only stop short of the threshold when there is a real blocker such as:

- very limited public audience evidence exists
- the niche is too new or too private for reliable public research
- the available sources are too thin, repetitive, or low-signal
- access to critical research sources is unavailable
- critical external tools or models needed for the research pass are rate-limited, unavailable, or unstable

In that case:

- do not claim the KYC is finished
- say the KYC is still incomplete
- identify exactly which checklist items remain weak
- recommend the next best evidence source to close the gap

## Strong KYC Shape

A strong KYC should read like a traceable customer understanding document, not like a strategy memo.

Good:

- supported segments
- real pains and desired outcomes
- direct user language
- explicit uncertainty
- claims that can be traced back to the bank

Bad:

- composite customer profile summaries that overstate certainty
- inferred pricing psychology with no direct evidence
- broad market conclusions with no quote trail
- category counts or validation scores that do not match the evidence bank

## Useful Universal Lenses

When the offer type changes, do not hardcode category examples.
Instead, inspect these universal dimensions:

1. Sale mechanics
2. Delivery mechanics
3. Payment model
4. Current substitute
5. Dominant perceived risk

These dimensions help you interpret what sections or customer concerns need more attention without forcing category-specific bias.
