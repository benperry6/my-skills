# Maturity Stages

Use this file to decide how heavy the stack should be.

## 1. Pre-launch

### Signals

- Product not live yet, or core conversion flow still unstable
- No reliable real user traffic yet

### Default recommendation

- Define event taxonomy, consent posture, and vendor priority
- Prepare first-party tracking contracts
- Do not invest in heavier infra yet

## 2. Pre-revenue / Validation

### Signals

- Product is live
- Revenue is zero or inconsistent
- Main acquisition is SEO, content, community, or organic
- Paid media is not live yet, or not serious yet

### Default recommendation

- This is the core target for the skill
- Avoid a paid sGTM/GCP setup by default
- Use a hybrid low-cost foundation:
  - browser-side tags where needed
  - first-party event store
  - selective server-side forwarding from the existing backend for the most valuable events

### Why

- You start collecting useful signal now
- You avoid fixed infra costs before the model is proven
- You keep an upgrade path later instead of painting yourself into a corner

## 3. Early traction

### Signals

- First paying customers exist
- Conversion flow is stable enough to trust
- Paid testing is about to start or has started modestly
- Ad spend is still limited

### Default recommendation

- Keep the hybrid model
- Harden server-side forwarding for key revenue events
- Expand QA, deduplication, identity stitching, and vendor-specific reliability checks
- Consider a heavier server-side layer only if direct backend forwarding becomes operationally painful

## 4. Scaling

### Signals

- Paid media is a real acquisition channel
- Spend is meaningful and sustained
- Data quality failures now have real cost
- Multiple vendors, teams, or flows need centralized routing and governance

### Default recommendation

- Re-evaluate direct backend forwarding vs dedicated server-side tagging infrastructure
- Dedicated sGTM or a more industrial relay becomes reasonable only here

## Default escalation thresholds

These are defaults, not laws:

- Stay on the low-cost foundation while the business is still validating
- Re-evaluate a dedicated server-side stack when paid spend is persistent enough that data loss clearly costs more than the infra
- Re-evaluate when event routing logic becomes too fragmented across app code, vendors, and business flows

The default bias of this skill is conservative on infrastructure cost until traction is real.
