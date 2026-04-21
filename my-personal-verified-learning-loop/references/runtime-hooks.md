# Runtime Hooks

Use explicit hooks instead of hoping an agent will always notice novelty by itself.

## Standard hooks

### `on_failure`

Fire when:

- a documented path fails
- a meaningful step breaks in real behavior

Capture:

- failing path
- failure evidence
- whether this contradicts current doctrine

### `on_repair_success`

Fire when:

- a repaired path succeeds after failure
- an undocumented fallback becomes proven
- a route, permissions issue, inventory issue, or delegation surface was repaired and the blocked task can continue again

Capture:

- failed path
- repaired path
- proof of success
- whether canonical guidance may need an update
- whether the primary user task is still waiting and therefore the learning must be persisted before resuming it

### `on_user_correction`

Fire when:

- the user corrected the doctrine
- the user supplied a crucial real-world nuance absent from the skill

Capture:

- what changed
- whether this is reusable doctrine or only project context

### `on_run_end`

Fire when:

- the run completed and the final successful path differed from the starting doctrine
- unresolved runtime incidents would otherwise be lost at session end

Capture:

- final path
- whether the divergence was material
- any unresolved runtime items that still need follow-up

### `before_resume_primary_task`

Fire when:

- the run temporarily detoured into debugging the agent's own execution surface
- that debug path is now repaired
- the original user task is about to resume

Capture:

- what was repaired
- what durable guidance must be written before resuming
- whether the repair should stay runtime-only or be promoted immediately

## Hook discipline

Hooks do not all need to be active in every skill.

The shared loop defines the names.
The downstream skill decides which ones matter and what extra fields they need.
