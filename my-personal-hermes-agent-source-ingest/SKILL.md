---
name: my-personal-hermes-agent-source-ingest
description: "[My Personal Skill] Use when Ben shares one external source in the Hermes & AI Agents Setup topic to improve Hermes VPS, agent workflows, prompts, memory, tools, MCPs, skills, Telegram operations, or future agent architecture. Process the source with knowledge-source-ingest mechanics: extract operational candidates, compare against the real setup, decide reject vs duplicate vs enrich vs hypothesis vs technique_candidate vs operator_verified vs new learning vs conflict, and update only safe durable artifacts. Do not use for direct unrelated project execution or broad unsourced brainstorming."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, agents, ingestion, telegram, skills, knowledge]
    related_skills: [my-personal-knowledge-source-ingest, hermes-agent, ben-hermes-vps-primary-agent]
---

# My Personal Hermes Agent Source Ingest

## Overview

Use this skill to turn one user-selected source into durable improvements for Ben's Hermes VPS and AI-agent operating system.

This is the Hermes/agent-setup specialization of `my-personal-knowledge-source-ingest`. It keeps the same ingestion mechanics as the SEO/GEO source-ingest workflow, but the domain is Hermes itself: gateway behavior, Telegram topic workflows, prompts, memory, vault notes, tools, MCPs, skills, orchestration patterns, reliability, safety, and future agent architecture.

The Telegram thread is intake and discussion, not the durable source of truth. Every retained item must either be applied safely, written to an appropriate durable artifact, or explicitly left as a bounded hypothesis/backlog item.

## When to Use

Use when Ben shares or asks you to process a source such as:

- X/Twitter thread or bookmark about AI agents
- blog post, docs page, transcript, screenshot, repo, prompt, or tool example
- ChatGPT/Claude/Codex export about agent workflows
- practical advice about memory, prompts, tool use, MCPs, subagents, evals, observability, or automation
- content explicitly intended to improve Hermes VPS, this Telegram topic, or future AI-agent setup

Do not use for:

- direct SEO/GEO source ingestion; use `my-personal-seo-geo-source-ingest`
- direct coding implementation unrelated to Hermes/agent setup
- broad brainstorming without a concrete source
- storing secrets or credentials from a source
- destructive, billing, credential, or cross-project changes without Ben's approval

## Required Reading Before Ingesting

For a fresh work session or after any setup change, read or verify:

- active topic binding / channel prompt for `Hermes & AI Agents Setup`
- `/home/hermes/.hermes/config.yaml` only as needed, and never expose secrets
- relevant vault notes under `/home/hermes/vault/ops/`
- relevant Hermes docs or repo files when the source recommends Hermes configuration changes
- `my-personal-knowledge-source-ingest` and this skill's reference files when the workflow is uncertain
- `references/skills-repo-update-lessons.md` when the task touches the skills repo itself, branch freshness, selective recovery from `origin/main`, or plain-language reporting of repo/setup fixes
- `references/personal-source-ingest-convention.md` when creating, recovering, or renaming source-ingest skills or deciding whether to create a vault workspace vs a new GitHub repo
- `references/codex-jsonl-source-location.md` when ingesting a Codex/Claude/agent JSONL session export from Drive or when the requested session file is missing or ambiguous
- `references/codex-era-solution-porting.md` when extracting lessons from older Codex/Claude sessions whose implemented solutions may not fit current Hermes architecture

For short social posts after the control plane is already fresh, use a fast path: verify only the relevant current files and neighboring records before deciding.

## Domain Scope

In scope:

- Hermes Agent setup and configuration
- Telegram gateway/topic operations
- memory discipline and vault/cold-memory workflows
- skill design and maintenance
- MCP/tooling choices and integration patterns
- multi-agent orchestration and delegation workflows
- reliability, observability, retries, recovery, and eval loops
- prompt/context discipline
- safe automation boundaries
- future reusable agent architecture patterns

Out of scope unless Ben explicitly asks:

- ProStrike product work unrelated to agent setup
- Studapart/Pauliani operations
- SEO/GEO execution content
- generic startup/product/marketing advice without agent-system relevance
- tools that require Ben's MacBook as an always-on relay

## Workflow

1. **Identify the source**
   - URL, screenshot, pasted text, transcript, repo, or user summary.
   - If practical, verify the URL or artifact directly. If blocked, record that and rely only on the supplied payload.
   - For Codex/Claude/agent JSONL exports, validate source identity before ingestion: requested filename, first meaningful user message, last assistant message, embedded rollout/session path if present, and topical match. If a candidate is close but not confirmed, keep it in `sources/inbox/` with a `needs-confirmation-` prefix and ask Ben before substituting it.

2. **Extract candidate recommendations**
   - Pull out concrete operational claims, patterns, warnings, tools, prompts, or architecture ideas.
   - Ignore motivational fluff, engagement bait, and vague AI discourse.

3. **Compare against the real setup**
   - Check actual Hermes config, repo, docs, skills, vault notes, or topic binding before saying something applies.
   - If not verified, label it as a hypothesis, not fact.

4. **Classify each candidate**
   - `reject`: not useful, unsafe, duplicate with no value, outside scope, or too vague.
   - `duplicate`: already covered with no meaningful new detail.
   - `enrich`: improves an existing rule, skill, note, prompt, or workflow.
   - `hypothesis`: plausible and testable but not ready to apply.
   - `technique_candidate`: concrete tactic worth preserving but thinly evidenced.
   - `operator_verified`: Ben reports first-party validation for a scoped technique.
   - `new learning`: robust reusable rule for Hermes/agents.
   - `conflict`: contradicts existing doctrine or setup constraints.

5. **Choose the action**
   - Apply now only if small, safe, reversible, local to Hermes, and non-sensitive.
   - Write durable notes to `/home/hermes/vault/ops/` for decisions/backlog/context.
   - Patch or create skills only when the workflow is reusable and validated enough.
   - Ask before destructive, credential, billing, external-service, cross-project, or architecture-level changes.

6. **Report succinctly**
   - Recommendation extracted.
   - Decision per candidate.
   - Verification performed.
   - Files/config changed, if any.
   - Next step.

## Output Contract

For each processed source, return a clear ingestion receipt before moving on to unrelated infrastructure notes. The receipt must let Ben audit what was retained, rejected, and changed without opening the vault.

Use this structure:

```md
Source: <title/link/type>
Status: ingested | blocked | rejected | partial
Core recommendation: <one concise sentence>
Classification: Hermes-specific | agent-general | project-specific | not applicable
Provenance confidence: <verified | qualified | supplied-only | blocked>
Verification performed: <what was checked>
Action taken: <files/config/skills changed, or none>
New learnings: <accepted durable learnings, or none>
Enrichments / hypotheses / technique candidates: <each retained non-canonical item>
Rejected / duplicate candidates: <what was rejected/duplicated and why>
Backlog / next step: <if any>
```

When a source has multiple candidates, list each candidate with its decision status. If QMD indexing, embedding, Drive lookup, or another infra step partially fails, explain that separately after the receipt; do not let the infra issue replace the ingestion receipt.

## Durable Artifact Guidance

Use the smallest durable artifact that fits:

- **Memory tool**: stable user/environment preference only; never task progress.
- **Vault note**: durable topic decision, backlog, source summary, or setup rationale.
- **Skill patch**: reusable procedure, pitfall, or workflow improvement.
- **Repo/code change**: only when the source implies a concrete implementation and scope is approved/safe.
- **No write**: if the source is rejected or only needs a conversational answer.

Never dump raw source text into memory. Never store secrets. Redact tokens, passwords, API keys, private keys, and connection strings as `[REDACTED]`.

## Decision Posture

- Treat Ben-selected sources as high-signal, not automatically true.
- Retain useful concrete tactics with uncertainty labels instead of over-rejecting them.
- Canonize slowly: a `new learning` should be reusable beyond one post.
- Prefer `hypothesis` or `technique_candidate` for promising but under-evidenced agent ideas.
- Explicitly reject ideas that conflict with Ben's setup constraints, especially MacBook-as-relay patterns, unsafe credential handling, or unverified UI claims.
- Keep Hermes VPS as the default target in this topic unless Ben says otherwise.

## Common Pitfalls

1. **Using chat memory as source of truth.** Always verify against files/config/docs when the claim affects setup.
2. **Calling something implemented because it sounds right.** Verify the actual config, repo, or runtime state first.
3. **Creating a big backlog from vague posts.** Keep only concrete, testable, bounded items.
4. **Over-writing memory.** Use memory for stable preferences only; use vault for source summaries and operational notes.
5. **Applying risky changes too early.** Ask before destructive, credential, billing, cross-project, or architecture changes.
6. **Confusing agent-general advice with Hermes-specific advice.** Classify before acting.
7. **Preserving secrets from screenshots or pasted logs.** Redact aggressively.
8. **Explaining repo/setup fixes with raw Git jargon.** When Ben asks what happened, translate first into plain human language: what was blocked, what harm it caused, what was changed, and current status. Keep commit hashes, branch names, and error strings as secondary detail only when useful.
9. **Assuming the active branch contains the newest skill.** If a skill is missing after updating the active branch, check `origin/main` and other origin branches before concluding it does not exist. If `origin/main` has only the needed skill directories and a full merge would create broad conflicts, copy/check out those directories selectively and commit/push the result.
10. **Silently substituting a similar session export.** A topically related Codex/agent JSONL is not equivalent to the requested session. Validate identity first; if the exact file is missing, document the search, quarantine plausible candidates as `needs-confirmation`, and block rather than ingest the wrong source.
11. **Porting Codex-era solutions literally.** Older Codex sessions may have created skills, scripts, or workflows because Codex lacked Hermes-native affordances such as native delegation, Telegram operations, toolsets, profiles, cron, or vault/QMD workflows. Preserve the findings, constraints, and failure modes first; treat the old implementation as a candidate adapter only. Before writing backlog items, ask: “What is the Hermes-native mechanism that satisfies this need today?” and word actions as tests/hypotheses unless real Hermes runs prove the old skill is load-bearing. If an old skill risks steering implementation before Hermes-native design, quarantine it into a non-discoverable archive and keep it as cold reference only.
12. **Writing vault artifacts without refreshing retrieval.** After creating or updating durable vault notes, run a QMD collection update before assuming the new files are searchable. `qmd embed` alone may report existing hashes while the collection file list is stale. Verify with fast BM25/keyword search first; semantic embedding can remain pending if the VPS falls back to slow CPU.

## Verification Checklist

- [ ] Source was read or access failure was recorded.
- [ ] Candidate recommendations were extracted explicitly.
- [ ] Relevant setup files/docs/skills were checked before claiming applicability.
- [ ] Each candidate has one decision status.
- [ ] Any durable write is placed in the correct system: memory, vault, skill, or repo.
- [ ] If vault artifacts were written under an indexed QMD collection, `qmd update` was run and keyword/BM25 retrieval was verified, or the reason for deferring it was recorded.
- [ ] Sensitive changes were not made without approval.
- [ ] Final answer states what changed and what did not.
