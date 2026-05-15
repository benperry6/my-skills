# Generic Contract for `my-personal-knowledge-source-ingest`

## Purpose

This skill is the parent ingestion pattern for any bounded knowledge domain.

It is generic on mechanics, not generic on judgment. It still requires a domain contract.

## Required domain contract

Before using this skill directly, the target repo or workflow must define:

- the domain scope
- the keep/reject quality bar
- the theme taxonomy
- the durable artifact layout
- the non-goals
- the future skill or execution direction

If those items do not exist, stop and bootstrap them first instead of improvising.

## Generic artifact expectations

A valid domain-specific repo should still provide:

- processed source records
- canonical learning records
- optional hypothesis or technique-candidate records for useful but under-evidenced claims when the domain contract supports them
- theme syntheses
- optional future skill specs

## Expected outcomes per source

For one processed source, the workflow must leave durable evidence of:

- what the source says
- what was kept
- what was kept only as a hypothesis, technique candidate, or operator-verified record, if applicable
- what was rejected
- what was duplicate vs enrichment vs hypothesis or technique candidate vs operator-verified vs new vs conflict
- which files changed
