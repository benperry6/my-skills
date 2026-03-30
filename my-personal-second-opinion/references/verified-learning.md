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
- repeated retries still ended in the same capacity failure:
  - `429 RESOURCE_EXHAUSTED`
  - `MODEL_CAPACITY_EXHAUSTED`

Implication:

- `-m pro` is still the correct subscription-backed first attempt under `oauth-personal`
- but on this machine today it is not yet a stable successful path
- treat this as a Google-side capacity/routing problem first, not as proof that the invocation syntax is wrong

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
- `gemini-3.1-pro-preview` remains worth retrying during future repair incidents, but it is not a verified default until it succeeds in real behavior here
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
