# Access Checklist

Use this file when moving from recommendation to implementation.

## Universal

- Access to the codebase and deployment platform
- Access to environment variable management
- DNS access if a first-party tracking subdomain is ever needed later
- Access to the first-party database or event store

## Google

- Google Tag Manager account access
- GA4 property access
- Google Ads access if future ad conversion import or linking is expected
- OAuth authorization for Tag Manager and Analytics Admin APIs if API-first setup is expected

### Common identifiers or settings

- GTM container ID
- GA4 measurement ID
- GA4 API secret only if Measurement Protocol is used

## Meta

- Meta Business / Events Manager access
- Meta Developer account access if API-first automation is expected
- Meta App access when the Marketing API / Conversions API bootstrap uses an app
- System user or user access token with the required permissions if API-first setup is expected
- Pixel or dataset access
- Conversions API token if server-side forwarding is implemented
- Ability to grant the asset permissions required by the app/token flow

## TikTok

- TikTok Ads / Events Manager access
- Pixel access
- Events API token if server-side forwarding is implemented

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
- container IDs
- pixel IDs
- tokens / secrets
- DNS or vendor admin access where needed
- OAuth / developer authorization when Google or Meta should be bootstrapped without manual clicking

## What the agent can typically do

- recommend the architecture
- map events
- prepare implementation changes
- wire env vars
- configure app-side tracking
- use Google APIs directly once OAuth access exists
- use Meta APIs directly once app/token/asset bootstrap exists
- validate the resulting data flow once the external access exists
- fall back to browser setup only when the vendor bootstrap still has UI-only gaps
