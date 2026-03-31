# Legal Surface Matrix

Map the real product to these obligation buckets.

## Core Buckets

### Identity and mandatory notices

Check:

- publisher / operator identity
- company details required by the scoped jurisdiction
- contact and complaints channels
- hosting / infrastructure disclosures when required

### Contract formation and pre-contractual information

Check:

- offer description
- price and billing cadence
- renewal / cancellation rules
- material limitations or exclusions
- wording around payment commitment

### Post-purchase / post-subscription confirmation

Check:

- whether a durable-medium confirmation exists
- what it contains
- whether it reflects the real product state after purchase

### Privacy / data-protection information

Check:

- data categories actually processed
- purposes
- legal bases
- processors and transfers
- retention
- user rights and contact path

### Cookies / tracking / advertising

Check:

- whether a cookie banner / CMP actually exists and appears in the real flow
- first-layer structure (accept / reject / settings) and symmetry of the primary choices
- banner pattern (bottom sheet, top bar, modal, inline) and whether it creates friction or layout issues
- what is proved on raw consent / interaction versus what is proved on business outcomes
- whether the business model is publisher / ad-supported or product / SaaS / ecommerce / lead-gen before extrapolating revenue claims
- whether the preference center is category-first or overly granular by default
- strictly necessary vs optional trackers
- consent collection
- proof of consent
- ability to re-open and revise choices later
- post-consent vendor firing logic
- consent initialization ordering before tags
- measurement resilience when consent is denied
- consent-funnel instrumentation for testing and optimization
- accessibility and mobile usability of the banner itself
- performance footprint (CLS / LCP / INP risks, script loading strategy)
- advertising and attribution disclosures

### Support / chatbot / AI

Check:

- stored conversation data
- model/vendor involvement
- abuse-prevention signals
- retention
- whether support promises match the actual channel

### Public sharing / public visibility

Check:

- tokenized public pages
- exposed photos, metadata, dates, or results
- who can activate or disable them
- whether legal text matches the actual exposure

### Email communications

Check:

- transactional emails
- marketing or lifecycle emails
- per-user vs per-object preference logic
- unsubscribe behavior
- post-click tracking

### Retention / termination / reactivation

Check:

- what happens on cancellation
- what happens on payment failure
- what remains visible to the user
- whether legal copy matches the real retention logic

## Review Questions

For each bucket, classify:

- covered correctly
- partially covered
- stale / contradictory
- missing

Then state the exact evidence path.
