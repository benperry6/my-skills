---
name: my-personal-paid-tracking-foundation
description: "[My Personal Skill] Use when a project needs a paid media tracking foundation that is professional but budget-friendly. Trigger for requests about Meta Pixel, TikTok Pixel, GA4, GTM, server-side tracking, CAPI, conversion tracking, audience building before paid spend, tracking architecture for a new SaaS/e-commerce/content site, or deciding what to install now vs later."
---

# My Personal Paid Tracking Foundation

## Overview

This skill chooses the right paid media tracking foundation for a project without defaulting too early to expensive enterprise infrastructure. It is designed to recommend a clear baseline, explain the trade-offs, and then output a concrete implementation plan rather than a vague comparison.

## Trigger Conditions

Use this skill when the user asks any variation of:

- "What tracking stack should I install now?"
- "Do I need Meta Pixel / TikTok Pixel / GA4 / GTM / CAPI?"
- "How do I prepare paid ads before I actually spend?"
- "Should I use browser-side, server-side, or both?"
- "What is the budget-friendly version of a serious paid tracking stack?"
- "What should I install on a new SaaS / e-commerce / affiliate site?"

Do not use this skill for:

- product analytics questions that are not about paid media readiness
- campaign strategy or bidding decisions
- creative generation

## Operating Principle

This skill is opinionated on purpose.

Its job is not to list every possible stack. Its job is to recommend the right foundation for the current context, then explain why that recommendation is the right trade-off now.

The canonical bias is:

1. Start collecting useful signal early
2. Avoid paying for heavy infrastructure before the business is proven
3. Keep a clean upgrade path toward a more industrial setup later
4. Open only the vendors that match the real channel plan, not every vendor that could theoretically matter
5. Prefer CLI/API/MCP orchestration over browser clicking whenever the vendor exposes a credible machine-to-machine path
6. Research the current official docs and API surface on the internet before declaring a vendor "browser-only"
7. Never choose a vendor account, business, profile, or cloud project without explicit user approval when multiple valid options may exist
8. Treat vendor names already present in the skill as examples, not a whitelist; the skill may recommend a niche or newly relevant vendor even if its name does not yet appear anywhere in the skill

## Decision Workflow

### Step 1 — Classify the project

Read:

- `references/project-archetypes.md`
- `references/maturity-stages.md`

Determine and state explicitly:

- project type
- maturity stage
- current acquisition model
- whether paid media is live, planned soon, or purely future-facing

If a project spans multiple models, choose the revenue motion that matters most in the next 6-12 months and call out the secondary motion separately.

### Step 2 — Choose the vendor priority

Read:

- `references/vendor-priority.md`

Default to disciplined rollout. Do not recommend opening a large number of platforms just because they exist.

### Step 3 — Choose the stack recipe

Read:

- `references/stack-recipes.md`

Pick the closest recipe and adapt only where the context clearly justifies it.

### Step 4 — Research the programmatic path first

Read:

- `references/programmatic-bootstrap.md`

Before suggesting any browser work:

- research the current official docs and API surface on the internet for each vendor the recommendation needs
- determine whether a credible programmatic bootstrap path exists
- state clearly what is verified, what is uncertain, and what still needs live validation

If a credible programmatic path exists, do not jump straight to the browser.

### Step 5 — Audit available access and require account approval

Read:

- `references/programmatic-bootstrap.md`
- `references/access-checklist.md`

Inventory any reusable access that already exists on the machine or in the current environment.

This includes, when available:

- machine-global tracking access state under `~/.config/tracking-skills/`
- vendor CLI authentication state
- secure local secret stores such as the macOS Keychain
- live API account/business/project summaries

Then:

- present the accessible account/business/project options
- recommend which one should be used for the current business
- wait for explicit user approval before acting on a specific account

If the user wants a new account or new business-level access, produce the exact bootstrap sequence for creating it.

### Step 6 — Prepare the access and execution checklist

Read:

- `references/access-checklist.md`
- `references/programmatic-bootstrap.md`

Use `scripts/materialize-google-oauth-client.sh` when a Google OAuth client file is stored in secure local storage and must be re-materialized into the standard local path for tooling compatibility.

Separate clearly:

- what the agent can design, wire, and verify
- what the user must provide as accounts, IDs, tokens, admin access, or OAuth/developer authorization
- what canonical naming should be used for vendor access objects and where a shortened variant is required by platform limits

## Canonical Doctrine

Unless the context proves otherwise, the default doctrine is:

- In pre-revenue or validation, do **not** default to a paid sGTM/GCP setup
- Prefer a **hybrid** foundation
- Browser-side is necessary for pixels, audiences, and browser-native signals
- A first-party event store is mandatory
- Server-side should exist early in a selective low-cost form via the existing backend or hosting layer
- A heavier server-side infrastructure is justified only after real traction, sustained spend, or operational pain
- For every vendor, search for a credible programmatic bootstrap path first
- Reuse existing machine-global access when it matches the current business and the user approves it
- For every vendor, target the broadest relevant machine-to-machine permissions the official flow actually exposes, then verify the real scopes and capabilities with live inspection or API probes
- For every vendor, enumerate whatever permissions the official flow exposes at runtime instead of freezing a historical scope list in the skill
- If the official flow exposes a non-expiring or "never expires" token option, prefer it and verify the resulting expiry state after minting
- Browser fallback is acceptable only when the programmatic path genuinely does not exist yet or still has a hard bootstrap gap

This doctrine exists for a business reason, not a tooling reason:

- collect data early
- avoid premature fixed costs
- prepare future paid media without pretending the business is already scaling
- upgrade infra only when the business can justify it

## What the Agent Does vs What the User Must Provide

### The agent should do

- classify the project and maturity stage
- recommend the stack
- explain the why and trade-offs
- define the event model at the right ambition level
- produce the implementation order
- produce the access checklist
- identify when a later infra upgrade becomes justified
- research the current official docs and APIs on the internet before recommending browser work
- detect reusable local access and account state before assuming nothing exists
- present the accessible accounts/businesses/projects and ask for explicit approval before using one
- prefer Google APIs directly when OAuth access exists
- prefer Meta APIs directly once app/token/asset bootstrap exists
- prefer the equivalent machine-to-machine path for any other vendor when it exists
- treat vendors named in the skill as examples, not a closed list, and recommend unnamed vendors too when the business context justifies them
- if a vendor has a programmatic path but the access is missing, ask for the exact missing authorization instead of sending the user straight to the admin UI
- for every vendor, try to issue the broadest relevant machine-to-machine permission set the official flow actually exposes, then verify the granted scopes and live capabilities instead of trusting the UI blindly
- when the official flow exposes permissions dynamically, enumerate the live options and select all relevant ones instead of hardcoding a stale list
- when the official flow exposes token-duration choices, prefer a non-expiring option if it exists and verify the real expiry with a live token inspection call
- persist reusable non-sensitive access state in machine-global storage when useful
- keep vendor-required on-disk auth files only in the standard paths the official tooling expects, with restrictive permissions
- prefer a secure local secret store for secrets and re-materializable bootstrap blobs; prefer 1Password if it is actually available and intended for team/shared secret management, otherwise use the macOS Keychain
- use the browser only for genuine bootstrap gaps or missing machine-to-machine permissions that cannot yet be solved programmatically

### The user must typically provide

- approval of which account / business / cloud project should be used
- account access
- container IDs
- pixel IDs
- tokens / secrets
- DNS or hosting admin access where relevant
- OAuth / developer authorization when a vendor supports API-first bootstrap
- confirmation when a brand-new account or business-level bootstrap is preferred over existing access

Do not blur those two responsibilities in the final answer.

## Output Format

The final output of this skill should always include these sections:

1. **Diagnostic**
   - short classification of the project and current stage
2. **Recommended stack**
   - the opinionated foundation to use now
3. **Why this is the right trade-off now**
   - business and technical justification
4. **Executable plan**
   - ordered next steps
5. **Accounts and programmatic bootstrap path**
   - which accessible accounts/businesses/projects exist
   - which one is recommended
   - which approval or missing authorization is still needed
   - how IDs / tokens / assets should be obtained programmatically and in what order
6. **Storage plan**
   - where reusable non-sensitive access state should live
   - where secrets should live
   - what, if anything non-sensitive, belongs in the project repo
7. **Upgrade criteria**
   - what would justify moving to a heavier stack later

Do not output a neutral vendor matrix unless the user explicitly asks for a comparison. The default must be a recommendation.

## Anti-Patterns

Actively call out these mistakes when relevant:

- paying for enterprise tracking infra before revenue exists
- assuming browser-only is enough
- assuming server-only replaces pixels and browser-side audiences
- opening too many vendors too early
- over-engineering attribution before the business model is proven
- confusing "collecting signal early" with "needing a full enterprise stack immediately"

## Defaults and Escalation

If the user gives little context, default to:

- pre-revenue / validation
- low-cost hybrid setup
- Google and Meta by default
- add any other vendor from day one only if the business model and planned channel justify it
- internet/docs/API research before any browser suggestion
- account-choice approval before touching a specific vendor account

Only escalate beyond that when the context clearly supports it.

If a recommendation depends on a missing fact, state the assumption explicitly instead of hiding it.
