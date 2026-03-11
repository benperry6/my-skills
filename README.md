# My Skills

This repository is the private home of my custom AI skills.

It is not just a random collection of prompts.

It is a working layer of reusable operational knowledge designed to make agents more useful across my real businesses and workflows.

## Why this repo exists

General-purpose AI agents are now very good at execution.

They can:

- read and write code
- search the web
- inspect files
- run tools
- automate workflows
- produce content

But raw capability is not enough.

The quality of the output still depends on two missing layers:

- specialization
- context

Skills solve the specialization problem.

They give a general agent:

- reusable workflows
- domain-specific guardrails
- bundled references
- deterministic helper scripts
- a repeatable way to think about a task

That matters because a general model can reason about almost anything, but it should not have to rediscover the same process from scratch every time.

## What makes these skills personal

Some skills are generic and broadly reusable.

Others are deeply shaped by how I work, what I build, and what I care about.

My personal skills usually exist because I want one or more of these things:

- a stronger output quality bar than the default
- a workflow that matches my real operating model
- a reusable method across many repos
- a way to preserve hard-won thinking instead of re-explaining it every session

They are not just "nice to have".

They are how I turn AI agents into repeatable collaborators instead of one-off assistants.

## Core philosophy

The underlying idea behind this repo is simple:

an agent becomes dramatically more useful when it has both:

- the right execution workflow
- the right context structure

That is why this repo contains skills across different layers:

- execution skills
- analysis skills
- writing skills
- context-building skills
- quality-control skills

Some skills help agents do the work.

Some skills help agents think better before doing the work.

Some skills make sure the next skill downstream does not have to operate in a vacuum.

## Featured personal skills

These are the skills that most clearly represent the way I want to work with AI agents.

| Skill | What it does | Why it matters |
|-------|---------------|----------------|
| [`my-personal-context-distillation`](./my-personal-context-distillation/README.md) | Turns messy founder notes, transcripts, market research, and learnings into durable source-of-truth context files plus a persistent VoC bank | Creates the missing context layer that makes downstream marketing and content work far less generic |
| [`my-personal-technical-writer`](./my-personal-technical-writer/SKILL.md) | Improves developer-facing documentation, READMEs, references, and tutorials | Helps convert technical work into clear, usable documentation |
| [`my-personal-executive-summary`](./my-personal-executive-summary/SKILL.md) | Produces concise executive-level summaries and strategic briefs | Useful when analysis exists but decision-makers need clarity, not raw detail |
| [`my-personal-developer-advocate`](./my-personal-developer-advocate/SKILL.md) | Supports DX, API onboarding, dev education, and developer-facing strategy | Bridges product, documentation, and audience understanding |
| [`my-personal-accessibility-auditor`](./my-personal-accessibility-auditor/SKILL.md) | Audits accessibility with real tooling and browser checks | Raises the quality bar beyond surface-level a11y commentary |
| [`my-personal-image-prompt-engineer`](./my-personal-image-prompt-engineer/SKILL.md) | Crafts high-quality prompts for image generation tools | Turns vague creative asks into structured, production-usable prompts |
| [`my-personal-og-image-mastery`](./my-personal-og-image-mastery/SKILL.md) | Covers both the technical and CTR-side strategy of Open Graph images | Useful because good OG images are both a design problem and a growth problem |

## Why `my-personal-context-distillation` matters so much

One skill deserves special mention because it sits unusually far upstream:

- [`my-personal-context-distillation`](./my-personal-context-distillation/README.md)

This skill exists because execution alone is not enough.

Across many businesses, the real bottleneck is not whether an agent can write something.

It is whether the agent knows enough about:

- the business model
- the story
- the customer
- the real market voice
- the accumulated learnings

Without that, even a strong agent tends to produce content that is still too generic.

So this skill was built as a foundational layer: it creates the durable memory that other skills can later consume.

## Repo layout

Each skill lives in its own folder.

Typical structure:

```text
skill-name/
├── SKILL.md
├── README.md              # Optional human-facing presentation page
├── references/            # Loadable supporting material
├── scripts/               # Helper scripts when determinism matters
└── agents/                # Tooling-specific metadata when needed
```

Notes:

- `SKILL.md` is the operational contract for the agent
- `README.md` is the human-facing explanation when a skill deserves a proper presentation page
- `references/` keeps detailed material out of the core skill body
- `scripts/` are used where reliability or repeatability matters more than re-generating code every time

## How I use this repo

In practice, this repo is meant to be:

- edited locally
- versioned privately
- synced between machines
- reused across many working sessions and repos

The goal is not just to store files.

The goal is to accumulate reusable intelligence.

## Installation

```bash
npx skills add benperry6/my-skills
```

## Final idea

This repo is how I try to close the gap between:

- what agents can technically do
- and what they need in order to do it well, repeatedly, across real business contexts

The more important the work becomes, the less I want to rely on generic prompting alone.

That is what these skills are for.
