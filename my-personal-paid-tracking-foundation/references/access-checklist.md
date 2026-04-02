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
- Google Analytics Data API access when CLI-side GA4 validation or reporting is expected
- Search Console property access or the ability to verify ownership programmatically
- Google Ads account access
- Google Ads manager-account access when Google Ads API administration or account creation is expected
- Google Ads developer token when Google Ads API administration is expected
- In the current verified workflow, Google Ads API access works once the approved OAuth identity is attached to a manager account and the developer token has been minted in API Center
- In the current verified workflow, a domain-level Search Console property can be fully owner-verified once the authoritative-DNS `TXT` record exists and the Site Verification API insert succeeds; the registrar and the DNS host can differ, and the current `lostnfound-app.com` live setup is `Hostinger registrar + Cloudflare DNS`
- In the current verified workflow, `sites.add` can also add a narrower URL-prefix property such as `https://lostnfound-app.com/` once the domain-property ownership already exists
- In the current verified workflow, the Search Console property can then be associated to the GA4 web stream, but the proven path here is the Analytics UI after checking that no public Analytics Admin API resource exists for that association
- In the current verified workflow, `analyticsdata.googleapis.com` can be enabled on the unified Google project and then used via `properties/{property_id}:runRealtimeReport` to validate GA4 ingestion from CLI; on 2026-03-31, a Measurement Protocol event named `manual_realtime_api_server_probe` returned `rowCount=1` immediately afterwards on property `530524280`
- In the current verified workflow, Google later approved Basic access for developer token `a_kKFXFmtzuc4UMoXad6Xg` on manager `9095768791`, and a rerun of `createCustomerClient` no longer failed on `DEVELOPER_TOKEN_NOT_APPROVED`; it now fails with `CustomerError.CREATION_DENIED_INELIGIBLE_MCC`, meaning the manager itself is not yet eligible to create fresh child accounts until it is linked to a Google Ads account that has spent more than `$1,000` and has a history of policy compliance
- In the current verified workflow, an existing Google Ads client account with visible spend above `$1,000` can at least be invited from the MCC side, but invite acceptance is a separate checkpoint: a real click on `Grant access` in the client account managers UI can still fail with `AUTH_ERROR_REAUTH_PROOF_TOKEN_REQUIRED`
- In the current verified workflow, account-repair work on an older Google Ads client can restart live spend if that client already contains `ENABLED` campaigns; before restoring billing or advertiser verification, query campaign statuses first, warn the user explicitly, and pause any unwanted `ENABLED` campaigns before continuing if the user does not want spend to resume automatically
- In the current verified workflow, the local Google Ads YAML refresh token can become revoked even while `gcloud auth application-default` remains valid; when that happens, prefer the official ADC path with `use_application_default_credentials: true` for fresh CLI probes instead of treating the Google Ads API path as blocked
- In the current verified workflow, after linking an active compliant spend-bearing client account to MCC `9095768791`, bringing that client back to an enabled/billable state, and then rerunning the probe with ADC, `createCustomerClient` succeeded and created child account `6528887954`
- In the current verified workflow, once `createCustomerClient` succeeded, the clean Google Ads structure was to rename the manager account to an umbrella/admin name (`ProStrike MCC (Manager Account)`) and rename the created child account to the business name (`Lost N Found`); treat that as the default pattern for future businesses instead of leaving the MCC named after a single project
- In the current verified workflow, once the dedicated project client account `6528887954` / `Lost N Found` existed, the clean Google setup was to move the GA4 `googleAdsLinks` association off the MCC and onto that client account directly; the earlier GA4 → MCC link was only a bootstrap shortcut, not the final per-business architecture
- In the current verified workflow, after the GA4 → Google Ads link was moved from MCC `9095768791` to client `6528887954`, the imported `purchase` conversion reappeared on the client account itself, was switched from `HIDDEN` to `ENABLED`, and was made `primary_for_goal=true`; the client account then reported `CONVERSION_TRACKING_MANAGED_BY_SELF`
- In the current verified workflow, once the dedicated client-account import was canonical, the obsolete MCC-level hidden `purchase` conversion was removed successfully via `ConversionActionOperation.remove`; do not leave a stale MCC conversion behind if the business now has its own direct GA4 → client-account link
- In the current verified workflow, a disabled legacy account such as `3174846691` may remain inaccessible by API and therefore not be immediately removable or renameable programmatically; if the platform does not allow clean removal, mark it clearly as legacy and hide or unlink it where the live UI actually permits
- In the current verified workflow, the dedicated client account `6528887954` still showed `0` clicks / `0` impressions / `0` conversions while the paused verification campaign remained the only campaign; treat the first true Google Ads-side conversion proof as deferred until intentional paid traffic exists and has had time to appear in Ads reporting
- OAuth authorization for Tag Manager, Analytics Admin, Search Console, and Site Verification APIs if API-first setup is expected
- Google Auth Platform publication status should be checked before relying on durable external-user refresh tokens; prefer production over testing when appropriate
- If Google Auth Platform is still in `Test` mode, add the explicitly approved Google email as a test user before retrying ADC bootstrap
- After OAuth bootstrap, verify the actual granted scopes with a live token inspection call instead of assuming the requested scope list was granted
- If the Google foundation includes `GSC`, the OAuth bootstrap must actually grant Search Console scopes; otherwise Search Console API calls will fail with `insufficient_scope`
- When the canonical Search Console property should cover the whole domain, prefer a domain property (`INET_DOMAIN`) with authoritative-DNS `TXT` verification instead of relying on a narrower URL-prefix property
- Before any browser action on a third-party platform, verify whether a CLI/API/MCP path exists and actually works with a real probe from the current machine and credentials
- If that programmatic path exists and works, use it as the mandatory default and treat browser work as disallowed unless the path is absent, broken, or insufficient for the exact operation
- If the user explicitly names a browser for one task, account, or vendor flow, keep that browser choice scoped to that exact need; do not carry it over to unrelated later steps, and otherwise fall back to the global default-browser rule
- If an existing browser tab is reused to inspect vendor state, refresh it before concluding anything from its contents unless that tab was opened by the current investigation moments ago
- If Google browser fallback is ever needed, verify the active top-right Google account email against the explicitly approved Google email before doing anything; never use `authuser=*`, `login_hint`, or account-index numbers as identity proof in a multi-account Google browser session
- If Google Ads returns `DEVELOPER_TOKEN_PROHIBITED` on a previously used project, prefer one new clean unified project and retire the blocked project after migration instead of normalizing two active Google M2M projects
- Approval of which Google account / GCP project should be used when multiple options exist

### Common identifiers or settings

- GTM container ID
- GA4 measurement ID
- Search Console property identifier
- Google Ads customer ID
- Google Ads manager customer ID when applicable
- Canonical Google Ads manager-account name vs dedicated project client-account name when multiple businesses will live under one umbrella MCC
- GA4 API secret only if Measurement Protocol is used

## Bing Webmaster Tools

- Verified search baseline extension for owned-domain sites in this skill
- Bing Webmaster Tools account access
- Verified site ownership in Bing Webmaster Tools
- OAuth or API key access if Bing Webmaster Tools APIs should be used programmatically
- Prefer authoritative-DNS verification when the canonical ownership target is the full domain rather than a narrower page-level verification method; the registrar and the DNS host can differ, and in the currently verified Bing flow the DNS method is `CNAME`, not `TXT`
- In the current verified workflow, a generated Bing Webmaster Tools API key can be stored locally and used programmatically; `GetUserSites`, `GetSiteRoles`, and `SubmitUrl` all succeeded in real behavior with that API key for `https://lostnfound-app.com/`
- In the current verified/public Bing flow, the owned object still appears as a site URL (`https://lostnfound-app.com/`); no Google Search Console-style domain-property object has yet been verified for Bing
- Approval of which Microsoft/Bing account should be used when multiple options exist

### Common identifiers or settings

- Bing Webmaster Tools site URL entry; do not assume a separate domain-property object exists unless it has been verified in the live Bing flow
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
- In the current verified workflow, an admin Meta system-user token can create a business-owned ad account by API
- In the current verified workflow, the Pixel Terms blocker was cleared by advancing the first dataset-creation flow in Business Settings to the ad-account association step, after which pixel creation by API succeeded
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

## Runtime verification and debug

- Access to the live runtime that should be verified, such as the public Vercel alias or the current production domain
- A clear statement of which environment is intentionally live and which one must not be touched yet
- CLI/API verification access for vendor-side ingestion when the vendor exposes it
- A place to persist the verified runtime/debug state, such as `~/.config/tracking-skills/access-bootstrap.json`
- For Google when GA4 is in scope, keep `analyticsdata.googleapis.com` available so `runRealtimeReport` can be used as a CLI-side ingestion check instead of relying only on browser DevTools
- For Google Ads, decide explicitly whether paid traffic is intentionally live now; if not, treat Ads-reporting proof as a deferred post-launch check rather than a current blocker
- For Meta browser-side verification, expect the loader and config requests to be easier to observe than the final beacon in some headless runs; if the final `facebook.com/tr` request is not visible in a specific headless probe, treat that result as inconclusive unless a stronger counter-proof exists

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
