# Dynamic Skill Selection For Value-First Compliance Assets

Use this reference when a legal/compliance gap requires a customer-facing asset that should be designed value-first and compliance-second.

## Goal

Do not hardcode a fixed list of downstream skills.

Instead:

1. inspect the full live installed skill inventory
2. reason from that live inventory
3. choose only the skills that are relevant to the current asset and business context
4. recommend an ordered orchestration, not just names

## Why This Matters

The installed skill set is not stable.

New skills may be added.
Old skills may be removed.
Existing skills may evolve.

If the agent relies on memory or on a stale shortlist, it will usually overuse the first few familiar skills and miss better-fit tools that are currently installed.

## Live Inventory Requirement

Before choosing downstream skills, run:

```bash
python3 ~/.agents/skills/my-personal-product-legal-review/scripts/list_installed_skills.py
```

Reason over the full live list.
Do not stop at the first few plausible skills.
Do not paste the raw full inventory into the final user-facing report unless explicitly requested.

## Selection Logic

Choose skills based on the actual asset to produce.

Examples:

- if the asset is an email, think about skills relevant to email copy, lifecycle logic, churn, or offer framing
- if the asset is an in-product upgrade or confirmation surface, think about paywall, onboarding, popup, or page CRO style skills
- if the asset is a broad messaging or trust surface, think about copywriting, positioning, product-marketing context, or structure skills
- if the asset needs visual UI work, think about the currently installed design or frontend-routing skills according to the project convention

Do not assume the same skill set will be right for every business.

## Ordering Rule

Prefer:

1. foundation or strategy skill first
2. execution skill second
3. optimization skill later

Examples:

- if messaging or framing is unclear, do not jump straight to UI execution
- if the asset is really an email lifecycle problem, do not default to generic page-copy skills
- if the asset needs delegated frontend work, choose the strategic skill first, then the routing / implementation path

## Output Requirement

When this logic is used, report:

- how many live skills were scanned
- which skills were considered relevant
- which skill is the primary driver for this asset
- the recommended execution order
- which skills were ignored or deferred because they are not the best fit for this task
