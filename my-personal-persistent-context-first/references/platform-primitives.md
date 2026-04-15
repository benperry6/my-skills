# Platform Primitives

This file separates what is officially documented from what is only inferred or locally verified.

## Codex — locally verified in the current environment

The current Codex environment already verifies these primitives:

- `AGENTS.md` files are local instruction files with repo-tree scoping
- deeper repo instructions apply to the repo they target
- skills trigger from their `SKILL.md` metadata and explicit naming
- creating or updating a skill belongs in the skills repo, not in an arbitrary product repo

These are environment facts for the current Codex session, even if the public docs found through search are less explicit.

## Codex — public official positioning

The public OpenAI material confirms the general shape:

- Codex is designed to work inside real repos and agent workflows
- instruction files such as `AGENTS.md` are the right native place for durable repo guidance

Official source to consult again if needed:

- [Introducing Codex | OpenAI](https://openai.com/index/introducing-codex/)

## Claude Code — officially documented primitives

Anthropic publicly documents:

- `CLAUDE.md` memory files for user/project instructions
- `/memory` as the command to inspect or edit loaded memory files
- hooks and permission management as first-class controls in Claude Code

Official entry points:

- [Manage Claude's memory | Anthropic](https://docs.anthropic.com/de/docs/claude-code/memory)
- [Slash commands | Anthropic](https://docs.anthropic.com/it/docs/claude-code/slash-commands)

The exact file hierarchy and control-plane behavior can evolve, so recheck the official docs when precision matters.

## Google Antigravity — officially documented primitives

The public Antigravity codelab documents the broad workflow shape:

- planning mode
- implementation plan
- task list
- walkthrough
- rules and workflows as configurable guidance

Official public source:

- [Getting Started with Google Antigravity | Google Codelabs](https://codelabs.developers.google.com/getting-started-google-antigravity?hl=zh_tw)

## Important limitation

There is not enough public official documentation to claim that Antigravity, Claude Code, or Codex already publish this exact "persistent-context first" doctrine as a turnkey standard.

This skill therefore does two things at once:

1. reuse the real official primitives
2. harden them into a stronger repo doctrine for transcript-to-implementation handoff

That hardening is deliberate transposition, not a fake quote from platform docs.
