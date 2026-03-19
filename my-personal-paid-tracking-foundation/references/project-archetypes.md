# Project Archetypes

Use this file to classify the business before recommending a stack.

## 1. SaaS

### Typical goal

Acquire users, qualify intent, and convert into paid subscriptions.

### Priority events

- landing_page_view
- signup_started
- signup_completed
- onboarding_started
- onboarding_completed
- trial_started
- checkout_started
- subscription_started
- purchase_completed

### Tracking implications

- Identity stitching matters early because conversion often happens after several sessions.
- CRM or lifecycle attribution can matter later, but it should not bloat the phase-1 stack.
- Server-side forwarding is most valuable for high-intent events tied to auth, billing, and subscriptions.

### Default vendor posture

- Google: open early
- Meta: open early
- TikTok: open early only if the product has clear broad-consumer or creator/discovery potential
- LinkedIn: only elevate if the motion is clearly B2B and the user already plans paid acquisition there

## 2. E-commerce

### Typical goal

Drive product discovery and purchases with short or medium buying cycles.

### Priority events

- page_view
- view_item
- search
- add_to_wishlist
- add_to_cart
- begin_checkout
- add_payment_info
- purchase

### Tracking implications

- Product feed quality and commerce event quality matter very early.
- Browser-side pixels are useful immediately for catalog, retargeting, and audience building.
- Server-side forwarding is highly valuable for checkout and purchase reliability.

### Default vendor posture

- Google: open early
- Meta: open early
- TikTok: open early if the category is visually driven or discovery-led
- Pinterest: only later if the catalog and creative format justify it

## 3. Affiliate / Content / Media Site

### Typical goal

Capture intent, route traffic to outbound offers, and monetize through clicks or partner conversions.

### Priority events

- page_view
- scroll_depth
- content_engaged
- comparison_viewed
- outbound_offer_clicked
- email_signup
- referral_click

### Tracking implications

- The site may never own the final conversion event.
- First-party click tracking and outbound attribution are more important than trying to fake purchase measurement.
- Server-side forwarding is useful for high-value owned events such as email signup or outbound click classification, not for pretending to own downstream sales data.

### Default vendor posture

- Google: open early
- Meta: open if remarketing or audience building is realistic
- TikTok: open only if the content model is discovery and short-form friendly

## How to classify ambiguous cases

- If the business sells a subscription product with app usage, classify as SaaS.
- If the business sells physical or digital products in a cart flow, classify as e-commerce.
- If the business mostly monetizes traffic, clicks, leads, or referrals, classify as affiliate/content.

When a project has two motions, choose the revenue motion that matters most in the next 6-12 months, then mention the secondary motion explicitly in the final recommendation.
