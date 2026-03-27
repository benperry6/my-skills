# Access Checklist

Use this file when moving from recommendation to implementation.

## Universal

- Search the current official docs and API surface on the internet before declaring a vendor UI-only
- Inventory reusable access already available on the machine before asking for new bootstrap work
- Present the accessible accounts / businesses / cloud projects and wait for explicit user approval before using one
- If a vendor is new or a documented flow is failing, update the skill only after the repaired or newly discovered path is verified in real behavior
- Access to the codebase and deployment platform
- Access to environment variable management
- DNS access if a first-party tracking subdomain is ever needed later
- Access to the first-party database or event store

## Google

- Default Google foundation for this skill: `GTM web + GA4 + GSC + Google Ads`
- Google Tag Manager account access
- GA4 property access
- Search Console property access or the ability to verify ownership programmatically
- Google Ads account access
- Google Ads manager-account access when Google Ads API administration or account creation is expected
- Google Ads developer token when Google Ads API administration is expected
- OAuth authorization for Tag Manager, Analytics Admin, Search Console, and Site Verification APIs if API-first setup is expected
- Google Auth Platform publication status should be checked before relying on durable external-user refresh tokens; prefer production over testing when appropriate
- After OAuth bootstrap, verify the actual granted scopes with a live token inspection call instead of assuming the requested scope list was granted
- If the Google foundation includes `GSC`, the OAuth bootstrap must actually grant Search Console scopes; otherwise Search Console API calls will fail with `insufficient_scope`
- When the canonical Search Console property should cover the whole domain, prefer a domain property (`INET_DOMAIN`) with registrar-level `DNS TXT` verification instead of relying on a narrower URL-prefix property
- Approval of which Google account / GCP project should be used when multiple options exist

### Common identifiers or settings

- GTM container ID
- GA4 measurement ID
- Search Console property identifier
- Google Ads customer ID
- Google Ads manager customer ID when applicable
- GA4 API secret only if Measurement Protocol is used

## Bing Webmaster Tools

- Recommended search baseline extension for owned-domain sites, but not yet verified end-to-end in this skill
- Bing Webmaster Tools account access
- Verified site ownership in Bing Webmaster Tools
- OAuth or API key access if Bing Webmaster Tools APIs should be used programmatically
- Prefer registrar-level `DNS TXT` verification when the canonical ownership target is the full domain rather than a narrower page-level verification method
- Approval of which Microsoft/Bing account should be used when multiple options exist

### Common identifiers or settings

- Bing Webmaster Tools site URL or domain entry
- Bing Webmaster Tools API key if the API-key path is used

## Meta

- Meta Business / Events Manager access
- Meta Developer account access if API-first automation is expected
- Meta App access when the Marketing API / Conversions API bootstrap uses an app
- System user or user access token with the required permissions if API-first setup is expected
- Prefer a system-user token over a human user token when long-lived CLI administration is the goal
- When the official token generator exposes permissions dynamically, inspect and select the live options it currently exposes instead of relying on a stale hardcoded list
- When the official token generator exposes `Jamais` or an equivalent non-expiring duration, prefer it for long-lived CLI administration
- After token generation, verify the real granted scopes and expiry with `debug_token`
- Pixel or dataset access
- Conversions API token if server-side forwarding is implemented
- Ability to grant the asset permissions required by the app/token flow
- Approval of which Meta business / app / system-user path should be used when multiple options exist

### Meta permissions verified in the current tested system-user flow

The current tested flow exposed these explicit permission choices in the official generator:

- `ads_management`
- `ads_read`
- `business_management`
- `catalog_management`
- `pages_manage_ads`
- `pages_read_engagement`
- `pages_show_list`
- `threads_business_basic`

The minted token then also showed an implicit `public_profile` scope in `debug_token`.

Treat this as "verified maximum for the current tested flow", not as a promise that every future app/business will expose the exact same set.

## TikTok

- TikTok Ads / Events Manager access
- Pixel access
- Events API token if server-side forwarding is implemented
- Approval of which TikTok account or business context should be used when multiple options exist

## Any vendor enabled by the plan

- A programmatic bootstrap path should be researched first
- The broadest relevant machine-to-machine permissions should be requested when the vendor exposes them
- The real granted scopes / capabilities should then be verified with live inspection or API probes
- If a credible programmatic path exists but access is missing, ask for the exact missing authorization instead of defaulting to browser work

## App / hosting / backend

- Vercel or equivalent hosting access
- Existing API routes or backend endpoints that can relay first-party events
- Secrets for any vendor server-side API calls

## Consent / legal

- Confirmation of legal posture by geography
- Ability to update cookie and privacy pages
- Ability to configure the consent layer already in place

## What the user typically must provide

- account access
- approval of the specific account / business / cloud project to use
- container IDs
- pixel IDs
- tokens / secrets
- DNS or vendor admin access where needed
- OAuth / developer authorization when Google or Meta should be bootstrapped without manual clicking
- confirmation when a brand-new account should be bootstrapped instead of reusing an existing accessible one

## What the agent can typically do

- recommend the architecture
- map events
- prepare implementation changes
- wire env vars
- configure app-side tracking
- research the current official docs and API surface on the internet before falling back to browser setup
- inventory accessible accounts and reusable local access first
- use Google APIs directly once OAuth access exists
- use Meta APIs directly once app/token/asset bootstrap exists
- use the equivalent machine-to-machine path for any other enabled vendor when it exists
- validate the resulting data flow once the external access exists
- fall back to browser setup only when the vendor bootstrap still has UI-only gaps

## Storage conventions

- Reusable non-sensitive access state may be stored machine-globally, for example under `~/.config/tracking-skills/`
- Secrets should be stored in a secure local secret store such as the macOS Keychain
- If `1Password CLI` is actually available and the user wants a team/shareable secret backend, it can replace or complement the local Keychain
- Files that official tooling expects on disk, such as Google ADC files, may stay in their standard tool paths with restrictive permissions
- Bootstrap blobs that can be re-materialized later, such as a Google OAuth desktop client JSON, should be copied into a secure local secret store as well
- Project repos may contain non-sensitive setup manifests or wiring notes if useful
- Secrets must not be committed to Git
