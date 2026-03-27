# Value-First Compliance Assets

Use this file when a legal gap requires a new customer-facing asset such as:

- post-purchase email
- onboarding disclosure
- upgrade confirmation
- cancellation confirmation
- support-channel notice
- cookie banner / CMP

## Principle

Do not design the asset as a pure legal patch.

But first:

## Precondition: Functional Fit Before Framing

Before applying any value-first logic, verify that the chosen asset can actually do the primary job it was introduced to do.

Examples:

- if the primary job is to satisfy a durable-medium obligation, the asset must actually be capable of carrying the required contract information on a durable medium
- if the primary job is to communicate mandatory cancellation or complaint information, the asset must be able to carry that information clearly and durably enough for the scoped obligation

If the asset cannot do the primary job, stop.

Do not improve the copy.
Do not optimize the tone.
Do not continue the review as if the vehicle were valid.

Choose a different vehicle first.

Value-first starts only after the vehicle passes this gate.

## Cookie Banner / CMP Specific Rule

Cookie banners are a special case.

Their primary job is not only "show a legal notice". It is usually a combined runtime job:

- expose the real consent choices that the scoped regime requires
- map those choices to the real measurement / advertising / personalization runtime
- stay usable on mobile and accessible to real users
- avoid creating unnecessary friction, performance regressions, or fake choice architecture

So for cookie banners:

1. verify the banner vehicle can do the consent/runtime job
2. verify the banner is compatible with the actual tracking stack
3. only then optimize the copy, placement, and interaction design for useful consent, lower friction, measurement quality, and performance

Do not optimize banner consent rates with asymmetry or misleading UI and call that "value-first".
For this surface, value-first means:

- maximum useful consent without dark-pattern steering
- minimum friction without hiding the real choice
- better measurement without breaking consent semantics
- better performance without breaking the consent flow

Sequence the asset like this:

1. confirm the vehicle is fit for the primary job
2. reassure
3. congratulate or acknowledge the user context
4. explain the unlocked value or next step
5. make the product state clearer
6. weave the required legal information into the same asset without making it feel threatening

## Default Pattern

### Top of asset

- positive confirmation
- what just happened
- what is now unlocked

### Middle of asset

- comparison with the previous state when relevant
- what the user can now do
- what happens next
- where to manage the feature/account if needed

Each block must earn its place.

Ask for every block:

- what unique job does this block do?
- what information does it add that is not already stated elsewhere?

If the answer is weak, merge it into another block or remove it.

### Compliance layer

Add:

- the contractually relevant summary
- cancellation / renewal / billing facts when required
- support or complaint channel
- any jurisdiction-specific mandatory element

Keep the compliance layer clear, but do not lead with fear-heavy wording unless the situation itself is negative.

## Hard Rules

- Never hide required legal information
- Never keep the wrong vehicle just because the framing is strong
- Never duplicate the same value or operational message across multiple blocks when one block can carry it clearly
- Never optimize for marketing so hard that the legal meaning becomes vague
- Never introduce new visible UX wording outside the approved scope without a before/after review
- Never assume the user wants a cold "you are now subscribed" tone
- Never treat an asset file as sufficient proof of implementation; the asset must be wired into the real runtime flow that is supposed to trigger it

## Recommended Framing

Prefer:

- "what you now have access to"
- "what changed compared with before"
- "what happens next"
- "how to manage it"

Avoid leading with:

- dense contract jargon
- fear-heavy payment language
- legal disclaimers before value confirmation
