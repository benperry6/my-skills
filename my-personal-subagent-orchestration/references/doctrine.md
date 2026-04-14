# Subagent Orchestration Doctrine

Use this reference when you need a reusable orchestration policy that survives provider quirks and session detachment.

## 1. Treat orchestration as its own problem

There are two separate layers:

- the business task
- the orchestration of delegated workers

Mixing them into the same worker prompt usually degrades both.

The orchestrator should keep the lifecycle policy.
Workers should keep the execution task.

## 2. Choose the right unit of delegation

Good delegated units are:

- self-contained
- independently checkable
- unlikely to collide on the same files or evidence
- small enough to finish without constant steering

Typical good units:

- one locale
- one review surface
- one hypothesis
- one module

Typical bad units:

- "do everything about this project"
- cross-cutting edits in the same files by many workers
- deeply sequential subtasks

## 3. Worker prompt discipline

Keep worker prompts narrow.

The default shape is:

- what the worker owns
- what artifact or deliverable it must produce
- any local constraints that materially change the output

Do not put the following inside the worker prompt unless absolutely required:

- retry policy
- polling cadence
- inactivity thresholds
- run-registry instructions
- downstream evaluator rules

## 4. Spawn policy

Default policy:

- spawn one worker per bounded unit
- launch all independent units in parallel by default
- keep inherited/default model settings

Only override model or reasoning when:

- the user asked for it
- the provider-specific skill explicitly requires it
- there is a verified technical reason to do so

## 5. Supervision policy

Default policy:

- supervise on a measured cadence such as every 2 to 5 minutes
- under 10 minutes without visible progress is not a death signal by default
- do not interrupt a worker only because it looks quiet for a few minutes

Warm-up is normal.
Provider UIs often show quiet periods before a worker emits the next visible step.

## 6. Death and replacement policy

A worker becomes a replacement candidate only when all of the following are true:

- there has been more than 10 minutes without observable activity or progress by default
- the run registry shows no newer observation or progress timestamp
- local artifacts show no real movement
- recovery or reattachment was attempted first when supported

If replacement is needed:

- create a new attempt number
- link it to the prior attempt with `replacement_of`
- record why the prior attempt was replaced

## 7. Durable run registry

Every delegated run needs one registry outside ephemeral UI state.

This registry exists so a later session can recover the run even if:

- the app was closed
- the terminal was closed
- the visual parent/child attachment is gone
- a quota incident interrupted the run

The orchestrator should update the registry after:

- spawn
- observation
- recovery attempt
- respawn
- verifier result
- evaluator decision
- final acceptance or rejection

## 8. Resume ladder

When reopening a run:

1. load the registry
2. identify non-terminal attempts
3. inspect local artifacts for evidence of completion or progress
4. check recorded timestamps against the inactivity threshold
5. recover or reattach if possible
6. only then decide to wait or respawn

Do not jump straight from "the UI is detached" to "the worker is dead".

## 9. Orchestrator duty cycle

The orchestrator should not stop after the initial spawn wave.

It stays active until:

- all units are accepted or rejected
- all required follow-up workers have completed
- the registry is left in a clean resumable state

If the orchestrator must stop before full completion, it should leave:

- the registry path
- the current phase per unit
- the last known blocker
- the next recovery step

## 10. Honesty rule

Never claim that delegated work is complete because:

- a worker said it was done
- the UI looked quiet
- the session detached
- the orchestrator spawned the workers successfully

Completion depends on the acceptance rule for the task, not on the existence of a worker message.
