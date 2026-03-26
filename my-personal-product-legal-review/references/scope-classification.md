# Scope Classification

Use this file to anchor the audit in the real implemented product before touching legal text.

## Capture Checklist

State explicitly:

- jurisdiction actually in scope
- B2C, B2B, or mixed
- product format: marketing site, SaaS, app, marketplace, community, hybrid
- auth model
- payment model: one-off, subscription, free trial, freemium, upsell, add-ons
- support model: email, chatbot, phone, no live support
- data categories processed
- analytics / advertising stack
- cookies / local storage / consent stack
- public-sharing or publicly visible user data surfaces
- email types sent
- cancellation / pause / suspension / reactivation flows
- post-purchase or post-upgrade confirmation surfaces

## Evidence Priority

Prefer this order:

1. code and configuration
2. API handlers and webhook flows
3. email templates and triggers
4. live product behavior
5. marketing pages and FAQs

Do not reverse this order unless the code is unavailable.

## Mandatory Evidence Questions

Before concluding on a feature, ask:

- Where is it implemented?
- Where is it triggered?
- What user data does it touch?
- What user-visible copy exists?
- What happens after payment / cancellation / failure / suspension / deletion?
- Does a public or semi-public surface expose any data?

## Typical Blind Spots

- chatbot storage and model providers
- tracking and attribution tables
- post-purchase emails
- unsubscribe granularity
- public share links
- admin-only toggles that still affect end users
- retention jobs and cron routes
