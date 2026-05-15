---
name: my-personal-knowledge-source-ingest
description: "[My Personal Skill] Process one pasted source into a durable domain knowledge base. Use when a repo already has a clear domain contract and needs one-source-at-a-time ingestion with candidate extraction, scoring, duplicate vs enrichment vs hypothesis or technique candidate vs operator-verified vs new vs conflict decisions, and durable artifact updates. Use it directly for new domains that do not yet have a specialized variant, or as the parent pattern for building variants such as `my-personal-seo-geo-source-ingest`. Do not use for direct execution work like rewriting content, shipping design changes, or optimizing live systems."
metadata:
  version: 1.0.0
---

# Knowledge Source Ingest

## Overview

Use this skill as the generic ingestion parent for domain-specific knowledge bases.

Read the generic contract before acting:

- `references/generic-contract.md`
- `references/generic-decision-rules.md`

This skill is generic on mechanics only. It must not invent domain judgment when the target repo has not defined it yet.

## Workflow

1. Confirm that the target repo already defines its domain contract.
2. Read the repo's local rules, brief, architecture, and current state before touching artifacts.
3. Read the source completely.
4. Extract candidate learnings.
5. Score them against the repo's domain-specific bar.
6. Decide duplicate vs enrichment vs hypothesis or technique candidate vs operator-verified vs new vs conflict vs reject.
7. Update only the repo artifacts that the domain contract expects.
8. Report exactly what changed.

## Non-negotiable rules

- Never rely on thread memory as the source of truth.
- Never create the same learning twice.
- Never keep a candidate because the source is long.
- Never flatten contradictions into certainty.
- Never guess the domain taxonomy if it is missing.
- Never use this parent skill as a substitute for a well-defined specialized variant when one exists.

## Use this skill for

- creating or bootstrapping a new domain ingestion variant
- directly ingesting sources in a domain that already has a clear contract but no dedicated variant yet
- checking whether a proposed domain specialization still follows the generic ingestion mechanics

## Do not use this skill for

- direct domain execution work
- live site optimization
- rewriting deliverables
- generating domain conclusions when the repo has not defined the judgment criteria
