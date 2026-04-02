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
5. Before any browser action on a third-party platform, explicitly check whether a CLI/API/MCP path exists and actually works with a real probe
6. If that programmatic path exists and works, it becomes the mandatory default; do not use the browser unless the programmatic path is absent, broken, or insufficient for the exact operation
7. Research the current official docs and API surface on the internet before declaring a vendor "browser-only"
8. Never choose a vendor account, business, profile, or cloud project without explicit user approval when multiple valid options may exist
9. Treat vendor names already present in the skill as examples, not a whitelist; the skill may recommend a niche or newly relevant vendor even if its name does not yet appear anywhere in the skill
10. Persist only verified learning: update the skill only after a vendor bootstrap or vendor-flow fix has been proven in real behavior, not just inferred from docs or theory
11. Treat the Google foundation as a connected cluster by default: `GTM web + GA4 + GSC + Google Ads`, keep the Google Analytics Data API available as a support API for CLI-side GA4 verification when GA4 is in scope, then document clearly which parts are already verified programmatically and which parts still have a real UI bootstrap gap
12. For owned-domain site projects, add Bing Webmaster Tools to the recommended search baseline, prefer verification at the authoritative DNS host when the goal is whole-domain ownership rather than a narrower page-level method, and record the actual live vendor method exposed in the real flow; the registrar and the DNS host may differ, and in the currently verified `lostnfound-app.com` flow here the registrar is `Hostinger` while the authoritative DNS host is `Cloudflare`; in the currently verified Bing flow here the method is `CNAME`, the site object itself is URL-based (`https://...`), and no Google Search Console-style `sc-domain:` equivalent has yet been verified in public Bing surfaces here
13. If Google ever requires browser fallback, treat Google account identity as a blocking precondition: verify the active top-right Google account email before touching the page, treat `authuser=*`, `login_hint`, account indexes, or similar session hints as unstable non-authoritative metadata or routing hints rather than proof of identity, prefer opening Google support/vendor flows from an already verified Google service context for the approved account when possible, and stop immediately if the visible browser email is not the explicitly approved Google account
14. Before unblocking, reactivating, or repairing billing / verification on an existing Google Ads client account, inspect current campaign states programmatically when possible; if any campaign is already `ENABLED`, warn the user explicitly that restoring account serving can cause immediate spend and threshold billing to resume, then either pause those campaigns first or get explicit approval to let them continue
15. For Google Ads and similar multi-account structures, use umbrella/admin naming for manager accounts and business-specific naming for the dedicated client accounts; do not name the MCC after a single project, rename temporary probe accounts immediately if they will be kept, and if a legacy or disabled account cannot be removed, mark it explicitly as legacy so it does not look like the active project account
16. Browser-choice instructions are scoped to the exact task, account, or vendor flow they were given for; do not silently persist "use Chrome" or any similar browser override to unrelated later work, and when that scoped task ends revert to the global default browser rule unless the user explicitly broadens the scope
17. When browser fallback is in use and an existing vendor tab is being reused, refresh that tab before drawing conclusions from its state; only skip the refresh when the page was opened by the current investigation moments ago and has not had time to go stale yet

## Canonical Phase Architecture

This skill must reason explicitly in 4 major phases:

### Phase 1 — Prepare the codebase

Adapt the site or app so the paid-tracking foundation can actually exist in code:

- choose the right stack
- define the event model
- wire the codebase in the right order

**Phase-1 completion gate:**

- the codebase-side tracking foundation is specified or implemented clearly enough that vendor assets can be connected to it next

### Phase 2 — Bootstrap vendor access

Give the skill the machine-to-machine access it needs for the approved vendor accounts:

- bootstrap or reuse Google / Meta / other vendor access
- verify the real scopes, permissions, projects, businesses, and tokens
- store reusable access state and secrets in the canonical places

**Phase-2 completion gate:**

- the approved vendor access exists
- the real permissions are verified
- the core vendor APIs respond in real behavior

### Phase 3 — Create, connect, and administer vendor assets

Use the verified vendor access to operate the real vendor layer:

- create or manage assets such as ad accounts, pixels, datasets, tags, and related objects
- link the relevant Google services together when the API path is real and verified
- connect the vendor assets to the codebase-side implementation from phase 1

**Phase-3 completion gate:**

- the required vendor assets and inter-service links are proven in real behavior, not just documented

### Phase 4 — Verify live data flow and debug runtime issues

Prove that the implemented tracking actually sends usable data in real conditions:

- verify browser-side vendor loading after consent where relevant
- verify server-side or first-party relays when they are part of the architecture
- verify final vendor ingestion via CLI/API when a credible programmatic path exists
- document the verified debugging path so future projects can reuse it without re-researching the same vendor behavior

**Phase-4 completion gate:**

- the important runtime data flows are proven in real behavior with the strongest available verification path
- any remaining vendor-side verification gaps are explicitly labeled as real platform limitations, not silent uncertainty

### Mandatory phase guardrails

- `Phase 2 complete` does **not** mean `Phase 3 complete`
- `Phase 3 complete` does **not** mean `Phase 4 complete`
- a default vendor cluster such as `GTM web + GA4 + GSC + Google Ads` does **not** mean every inter-service link is already verified
- creating or linking an asset is not the same thing as proving live data ingestion
- every final answer should label each phase explicitly as `complete`, `partially complete`, or `unverified`

## Decision Workflow

The workflow below supports the 4-phase architecture above. When execution begins, always map the work back to `Phase 1`, `Phase 2`, `Phase 3`, or `Phase 4` explicitly instead of treating the whole skill as one undifferentiated block.

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
- verify with a real read/write probe that the CLI/API/MCP path actually works from the current machine and credentials when that is possible
- state clearly what is verified, what is uncertain, and what still needs live validation

If a credible programmatic path exists and the real probe works, the browser is no longer the default fallback. Use the programmatic path unless it is genuinely absent, broken, or insufficient for the exact operation, and if browser fallback still becomes necessary explain why the programmatic path was not enough.

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
- for Google Ads-like hierarchies, what the canonical manager-account name, project client-account name, and legacy-account labeling strategy should be before any assets are created

### Step 7 — Update the verified learning base

Read:

- `references/programmatic-bootstrap.md`
- `references/access-checklist.md`
- `references/runtime-verification.md`

When a vendor was not documented before, or when a documented flow had become outdated and had to be debugged:

- research first
- execute the bootstrap or fix
- verify the result in real behavior
- only then update the skill references with the concise verified learning

Do not save theoretical findings, untested doc snippets, or speculative fixes into the skill.

### Step 8 — Execute runtime verification

Read:

- `references/runtime-verification.md`

When Phase 3 work appears complete:

- choose the strongest available verification path for each important vendor flow
- prefer CLI/API verification when the vendor exposes it and it works from the current machine
- use browser/runtime observation only when it is genuinely needed
- separate clearly:
  - asset/admin proof
  - runtime/browser proof
  - final vendor-ingestion proof
- save the verified runbook only after the proof works in real behavior

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
- For Google specifically, the default cluster is `GTM web + GA4 + GSC + Google Ads`; do not silently drop `GSC` or `Google Ads` from the default baseline once Google is part of the approved foundation
- For search-relevant owned-domain projects, extend the default search baseline with `BWT`
- When the goal is whole-domain ownership, prefer verification at the authoritative DNS host over narrower page-level or subfolder-level methods; the registrar and the DNS host may differ, and in the currently verified `lostnfound-app.com` flow here the registrar is `Hostinger` while the authoritative DNS host is `Cloudflare`; in the currently verified Google Search Console flow that method is `DNS TXT`, and in the currently verified Bing Webmaster Tools flow that method is `CNAME`
- Do not assume Bing exposes a Google Search Console-style domain-property object; in the currently verified Bing flow here the owned site still appears as a URL entry (`https://lostnfound-app.com/`)
- If Google requires browser fallback because a bootstrap gap is real, verify the active Google account email in the top-right account switcher before any action, do not use `authuser=*` or account-index numbers as identity proof, and do not proceed until that visible browser email matches the explicitly approved Google account
- When a new vendor bootstrap succeeds in real behavior, or when an outdated vendor flow is corrected and re-verified, update the skill so that future projects can reuse the verified path instead of repeating the same research
- If research findings do not work in real conditions, do not add them to the skill; keep debugging until a real working path is verified or leave the gap explicitly marked as unverified
- Browser fallback is acceptable only when the programmatic path genuinely does not exist yet or still has a hard bootstrap gap
- Runtime verification is a first-class phase of the workflow, not an optional polish step after implementation

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
- if Google requires browser fallback, verify the currently selected Google account email in the page chrome itself before doing anything, never rely on `authuser=*` or account-index numbers to identify the right Google account, and treat a mismatch between the visible browser email and the approved Google account as a hard stop rather than a recoverable detail
- when a new vendor or a repaired vendor flow is proven in real behavior, add the concise verified learning to the skill references so it becomes reusable across future projects
- when a documented vendor flow no longer works, treat the docs as potentially outdated, re-research it, debug it in real conditions, and replace the outdated instructions only after the new path is verified
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
   - explicit phase status for `Phase 1`, `Phase 2`, `Phase 3`, and `Phase 4`
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
