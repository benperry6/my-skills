---
name: copy-editing
description: "When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' 'copy sweep,' 'tighten this up,' 'this reads awkwardly,' 'clean up this text,' 'too wordy,' 'sharpen the messaging,' 'refresh this content,' 'update this page,' 'this content is outdated,' or 'content audit.' Use this when the user already has copy and wants it improved or refreshed rather than rewritten from scratch. For writing new copy, see copywriting."
metadata:
  version: 1.3.0
---

# Copy Editing

Use this skill to improve existing marketing copy while preserving the original message and intent.

## Core Philosophy

Good copy editing is not a rewrite by default. It improves clarity, voice, proof, specificity, emotion, and perceived risk through focused passes.

Before editing, read `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md` when present, and use the brand voice and customer language from that context.

## Reference Map

Use these references for detailed execution:

- [references/full-operating-manual.md](references/full-operating-manual.md) - complete long-form workflow preserved from the original skill
- [references/plain-english-alternatives.md](references/plain-english-alternatives.md) - clearer replacements for common weak phrasing
- [references/content-refresh.md](references/content-refresh.md) - workflow for outdated or stale content

## Seven Sweeps

Edit through focused sweeps. After each sweep, check that earlier improvements were not broken.

1. Clarity: remove confusing structure, vague language, and missing context.
2. Voice and Tone: make the copy sound consistent with the brand and audience.
3. So What: connect every claim to a reader-relevant benefit or consequence.
4. Prove It: add evidence, examples, specificity, or qualifiers where claims are unsupported.
5. Specificity: replace generic claims with concrete language, numbers, mechanisms, or use cases.
6. Heightened Emotion: increase stakes, urgency, aspiration, or relief without exaggerating.
7. Zero Risk: reduce hesitation by addressing objections, friction, ambiguity, and perceived downside.

## Workflow

1. Confirm the copy's goal, audience, and surface.
2. Read product-marketing context if available.
3. Identify whether the user wants a light edit, deep copy sweep, proofread, content refresh, or diagnostic review.
4. Run the relevant sweeps in order.
5. Preserve the core message unless the user explicitly asks for a rewrite.
6. Explain high-impact edits briefly when useful.
7. Provide the edited copy and any remaining risks or assumptions.

## Quick Checks

At minimum, check for:

- unclear audience or promise
- jargon and corporate phrasing
- unsupported claims
- buried CTA
- weak opening
- feature lists without benefits
- inconsistent tone
- excessive wordiness
- mixed audiences
- stale facts or outdated positioning

## Content Refresh

For outdated content, verify what changed before editing. Refresh claims, examples, references, and positioning only when the source context supports the change.

## Related Skills

- For writing new copy from scratch, use `copywriting`.
- For aggressive direct-response angles, use `aggressive-copywriting`.
- For page-level conversion strategy, use `page-cro`.
- For product context creation, use `product-marketing-context`.
