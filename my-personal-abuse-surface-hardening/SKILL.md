---
name: my-personal-abuse-surface-hardening
description: "[My Personal Skill] Use when a website, SaaS, app, API, or public workflow needs to identify and harden exposed or weakly protected surfaces that can be abused by bots, brute-force, email enumeration, spam, scraping, costly anonymous AI/chat usage, upload abuse, share-link abuse, or weak public endpoints. Also use for Cloudflare vs Vercel questions, WAF, rate limiting, Turnstile, CAPTCHA, bot mitigation, DNS proxying, edge protection, cache bypass, or Zero Trust / Access on admin surfaces. This skill audits context first, maps abuse mode to business impact, recommends proportional controls across provider, headers, app logic, UX, and verification, and prefers CLI/API/MCP over browser automation."
---

# Abuse Surface Hardening

This skill hardens public or weakly protected business surfaces that can be abused by low-cost attackers, bots, scrapers, brute-force actors, spammers, or anonymous traffic.

The goal is not "security in general".
The goal is to reduce business-damaging abuse on exposed surfaces without adding unnecessary friction.

## Use This Skill When

Use this skill when the product has one or more of these:

- Public forms
- Public auth entry points
- Email or account discovery flows
- Public AI, chat, or search endpoints
- Public uploads
- Public share links or public result pages
- Public webhooks or callback endpoints
- Public APIs with weak or anonymous identity
- Public error logging or diagnostics endpoints
- Admin, staging, preview, or internal surfaces that should not be broadly reachable
- Questions about Cloudflare, WAF, rate limiting, Turnstile, CAPTCHA, edge protection, or bot mitigation

Typical prompts:

- "Do I need Cloudflare on top of Vercel?"
- "Where is Turnstile actually justified?"
- "This public chatbot is expensive and bot-prone"
- "Audit my exposed attack surface"
- "Which endpoints need rate limiting vs CAPTCHA?"
- "What public flows are abusable here?"
- "Harden this app against low-cost public abuse"

## Do Not Use This Skill For

Do not use this skill for:

- Full pentests
- Generic appsec review across the whole codebase
- Deep OWASP review outside the exposed abuse surface
- Internal authorization, RBAC, RLS, or privilege audits
- Secrets management or key rotation
- Compliance or legal/privacy reviews
- Dependency or supply-chain auditing
- Complete vulnerability assessment of the entire stack

If the request expands into those areas, say so explicitly and hand off to more appropriate specialized skills or audits.

## Core Doctrine

- Start with business context, not tools.
- Focus on abuseable public or weakly protected surfaces, not all vulnerabilities.
- Choose control families before choosing vendors.
- Prefer proportional defenses, not maximal defenses.
- Prefer low-friction protection on conversion-critical flows.
- Prefer CLI, API, or MCP access over browser automation whenever provider access exists.
- Do not declare a provider "browser-only" until the current official docs and API surface have been checked.
- Persist only verified learning after real behavior has been proven.
- Keep audit and implementation logically separate.
- Do not implement provider or code changes unless the user explicitly asks for execution.

## Reference Map

Read only what the current task needs:

- `references/provider-matrix.md`
  - Known control families, when they matter, and which provider or implementation layers typically fit.
- `references/programmatic-bootstrap.md`
  - The live vendor-doc research loop, programmatic-first decision rules, and account selection guardrails.
- `references/cloudflare.md`
  - The currently verified Cloudflare path on this machine, centered on the local API wrapper instead of the browser.
- `references/verification-benchmarks.md`
  - Safe verification patterns and lightweight stress tests for proving hardening changes.
- `references/rollback-procedures.md`
  - How to stage, narrow, and roll back hardening changes that create false positives.
- `references/verified-learning.md`
  - Durable, reusable learnings already proven in real behavior.
- `references/runtime-learning.md`
  - Auto-managed working log for new findings before they are promoted into verified learning.

Use these scripts when relevant:

- `scripts/verify_cloudflare_api.sh`
  - Read-only verification of the local Cloudflare API path.
- `scripts/record_learning.py`
  - Append a structured entry to `verified-learning.md` or `runtime-learning.md`.

## Required Inputs

Gather or derive the following first:

- Product type
- Hosting and runtime model
- Public entry points
- Auth model
- Billing or cost-sensitive flows
- Anonymous or weakly authenticated traffic paths
- AI or third-party pay-per-request endpoints
- File upload flows
- Public share or result pages
- Public webhooks or callbacks
- Existing CDN, DNS, WAF, or edge provider
- Current rate limiting and bot protection
- Current admin or internal access model
- Known abuse symptoms, if any
- Which user flows are conversion-critical

If the codebase, runtime, or provider state already exposes enough evidence, use that and avoid unnecessary questions.

## Workflow

### 1. Classify The Product Context

Identify the product archetype:

- Marketing site
- SaaS
- Consumer app
- Ecommerce
- Marketplace
- AI app
- API product
- Hybrid

Then identify abuse-sensitive characteristics:

- Public signup, login, or reset
- Anonymous traffic
- Public uploads
- Cost-per-request endpoints
- Public support or chat forms
- Shareable URLs
- Admin or preview surfaces
- Machine-to-machine endpoints
- Reputation-sensitive public flows

### 2. Inventory Abuse Surfaces

Build a concrete list of public or weakly protected surfaces, such as:

- Login
- Signup
- Password reset
- Check-account or account discovery
- Contact, demo, or support forms
- AI chat or search endpoints
- Upload endpoints
- Search endpoints
- Public result pages
- Share links
- Error-log endpoints
- Public webhooks
- Cron endpoints exposed by mistake
- Admin or preview routes that should not be publicly reachable
- Any route callable without strong identity

For each surface, capture:

- Access level
- Abuse mode
- Business impact
- Existing controls
- Existing gaps

### 3. Score Abuse Risk In Business Terms

For each surface, classify likely abuse:

- Brute-force
- Credential stuffing
- Email enumeration
- Spam submission
- Cost amplification
- Storage abuse
- Link abuse
- Log pollution
- Replay
- Forged state transitions
- Automated scraping
- Volumetric bursts

Evaluate impact in business terms:

- Direct cost
- Fraud risk
- Support load
- Reputation damage
- Infrastructure strain
- Data quality degradation
- UX degradation for real users

### 4. Choose Control Families Before Choosing Vendors

Use `references/provider-matrix.md`.

Pick controls by need first, vendor second. Typical control families include:

- DNS and nameserver control
- Proxying and edge filtering
- WAF managed rules
- WAF custom rules
- Rate limiting
- Bot detection
- CAPTCHA or Turnstile
- DDoS protection
- Cache rules and cache bypass for dynamic paths
- Transform rules and response or request header controls
- Zero Trust or Access controls for admin or internal surfaces
- API protection controls such as schema validation, mTLS, signed requests, or API shielding
- Security headers
- CORS restrictions
- Server-side validation
- State validation against server truth
- Payload caps
- Sanitization
- Signature validation
- Token design
- UX challenge behavior
- QA and test modes
- Documentation and runbook updates

Do not recommend every control everywhere.

### 5. Research The Current Programmatic Path First

Use `references/programmatic-bootstrap.md`.

Before suggesting browser work:

1. Check the current official docs and API surface.
2. Check the local machine for reusable wrappers, scripts, CLIs, MCPs, 1Password items (vault `Employee`), or auth state.
3. Verify the best read-only path first.
4. Only then decide whether browser fallback is genuinely necessary.

Vendors already named in the skill are examples, not a whitelist. If a different provider is relevant in a future context, research it live instead of pretending the matrix is exhaustive.

### 6. Distinguish Protection From Visible Friction

For bot mitigation, always separate these questions:

- Should this surface be protected at all?
- Should the challenge exist only on selected flows?
- Should it be invisible by default?
- When should a visible challenge appear?
- How should QA force challenge or fail modes outside production?

Prefer low-friction defaults on important user flows.

### 7. Validate Against Server Truth

If a protection depends on client-supplied state, explicitly test whether it can be bypassed.

Examples:

- Client-provided conversation ID
- Client-provided verification status
- Client-provided step completion
- Replayable tokens
- "First request only" logic tied to untrusted state

If client state can be forged, require server-truth validation.

### 8. Produce Either An Audit Or An Implementation Plan

By default, output an audit and a proportional hardening plan.

Only switch into implementation mode when the user explicitly asks for execution.

Implementation plans should separate:

- Edge or provider changes
- App or code changes
- UX or challenge behavior changes
- Verification steps
- Rollback steps

### 9. Verify Adversarially

Use `references/verification-benchmarks.md`.

After the audit or implementation, run a second-pass review:

- Can a client-controlled value bypass the control?
- Does the schema match runtime assumptions?
- Does the behavior hold in the real runtime, not just in code?
- Do non-default locales or variants break the flow?
- Are there differences between technical validation and real human-production validation?
- Are there QA modes for what cannot be proven reliably in production automation?

Treat "implemented" and "actually hardened" as different states.

### 10. Persist Learning Carefully

Use `scripts/record_learning.py`.

When a new provider path, vendor capability, or local wrapper workflow is observed:

- Write it to `references/runtime-learning.md` first if it is still provisional or newly discovered.
- Promote it to `references/verified-learning.md` only after it has been proven in real behavior.
- Do not add theory, guesses, or doc-only claims to verified learning.

This is the skill's auto-learning loop.

## Output Format

Produce these sections:

### A. Context Classification

- Product type
- Exposure level
- Cost-sensitive surfaces
- Why this app is or is not a meaningful abuse target

### B. Abuse Surface Matrix

For each surface, include:

- Surface
- Access level
- Abuse mode
- Business impact
- Existing controls
- Gap
- Recommended control family
- Recommended implementation layer
- Verification method

### C. Defense Plan

Group by layer:

- Edge or provider controls
- HTTP and security headers
- App logic
- UX and challenge behavior
- Documentation and QA

### D. Provider Fit

State clearly:

- Whether a provider layer is justified
- Whether native platform controls are enough
- Whether Cloudflare is recommended, optional, or unnecessary
- Which provider features are actually relevant in this context

### E. Execution Path

State clearly:

- What can be done via CLI, API, or MCP
- What still requires browser fallback
- Which local wrappers or scripts already exist
- What should be verified read-only first
- What should not be changed without explicit implementation approval

### F. Prioritization

- P0
- P1
- P2
- Optional

### G. Verification Plan

Separate:

- What can be verified automatically
- What needs runtime proof
- What needs human validation
- What remains uncertain

### H. Scope Boundary

State clearly:

- What this skill covered
- What it did not cover
- Which other specialized audits or skills are needed next

## Final Rule

This skill is about abuse resilience of public or weakly protected business surfaces.

It is not a generic "security" skill.
It is not a full pentest skill.
It is not an infrastructure-wide security skill.
It is not a complete vulnerability detection skill.

If the request goes broader than exposed abuse surfaces, say so explicitly before continuing and route toward a wider audit or other specialized security skills.
