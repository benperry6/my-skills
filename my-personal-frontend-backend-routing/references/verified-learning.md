## 2026-04-21T09:45:43+00:00 - claude-headless-routing-stable-invocation

- Summary: Stable Claude Code frontend delegation uses repo-local scope or --add-dir, prompt immediately after -p, acceptEdits, and a max-turn budget high enough for Read/Write retries.
- Failed path: `Claude Code was misdiagnosed as blocked from a false-negative headless invocation.`
- Repaired path: `Use the proven headless invocation recipe and invoke the learning loop before resuming the blocked delegated task.`
- Source skill: `my-personal-frontend-backend-routing`
- Source session: `2026-04-21-ShopifyMCP_Codex-route-debug`
- Agent: `codex`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-frontend-backend-routing/SKILL.md`
- Evidence: A repo-local JS probe and a copy of the real embedded-admin app.js were both successfully edited by Claude Code headless.
- Evidence: The earlier false failures were explained by outside-cwd targets, prompt ordering, and max-turns too low for Write -> Read -> Write.
