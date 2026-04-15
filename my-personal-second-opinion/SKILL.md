---
name: my-personal-second-opinion
description: "[My Personal Skill] Use when Claude Code, Codex, or Gemini needs a second opinion, verification, or deeper research on technical matters. Routes to the OTHER engines, repairs broken cross-engine calls before continuing, and persists only real-world verified learning when a broken invocation has been debugged successfully."
---

# Second Opinion — Multi-Engine Verification Agent

Unified skill for getting independent second opinions from external AI engines and keeping the invocation paths current as the CLIs evolve.

## Canonical Entry Point

Do not re-implement the orchestration ad hoc when this skill is invoked. Use the shared runner:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --current-engine codex \
  --working-directory "$PWD" \
  --prompt-file /tmp/second-opinion-prompt.txt \
  --output-json /tmp/second-opinion-result.json
```

For a post-implementation audit of a real Claude Code implementation:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --mode post-implementation-audit \
  --current-engine codex \
  --working-directory "$PWD" \
  --session-cwd "$PWD" \
  --audit-path src/app/[locale]/cookies/page.tsx \
  --audit-report-dir .claude/audits \
  --output-json /tmp/second-opinion-post-impl.json
```

What the runner enforces:

- consults only the OTHER engine(s) by default
- retries through the locally verified fallback chain
- captures full logs for every attempt
- emits whether local repair succeeded or whether web research is still needed
- persists runtime-learned repairs only after a real successful invocation
- leaves the orchestrator responsible for any upstream web research that cannot be solved from local evidence alone

## Core Doctrine

1. **No silent degradation**: if one of the external engine calls fails, do not quietly continue with only the surviving engine unless the user explicitly asked for a single-engine review.
2. **Second opinion is blocking infrastructure**: if this skill was invoked, the orchestrator needs it. Repair the broken invocation path first, then continue the original mission.
3. **Verified learning only**: update this skill only after a repaired invocation works in real behavior on the current machine.
4. **Local evidence first**: inspect local `--help`, local config, installed package docs, and actual command behavior before assuming internet docs are needed.
5. **Internet research when necessary**: if local evidence is insufficient or contradicts reality, research the current official docs and credible upstream sources on the web.
6. **Automatic resume**: once the second-opinion path is working again, rerun the needed review if appropriate and resume the original task without asking the user to restart it manually.
7. **Never consult yourself**: always route to the OTHER engine(s), never recurse into the current one.

## Engines Available

| Engine | Verified CLI family | Strengths |
|--------|----------------------|-----------|
| **Codex** (OpenAI) | `codex exec ...` | Code, architecture, computer use |
| **Claude Code** (Anthropic) | `claude -p ...` | Codebase context, multi-file reasoning, implementation review |
| **Gemini** (Google) | `gemini -m ... -p ...` | Long context, multimodal reasoning, broad alternative perspective |

## Verified Learning Base

Before invoking any engine, read:

- `references/verified-learning.md`
- `references/runtime-learning.md`
- `references/learning-overlay.md` when reasoning about convergence with `my-personal-verified-learning-loop`
- `references/shared-learning-adapter-plan.md` for the phased convergence plan and non-goals

These files are the reusable memory for:

- commands that were actually proven to work
- failure signatures that were actually observed
- working fallbacks that were actually re-validated
- outdated paths that were replaced after a real fix
- recent runtime repair incidents that were auto-captured by the runner

Memory split:

- `references/verified-learning.md` = curated durable base for canonical guidance
- `references/runtime-learning.md` = auto-managed incident log written by the runner
- `references/runtime-learning.shared.json` = shared-compatible machine-readable mirror derived from accepted native runner incidents
- `references/runtime-learning.shared.md` = human-readable mirror of the shared-compatible incidents
- `references/learning-overlay.md` = second-opinion-specific overlay for the shared verified-learning doctrine
- `references/shared-learning-adapter-plan.md` = current phased plan for eventual convergence without downgrading the runner
- `scripts/smoke_test_shared_incident_bridge.py` = repo-level smoke test for the shared incident bridge and schema compatibility

**Do not update either from theory.** Update them only after a repaired path succeeds in real behavior.

## Tool Detection — Who Am I?

This skill is context-aware. It detects which tool it is running in and consults the OTHER engine(s).

Primary detection via environment variables:

- `CLAUDECODE=1` → running in Claude Code → consult Codex + Gemini
- `CODEX_CI=1` → running in Codex → consult Claude Code + Gemini
- `GEMINI_CLI=1` → running in Gemini → consult Claude Code + Codex

### Routing table

| Running in... | Engine 1 | Engine 2 |
|---|---|---|
| **Claude Code** | Codex | Gemini |
| **Codex** | Claude Code | Gemini |
| **Gemini** | Claude Code | Codex |

### If detection is missing or ambiguous

1. Prefer explicit positive markers (`CLAUDECODE`, `CODEX_CI`, `GEMINI_CLI`).
2. If they are absent, inspect the current process/CLI context and available binary that launched the session.
3. If the current engine still cannot be established with confidence, stop and report the ambiguity instead of risking a self-consultation loop.

**NEVER consult yourself.** If running in Codex, do not call `codex exec` for the second opinion.

## Routing Decision

### When to use BOTH in parallel

- Critical architectural decisions
- Security-sensitive code review
- Complex debugging with no clear root cause
- When the user explicitly asks for a second opinion
- Any decision with material consequences (money, data, production)

### When to use Gemini ONLY

- Audio analysis
- Video analysis
- When the user explicitly says "ask Gemini"

### When to use Codex ONLY

- When the user explicitly says "ask Codex"
- Quick code-pattern verification where speed matters

### Default

- Use BOTH in parallel

## Post-Implementation Audit Mode

Use `--mode post-implementation-audit` when the goal is no longer to challenge a plan, but to audit a completed implementation against what was supposed to be delivered.

This mode is for:

- non-trivial feature work
- significant refactors
- auth, payment, data, infra, or security-sensitive changes
- any implementation that followed a validated plan
- any situation where the orchestrator wants an independent review of completeness and real-behavior plausibility

Inputs accepted by the runner:

- `--session-cwd <path>` to auto-resolve the latest Claude session tied to that working directory
- `--session-file <path>` for an explicit Claude session file
- `--session-manifest-json <path>` for a precomputed transcript/plan manifest
- `--transcript-file ...` and optional `--plan-file ...` when the caller already knows the exact files
- `--audit-path ...` to constrain git evidence and the audit scope to the relevant files/directories in a dirty repo
- `--audit-report-dir <path>` to persist a durable audit artifact pair (`.json` + `.md`) for later handoff or revalidation
- `--audit-report-prefix <name>` to control the artifact filename stem

How it works:

1. resolve the Claude transcript chain and any referenced plan files
2. collect local git evidence from the working tree
3. ask the other engine(s) to read the transcripts, inspect the code, and compare implementation vs intent through an explicit rubric
4. surface findings, a rubric scorecard, completeness verdict, behavior-confidence verdict, and test recommendations
5. optionally persist a durable audit artifact for later correction / replay / revalidation

Important local heuristics:

- when auto-resolving `--session-cwd`, the helper ignores transcript files under `/subagents/`
- it also ignores sessions generated by this skill's own audit/planning prompts, so it does not recursively audit prior audits
- on dirty repos, prefer `--audit-path` to avoid flooding the review with unrelated changes

Audit rubric used in this mode:

- `Plan coverage`
- `Scope drift`
- `Correctness risk`
- `Runtime confidence`
- `Test adequacy`

What this mode does **not** guarantee:

- it does not claim impossible `100%` certainty
- it does not replace real tests
- it does not treat a clean review as proof that runtime behavior is correct

Treat it as an independent audit layer that detects plan drift, missing pieces, suspicious changes, and unverified runtime assumptions.

Durable audit artifact behavior:

- when `--audit-report-dir` is provided, the runner writes:
  - one `.json` artifact with prompt, manifest, and raw engine results
  - one `.md` artifact with a human-readable handoff summary
- use this when the orchestrator will likely fix findings in a later step or later session
- do not confuse the artifact with proof that the implementation is correct; it is an auditable handoff, not a runtime guarantee

## CLI Usage — Current Verified Paths

### Codex

Primary verified non-interactive pattern:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --output-last-message /tmp/codex-review.txt \
  "Your query here" > /tmp/codex-review.log 2>&1
```

- `exec` is required for headless use.
- `--output-last-message` is the cleanest success signal currently verified on this machine.
- Use `-C <git-root>` instead of `--skip-git-repo-check` when the review really needs a repo-aware working root and you know the actual git root.
- `--json` is available and works, but in the current local environment stdout can still contain startup warnings before the JSON events.
- Exit code `0` plus a populated `--output-last-message` file counts as success even if the log contains non-fatal state-db or MCP startup warnings.

### Claude Code

Primary verified structured-output pattern:

```bash
claude -p "Your query here" --output-format json > /tmp/claude-review.json 2>&1
```

- `-p` is verified locally for headless mode.
- `--output-format json` gives a clean machine-readable result.
- `--output-format text` is acceptable when a plain-text answer is enough.

### Gemini

Current local auth mode observed on this machine:

```bash
~/.gemini/settings.json -> security.auth.selectedType = oauth-personal
```

Primary subscription-backed attempt on this machine:

```bash
gemini -m pro -p "Your query here" --output-format json > /tmp/gemini-review.json 2>&1
```

Verified routing fallback on this machine:

```bash
gemini -m auto -p "Your query here" --output-format json > /tmp/gemini-review.json 2>&1
```

Emergency fixed-model fallbacks:

```bash
gemini -m gemini-3-flash-preview -p "Your query here" --output-format json > /tmp/gemini-review.json 2>&1
gemini -m gemini-2.5-flash -p "Your query here" --output-format json > /tmp/gemini-review.json 2>&1
gemini -m gemini-2.5-pro -p "Your query here" --output-format json > /tmp/gemini-review.json 2>&1
```

- Re-validated locally after upgrading Gemini CLI from `0.33.0` to `0.35.3`.
- `gemini -m pro ...` is the correct subscription-backed first attempt for this skill under `oauth-personal`.
- A fresh runner smoke test on 2026-03-30 succeeded with `gemini -m pro ...`, `response = "OK"`, and `stats.models.main = gemini-3.1-pro-preview`.
- That successful run still reported internal API retries/errors in `stats.models.gemini-3.1-pro-preview.api` (`totalRequests = 4`, `totalErrors = 3`), so treat `pro` as the canonical path but keep bounded retry/backoff behavior.
- `gemini -m auto ...` succeeded in real behavior after the CLI upgrade and kept Gemini on subscription-backed routing. A verified successful run showed:
  - `stats.models.utility_router = gemini-2.5-flash-lite`
  - `stats.models.main = gemini-3-flash-preview`
- `gemini -m gemini-3-pro-preview ...` is not a verified bypass here. In real behavior after the upgrade it also hit `gemini-3.1-pro-preview` capacity failure.
- `gemini -m gemini-3-flash-preview ...` remains a verified fixed fallback with exit code `0` and a usable JSON payload.
- `gemini -m gemini-3.1-flash-lite-preview ...` is also listed in the official Google docs, but in this `oauth-personal` environment it returned `404 ModelNotFoundError`.
- The no-model path is not deterministic enough for this skill. It was observed once to fail with `429 RESOURCE_EXHAUSTED` on `gemini-3-flash-preview`, and later to succeed only after routing through `gemini-2.5-flash-lite` as a utility router while attempting one failed tool call.
- Official Gemini CLI docs state that API key mode is the path for specific model control or paid-tier access. Do not assume behavior verified under `oauth-personal` automatically transfers to `GEMINI_API_KEY` mode, or vice versa.
- If the local environment later exposes `GEMINI_API_KEY`, re-test the current Gemini 3.1 model path in real behavior before replacing the canonical invocation guidance.
- Headless remains the canonical mode for this skill. Interactive `/model` or `/auth` can be useful during diagnosis, but they are not the default repair path because they depend on TUI dialogs and human choices.
- `--output-format json` gives a structured payload with `response` and `stats.models`.
- Current verified fallback order on this machine:
  1. `pro` with bounded retries/backoff
  2. `auto`
  3. `gemini-3-flash-preview`
  4. `gemini-2.5-flash`
  5. `gemini-2.5-pro`
- If `-p` ever becomes deprecated or starts failing, verify the current headless equivalent from local help and upstream docs before changing the skill.

## Output Integrity

These rules are non-negotiable:

1. **Never truncate stdout** with `head`, `tail`, or similar filters before the engine has completed.
2. **Always capture logs to a file** so the failure signature can be inspected and the success signal can be separated from startup noise.
3. **Prefer structured outputs** when the CLI supports them:
   - Codex: `--output-last-message` and optionally `--json`
   - Claude: `--output-format json`
   - Gemini: `--output-format json`
4. **Do not confuse noisy success with failure**. Some CLIs print warnings or startup chatter even when the invocation succeeded.

## Failure Handling — Mandatory Self-Healing Protocol

When an engine call fails, the orchestrator must treat it as an incident in the second-opinion infrastructure.

### Step 1 — Capture the real failure

- Save full stdout/stderr to a file.
- Record the exact command used.
- Record exit code, timeout behavior, and whether any output file was produced.

### Step 2 — Classify the failure

Typical buckets:

- **Local harness bug**: shell quoting, redirection bug, bad variable name, wrong working directory
- **CLI surface drift**: command, flag, or subcommand changed
- **Git topology mismatch**: command assumes a git repo but current cwd is not the git root
- **Auth/session problem**: login expired, permission missing
- **Auth-mode mismatch**: current auth mode does not expose the same model surface as the docs path you are reading
- **Capacity/rate-limit problem**: `429`, `RESOURCE_EXHAUSTED`, temporary backend saturation
- **Non-fatal warning noise**: warnings on stdout/stderr but valid result actually produced
- **Model availability problem**: requested model not found, no access, preview removed

### Step 3 — Retry with the smallest justified fix

Examples:

- fix the shell wrapper instead of blaming the engine
- change `cwd`, add `-C <git-root>`, or add `--skip-git-repo-check`
- switch to structured output instead of parsing noisy stdout
- back off and retry on transient capacity issues
- for Gemini under `oauth-personal`, try `pro` first, but on repeated `MODEL_CAPACITY_EXHAUSTED` degrade to `auto` before falling back to fixed older model IDs
- use a verified fixed-model fallback only when alias routing is degraded or no longer trustworthy

### Step 4 — Inspect local evidence

Before going to the web, inspect:

- `<cli> --help`
- relevant subcommand help (`codex exec --help`)
- local config (`~/.codex/config.toml`, `~/.gemini/settings.json`, Claude settings when relevant)
- current auth mode and whether an API key is actually present
- installed package docs on disk
- the current version (`<cli> --version`)
- any previous verified entries in `references/verified-learning.md`
- any recent incident entries in `references/runtime-learning.md`

### Step 5 — Research the internet if local evidence is insufficient

When the local evidence is incomplete or contradictory:

- research the current official docs first
- then use credible upstream sources such as the official repo, release notes, or issue tracker
- treat third-party blog posts or forum answers as hypotheses until validated locally

### Step 6 — Verify in real behavior

The repair is not complete until an actual invocation succeeds.

Success means:

- exit code is consistent with success
- the expected output file or structured response exists
- the returned payload is usable for the second-opinion workflow

### Step 7 — Persist only the verified learning

After a real successful repair:

1. Let the runner append the real incident to `references/runtime-learning.md`
2. Update `references/verified-learning.md` only if the repair changes the durable canonical path
3. Update this `SKILL.md` only if the canonical guidance changed
4. Replace or mark outdated instructions explicitly

Never save:

- speculative commands
- untested web findings
- "should work" hypotheses

### Step 8 — Resume the original mission automatically

After the repaired path is validated:

1. rerun the second-opinion request if the failed engine missed the review
2. synthesize the responses
3. continue the original task automatically

Do not ask the user to manually restart the task just because the skill had to repair itself.

## Prompt Template

Use the same structured prompt for all engines:

```text
Context: [Project name] ([tech stack]).
Working directory: [pwd]
Relevant docs: CLAUDE.md / AGENTS.md and any local project memory files that matter.
Repository evidence: [paths/lines from prior search]

Task: [specific question]

Constraints: [any constraints]

Please return:
(1) Decisive answer
(2) Supporting citations (file paths:line numbers)
(3) Risks/edge cases
(4) Recommended next steps/tests
(5) Open questions — list uncertainties explicitly
```

## Search-First Checklist

Before querying any external engine:

- [ ] `rg <token>` in the repo for existing patterns
- [ ] skim relevant `CLAUDE.md` / `AGENTS.md`
- [ ] inspect git history if history matters
- [ ] include repository evidence in the prompt
- [ ] read `references/verified-learning.md`
- [ ] read `references/runtime-learning.md`

## Output Discipline

### Single-engine response

Present:

1. Decisive answer
2. Citations
3. Risks/edge cases
4. Next steps
5. Open questions

### Parallel synthesis

Present:

1. **Consensus**
2. **Divergences**
3. **Orchestrator synthesis**
4. **Combined risks**
5. **Unified next steps**

## Verification Checklist

After receiving responses, verify:

- [ ] the invocation path used is still valid on the current machine
- [ ] the answer matches current project conventions
- [ ] the answer does not rely on hallucinated files or APIs
- [ ] the repair, if any, was verified in real behavior
- [ ] any new learning has been persisted only after verification

## Key Principles

1. **Independence**: each consulted engine analyzes without seeing the other's answer
2. **Evidence-based**: require citations, not just opinions
3. **Self-healing**: broken invocation paths are repaired before the orchestrator continues
4. **Verified memory**: only real working paths enter the skill
5. **Transparency**: tell the user which engines were consulted and whether a repair was needed
6. **Pragmatism**: second opinion is for decisions that matter, not trivialities

## Runner Contract

`scripts/second_opinion_runner.py` is the enforcement layer for this skill.

Use it to:

- route to the other engines
- capture logs and structured results
- apply the local retry/fallback policy
- persist runtime-learned repairs after verified success
- run a `post-implementation-audit` against a Claude session + current codebase when requested
- optionally write durable post-implementation audit artifacts for follow-up work

`scripts/claude_session_bundle.py` is the local helper that resolves:

- the latest Claude session for a given working directory
- the full transcript chain through `read the full transcript at: ...`
- any plan-like markdown files referenced in those transcripts
- while skipping self-generated second-opinion audit sessions and `/subagents/` transcript files

Treat a runner result with `needs_web_research = true` as a blocking signal:

1. pause the original task
2. research the upstream CLI/doc changes
3. validate the repaired invocation locally
4. update the curated skill files if the canonical path changed
5. rerun the second-opinion request
6. resume the original task automatically

## Execution Ownership and Automatic Resume

The current orchestrator remains the default executor of the original task. The external engines are advisors unless the user explicitly asks for delegated implementation.

This means:

- the orchestrator pauses only long enough to repair and complete the second-opinion phase
- the orchestrator then resumes the original mission automatically
- the user does not need to issue a second prompt just to restart the interrupted work

## Optional Delegated Execution (explicit user request only)

If the user explicitly asks another engine to implement:

1. prepare a full context package
2. make the delegated call
3. review the result locally
4. run the relevant tests
5. report what was delegated and what was adjusted afterward

For headless delegated execution, prefer engines that can actually modify files in the current environment. Text-only headless advisors remain advisors.

## Post-Implementation Follow-Through

When `post-implementation-audit` returns findings, the orchestrator should:

1. correct the issues or explain why a flagged divergence is intentional
2. run the most relevant real tests for the touched surface
3. re-run the audit if the first pass identified material gaps that were then fixed
4. report what is now verified vs what still remains unverified in runtime

Do not present a post-implementation audit as if it were a substitute for integration, E2E, API, or real-environment testing.

## Relationship to old `codex` skill

This skill supersedes the standalone `codex` skill. All second-opinion work should go through `my-personal-second-opinion`.
