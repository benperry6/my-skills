# Runtime Learning

## 2026-04-21T09:45:29+00:00 - claude-headless-routing-stable-invocation

- Summary: Claude Code headless routing can false-fail from wrong cwd scope, wrong prompt placement, or too-low max-turns; use the stable invocation recipe.
- Status: repaired
- Confidence: high
- Record ID: `b6c34bc30003faab`
- Failed path: `Claude Code frontend delegation was judged blocked before validating cwd scope, prompt placement, and max-turn budget.`
- Repaired path: `Use repo-local target paths, prompt immediately after -p, acceptEdits, and max-turns >= 5; use --add-dir for files outside cwd.`
- Source skill: `my-personal-frontend-backend-routing`
- Source session: `2026-04-21-ShopifyMCP_Codex-route-debug`
- Agent: `codex`
- Target files:
  - `/Users/benjaminperry/.agents/skills/my-personal-frontend-backend-routing/SKILL.md`
- Canonical change candidate: `true`
- Evidence: Repo-local JS probe in embedded-admin succeeded with Claude Code headless using acceptEdits and sufficient max-turns.
- Evidence: Verbose trace showed initial Write failed because the file had not been read yet, then Read -> Write succeeded.
- Note: This was a route-debug incident, not a frontend implementation failure.
