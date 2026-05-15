# Domain Contract for `my-personal-hermes-agent-source-ingest`

## Purpose

This skill processes one external source at a time into durable improvements for Ben's Hermes VPS and AI-agent operating system.

It is a specialization of `my-personal-knowledge-source-ingest`: generic mechanics, Hermes/agent-specific judgment.

## Domain Scope

Retain candidates that help improve one or more of:

- Hermes VPS setup and configuration
- Telegram topic/channel operation
- gateway reliability and message handling
- prompt/context discipline
- memory and vault workflows
- skill creation, maintenance, and routing
- MCP/tool integration and tool-use discipline
- subagent/delegation orchestration
- evals, observability, QA, and recovery loops
- future reusable AI-agent patterns

Reject or defer candidates that are:

- unrelated to Hermes/agents
- generic AI commentary without a concrete operational takeaway
- project-specific work outside this topic unless Ben asks
- destructive, credential, billing, or external-service changes without approval
- dependent on Ben's MacBook as an always-on relay

## Artifact Targets

Use the smallest durable target:

- `memory`: stable user/environment facts only.
- `/home/hermes/vault/ops/`: source summaries, durable decisions, backlog, and setup notes.
- skill patch/create: reusable procedures, pitfalls, workflows, and routing rules.
- code/config: only for concrete, safe, verified, approved changes.
- no write: rejected or purely conversational items.

## Expected Source Record

When a durable note is warranted, keep it compact:

```md
---
title: "Source title"
source_type: tweet | article | screenshot | transcript | repo | docs | other
url: <optional>
captured_at: YYYY-MM-DD
processed_at: YYYY-MM-DD
themes: [memory, skills, mcp, prompts, reliability, orchestration]
status: processed
---

## Source Summary
- What the source actually says.

## Candidate Decisions
- Candidate: ...
  - Decision: reject | duplicate | enrich | hypothesis | technique_candidate | operator_verified | new_learning | conflict
  - Reason: ...
  - Verification: ...
  - Action: ...

## Follow-ups
- Optional backlog or test item.
```

## Canonical Bar

A Hermes/agent learning can become canonical only when it is:

- actionable in Ben's setup
- verified against actual files/config/runtime or official docs
- reusable beyond one source
- compatible with Ben's explicit constraints
- safe or clearly bounded

If useful but not verified enough, keep as `hypothesis` or `technique_candidate`.
