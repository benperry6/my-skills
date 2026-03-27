# Stack Recipes

Use these recipes after classifying the archetype and maturity stage.

## Recipe A — Pre-revenue SaaS

### Recommended stack

- GTM web
- GA4
- Google Search Console
- Google Ads
- Bing Webmaster Tools
- Meta Pixel
- Any additional vendor pixel/tag only if the near-term channel plan already justifies it (TikTok, LinkedIn, Microsoft, Reddit, etc.)
- First-party event store in the app/backend
- Server-side forwarding from the existing backend or hosting layer for high-value events only

### High-value server-side events

- signup_completed
- onboarding_completed
- checkout_started
- subscription_started
- purchase_completed

### Why

- SaaS often converts after several touches, so identity and key lifecycle events matter more than brute-force event volume
- The Google cluster should be wired early as one system: traffic measurement, search visibility, and future paid-search activation should not be treated as separate late-phase concerns
- Search visibility should not rely on Google alone; Bing Webmaster Tools should start collecting domain-level signals early too, but its bootstrap should still be treated as unverified until a live reusable path is proven
- This stack starts audience building and historical signal collection without paying for enterprise infrastructure too early

### Do not default to

- paid sGTM on GCP before revenue exists
- routing every low-value interaction server-side from day one

## Recipe B — Pre-revenue E-commerce

### Recommended stack

- GTM web
- GA4
- Google Search Console
- Google Ads
- Bing Webmaster Tools
- Meta Pixel
- Any additional vendor pixel/tag only if the category and channel plan justify it (TikTok, Pinterest, Snap, Microsoft, etc.)
- First-party event store
- Server-side forwarding from backend for checkout and purchase-critical events

### High-value server-side events

- add_to_cart
- begin_checkout
- add_payment_info
- purchase

### Why

- E-commerce benefits quickly from browser-side commerce signals and retargeting
- The Google cluster should be wired early as one system: analytics, search visibility, and paid-search readiness reinforce each other from the start
- Search visibility should not rely on Google alone; Bing Webmaster Tools should start collecting domain-level signals early too, but its bootstrap should still be treated as unverified until a live reusable path is proven
- Reliability matters most around checkout and purchase, not every single page interaction

## Recipe C — Pre-revenue Affiliate / Content Site

### Recommended stack

- GTM web
- GA4
- Google Search Console
- Google Ads
- Bing Webmaster Tools
- Meta Pixel if remarketing is part of the model
- Any additional vendor pixel/tag only if the distribution model already justifies it (TikTok, Pinterest, Reddit, Microsoft, etc.)
- First-party event store
- Server-side forwarding only for owned high-value events

### High-value server-side events

- email_signup
- referral_click
- outbound_offer_clicked if it is modeled cleanly in first-party systems

### Why

- Affiliate/content businesses often do not own the final sale event
- The Google cluster should be wired early as one system: analytics, search performance, and future search monetization should not start from zero later
- Search visibility should not rely on Google alone; Bing Webmaster Tools should start collecting domain-level signals early too, but its bootstrap should still be treated as unverified until a live reusable path is proven
- The real leverage is clean first-party click and audience data, not over-engineering fake downstream attribution

## Recipe D — Early traction

### Recommended stack

- Keep the recipe from phase 2
- Add stronger event contracts, deduplication rules, and QA discipline
- Expand server-side coverage only where reliability materially matters

### Typical triggers to expand

- revenue events are too noisy or under-counted
- checkout attribution breaks too often
- browser-only measurement clearly loses too much value

## Recipe E — Scaling

### Recommended stack

- Re-evaluate a centralized server-side tagging layer
- Standardize routing, deduplication, governance, and vendor mappings

### Why

- At scale, the operational cost of ad-hoc backend forwarding can exceed the infra cost of a dedicated server-side layer

## Canonical doctrine

The default doctrine of this skill is:

1. Browser-side is necessary, not sufficient
2. First-party data storage is mandatory
3. Server-side should exist early, but in a low-cost selective form
4. Dedicated paid infrastructure comes later, not by default
