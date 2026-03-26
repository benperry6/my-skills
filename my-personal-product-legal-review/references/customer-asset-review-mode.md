# Customer-Asset Review Mode

Use this reference when the legal/compliance gap touches a customer-facing asset outside the legal pages themselves.

Examples:

- post-purchase email
- upgrade confirmation
- onboarding explanation
- cancellation confirmation
- support disclosure surface
- any visible copy or UI block where value delivery and compliance need to coexist

## Goal

Do not jump from diagnosis to implementation.

Before any visible change outside legal pages:

1. load the real business and customer context
2. inspect the full product flow where the asset appears
3. review the asset with the user one element at a time
4. get explicit approval before patching

## Required Context Load

If these files exist in the repo, load them before drafting:

- `.agents/product-marketing-context.md`
- `.agents/business-model.md`
- `.agents/know-your-customer.md`
- `.agents/storytelling.md`
- `.agents/performance-memory.md`

Then load:

- the current asset code
- the current translations for that asset
- the adjacent surfaces in the same flow

Adjacent surfaces means the assets the user likely saw before and after this moment.

For an email, this usually includes:

- the triggering page or conversion flow
- any previous transactional or lifecycle emails already sent in the same journey
- the in-product state the user lands in after clicking the email

## Flow-First Review

Do not review a phrase in isolation.

First determine:

- when this asset is received or shown
- what the user has just done
- what the user already knows
- what they are likely feeling at that exact moment
- what action the product wants them to take next

The proposal must fit that full flow, not just the local sentence.

## Review Format

Open the review in collaborative mode.

Equivalent framing is:

"Ok, on peut revoir le fond et la forme de chaque élément ensemble, un par un. L'objectif est que chaque élément délivre exactement ce qu'il faut à l'utilisateur à ce moment précis du parcours."

Then review each element individually.

For each element, show:

1. current form
2. proposed form
3. current content
4. proposed content
5. why the proposed change fits the real flow and emotional context better

Rules:

- do not show one big before block and one big after block
- do not omit any part of the element under review
- keep comparison easy to scan
- for review examples, show the content only in French
- implementation may still patch all supported locales after approval

## Approval Rule

If the asset is visible outside legal pages, do not implement the change until the user has validated the reviewed element or reviewed bundle explicitly.
