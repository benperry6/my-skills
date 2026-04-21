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
## 2026-04-21T10:17:14+00:00 - claude-headless-large-file-routing

- Summary: Stable Claude Code frontend delegation uses --tools, not --allowedTools, and large-file edits need exact excerpts/anchors because --no-session-persistence does not suppress SessionStart bootstrap here.
- Failed path: `Claude Code frontend delegation was still treated as effectively blocked because large-file tasks either hung, spent turns on SessionStart/bootstrap, or attempted full-file Read calls that exceeded the token cap.`
- Repaired path: `Use repo-local Claude Code headless with prompt immediately after -p, --permission-mode acceptEdits, --tools Read,Edit,Write (optionally Grep while debugging), and targeted excerpts/anchors for large files; do not rely on --no-session-persistence to remove SessionStart bootstrap in this environment.`
- Source skill: `my-personal-frontend-backend-routing`
- Source session: `2026-04-21-ShopifyMCP_Codex-route-debug-2`
- Agent: `codex`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-frontend-backend-routing/SKILL.md`
- Evidence: The successful queue debug session used --tools Read,Edit,Write,Grep and produced real edits on _route_debug_queue_app_tools.js before stopping only on max_turns.
- Evidence: A separate probe showed --no-session-persistence still emitted the previous-session summary and SessionStart/superpowers bootstrap in this environment.
- Evidence: The no-session probe also showed a full-file Read on a 25k-token JS file can fail before narrowing, which is avoided by supplying exact excerpts or grep anchors.
