# Verified Learning — my-personal-second-opinion

Only record entries here after the command path was verified in real behavior on the current machine.

## 2026-04-21 — skill surfacing incident does not excuse a skip

Verified evidence:

- `my-personal-second-opinion` existed on disk at `~/.agents/skills/my-personal-second-opinion`
- the Codex and Claude symlink surfaces also existed:
  - `~/.codex/skills/my-personal-second-opinion`
  - `~/.claude/skills/my-personal-second-opinion`
- the active Codex session still did not expose the skill in its live skill inventory
- the canonical runner was then verified directly from Codex with a real smoke:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --current-engine codex \
  --working-directory "$PWD" \
  --smoke-test \
  --timeout-seconds 180 \
  --output-json /tmp/second-opinion-smoke.json \
  --no-persist-learning \
  --no-git-persist
```

Observed behavior:

- Claude returned `OK`
- Gemini recovered through fallback:
  - `gemini -m pro` timed out after 180s
  - `gemini -m auto` then returned `OK`

Implication:

- a missing live skill surface is a blocking infrastructure incident, not permission to skip the rule
- when the on-disk skill exists, the canonical runner must be invoked directly and proved
- the incident must be surfaced explicitly and learned from
- keep `SKILL.md` lean enough to reduce avoidable surfacing/debug friction

## 2026-03-27 — Detection markers

- In Codex Desktop, `CODEX_CI=1` is present and is a valid positive marker for "running in Codex".

## 2026-03-27 — Codex CLI

Verified on this machine:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --output-last-message /tmp/codex-review.txt \
  "Reply with exactly: OK" > /tmp/codex-review.log 2>&1
```

Observed behavior:

- `exec` is required for headless use.
- `--skip-git-repo-check` matters when the current working directory is outside the actual git root.
- `--output-last-message` writes a clean final answer even when stdout contains a large amount of startup noise.
- `--json` works, but stdout still contained local startup warnings before the JSONL events in this environment.
- Exit code `0` plus a populated `--output-last-message` file counted as success even though stdout contained:
  - state database migration warnings
  - MCP startup chatter
  - one non-fatal MCP startup failure (`n8n-official`)

Implication:

- Do not treat Codex startup warnings or a non-critical MCP failure as a second-opinion failure if the final answer file was produced successfully.

## 2026-03-27 — Claude CLI

Verified on this machine:

```bash
claude -p "Reply with exactly: OK" --output-format text
claude -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- `-p` is valid for headless use.
- `--output-format json` returns a clean structured result object.
- `--output-format text` returns the plain answer directly.

Implication:

- Prefer `--output-format json` when the orchestrator needs deterministic parsing.

## 2026-03-27 — Gemini CLI

Observed failure in real behavior:

```bash
gemini -p "Reply with exactly: OK" --output-format json
```

Observed failure signature:

- `429 RESOURCE_EXHAUSTED`
- message: `No capacity available for model gemini-3-flash-preview on the server`

Verified working fallback paths:

```bash
gemini -m gemini-2.5-flash -p "Reply with exactly: OK" --output-format json
gemini -m gemini-2.5-pro -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- both fallbacks returned exit code `0`
- both returned a structured JSON payload with `response` and `stats.models`
- stdout still contained MCP startup chatter and skill-conflict noise before the JSON payload

Implication:

- In the current environment, do not rely on the no-model Gemini path for this skill
- Prefer explicit model selection

## 2026-03-30 — Gemini CLI revalidation

Observed local auth mode:

```bash
~/.gemini/settings.json
{
  "security": {
    "auth": {
      "selectedType": "oauth-personal"
    }
  }
}
```

Observed local CLI version upgrade:

- before revalidation: `gemini --version -> 0.33.0`
- after revalidation: `gemini --version -> 0.35.3`
- package registry at the time of revalidation: `npm view @google/gemini-cli version -> 0.35.3`

Official upstream context checked before reclassification:

- Google Gemini 3 docs list current model IDs including:
  - `gemini-3.1-pro-preview`
  - `gemini-3.1-flash-lite-preview`
  - `gemini-3-flash-preview`
- Gemini CLI docs state that API key mode is the path for specific model control or paid-tier access.
- Gemini CLI docs also state:
  - `gemini -m pro` should prioritize the most capable model available
  - capacity issues on Gemini 3 Pro can require retries or fallback
  - `/model` + **Manual** is the way to inspect whether `gemini-3.1-pro-preview` is exposed interactively

Verified interactive UI facts:

- launching `gemini` interactively showed:
  - `Signed in with Google: benjaminperry69@gmail.com`
  - `Plan: Gemini Code Assist in Google One AI Pro`
- interactive mode also raised folder-trust dialogs before reaching a stable prompt

Implication:

- interactive mode is useful for diagnosis, but it is not a good canonical execution path for an autonomous orchestration skill

Observed failure in real behavior:

```bash
gemini -m gemini-3.1-pro-preview -p "Reply with exactly: OK" --output-format json
```

Observed failure signature:

- `429 RESOURCE_EXHAUSTED`
- message: `No capacity available for model gemini-3.1-pro-preview on the server`
- detail: `MODEL_CAPACITY_EXHAUSTED`

Observed failure in real behavior:

```bash
gemini -m pro -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- after the CLI upgrade, `-m pro` resolved to `gemini-3.1-pro-preview`
- one earlier revalidation run ended in the same capacity failure:
  - `429 RESOURCE_EXHAUSTED`
  - `MODEL_CAPACITY_EXHAUSTED`

Implication:

- `-m pro` is still the correct subscription-backed first attempt under `oauth-personal`
- treat capacity failure as a Google-side availability/routing problem first, not as proof that the invocation syntax is wrong

Observed failure in real behavior:

```bash
gemini -m gemini-3.1-flash-lite-preview -p "Reply with exactly: OK" --output-format json
```

Observed failure signature:

- `404 ModelNotFoundError`
- message: `Requested entity was not found.`

Observed failure in real behavior:

```bash
gemini -m gemini-3-pro-preview -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- after the CLI upgrade, this path was not a stable bypass
- it also ended up failing against `gemini-3.1-pro-preview` capacity on this machine

Implication:

- do not assume `gemini-3-pro-preview` is a safe workaround for `gemini-3.1-pro-preview` under `oauth-personal`

Verified routing fallback path:

```bash
gemini -m auto -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- exit code `0`
- structured JSON payload with `response: "OK"`
- `stats.models.utility_router = gemini-2.5-flash-lite`
- `stats.models.main = gemini-3-flash-preview`

Implication:

- after `pro` capacity failures, `auto` is the best current subscription-backed degradation path on this machine
- prefer it before pinning a fixed older model ID

## 2026-03-30 — Runner smoke tests

Verified runner path:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --smoke-test \
  --current-engine codex \
  --working-directory "/Users/benjaminperry/My Drive/ProStrike Holdings/ProStrike Brands/Lost N Found" \
  --output-json /tmp/second-opinion-codex-smoke.json \
  --no-git-persist
```

Observed behavior:

- target selection respected "never consult yourself":
  - current engine `codex`
  - targets `claude`, `gemini`
- `claude` returned `OK` with `claude -p ... --output-format json`
- `gemini` returned `OK` on the first runner strategy `gemini -m pro ...`
- `stats.models.main = gemini-3.1-pro-preview`
- the same successful Gemini run still reported transient API churn:
  - `totalRequests = 4`
  - `totalErrors = 3`
- no runtime-learning entry was added because the first strategy succeeded from the runner's point of view

Implication:

- `gemini -m pro ...` is now re-verified as a working primary path on this machine
- keep bounded retries/backoff because success can still involve transient backend errors before the final usable answer
- `auto` remains the correct degradation path if `pro` does not end in a usable response

Verified runner path:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --smoke-test \
  --current-engine claude \
  --targets codex \
  --working-directory "/Users/benjaminperry/My Drive/ProStrike Holdings/ProStrike Brands/Lost N Found" \
  --output-json /tmp/second-opinion-claude-smoke.json \
  --no-git-persist
```

Observed behavior:

- `codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --output-last-message ...` returned `OK`
- exit code `0`
- the runner captured the final answer from the output file as intended

Implication:

- the shared runner is verified to execute the Codex, Claude, and Gemini consultation paths successfully in real behavior on this machine

## 2026-04-15 — Claude Code Codex plugin

Observed local plugin surface:

- marketplace/plugin: `openai/codex-plugin-cc`
- installed plugin id: `codex@openai-codex`
- local helper entrypoint:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs
```

Verified local preflight:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs setup --json
```

Observed behavior:

- `ready: true`
- `codex.detail = "codex-cli 0.116.0; advanced runtime available"`
- `auth.loggedIn = true`
- `sessionRuntime.mode = "direct"` when no shared runtime is already active for the current Claude session

Verified read-only review path:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs review --wait
```

Observed behavior:

- succeeded on a real temporary git repo with a working-tree diff
- returned exit code `0`
- returned a usable review body
- stderr contained progress events from the Codex reviewer/runtime, including:
  - thread creation
  - reviewer start/finish
  - shell commands executed by the reviewer

Verified task path:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs task --fresh "Reply with exactly OK and nothing else."
```

Observed behavior:

- succeeded on a real temporary git repo
- returned exit code `0`
- returned `OK`
- stderr contained task-thread lifecycle events:
  - thread ready
  - turn started
  - assistant message captured
  - turn completed

Observed failure in real behavior:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs task --fresh --effort minimal "Reply with exactly OK and nothing else."
```

Observed failure signature:

- `invalid_request_error`
- message: `The following tools cannot be used with reasoning.effort 'minimal': web_search.`

Implication:

- the Claude Code Codex plugin is a legitimate supported Codex access surface on this machine
- the review path is verified and usable
- the task path is also verified and usable when no explicit `--effort minimal` is forced
- for this skill, do not treat the plugin as the canonical orchestration path yet
- if the plugin is used as a Claude-specific fallback or validation surface, avoid `--effort minimal` on `task` until the plugin/runtime contract is revalidated

## 2026-04-15 — Claude Code Codex plugin long-run audit

Verified background task launch:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs task --background --write --fresh "..."
```

Observed behavior:

- returns a queued job payload with:
  - `jobId`
  - `status = "queued"`
  - `logFile`
- `status <job-id>` on a real temporary git repo showed:
  - `queued` -> `running`
  - tracked `threadId`
  - tracked `turnId`
  - live `progressPreview`

Verified cancellation path:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs cancel <job-id> --json
```

Observed behavior:

- returned exit code `0`
- returned:
  - `status = "cancelled"`
  - `turnInterruptAttempted = true`
- `status <job-id>` then reported:
  - `status = "cancelled"`
  - `phase = "cancelled"`
  - `errorMessage = "Cancelled by user."`
- `result <job-id>` returned the stored cancelled job payload
- the target file for the cancelled task was **not** created

Observed long-run task hazard in real behavior:

- one supervised background write task did create the requested file (`plugin-audit-output.txt = "LONGRUN_OK\\n"`)
- but the job remained in `running` state for more than one minute because Codex continued repairing a later verification-side shell failure (`exit 127`)
- implication:
  - observable side effect alone does **not** prove a clean terminal job state
  - `status` must remain the source of truth for terminal state

Verified failure-surfacing path:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs status <job-id> --wait --timeout-ms 120000 --poll-interval-ms 2000 --json
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs result <job-id> --json
```

Observed behavior:

- a real background task terminated as `failed`
- `status --wait` surfaced the terminal failure state correctly
- `result` returned the stored failed payload correctly
- one verified failure message was:
  - `You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 1:54 PM.`

Observed resume mismatch:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs task-resume-candidate --json
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs task --resume-last "Reply with exactly RESUME_OK and nothing else."
```

Observed behavior:

- `task-resume-candidate` reported `available: true` for a failed task with a recorded `threadId`
- `task --resume-last` then failed with:
  - `No previous Codex task thread was found for this repository.`
- local code inspection explains the mismatch:
  - `task-resume-candidate` treats any non-queued/non-running task with `threadId` as resumable
  - `task --resume-last` only resumes tracked tasks in `status === "completed"` before falling back to thread lookup

Observed review-background mismatch:

```bash
node /Users/benjaminperry/.claude/plugins/cache/openai-codex/codex/1.0.1/scripts/codex-companion.mjs review --background --json
```

Observed behavior:

- did **not** return queued background job metadata
- instead returned a direct review payload
- local code inspection confirmed no `background` branch exists for `handleReviewCommand(...)`; only `task` implements true detached background execution

Implication:

- the plugin is suitable as a supervised Claude-specific secondary surface
- the currently verified safe subset is:
  - `setup`
  - `review --wait`
  - `task --fresh` without `--effort minimal`
  - `task --background` only with active supervision
  - `status`
  - `result`
  - `cancel`
- do **not** rely on:
  - `review --background`
  - `task --effort minimal`
  - `task-resume-candidate` alone as proof that `task --resume-last` will succeed
- keep the shared `second_opinion_runner.py` path as the canonical orchestration path for this skill

## 2026-03-30 — Post-implementation audit mode

Verified helper behavior:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/claude_session_bundle.py \
  --cwd "/Users/benjaminperry/My Drive/ProStrike Holdings/ProStrike Brands/Lost N Found/app" \
  --latest \
  --format json
```

Observed behavior:

- the helper auto-resolved a real Claude source session:
  - `/Users/benjaminperry/.claude/projects/-Users-benjaminperry-My-Drive-ProStrike-Holdings-ProStrike-Brands-Lost-N-Found-app/30a94e62-2283-4d02-8baa-e8f867e66759.jsonl`
- after revalidation, it no longer preferred:
  - self-generated second-opinion audit sessions
  - transcript files under `/subagents/`

Implication:

- `--session-cwd` is now usable for the post-implementation audit flow without recursively selecting prior audit transcripts

Verified runner path:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --mode post-implementation-audit \
  --current-engine claude \
  --targets codex \
  --working-directory "/private/tmp/second-opinion-post-impl-sandbox" \
  --session-file "/Users/benjaminperry/.claude/projects/-Users-benjaminperry-My-Drive-ProStrike-Holdings-ProStrike-Brands-Lost-N-Found-app/30a94e62-2283-4d02-8baa-e8f867e66759.jsonl" \
  --audit-path "src/app/[locale]/cookies/page.tsx" \
  --audit-focus "Focus on the cookie-banner regression described in the Claude transcript and on whether the current scoped code actually addresses that diagnosis." \
  --output-json /tmp/second-opinion-post-impl-sandbox-codex.json \
  --timeout-seconds 300 \
  --no-git-persist
```

Observed behavior:

- exit code `0`
- `mode = "post-implementation-audit"`
- `audit_manifest.session_file` matched the real Claude transcript passed in
- `audit_manifest.audit_paths = ["src/app/[locale]/cookies/page.tsx"]`
- `codex exec ... --output-last-message ...` returned a full audit with:
  - findings first
  - completeness verdict
  - behavior-confidence verdict
  - exact fixes / next tests
  - open questions
- on this machine, that successful Codex audit took about `241816 ms`

Implication:

- the new post-implementation audit mode is verified end-to-end in real behavior
- on heavier audits, scope control matters; use `--audit-path` to keep the review focused and avoid unrelated repo noise
- Codex can complete the audit successfully, but heavy post-implementation reviews may need several minutes even on a small scoped repo

## 2026-03-30 — Post-implementation audit rubric and durable artifacts

Verified runner path:

```bash
python3 ~/.agents/skills/my-personal-second-opinion/scripts/second_opinion_runner.py \
  --mode post-implementation-audit \
  --current-engine claude \
  --targets codex \
  --working-directory "/private/tmp/second-opinion-post-impl-sandbox" \
  --session-file "/Users/benjaminperry/.claude/projects/-Users-benjaminperry-My-Drive-ProStrike-Holdings-ProStrike-Brands-Lost-N-Found-app/30a94e62-2283-4d02-8baa-e8f867e66759.jsonl" \
  --audit-path "src/app/[locale]/cookies/page.tsx" \
  --audit-focus "Focus on the cookie-banner regression described in the Claude transcript and on whether the current scoped code actually addresses that diagnosis." \
  --audit-report-dir /private/tmp/second-opinion-audit-artifacts \
  --audit-report-prefix cookie-banner-post-impl \
  --output-json /tmp/second-opinion-post-impl-sandbox-codex-artifact.json \
  --timeout-seconds 300 \
  --no-git-persist
```

Observed behavior:

- exit code `0`
- `mode = "post-implementation-audit"`
- `results[0].success = true`
- `audit_manifest.rubric` was present in the output JSON
- the Codex answer included the requested `Rubric Scorecard` section
- `audit_artifact` was written with both files:
  - `/private/tmp/second-opinion-audit-artifacts/20260330T165353Z-cookie-banner-post-impl.json`
  - `/private/tmp/second-opinion-audit-artifacts/20260330T165353Z-cookie-banner-post-impl.md`
- on this machine, that successful Codex audit with artifact output took about `259125 ms`

Implication:

- the post-implementation audit now has an explicit grading frame instead of a free-form review only
- `--audit-report-dir` is verified as a durable handoff path for later correction or later-session replay
- the artifact should be treated as an auditable handoff, not as proof that runtime behavior is correct by itself

Verified working primary path:

```bash
gemini -m gemini-3-flash-preview -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- exit code `0`
- structured JSON payload with `response: "OK"`
- `stats.models.main = gemini-3-flash-preview`

Observed nondeterministic no-model behavior:

```bash
gemini -p "Reply with exactly: OK" --output-format json
```

Observed behavior:

- one earlier real run failed with `429 RESOURCE_EXHAUSTED` targeting `gemini-3-flash-preview`
- a later real run succeeded, but `stats.models` showed:
  - `utility_router = gemini-2.5-flash-lite`
  - `main = gemini-3-flash-preview`
- that later successful run also recorded one failed tool attempt: `run_shell_command`

Implication:

- For this skill, do not treat the no-model path as deterministic infrastructure
- In the current `oauth-personal` environment, prefer explicit model selection or explicit routing aliases
- Current verified order on this machine:
  1. `pro` with bounded retries/backoff
  2. `auto`
  3. `gemini-3-flash-preview`
  4. `gemini-2.5-flash`
  5. `gemini-2.5-pro`
- `gemini-3.1-pro-preview` is now verified as the current `pro` resolution in real successful behavior here
- `gemini-3.1-flash-lite-preview` should not be promoted in this environment unless it is first re-validated successfully

## Update Rule

When a future invocation path breaks:

1. capture the failure signature
2. repair the path
3. verify the repaired path in real behavior
4. update this file with:
   - date
   - engine and version/context
   - broken path
   - observed failure signature
   - working repaired path
   - verification notes

Do not add speculative or unverified findings.
