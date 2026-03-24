---
name: my-personal-seo-first-domain-selector
description: "[My Personal Skill] Use when the user wants to choose a domain name with a SEO-first EMD or quasi-EMD strategy, compare keyword-based domain options, validate an EMD theory, or rank shortlist candidates using keyword volume, SERP intent, and real registrar-backed availability. Not for pure branding, creative naming, trademark clearance, or simple raw availability checks on a fixed list."
metadata:
  version: 1.0.0
---

# SEO-First Domain Selector

This skill selects the best **SEO-first keyword-domain**, not the prettiest brand.

Its job is to answer:
- which searched keyword should become the domain
- which keyword-domain best exploits an EMD or quasi-EMD strategy
- whether the highest-volume candidate is actually relevant enough
- whether Google's SERP intent matches the offer closely enough
- whether the final candidates are really available

This is **not**:
- a branding skill
- a brainstorming skill
- a trademark clearance skill
- a simple availability checker

## Core theory

The user’s theory is:
1. choose an EMD or quasi-EMD on a searched keyword
2. rank faster on that keyword
3. satisfy intent strongly once users land
4. concentrate clicks and usage signals on that term
5. let Google progressively associate the keyword with the site in a brand-like way

Therefore the skill must maximize **relevant keyword volume**, not generic volume.

## Trigger guidance

Use this skill when the request is about:
- EMD / exact match domain
- keyword-based domain selection
- best domain for SEO
- domain name based on keyword
- which domain should we choose to rank
- compare several SEO-first domain options
- validate an EMD theory
- shortlist domains using volume + SERP + availability

Do **not** use this skill when the request is about:
- pure branding
- catchy or creative names
- trademark research or legal clearance
- checking a fixed list of domains for availability only

For raw availability checks only, call the dedicated checker directly:

```bash
python3 "/Users/benjaminperry/My Drive/ProStrike Holdings/VisualCode/Registrar Domain Availability Checker/check-domains.py" --mode final --json domain1.com domain2.com
```

## Workflow

Follow this order strictly. Do not jump to domain ideas before business context and search intent are clear.

### 1. Ingest the project context first

Before asking the user anything, inspect the repo and existing docs.

Prioritize:
- `.agents/`
- `.claude/`
- keyword research files
- product / business context files
- prior decision docs
- architecture docs if they clarify the offer

Default goal:
- identify the offer
- identify the exact lead or buyer the site wants
- identify what would count as bad traffic
- identify how narrow the niche can be before volume collapses

If that context is already in the repo, do not re-ask it.
Ask the user only if the business context is still too ambiguous to know what “relevant keyword volume” means.

### 2. Define the SEO job to be done

State explicitly:
- what the offer is
- who the target visitor is
- what action they should take
- what kind of query intent must be captured
- what kind of traffic would be harmful

This step matters because the skill must reject high-volume keywords that attract the wrong traffic.

### 3. Route the keyword data source by market

Default routing:
- **France**: use `Haloscan` first
- **Non-France**: use `DataForSEO` first
- fallback is allowed when the preferred source does not cover the task well enough

Important:
- do not use DataForSEO for French keyword discovery if Haloscan can do the job
- do not stay blocked on Haloscan outside France, DataForSEO is the better international source

### 4. Build the candidate keyword pool

Start from existing material first:
- current keyword research
- cluster docs
- known market language
- competitor language
- phrases already validated in the repo

Only add fresh queries when necessary to fill gaps.

Target:
- exact-match or quasi-exact-match candidates
- literal keyword-domains
- boring, descriptive candidates are acceptable

Avoid:
- made-up brand names
- vague category words
- catchy but data-free names

Longer domains are acceptable if:
- the keyword is strongly aligned
- the SERP intent is right
- the search volume meaningfully improves

### 5. Rank by relevant volume, not raw volume

For each strong candidate, evaluate:
- search volume
- CPC or equivalent commercial signal
- exactness of fit with the offer
- risk of attracting the wrong audience
- length and oral usability
- how much explanatory burden the name creates

Make the trade-off explicit.

Typical pattern:
- highest volume, wrong intent -> reject
- medium volume, mixed intent -> caution
- lower volume, strong fit -> viable

Do not rank by keyword difficulty as the main sorting logic unless the user explicitly changes the objective.

### 6. Perform mandatory SERP validation

This is a **hard gate**, not a nice-to-have.

Keyword data generates candidates. SERP validation decides whether a candidate is actually admissible.

Why this step is critical:
- a keyword can have strong volume and still be the wrong domain if Google interprets the query differently from the offer
- if the domain matches the keyword but the page does not match the SERP intent, users will disengage or bounce
- that breaks the whole EMD theory: weak usage signals prevent Google from associating the keyword with the site in a brand-like way
- therefore, if the SERP contradicts the offer, reject the candidate even if its keyword metrics look better

For the best candidates, inspect the real SERP and the key pages behind it.

The goal is not only to see rankings. The goal is to reverse-engineer Google’s interpretation of intent and verify that this keyword can realistically support the user’s EMD strategy.

Check:
- top results type
- transactional vs informational balance
- whether direct operators rank
- whether guides dominate
- whether the user’s offer type already appears in the top results
- whether the SERP is dominated by giants that imply a different intent

Inspect actual page content for the key results when needed. Do not infer intent from titles alone if the decision is important.

Strict rules:
- never finalize a meaningful domain recommendation without this step
- reject any candidate whose SERP is materially misaligned with the offer
- prefer the lower-volume candidate if its SERP clearly matches the offer better
- never treat keyword volume or CPC as sufficient proof of domain fit on their own

### 7. Verify real availability

Use the checker as the final availability gate:

```bash
python3 "/Users/benjaminperry/My Drive/ProStrike Holdings/VisualCode/Registrar Domain Availability Checker/check-domains.py" --mode final --json candidate1.com candidate2.com
```

For multi-TLD checks:

```bash
python3 "/Users/benjaminperry/My Drive/ProStrike Holdings/VisualCode/Registrar Domain Availability Checker/check-domains.py" --mode final --json --brand mailhoist --tlds com,fr,co,io,app,net,org
```

Use the checker with a simple decision rule:
- if it confirms the domain is available strongly enough, it can be recommended
- if it confirms the domain is taken, reject it
- if it is not verified strongly enough, do not present it as really available

The skill does not need to expose or explain the checker’s full internal certainty model unless the user explicitly asks.

### 8. Recommend a ranked shortlist and one winner

Final output should contain:
- a ranked top 10
- one clear winner
- one short factual reason per candidate
- an explicit explanation for why #1 beats #2

## Default guardrails

Always enforce these unless the user overrides them:
- pragmatic trademark filter: reject names that directly include, combine, or closely mimic well-known third-party brands, especially for products in a related category. Treat obvious brand piggybacking as invalid by default and prefer neutral names.
- do not let availability override SEO fit
- do not let raw volume override intent
- do not let SERP assumptions replace SERP inspection

## Output requirements

### Chat response

Use this structure:
1. `Assumptions`
2. `Selected business context`
3. `Shortlist of keyword domains`
4. `Volume vs. relevance trade-off`
5. `SERP analysis`
6. `Availability results`
7. `Final top 10`
8. `Winner + why`

### Decision file

Write or update:

```text
.agents/decisions/domain-selection.md
```

Use this structure:
- Date
- Objective
- Business context retained
- Target market / country / TLD targeted
- Data source used
- Candidates reviewed
- Keyword signals
- SERP analysis
- Availability results
- Final recommendation
- Residual risks / uncertainties

This file is a durable decision trace, not a raw dump of every tool response.

## Success criteria

A good result from this skill means:
- volume is filtered by relevance
- SERP intent was actually checked
- domain availability was actually checked
- the reasoning is durable and documented

If the result is just “10 nice names,” the skill failed.
