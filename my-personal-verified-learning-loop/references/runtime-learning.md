# Runtime Learning

## 2026-04-21T09:45:29+00:00 - route-repair-closeout

- Summary: When a repaired route unblocks the main task, persist the learning before resuming; a user reminder counts as a trigger miss.
- Status: repaired
- Confidence: high
- Record ID: `d6db3fde84354739`
- Failed path: `Learning loop not applied proactively after Claude Code route debugging in ShopifyMCP_Codex.`
- Repaired path: `Add an explicit before-resume checkpoint and treat user reminders as trigger-miss evidence.`
- Source skill: `my-personal-verified-learning-loop`
- Source session: `2026-04-21-ShopifyMCP_Codex-route-debug`
- Agent: `codex`
- Target files:
  - `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/SKILL.md`
  - `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/references/triggering-rules.md`
  - `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/references/runtime-hooks.md`
  - `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/references/implementation-checklist.md`
- Canonical change candidate: `true`
- Evidence: User explicitly pointed out that auto-learning should have been applied proactively after the route repair.
- Evidence: Claude Code route debugging ended with a repaired path that was ready for reuse before the learning loop was run.
- Note: This incident is reusable doctrine, not project memory.
