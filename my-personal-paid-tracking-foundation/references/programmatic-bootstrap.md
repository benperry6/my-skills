# Programmatic Bootstrap

Use this file when moving from "what should we install?" to "how do we obtain access and assets without defaulting to the browser?"

## Canonical rule

For every vendor:

1. Search the current official docs and API surface on the internet first
2. Determine whether a credible CLI/API/MCP path exists
3. Reuse existing access if it already exists and the user approves the account choice
4. Ask for the exact missing authorization if the path exists but access is incomplete
5. Use the browser only when the programmatic path is genuinely missing or blocked by a real bootstrap gap

Do not treat Meta as a special exception. Apply the same logic to Google, Meta, TikTok, LinkedIn, Microsoft, Reddit, Pinterest, Snap, or any other vendor that becomes relevant.

## Account-choice rule

Before touching any vendor account:

- inventory the accessible accounts/businesses/projects first
- present the options
- recommend the best-fit option for the current business
- wait for explicit user approval

If the user says the work must happen on a brand-new account or a different partner-owned account, switch into bootstrap mode and document that sequence instead of silently using an existing personal account.

## What to inspect before assuming access is missing

- machine-global tracking access state such as `~/.config/tracking-skills/`
- vendor CLI login state
- secure local stores such as the macOS Keychain
- live account / business / project listing APIs

## Cross-vendor validation rule

For every vendor, verify the resulting access in real conditions:

- inspect the granted scopes, roles, or capabilities
- check expiry where relevant
- probe the live API for the expected account, business, project, or asset listing

Do not trust the UI selection alone.

## Storage convention

- reusable non-sensitive access state may live in machine-global storage such as `~/.config/tracking-skills/`
- secrets should live in a secure local secret store such as the macOS Keychain
- project repos may contain non-sensitive vendor wiring manifests, IDs, or setup notes if useful
- secrets must not be committed to Git
- the skill repo should document the procedure, not store live credentials

## Verified examples from this workflow

### Google

Verified sequence used successfully:

1. Create or choose a dedicated GCP project for tracking access
2. Enable the needed APIs such as Tag Manager and Analytics Admin
3. Create the OAuth client needed for local programmatic access
4. Mint local credentials for CLI/API use
5. Verify the access with live GTM and GA4 Admin API calls

### Meta

Verified sequence used successfully:

1. Identify a non-restricted Meta Business that can own the automation assets
2. Create a Meta app for the tracking access use case
3. Configure the business login / system-user flow
4. Mint the broadest relevant machine-to-machine token the official flow exposes
5. Verify the real scopes with `debug_token`
6. Probe the Graph API for the business, apps, system users, and assets

## What the final plan must include

When the skill outputs an executable plan, it should not stop at "need pixel ID" or "need GTM container ID".

It should state:

- whether a programmatic bootstrap path exists
- what the exact bootstrap order is
- which missing approvals or authorizations block it
- which parts can be done immediately by the agent
- which parts require explicit user approval or third-party admin rights
