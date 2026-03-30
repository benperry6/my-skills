# Programmatic Bootstrap

Use this file when moving from recommendation to actual provider access and configuration.

## Canonical Rule

For every provider:

1. Search the current official docs and API surface first
2. Determine whether a credible CLI, API, MCP, or local-wrapper path exists
3. Reuse existing access if it already exists and the user approves the account, business, or zone choice
4. Ask for the exact missing authorization if the path exists but access is incomplete
5. Use the browser only when the programmatic path is genuinely missing or blocked by a real bootstrap gap
6. If the official docs expose options dynamically, inspect the live options instead of relying on a frozen historical list

Do not treat providers already named in the skill as a whitelist.

## What To Check Before Assuming Access Is Missing

- Existing local wrapper scripts
- Existing MCP integrations
- Existing CLI login state
- Keychain items or secure local secret stores
- Live account, business, project, or zone listing APIs
- Local config files that point to reusable access

## Read-Only First

Before changing anything:

- verify the auth path
- list the available accounts, businesses, projects, or zones
- identify the exact target object
- snapshot the current state where possible

If there are multiple valid targets, present them and ask for approval before acting on one.

## Live-Docs Rule

When a provider capability is not already documented in this skill:

1. Check the official docs and the live API surface
2. Check local CLI `--help` output if a CLI is in play
3. Prefer the provider's own docs over third-party summaries
4. If docs and real behavior diverge, trust the real behavior and keep debugging
5. Persist only the path that is proven locally

## Verified Learning Update Loop

Use this rule whenever:

- a newly relevant provider is not documented yet
- a previously documented provider flow no longer works
- a local wrapper or auth path changes

Workflow:

1. Research the current official docs and API surface
2. Try the best programmatic path first
3. If the path fails, debug it in real conditions instead of assuming the docs are right
4. Record the finding in `runtime-learning.md`
5. Promote it to `verified-learning.md` only after a real working path has been verified
6. If the path is still unresolved, leave the gap marked as unverified instead of polluting the skill with theory

## Account-Choice Rule

Before touching any provider account:

- inventory the accessible accounts, businesses, projects, or zones first
- present the options
- recommend the best-fit option for the current business
- wait for explicit user approval if the choice is not already obvious and approved

## Browser Identity Rule

If a real bootstrap gap forces browser fallback:

- verify the currently active account identity in the browser UI itself
- do not trust URL hints, session indexes, or stale assumptions
- stop on ambiguity rather than acting in the wrong account

## Storage Convention

- reusable non-sensitive access state may live in machine-global storage
- secrets should live in a secure local secret store such as the macOS Keychain
- files that tooling requires on disk may stay in the standard config paths that tooling expects, with restrictive permissions
- skill references should document the path, not store live credentials
