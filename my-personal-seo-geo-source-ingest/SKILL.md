---
name: my-personal-seo-geo-source-ingest
description: "[My Personal Skill] Process one pasted SEO/GEO source into the durable SEO/GEO brain for this repo. Use when a user provides a single tweet, LinkedIn post, blog article, video transcript, note, or other source that should be ingested into the SEO/GEO knowledge base. Treat user-selected sources as high-signal inputs, extract what is operationally useful, recover the mechanism behind advice when possible, decide duplicate vs enrichment vs hypothesis vs technique candidate vs operator-verified vs new vs conflict vs reject, and update the repo artifacts. This is the SEO/GEO specialization of `my-personal-knowledge-source-ingest`. Do not use for direct site optimization, keyword research execution, content rewriting, or final execution skill generation."
metadata:
  version: 1.0.0
---

# SEO-GEO Source Ingest

## Overview

Use this skill to process one SEO/GEO source at a time and convert it into durable repo artifacts.

Read the repo contract before acting:

- `references/repo-contract.md`
- `references/decision-rules.md`

This skill is the ingestion and curation layer only. It must not optimize pages, rewrite content, or generate final execution skills too early.

It is the SEO/GEO specialization of `my-personal-knowledge-source-ingest`, so it keeps the generic ingestion mechanics but applies SEO/GEO-specific scope and examples.

## Core doctrine

- User-selected sources are high-signal inputs. Treat them as likely to contain something worth retaining, enriching, or downgrading rather than as noisy by default.
- High-signal is not the same thing as true. User curation raises the presumption of usefulness, not the presumption of correctness.
- The right default question is not `is this officially proven?` but `what is recoverable here, for what use, at what confidence level?`
- Retain broadly, qualify precisely, canonize slowly.
- SEO/GEO advantage often comes from non-official operator knowledge, field reports, workflow tricks, prompt patterns, tooling choices, and edge tactics. Do not over-penalize them for being non-official.
- For every retained candidate, prefer extracting the mechanism behind the advice, not just the advice itself.
- When a source presents a risky, hacky, or over-strong tactic, split it before deciding: reject the naive/abusive version, but retain the bounded, visible, compliant, testable version when it has operational value.
- For user-interaction, click, NavBoost, Chrome-like, and behavioral-signal claims, treat broad practitioner consensus plus leak-derived corroboration as strong operational evidence that the signal family matters. Keep exact collection source, weights, formulas, and timing as uncertain unless the source proves them.

## Workflow

1. Read the current control plane before touching artifacts:
   - `docs/PROJECT_BRIEF.md`
   - `docs/ARCHITECTURE.md`
   - `docs/PROJECT_STATE.md`
   - `PRODUCT_MEMORY.md`
2. Read the source carefully and normalize it into a concise, faithful source record.
   - If the source contains attached visuals, inspect them too and use them when they add distinct evidence beyond the text.
3. Extract candidate learnings only after understanding the whole source.
4. For each candidate, try to capture:
   - the claim itself
   - the safest bounded version of the claim, when the original wording is too broad or risky
   - the mechanism given by the source, if explicit
   - the mechanism inferred from the source, if useful and plausibly reconstructable
   - scope or context of application
   - boundaries, caveats, or failure modes
   - evidence type and confidence level
5. Score each candidate using `references/decision-rules.md`.
6. For each candidate, decide exactly one outcome:
   - reject
   - duplicate
   - enrich existing learning
   - hypothesis
   - technique candidate
   - operator-verified learning
   - new learning
   - conflict
7. Update only the impacted repo artifacts:
   - one processed source file in `sources/processed/`
   - zero or more learning files in `learnings/atomic/`
   - zero or more hypothesis files in `learnings/hypotheses/`
   - only the affected synthesis files in `learnings/syntheses/`, creating the theme file on first use if it does not exist yet
   - draft skill specs only when the pattern is clearly reinforced
8. Report the exact file updates performed and the decision taken for each retained or rejected candidate.

## Short social source fast path

Use this fast path for a single short social post, tweet/X post, LinkedIn post, brief note, or small screenshot-backed post when the source itself is short and self-contained.

This is not a lower-quality mode. It only reduces fixed overhead. The decision standard stays identical.

Eligibility:

- one source only
- short source body, usually a few paragraphs or one short thread
- at most a small number of attached visuals
- no long linked article, video, paper, dataset, or external artifact that is the real payload
- no obvious legal, medical, security, or high-risk compliance claim
- no material conflict with the existing base visible after the first duplicate/neighbor search

If any eligibility condition is uncertain, use the full workflow.

Mandatory guarantees that do not change:

- never rely on thread memory as the source of truth
- verify the source URL by direct CLI/API access when practical
- if direct access fails, record the failure and use the user-supplied payload explicitly
- scan the repo for next IDs before writing
- search for duplicates before opening or updating records
- read the relevant neighboring records before deciding
- decide every candidate explicitly as `reject`, `duplicate`, `enrich`, `hypothesis`, `technique_candidate`, `operator_verified`, `new learning`, or `conflict`
- prefer enrichment over new records when an existing `LRN-*` or `HYP-*` covers the point
- keep useful but weak practitioner tactics as bounded hypotheses or technique candidates rather than promoting them to canon
- reject rhetoric, product framing, testimonials, engagement prompts, and non-actionable anecdotes
- run observable verification after writing

Fast path procedure:

1. Control plane refresh:
   - For the first source in a work session, after any control-plane or skill edit, or whenever unsure, read the full control plane listed in the standard workflow.
   - For subsequent short social sources in the same active work session, use a file-backed freshness check instead of re-opening every full artifact: inspect the target control files, re-read `docs/PROJECT_STATE.md` and any file whose timestamp/content changed, and fall back to the full read if anything is ambiguous.
   - This optimization is allowed only because it is anchored to repo files. Do not treat chat memory as the source of truth.
2. Source verification:
   - Try one direct URL verification path first, such as `curl -I` or another CLI/API-accessible method.
   - If X/Twitter, LinkedIn, or another platform blocks access with login/403/CAPTCHA, do not spend time on browser retries unless the source content is missing or the user asked for browser verification. Record the access failure in `Evidence Notes`.
3. Compact source normalization:
   - Create one concise processed source record.
   - Keep the raw extract faithful but compact.
   - Mention screenshots only when they add distinct evidence, structure, or nuance.
4. Targeted neighbor search:
   - Search by URL, author, quoted phrase, named tool/product, core tactic terms, and likely theme terms.
   - Read only matched `LRN-*`, `HYP-*`, prior `SRC-*`, and synthesis files that can plausibly absorb or conflict with the candidates.
   - If a concrete useful candidate has no match, broaden the search once before creating a new record.
5. Candidate handling:
   - Extract all distinct durable candidates, but expect many social posts to resolve to a small number of enrichments and rejects.
   - Do not invent a one-learning cap.
   - Do not force a new `LRN-*` or `HYP-*` merely because the source is operator-selected.
6. Writes:
   - Always create the processed source record when the source is being ingested.
   - Update only records that receive meaningful new precision, example, boundary, mechanism, or review path.
   - Skip synthesis updates when the source is a pure duplicate or adds no theme-level wording improvement.
7. Verification:
   - Run a duplicate-ID scan for `SRC-*`, `LRN-*`, and `HYP-*`.
   - Run `rg` for the new source ID across the expected updated files.
   - Read the new processed source record enough to verify structure and candidate decisions.
   - Use fuller verification when a new `LRN-*`, new `HYP-*`, conflict, broad synthesis update, or multi-file governance change is introduced.

Escalate from the fast path to the full workflow when the source is a long thread, contains a rich linked payload, introduces a genuinely new mechanism, conflicts with existing doctrine, needs legal/medical/financial precision, or requires multiple independent record families to be reconciled.

## Decision posture

- When choosing between `reject` and a non-canonical status, prefer `hypothesis`, `technique candidate`, or `operator_verified` if the idea is operationally useful and can be bounded.
- Do not require official Google or LLM-vendor confirmation for retention.
- Do not require perfect causal proof before storing a useful SEO/GEO pattern.
- Do require a plausible mechanism, a usable action, or a clear bounded observation before retention.
- Use `new learning` sparingly. A canonical learning should be reusable beyond one anecdote and should survive contact with adjacent cases.
- Use `operator_verified` when the operator explicitly reports first-party validation for a scoped technique.
- Use `technique candidate` aggressively for concrete tactics that may matter for the future agent's secret sauce but are still too thin for canon.
- Do not let a rejected overclaim erase the useful tactic hiding inside it. If the rejected version is `fake/invisible/automatic`, check whether a `visible/real/aligned/testable` version should be retained.
- When multiple independent practitioner sources, operator tests, and leak-derived commentary converge on the same signal family, prefer a strong operational, non-canonical hypothesis over a low-confidence dismissal. Preserve uncertainty around implementation details, not around the whole signal family.

## Non-negotiable rules

- Never rely on thread memory as the source of truth.
- Never create the same learning twice.
- Never keep a candidate just because the source is long or the speaker is famous.
- Never collapse a contradiction into fake certainty.
- Never create final execution skills from one isolated source.
- Never use hypotheses as canonical doctrine.
- Never reject a concrete SEO/GEO technique from a user-selected source solely because the evidence is anecdotal, practitioner-reported, black-hat, gray-hat, non-official, or not fully isolated; downgrade status or confidence instead.
- Never reject only the abusive wording of a tactic without also deciding whether a bounded compliant variant should be retained. If no safe variant exists, say that explicitly.
- Never confuse operator pre-curation with proof.
- Never retain rhetoric, posture, or motivational phrasing unless it carries a reusable operational takeaway.
- Never present an inferred mechanism as if the source stated it directly; mark it as inference in the processed source when that distinction matters.

## Output contract per source

A processed source must leave durable evidence of:

- concise source summary
- retained learnings
- retained hypotheses when applicable
- retained technique candidates or operator-verified learnings when applicable
- rejected candidates with rejection reason
- duplicate, enrichment, or conflict decisions
- exact file updates performed

## Quality bar

- Prefer precise operational wording over abstract summaries.
- Separate robust claims from opinions, inferences, and hypotheses.
- Preserve actionable techniques with uncertainty labels instead of deleting them for weak proof.
- Extract the `why this might work` layer whenever the source gives or supports one.
- A learning must be reusable beyond one anecdote.
- A hypothesis or technique candidate must still be specific enough to revisit, test, combine, or promote later.
- If a source adds no durable operational value, the correct outcome can still be zero retained learnings, but this should be uncommon for user-curated high-signal inputs.

## Example trigger requests

- "Ingest this LinkedIn post into the SEO/GEO brain."
- "Process this blog article and update the durable learnings."
- "Read this Twitter thread and decide what is worth keeping."
- "Treat this transcript as one source and update the repo artifacts."

## Do not use this skill for

- direct page optimization
- keyword discovery
- schema implementation
- article rewriting
- internal linking execution
- final SEO/GEO execution skill generation
