---
name: my-personal-paid-tracking-foundation
description: "[My Personal Skill] Use when a project needs a paid media tracking foundation that is professional but budget-friendly. Trigger for requests about Meta Pixel, TikTok Pixel, GA4, GTM, server-side tracking, CAPI, conversion tracking, audience building before paid spend, tracking architecture for a new SaaS/e-commerce/content site, or deciding what to install now vs later."
---

# My Personal Paid Tracking Foundation

## Overview

This skill chooses the right paid media tracking foundation for a project without defaulting too early to expensive enterprise infrastructure. It is designed to recommend a clear baseline, explain the trade-offs, and then output a concrete implementation plan rather than a vague comparison.

## Trigger Conditions

Use this skill when the user asks any variation of:

- "What tracking stack should I install now?"
- "Do I need Meta Pixel / TikTok Pixel / GA4 / GTM / CAPI?"
- "How do I prepare paid ads before I actually spend?"
- "Should I use browser-side, server-side, or both?"
- "What is the budget-friendly version of a serious paid tracking stack?"
- "What should I install on a new SaaS / e-commerce / affiliate site?"

Do not use this skill for:

- product analytics questions that are not about paid media readiness
- campaign strategy or bidding decisions
- creative generation

## Operating Principle

This skill is opinionated on purpose.

Its job is not to list every possible stack. Its job is to recommend the right foundation for the current context, then explain why that recommendation is the right trade-off now.

The canonical bias is:

1. Start collecting useful signal early
2. Avoid paying for heavy infrastructure before the business is proven
3. Keep a clean upgrade path toward a more industrial setup later

## Decision Workflow

### Step 1 — Classify the project

Read:

- `references/project-archetypes.md`
- `references/maturity-stages.md`

Determine and state explicitly:

- project type
- maturity stage
- current acquisition model
- whether paid media is live, planned soon, or purely future-facing

If a project spans multiple models, choose the revenue motion that matters most in the next 6-12 months and call out the secondary motion separately.

### Step 2 — Choose the vendor priority

Read:

- `references/vendor-priority.md`

Default to disciplined rollout. Do not recommend opening a large number of platforms just because they exist.

### Step 3 — Choose the stack recipe

Read:

- `references/stack-recipes.md`

Pick the closest recipe and adapt only where the context clearly justifies it.

### Step 4 — Prepare the access and execution checklist

Read:

- `references/access-checklist.md`

Separate clearly:

- what the agent can design, wire, and verify
- what the user must provide as accounts, IDs, tokens, or admin access

## Canonical Doctrine

Unless the context proves otherwise, the default doctrine is:

- In pre-revenue or validation, do **not** default to a paid sGTM/GCP setup
- Prefer a **hybrid** foundation
- Browser-side is necessary for pixels, audiences, and browser-native signals
- A first-party event store is mandatory
- Server-side should exist early in a selective low-cost form via the existing backend or hosting layer
- A heavier server-side infrastructure is justified only after real traction, sustained spend, or operational pain

This doctrine exists for a business reason, not a tooling reason:

- collect data early
- avoid premature fixed costs
- prepare future paid media without pretending the business is already scaling
- upgrade infra only when the business can justify it

## What the Agent Does vs What the User Must Provide

### The agent should do

- classify the project and maturity stage
- recommend the stack
- explain the why and trade-offs
- define the event model at the right ambition level
- produce the implementation order
- produce the access checklist
- identify when a later infra upgrade becomes justified

### The user must typically provide

- account access
- container IDs
- pixel IDs
- tokens / secrets
- DNS or hosting admin access where relevant

Do not blur those two responsibilities in the final answer.

## Output Format

The final output of this skill should always include these sections:

1. **Diagnostic**
   - short classification of the project and current stage
2. **Recommended stack**
   - the opinionated foundation to use now
3. **Why this is the right trade-off now**
   - business and technical justification
4. **Executable plan**
   - ordered next steps
5. **Access / IDs / tokens needed**
   - what the user must provide
6. **Upgrade criteria**
   - what would justify moving to a heavier stack later

Do not output a neutral vendor matrix unless the user explicitly asks for a comparison. The default must be a recommendation.

## Anti-Patterns

Actively call out these mistakes when relevant:

- paying for enterprise tracking infra before revenue exists
- assuming browser-only is enough
- assuming server-only replaces pixels and browser-side audiences
- opening too many vendors too early
- over-engineering attribution before the business model is proven
- confusing "collecting signal early" with "needing a full enterprise stack immediately"

## Defaults and Escalation

If the user gives little context, default to:

- pre-revenue / validation
- low-cost hybrid setup
- Google, then Meta, then TikTok only if justified

Only escalate beyond that when the context clearly supports it.

If a recommendation depends on a missing fact, state the assumption explicitly instead of hiding it.
