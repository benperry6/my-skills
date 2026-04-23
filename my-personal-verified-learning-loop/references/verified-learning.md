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
## 2026-04-23T18:09:32+00:00 - shared-runtime-path-override

- Summary: record_learning.py now supports explicit runtime path overrides so specialized skills can write shared-schema incidents into a mirror without colliding with a native runtime store.
- Failed path: `Assuming every skill uses references/runtime-learning.json as its shared-schema runtime sink.`
- Repaired path: `Allow explicit --runtime-json-path and --runtime-md-path overrides when the target skill keeps a native runtime store plus a separate shared-compatible mirror.`
- Source skill: `my-personal-verified-learning-loop`
- Source session: `2026-04-24-second-opinion-surfacing`
- Agent: `codex`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/SKILL.md`
- Target file: `/Users/benjaminperry/.agents/skills/my-personal-verified-learning-loop/scripts/record_learning.py`
- Evidence: Using record_learning.py against my-personal-second-opinion default runtime paths failed because that skill stores native runtime records in a different shape.
- Evidence: Writing the same incident to runtime-learning.shared.json/.md succeeded once explicit override paths were supported and used.
- Evidence: my-personal-second-opinion intentionally keeps native persistence authoritative and uses a shared-compatible mirror for cross-skill doctrine.
