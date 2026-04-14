# Provider Notes

These notes are here to prevent false certainty about session and subagent behavior.

Provider semantics evolve.
Use the current provider docs when behavior looks different from these notes.

## OpenAI Codex

Current verified notes from OpenAI's official docs:

- the Codex app says agents run in separate threads organized by projects
- the Codex app says it picks up session history and configuration from the CLI and IDE extension
- the Codex help docs say delegated work can run in the background

Operational implication:

- visual attachment in the current app window is not the same thing as task persistence
- a detached worker may still have a durable transcript or resumable session behind it
- keep a run registry anyway; do not rely on the UI alone

## Anthropic Claude Code

Current verified notes from Anthropic's official docs:

- subagents run in their own context window and return results to the main session
- agent teams are experimental and have known limitations around session resumption, task coordination, and shutdown behavior
- Claude Code supports `claude --resume`, and its docs mention background summarization for resume support

Operational implication:

- context isolation is real, but resumability guarantees differ by mechanism
- do not assume a lost visual link means a worker disappeared
- also do not assume a detached teammate can always be reattached cleanly
- use the registry and local artifacts as the source of truth

## Gemini CLI

Current verified notes from Gemini CLI docs:

- session history is automatically saved per project and can be resumed with `--resume`
- subagents are experimental and operate in a separate context loop
- checkpointing stores conversation and file-state artifacts locally before write operations when enabled

Operational implication:

- Gemini offers durable local recovery primitives
- subagent behavior is still marked experimental, so orchestration should stay conservative
- record session ids, transcript paths, and artifact paths whenever discoverable

## Cross-provider rule

Do not write orchestration doctrine that assumes:

- UI attachment is durable
- all spawned workers survive app closure the same way
- every provider can reattach to detached workers symmetrically

Instead, standardize on:

- durable registry
- explicit timestamps
- explicit terminal states
- local artifact inspection before acceptance or respawn
