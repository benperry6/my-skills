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
- Current verified fallback order:
  1. `gemini-2.5-flash`
  2. `gemini-2.5-pro`

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
