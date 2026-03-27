# Programmatic Bootstrap

Use this file when moving from "what should we install?" to "how do we obtain access and assets without defaulting to the browser?"

## Canonical rule

For every vendor:

1. Search the current official docs and API surface on the internet first
2. Determine whether a credible CLI/API/MCP path exists
3. Reuse existing access if it already exists and the user approves the account choice
4. Ask for the exact missing authorization if the path exists but access is incomplete
5. Use the browser only when the programmatic path is genuinely missing or blocked by a real bootstrap gap
6. If the official flow exposes permissions or token-duration choices dynamically, inspect those live options instead of relying on a frozen historical list
7. Prefer a non-expiring option when the official flow exposes one, then verify the actual expiry in the minted token

Do not treat Meta as a special exception. Apply the same logic to Google, Meta, TikTok, LinkedIn, Microsoft, Reddit, Pinterest, Snap, or any other vendor that becomes relevant.

Treat vendor names already present in the skill as examples, not a whitelist. The skill may recommend a vendor whose name does not yet appear anywhere in the skill if the business context and channel plan justify it.

## Verified learning update loop

Use this rule whenever:

- a newly recommended vendor is not documented yet
- a previously documented vendor flow no longer works

Workflow:

1. Research the current official docs and API surface on the internet
2. Try the best programmatic path first
3. If the path fails, debug it in real conditions instead of assuming the docs are right
4. Update the skill only after a real working path has been verified
5. If the path is still unresolved, leave the gap marked as unverified instead of polluting the skill with theory

The skill should therefore learn continuously across projects, but only from verified behavior.

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
- if `1Password CLI` is actually available and the user wants a shareable/team secret backend, it can be used instead of or alongside the local Keychain
- files that vendor tooling requires on disk may remain in the standard config paths that tooling expects, but with restrictive permissions
- rematerializable bootstrap blobs should be kept in a secure local secret store even when a compatibility copy still exists on disk
- project repos may contain non-sensitive vendor wiring manifests, IDs, or setup notes if useful
- secrets must not be committed to Git
- the skill repo should document the procedure, not store live credentials

## Naming convention

Use a name that describes the access mechanism, not the business goal of the skill.

Preferred canonical label:

- `Paid Media Vendor M2M API Access`

Apply it to:

- vendor apps
- business login / integration configurations
- keychain item labels
- reusable local compatibility files where practical

If a vendor imposes naming limits, use the closest shorter variant that preserves the meaning, and document the exception.

## Verified examples from this workflow

### Google

Verified sequence used successfully:

1. Create or choose a dedicated GCP project for tracking access
2. Enable the needed APIs such as Tag Manager and Analytics Admin
3. Create the OAuth client needed for local programmatic access
4. Move the Google Auth Platform app to production before relying on durable external-user refresh tokens
5. Mint local credentials for CLI/API use
6. Verify the actual granted scopes with a live token inspection call instead of trusting the requested scope list
7. Verify the access with live GTM and GA4 Admin API calls
8. If a reusable local client file is needed later, re-materialize it from secure local storage into the standard path instead of recreating it manually

Default Google cluster target for this skill:

- `GTM web`
- `GA4`
- `GSC`
- `Google Ads`

Documented programmatic path to pursue before any browser fallback:

1. Use the Tag Manager API for GTM account/container/tag administration
2. Use the Analytics Admin API for GA4 property, web data stream, and `googleAdsLinks` administration
3. Use the Search Console API plus the Site Verification API to add and verify Search Console properties programmatically when possible
4. Treat Google Ads API administration as a separate bootstrap that requires a manager account plus a developer token
5. Check the current official docs for Google-service associations each time; if the association is documented only in help-center UI flows and not in a developers API surface, mark it as a real UI bootstrap gap instead of pretending the CLI path is already verified

Important verified constraint:

- Google Cloud project display names are limited to 30 characters, so the canonical access label may need a shortened variant such as `Paid Media Vendor API Access`
- If `gcloud auth application-default login` crashes on a scope-normalization warning during ADC bootstrap, retry with `https://www.googleapis.com/auth/userinfo.email` instead of the short `email` scope
- In the current verified ADC state, GTM and GA4 API probes work, but Search Console API probes fail with `insufficient_scope`; if the Google foundation includes `GSC`, the OAuth bootstrap must be expanded before claiming the Google cluster is fully ready

Documented but not yet verified end-to-end in real behavior here:

- Search Console property creation via `sites.add`
- Search Console ownership verification via the Site Verification API
- GA4 to Google Ads linking via the Analytics Admin API `googleAdsLinks` surface
- End-to-end Google Ads API bootstrap with a usable developer token
- Search Console associations that appear documented in help-center UI flows but do not yet have a verified developers API path in this skill

### Meta

Verified sequence used successfully:

1. Identify a non-restricted Meta Business that can own the automation assets
2. Create a Meta app for the tracking access use case
3. Configure the business login / system-user flow
4. Open the official system-user token generator, inspect the currently exposed permission options, and select all options it exposes for the approved use case
5. If the expiration step exposes `Jamais`, choose it; otherwise choose the most durable option available
6. If direct rename of the system user is denied, create a new correctly named system user instead of keeping a misnamed long-term M2M identity
7. Assign that new system user to the app with full control in Business Settings > Applications
8. Mint the token and verify the real scopes plus expiry with `debug_token`
9. Probe the Graph API for the business, apps, system users, and assets
10. If the business login configuration name is still misaligned, open the configuration list, follow `Modifier`, and update the name through the configuration editor flow

Important verified constraints:

- The tested Meta generator exposed 8 explicit permission choices plus an implicit `public_profile` scope visible in `debug_token`
- The tested Meta generator can issue a token with `expires_at = 0` and `data_access_expires_at = 0` when `Jamais` is selected
- Meta app names are limited to 30 characters, so the canonical access label may need a shortened variant such as `Paid Media Vendor API Access`
- Direct rename of an existing system user can still be denied even when the token is broad and non-expiring; creating a new correctly named system user, then assigning it full app control, is a valid fallback
- The business login configuration was successfully renamed through the real edit route `/apps/<app_id>/create-login-configuration/?config_id=<config_id>`
- The official Business reference documents business rename by `POST /{business_id}` with a `name` parameter, but live calls can still fail with `3910` when the current identity lacks permission to edit Business Manager details
- The official Meta Business Help docs document business portfolio deletion in UI, but the Business API delete section documents dissociation of relationships/assets, not direct deletion of the business itself via `DELETE /{business_id}`
- The official Meta Business Help troubleshooting doc states that a business portfolio with system users cannot be deleted until that blocker is resolved
- In the verified workflow here, trying to mint a token for an existing admin system user with the current regular system-user token failed with `GENERATE_TOKEN_AUDIT_NEEDED`; treat that as evidence that a stronger admin identity may still be required for some business-level admin actions

## What the final plan must include

When the skill outputs an executable plan, it should not stop at "need pixel ID" or "need GTM container ID".

It should state:

- whether a programmatic bootstrap path exists
- what the exact bootstrap order is
- which missing approvals or authorizations block it
- which parts can be done immediately by the agent
- which parts require explicit user approval or third-party admin rights

## What should be written back into the skill

Only write back concise learnings that have been verified in real behavior, for example:

- a vendor bootstrap sequence that actually worked
- a corrected workaround for a vendor flow that had become outdated
- a newly verified permission or token-duration constraint
- a platform naming or storage constraint that was proven in practice

Do not write back:

- doc snippets that were never tested
- speculative explanations
- partial theories that did not result in a working path
