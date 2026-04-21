# Triggering Rules

This reference exists because the hardest part of auto-learning is not promotion.

It is deciding when the learning loop should run at all.

## Core rule

Do not depend on hidden chain-of-thought.

Instead, trigger learning from explicit runtime checkpoints and explicit event classes.

This is the key lesson to borrow from systems like Hermes:

- learning becomes reliable when memory/skill updates are explicit runtime actions
- learning becomes unreliable when it depends on hoping the model will remember to self-report something important

## Trigger classes

Run the learning loop when one or more of these happened:

### 1. Documented path failed

Examples:

- command in the skill no longer works
- wrapper path is outdated
- provider flow drifted
- auth assumptions were wrong in real behavior

### 2. Undocumented path worked

Examples:

- a new CLI invocation succeeded
- a new provider path succeeded
- a better fallback was found and verified

### 3. User correction changed the execution path

Examples:

- the user said the current doctrine was wrong
- the user gave a correction that materially changed the successful path
- the user explained a real-world nuance absent from the current skill

### 4. Non-trivial workflow was discovered

Examples:

- several steps had to be chained before the task worked
- the real flow was not obvious from the current skill
- a reusable operational sequence emerged from the debugging process

### 5. Repaired path differs from canonical guidance

Examples:

- the skill says "A first" but the environment now requires "B first"
- the skill says "browser-only" but programmatic path is now verified
- the skill says "use command X" but only command Y works now

### 6. Mandatory skill surfacing failed

Examples:

- a required skill is missing from the active tool inventory even though it exists on disk
- the symlink/install surface is healthy, but the live session still cannot invoke the skill normally
- a canonical runner had to be called directly because the skill itself was not surfaced to the agent

## Checkpoints

Check for triggers at explicit moments:

- immediately after a meaningful failure
- immediately after a meaningful repair succeeds
- immediately after discovering that a mandatory skill is not surfaced in the current live session
- after a user correction changed the course of execution
- at the end of a run if the final successful path differed from the starting doctrine
- before closing the session if unresolved runtime incidents would otherwise be lost

## Non-triggers

Do not trigger the learning loop just because:

- the run was long
- the model thought hard
- a small one-off project detail appeared
- a normal successful run followed the current doctrine exactly

## Minimal triggering heuristic

If you need one simple question, use:

"Did this run materially contradict, extend, or repair the skill's current reusable doctrine?"

If yes, trigger the loop.
If no, do not.
