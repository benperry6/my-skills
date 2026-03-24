---
name: "my-personal-seo-market-mapper"
description: "[My Personal Skill] Turn a business offer into an actionable SEO market map. Use when the user wants SEO market research, keyword discovery, cluster mapping, page and hub prioritization, geo/programmatic/tool opportunities, or competitor refinement. Produces a business-aware SEO map with P1/P2/P3 priorities. Not for final domain selection, final content writing, or site implementation."
---

# SEO Market Mapper

## Purpose

This skill converts business context into an actionable SEO market map.

It should identify:
- business-relevant demand
- keyword clusters and sub-clusters
- pages to launch first
- hubs and supporting pages
- geo, programmatic, and tool opportunities
- second-pass competitor findings
- durable outputs for downstream skills

This skill is not for:
- final domain selection
- final content writing
- site build or implementation
- broad branding work detached from SEO demand mapping

## Core doctrine

Default rules:
- context first, tools second
- business fit beats vanity traffic
- volume matters only inside the right business lens
- keyword difficulty is reporting context, not the main sorting rule
- interpretation, deduplication, prioritization, and decisions stay centralized
- never invent search volume, CPC, or keyword difficulty
- if hard data is missing, mark it explicitly as qualitative or unverified

This skill uses three demand circles:

1. `Direct Demand Capture`
- keywords closest to the offer and action
- label as `P1`
- launch first

2. `Business-Relevant Demand Capture`
- demand still materially connected to the offer, the customer problem, or a situation the offer can solve
- broader than direct demand, but still part of the first real market map
- label as `P2`

3. `Authority Expansion`
- broader niche demand used later to grow topical authority
- label as `P3`
- only expand when the user asks for it or when `P1` and `P2` are already sufficiently covered

Important default:
- the first market map covers `P1` and `P2`
- `P3` is an expansion layer, not the default launch scope

## When to use

Use this skill when the user wants:
- SEO market research
- keyword research for a business or site
- cluster mapping
- hub and spoke planning
- page priorities for SEO
- SEO architecture
- geo SEO opportunities
- programmatic SEO opportunities
- competitor-led refinement of an existing keyword map

Do not use this skill when the user wants:
- final domain selection
- EMD validation
- domain availability checks
- final article or landing page writing
- site implementation

## Workflow

Follow this order strictly.

### 1. Ingest the business context first

Before doing keyword research, inspect the existing context.

Prioritize:
- `.agents/`
- `.claude/`
- business docs
- architecture docs
- prior keyword research
- competitor notes
- source and transcript files if available

The goal is to identify:
- the offer
- the target lead
- the desired conversion action
- what counts as bad traffic
- geographic scope
- business constraints that change keyword value

Do not ask the user questions already answerable from the repo.

### 2. Define the business lens explicitly

State clearly:
- what the offer is
- who the target lead is
- what qualified demand means here
- what bad traffic means here
- which kinds of queries are direct, adjacent, or too generic

This step is mandatory because the whole market map depends on how demand is interpreted.

### 3. Choose the mapping mode

Infer the mode from the request.

Modes:
- `initial-market-map`
  - default
  - covers `Direct Demand Capture` and `Business-Relevant Demand Capture`
- `authority-expansion`
  - only for broader niche demand after the core map is in place
- `refinement`
  - update an existing map with deeper cluster work or competitor findings

### 4. Route the data source by market

Default routing:
- France: `Haloscan` first
- non-France: `DataForSEO` first
- fallback allowed when the preferred source cannot do the job well enough

Important:
- do not use DataForSEO for French discovery if Haloscan can do it
- do not stay blocked on Haloscan outside France

### 5. Build the initial demand universe

Start from:
- offer language
- customer problem language
- situation-based language
- existing repo language
- known competitor language
- geographic constraints
- tool or calculator opportunities if they are business-relevant

Do not jump straight to one keyword list.
First build the universe of ways the market expresses the problem.

### 6. Cluster the demand

Organize the universe into clusters and sub-clusters.

For each cluster, capture:
- cluster name
- why this cluster matters for the offer
- exploitable volume for the business
- total observed volume
- dominant intent mix
- risk of low-fit traffic
- recommended page types
- cross-links to other clusters

For each important keyword or page idea, capture:
- `circle`: `direct-demand-capture`, `business-relevant-demand-capture`, or `authority-expansion`
- `launch_priority`: `P1`, `P2`, or `P3`
- `intent`: `Informational`, `Commercial`, `Transactional`, `Navigational`, or mixed
- `data_status`: `verified` or `qualitative`

Default mapping:
- `Direct Demand Capture` -> `P1`
- `Business-Relevant Demand Capture` -> `P2`
- `Authority Expansion` -> `P3`

### 7. Apply prioritization rules

Prioritize by:
- business fit
- demand volume inside the right intent
- expected lead quality
- strategic leverage for the site architecture
- geo, programmatic, or tool multiplier effects

Do not prioritize mainly by:
- keyword difficulty
- vanity volume
- generic category traffic
- topics with weak business relevance

Edge case:
- if `P1` demand is genuinely thin, do not force fake `P1`
- say so explicitly and pivot to the strongest `P2` opportunities

### 8. Decide whether deep-dives should be exhaustive or selective

Deep-dives are not optional fluff.
They turn a rough map into an actionable page and architecture plan.

Default rule:
- in `initial-market-map`, deep-dive exhaustively all `P1` and `P2` clusters
- in `authority-expansion` or `refinement`, deep-dive only the targeted clusters

Why:
- `P1` and `P2` define the launch roadmap
- `P3` is expansion work and should not automatically receive the same depth

A deep-dive should clarify:
- the exploitable subset vs total observed demand
- the intent mix
- the highest-value pages to create
- the internal links to neighboring clusters
- the risks of low-fit traffic

### 9. Refine with competitors as a second-pass layer

Competitor refinement is a second-pass layer, not a mandatory first step.

Use it after a solid first market map already exists, especially when:
- the user provides competitor names
- the first map still feels incomplete
- real market winners may reveal missed demand
- you want to expand or correct existing clusters with live market evidence

The purpose is not just to see where competitors rank.
The purpose is to discover:
- missing keywords
- missing sub-clusters
- missing page formats
- adjacent solution paths worth capturing

This second-pass refinement can:
- strengthen existing clusters
- create new sub-clusters
- justify a new cluster if the evidence is strong enough

Use three competitor types.

#### A. Offer competitors

Definition:
- same lead
- same promise
- same problem solved

Why they matter:
- if the lead converts with them, we lose the lead
- we want to identify the non-brand demand they capture from our market

How to find them:
- from the business context
- from user-provided names
- from SERPs on core offer queries
- from known players repeatedly associated with the offer type

#### B. SEO competitors

Definition:
- domains or pages that rank on our target SERPs, even if their business model differs

Why they matter:
- they show what Google rewards on the SERP
- they reveal winning formats, angles, and topics

How to find them:
- inspect top results on cluster keywords
- note recurring domains or pages across multiple SERPs
- separate domain-level presence from page-level wins

#### C. Adjacent-solution competitors

Definition:
- alternative ways a user might solve the same problem without thinking of our offer or our direct keywords

Why they matter:
- they reveal new clusters where our offer can be positioned as an alternative

How to find them:
- look for alternative solutions mentioned in SERPs, PAA, FAQs, competitor pages, and market language
- identify solution categories the user may consider before our offer

#### Classification rule

For each candidate competitor, apply this decision tree:
1. same lead + same promise + same problem solved -> `offer competitor`
2. else if it repeatedly ranks on our target SERPs -> `SEO competitor`
3. else if it represents an alternative path to solve the same problem -> `adjacent-solution competitor`

For every competitor documented, store:
- `type`
- `source`
- `why it belongs in that type`
- `what we learn from it`

### 10. Derive the SEO architecture

Turn research into an actionable site map.

Possible outputs:
- hub pages
- supporting pages
- tool or calculator ideas
- geo pages
- programmatic page families
- FAQ or glossary opportunities
- comparison pages
- internal linking logic

The output should answer:
- what gets built first
- what supports what
- which pages are pillars
- which pages are supporting assets

### 11. Write durable outputs

Write or update outputs under:

```text
.agents/seo-market-mapper/
  market-map.md
  cluster-index.md
  clusters/
  competitors/
```

Default rule:
- canonical cross-skill truth files stay at `.agents/` root
- working outputs for this skill stay under `.agents/seo-market-mapper/`

Do not update the canonical context-distillation files unless the user explicitly asks for that separate job.

`cluster-index.md` is mandatory.
It gives downstream skills a compact handoff contract without forcing them to read every cluster file first.

### 12. Handoff cleanly

End by stating what the next skill should do.

Typical handoffs:
- domain selection -> `my-personal-seo-first-domain-selector`
- implementation or build -> engineering or build skill

## Orchestration rule

Default orchestration:
- one main agent owns the reasoning
- tool calls can run in parallel when helpful
- data collection may be parallelized
- interpretation, deduplication, prioritization, and final decisions stay centralized

Use sub-agents only when the sub-task is:
- mechanical
- independent
- low-interpretation
- safe to merge without business ambiguity

Do not use sub-agents for:
- final cluster definitions
- final page prioritization
- final competitor classification
- final architecture decisions

## Guardrails

Always enforce these unless the user overrides them:
- during the initial market map, do not optimize for generic demand detached from the offer
- in authority expansion, broader demand is allowed only when a credible bridge back to the business is explicit
- do not let `P3` authority expansion delay, outrank, or replace `P1/P2` priorities in the launch roadmap
- do not sort mainly by keyword difficulty
- do not classify competitors without recording source and reason
- do not jump to final domain ideas inside this skill
- do not drift into full content writing or actual site implementation inside this skill
- do not ignore SERP features when they materially affect viability

## Output requirements

### Chat response

Use this structure:
1. `Présupposés`
2. `Business context retained`
3. `Demand circles`
4. `Cluster map`
5. `Priority labels (P1/P2/P3)`
6. `Competitor findings` (if used)
7. `SEO architecture recommendations`
8. `Files written or updated`
9. `Next handoff`

### `market-map.md`

Use this structure:
- Date
- Objective
- Business context retained
- Geographic scope
- Data source used
- Mapping mode used
- Demand circles summary
- Cluster summary table
- Priority pages to launch first
- Hub and spoke recommendations
- Geo, programmatic, and tool opportunities
- Competitor insights
- Open questions
- Recommended next handoff

### `cluster-index.md`

Use this structure:
- cluster name
- circle
- launch priority
- intent mix
- volume exploitable
- volume total
- recommended page types
- whether a deep-dive file exists
- whether competitor refinement changed the cluster
- notes for downstream skills

### Cluster deep-dive files

For each cluster, use:
- Cluster name
- Date
- Source
- Status
- Cluster synthesis
- Why this cluster matters for the offer
- Volume exploitable
- Volume total
- Dominant intents
- Keyword table
- Priority labels
- Recommended pages
- Cross-cluster links
- Risks and notes

## Success criteria

A good result from this skill means:
- the map is business-aware, not just SEO-aware
- `P1` pages are obvious
- the first launch scope is realistic
- the broader roadmap is visible
- downstream skills can pick up the outputs without redoing the research
