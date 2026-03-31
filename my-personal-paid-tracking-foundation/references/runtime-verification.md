# Runtime Verification

Use this file after vendor assets and links appear complete.

Its job is to stop the workflow from ending at "the asset exists" and force proof that the data flow works in real conditions.

## Canonical rule

Separate runtime verification into 3 layers:

1. Runtime/bootstrap proof
2. Transport proof
3. Vendor-ingestion proof

Do not collapse these into one vague "tracking works" statement.

Examples:

- A script loader appearing in the page is runtime/bootstrap proof
- A browser request to a vendor endpoint is transport proof
- A vendor-side report, realtime API, or equivalent accepted event is vendor-ingestion proof

The strongest available proof wins, but weaker layers are still useful for debugging.

## Preferred verification order

1. Prefer CLI/API verification when the vendor exposes a real path
2. Use browser/runtime observation to prove the app is actually dispatching
3. Use server-side relay inspection when the architecture includes first-party collection or forwarding
4. Treat absence of one weak signal as inconclusive if a stronger signal already proves success

## Google — verified runbook

### Browser/runtime proof

Verified useful signals in the current flow:

- `gtm.js` loads for the GTM public ID
- `gtag/js?id=<measurement_id>` loads for the GA4 measurement ID
- `gtag('get', measurement_id, 'client_id', callback)` returns a non-null client ID once GA4 is truly operational
- a final `https://www.google-analytics.com/g/collect...` request can be observed after a manual event on the live runtime

Important verified learning:

- a custom `gtag` shim that pushes arrays instead of canonical `arguments` objects can load the Google scripts while still leaving GA4 functionally broken
- in the verified repair here, restoring the official queue shape `dataLayer.push(arguments)` brought back both `client_id` resolution and final `g/collect` requests

### CLI/API proof

Keep `analyticsdata.googleapis.com` enabled when GA4 is in scope.

Verified useful path:

1. send a Measurement Protocol event to the current GA4 measurement ID and API secret
2. query `properties/{property_id}:runRealtimeReport`
3. treat a matching `rowCount` / returned row as proof that GA4 ingestion is observable from CLI

Verified example from the current flow:

- on `2026-03-31`, a Measurement Protocol event named `manual_realtime_api_server_probe` returned `rowCount=1` via `properties/530524280:runRealtimeReport`

### Current Google limitation that remains real

- `Search Console ↔ GA4` association is still `UI-only` in the verified flow here because no public Analytics Admin API resource was found for that association

## Meta — verified runbook

### Browser/runtime proof

Verified useful signals in the current flow:

- `https://connect.facebook.net/en_US/fbevents.js` loads
- `window.fbq.loaded === true`
- `window.fbq.callMethod` is callable
- a final `https://www.facebook.com/tr/...` request was observed in a verified browser-side probe earlier in this flow

Important verified nuance:

- in some headless probes, the loader and config requests are visible while the final `facebook.com/tr` beacon is not
- treat that situation as inconclusive unless a stronger counter-proof exists; do not silently downgrade a previously verified Meta runtime path to "broken" just because one headless run was noisier than another

### Asset/admin proof that should not be confused with runtime proof

The following are Phase 3, not Phase 4:

- ad-account creation
- system-user assignment to the ad account
- pixel creation
- paused campaign creation

These prove admin capability, not live event delivery by themselves.

## Bing Webmaster Tools — verified runbook

### Ownership and API reuse proof

Verified useful path in the current flow:

1. verify the site in Bing Webmaster Tools through the vendor-issued DNS method
2. generate an API key in `Settings > API access`
3. verify `GetUserSites`
4. verify `GetSiteRoles`
5. verify a low-risk write such as `SubmitUrl`

Verified example from the current flow:

- `GetUserSites`, `GetSiteRoles`, and `SubmitUrl` all succeeded for `https://lostnfound-app.com/`

## What to persist after runtime verification

Record only stable, reusable learning such as:

- which API had to be enabled
- which endpoint proved ingestion
- which browser/runtime signal was actually decisive
- which headless/browser caveats produced false negatives
- which signals were only weak indicators and should not be over-trusted

Do not persist throwaway debugging noise.
