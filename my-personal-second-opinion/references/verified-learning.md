# Verified Learning — my-personal-second-opinion

Only record entries here after the command path was verified in real behavior on the current machine.

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
