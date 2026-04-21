## 2026-04-21T09:45:43+00:00 - route-repair-closeout

- Summary: After repairing a route or execution surface that unblocks the main task, persist learning before resuming; user reminder is evidence of a trigger miss.
- Failed path: `The repaired route was ready, but the learning loop had not been invoked proactively.`
- Repaired path: `Use an explicit before-resume checkpoint in the learning loop and treat user reminders as trigger evidence.`
- Source skill: `my-personal-verified-learning-loop`
- Source session: `2026-04-21-ShopifyMCP_Codex-route-debug`
- Agent: `codex`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/SKILL.md`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/references/triggering-rules.md`
- Evidence: The user had to explicitly remind the agent to apply the auto-learning logic after the route debug.
- Evidence: The route repair was real and reusable, so the omission was in trigger discipline rather than in missing evidence.
