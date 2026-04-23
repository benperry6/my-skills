---
name: my-personal-second-opinion
description: "[My Personal Skill] Use when Claude Code, Codex, or Gemini needs a blocking second opinion on a plan, implementation, architecture, or deep technical decision. Routes only to the OTHER engines, repairs broken cross-engine invocations before continuing, and must never degrade silently. For shared runtime-learning doctrine, see my-personal-verified-learning-loop."
---

# Second Opinion — Multi-Engine Verification

Use this skill when the current engine needs an independent review from the other engines before trusting a plan, an implementation, or a high-stakes technical decision.

## Canonical entry point

Do not re-implement the orchestration ad hoc. Use the shared runner:

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
  --audit-report-dir .claude/audits \
  --output-json /tmp/second-opinion-post-impl.json
```

## If the skill is not surfaced in the active session

This is a blocking infrastructure incident.

Do not silently skip the second opinion.

If the skill is missing from the live skill inventory but exists on disk at `~/.agents/skills/my-personal-second-opinion`:

1. say explicitly that the surfacing layer is broken
2. verify the on-disk skill and symlink surface first
3. if you only need a fast surfacing preflight, run the doctor with `--skip-smoke`
4. if that preflight passes, treat this as a surfacing-layer omission, not proof that the skill itself is broken
5. run the canonical runner directly
6. keep proof of the diagnosis and the runner result
7. record the learning instead of pretending the rule was satisfied

Use the doctor helper when needed:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/doctor.py \
  --current-engine codex \
  --working-directory "$PWD"
```

For a fast surfacing-only preflight:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/doctor.py \
  --current-engine codex \
  --working-directory "$PWD" \
  --skip-smoke
```

Use the full smoke only when runner health itself is uncertain.

## Core doctrine

1. No silent degradation. If this skill is required, do not continue with only one surviving engine unless the user explicitly asked for that.
2. Never consult yourself. Route only to the other engines.
3. Repair first. If a cross-engine path is broken, repair that before resuming the task.
4. Local evidence first. Prefer real CLI behavior, local config, and local logs before web research.
5. Verified learning only. Persist durable learning only after a repaired path worked in real behavior.
6. Automatic resume. Once the path is repaired, rerun the needed review and resume the original mission.

## Routing

### Detect the current engine

Primary markers:

- `CLAUDECODE=1` → current engine is Claude
- `CODEX_CI=1` → current engine is Codex
- `GEMINI_CLI=1` → current engine is Gemini

If detection is ambiguous, stop and report the ambiguity instead of risking a self-consultation loop.

### Default targets

| Current engine | Consult |
|---|---|
| Claude | Codex + Gemini |
| Codex | Claude + Gemini |
| Gemini | Claude + Codex |

Default behavior: use both other engines in parallel.

## When to use

Use this skill when:

- a plan is about to be validated
- a user explicitly asks for a second opinion
- an architectural decision has real cost or risk
- a bug is subtle enough that an independent view matters
- an implementation needs a completeness audit after coding
- a security, money, data, or production risk needs adversarial review

## Standard workflow

1. Gather the exact prompt or plan to review.
2. Run the canonical runner with the correct `--current-engine`.
3. Let the runner consult only the other engines.
4. Inspect the JSON result and the per-engine logs.
5. If one engine failed and was repaired, keep that evidence.
6. Summarize agreements, disagreements, and required follow-up.

## Post-implementation audit workflow

Use `--mode post-implementation-audit` when the work has already been coded and the question is whether the delivered implementation really matches the intended plan.

Important inputs:

- `--session-cwd` to locate the relevant Claude transcript chain
- `--session-file` when the exact transcript is already known
- `--audit-path` to constrain review in a dirty repo
- `--audit-report-dir` to persist a durable JSON + Markdown handoff artifact

The audit rubric is:

- `Plan coverage`
- `Scope drift`
- `Correctness risk`
- `Runtime confidence`
- `Test adequacy`

## Failure handling

### Expected categories

- `cli-missing`
- `cli-surface-drift`
- `auth`
- `git-topology`
- `capacity`
- `model-unavailable`
- `timeout`

### What to do

- inspect the attempt logs first
- prefer the next locally verified fallback before inventing a new path
- if local evidence is insufficient, research the official docs
- only then update durable learning

Do not ask the user to restart the task just because the second-opinion plumbing had to be repaired.

## What the runner guarantees

The runner:

- calls only the other engines by default
- records per-attempt logs
- applies the verified fallback chain
- persists runtime learning only after a real repaired success
- can write durable audit artifacts in post-implementation mode

## Required references

Read these before changing doctrine:

- `references/verified-learning.md`
- `references/runtime-learning.md`
- `references/learning-overlay.md`
- `references/shared-learning-adapter-plan.md`

For the shared learning contract, see `my-personal-verified-learning-loop`.

## Verification before claiming it works

At minimum, prove:

1. the on-disk skill exists
2. the Claude and Codex symlink surfaces are correct
3. `second_opinion_runner.py --help` works
4. if runner health is in doubt, a smoke test succeeds in real behavior

The doctor helper performs that preflight.

## Non-goals

This skill does not replace:

- project memory
- product memory
- normal tests
- human judgment about whether the review evidence is enough

It is an independent review layer, not proof that the code is correct.
