# Post-Distillation Handoff

Use this reference after a successful `bootstrap`, `update`, or meaningful `performance-update`.

## Goal

Turn freshly updated canonical context into an actionable next-step execution plan.

The handoff must not stop at:

- "run `product-marketing-context` next"
- a short guessed list of skills
- unordered skill suggestions with no method

It must recommend:

- the immediate next skill
- the ordered sequence after that
- the execution method for the sequence
- which skills are deferred until later

## Required First Step

If the canonical files were successfully updated, the immediate next skill is:

- `product-marketing-context`

That is the compilation step that prepares downstream marketing work.

If the project is still in the early business-foundation phase and SEO is expected to shape what gets built next, recommend:

1. `product-marketing-context`
2. `my-personal-seo-market-mapper`

before recommending SEO-shaped execution skills.

## Live Inventory Requirement

Before choosing any downstream skills, inspect the full live installed skill inventory by running:

```bash
python3 ~/.agents/skills/my-personal-context-distillation/scripts/list_installed_skills.py
```

Reason over the full live list.
Do not rely on memory.
Do not stop at the first few plausible skills.
Do not paste the raw full inventory into the final user-facing report unless the user explicitly asks for it.

## Foundation vs Later

When recommending next skills, prefer `business foundation` work first.

Typical foundation work includes:

- positioning and compiled context
- SEO market mapping when SEO is part of the near-term acquisition plan
- pricing and packaging
- site architecture and page planning
- core messaging and page copy
- launch planning
- early sales collateral
- initial outbound or lead-generation assets when they are part of the go-to-market plan

Typical later-stage or post-launch work to defer by default includes:

- CRO
- A/B testing
- churn reduction
- SEO audits
- analytics or instrumentation tuning
- optimization layers that assume a live site or active funnel

Do not defer a skill merely because it is marketing-related.
Defer it when it is primarily about optimizing an already launched system rather than establishing the business foundation.

If `my-personal-seo-market-mapper` is the expected next strategic step, do not front-load skills whose output should be shaped by that map.

Common examples to hold until after the map:

- `site-architecture`
- `content-strategy`
- `competitor-alternatives`
- `programmatic-seo`
- SEO-led page-copy production

## Recommended Execution Method

Default orchestration:

1. sequential compilation first
2. sequential strategy and structure work second
3. parallelize only the independent execution layers after shared strategic decisions are fixed

Practical default:

1. `product-marketing-context`
2. `my-personal-seo-market-mapper` when SEO is part of the near-term plan
3. strategy / structure skills such as pricing, site architecture, or launch planning
4. execution skills such as copywriting, sales enablement, lead magnets, or outbound assets

Parallelize only when the outputs no longer depend on unresolved upstream decisions.

Examples:

- If pricing is undecided, do not run pricing-dependent page copy first.
- If site architecture is unsettled, do not branch into multiple page-production skills yet.
- Once the structure and positioning are stable, content production skills can be recommended in the same phase.

## What `Recommended next step` Should Contain

Inside the report section `Recommended next step`, include:

- `Immediate next skill: ...`
- `Live skills scanned: ...`
- `Foundation skills considered: ...`
- `Recommended sequence: ...`
- `Execution method: ...`
- `Deferred until later: ...`

Keep it concise, but make it operational.
