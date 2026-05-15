---
name: linkedin-personal-branding
description: Comprehensive LinkedIn personal branding analysis, profile optimization, and visibility improvement skill using Claude for Chrome browser tools. Use when users request LinkedIn profile analysis, personal branding audit, profile optimization recommendations, LinkedIn visibility improvement, headline optimization, About section review, content strategy guidance, engagement analysis, or Social Selling Index improvement. Works with Claude for Chrome to analyze profile photos, banners, headlines, About sections, experience, skills, recommendations, featured content, activity/posts, and network engagement directly from the user's browser.
---

# LinkedIn Personal Branding Skill

## Purpose

Use this skill to audit and improve a LinkedIn profile, personal brand, content strategy, and visibility using the user's real LinkedIn session when available.

This skill supports:

- full profile audits
- quick profile reviews
- headline and About section optimization
- content strategy and engagement analysis
- visibility and discoverability improvements
- Social Selling Index review when available

## Required Context

Before producing recommendations, identify and include these fields in the report header:

- industry or sector
- profile type: employee, consultant, freelancer, entrepreneur, or job seeker
- target audience: recruiters, clients, peers, investors, partners, or other
- geographic and language focus
- engagement rate when post metrics are available
- SSI score when available, or mark as estimated/unavailable

Do not apply generic LinkedIn advice without first classifying the profile and audience.

## Reference Map

Use these references for detailed execution:

- [references/full-operating-manual.md](references/full-operating-manual.md) - complete workflow preserved from the long-form skill
- [references/scoring_framework.md](references/scoring_framework.md) - profile scoring criteria
- [references/metrics_benchmarks.md](references/metrics_benchmarks.md) - industry-specific benchmarks
- [references/content_strategy.md](references/content_strategy.md) - posting and content strategy guidance
- [assets/profile_audit_template.md](assets/profile_audit_template.md) - full audit report template
- [assets/quick_review_template.md](assets/quick_review_template.md) - quick review template
- [assets/action_plan_template.md](assets/action_plan_template.md) - action plan template

## Workflow

1. Determine the analysis type: full audit, quick review, content strategy, visibility optimization, or focused section rewrite.
2. Classify the profile by industry, role type, audience, market, and language.
3. Gather profile data from the user's available LinkedIn page or from user-provided screenshots/text.
4. Score the relevant sections using the scoring framework.
5. Compare metrics against the appropriate industry benchmarks when metrics exist.
6. Produce prioritized recommendations tied to the user's audience and goals.
7. Return an actionable report with quick wins, strategic fixes, and next steps.

## Browser Rules

Prefer direct profile data provided by the user. When browser access is needed, use the active authenticated browser session according to the current environment's browser-safety rules.

Do not close tabs, alter profile content, publish posts, send messages, change account settings, or interact with other users unless explicitly requested.

## Sections To Audit

Audit only the sections relevant to the request:

- profile photo
- banner image
- headline
- About section
- featured section
- experience
- skills and recommendations
- services section for consultants or freelancers
- recent posts and activity
- creator analytics or SSI if available

## Output Standards

Every full audit should include:

- profile classification
- scored findings by section
- benchmark context where metrics exist
- prioritized recommendations
- examples of improved copy where useful
- risks, assumptions, and missing data
- a concise action plan

Keep advice specific to the user's industry, audience, and current profile state.
