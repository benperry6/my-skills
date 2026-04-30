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
- a differentiated output layer that does not collapse into the same patterns as commodity AI usage

They are not just "nice to have".

They are how I turn AI agents into repeatable collaborators instead of one-off assistants.

## Why private skills matter beyond expertise

There is another reason these skills matter to me:

if everyone has access to the same base models, the same general agents, and the same public workflows, then everyone starts from the same intelligence substrate.

That means differentiation matters even more.

Public skills are useful.

But if everyone eventually uses the same public skills, then everyone risks producing:

- similar structures
- similar defaults
- similar sites
- similar content
- similar strategic blind spots

I do not want to rely only on generic prompting or on a fully commoditized skill layer.

I want a private layer of method, context structure, and operating logic that reflects how I actually build businesses.

That private layer exists for two reasons at once:

- to increase task-specific expertise
- to increase differentiation

## Differentiation and search quality

One of my working theses is that mass-produced patterns eventually become easier for search systems to classify as low-value, low-oversight, or overly templated.

Google does not publicly say that a site is penalized simply because it uses a given CMS, a coding assistant, or a specific toolchain.

But Google does publicly say that:

- Search uses many signals and systems, including some site-wide signals and classifiers
- search quality raters help evaluate system performance, but do not directly rank pages
- scaled content abuse is a problem regardless of whether content is produced by humans, automation, or both, when the primary purpose is manipulating rankings rather than helping users

So the practical conclusion for me is not "tool X is banned".

The practical conclusion is:

- avoid commodity output
- avoid lazy patterns
- avoid low-oversight mass production
- build a private layer of differentiation and quality control

That is one of the reasons personal skills matter.

They are not only a way to specialize the agent.

They are also a way to avoid collapsing into the same defaults as everyone else.

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
| [`my-personal-accessibility-auditor`](./my-personal-accessibility-auditor/SKILL.md) | Audits accessibility with real tooling and browser checks | Raises the quality bar beyond surface-level a11y commentary |
| [`my-personal-og-image-mastery`](./my-personal-og-image-mastery/SKILL.md) | Covers both the technical and CTR-side strategy of Open Graph images | Useful because good OG images are both a design problem and a growth problem |
| [`my-personal-frontend-backend-routing`](./my-personal-frontend-backend-routing/README.md) | Auto-routes frontend work to Claude Code and backend work to Codex, regardless of starting tool | Eliminates manual switching between AI tools when a task spans both frontend and backend |
| [`my-personal-gemini-design`](./my-personal-gemini-design/README.md) | Design assistant: shadcn-first, Gemini consultation for aesthetics, quality gate | Combines Claude Code's codebase mastery with Gemini's visual design sense |
| [`my-personal-second-opinion`](./my-personal-second-opinion/README.md) | Gets independent second opinions from two other AI engines before validating plans | Catches blind spots by requiring consensus from multiple models before committing to a plan |

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

## Cross-tool setup

This repo also contains the documentation for the cross-tool AI infrastructure that makes Claude Code, Codex CLI, Gemini CLI, Hermes VPS, and any future tool share the same rules, memory, and configuration.

See [`setup/README.md`](./setup/README.md) for the full guide — including how to reproduce the entire setup on a new machine from scratch and how to verify the Hermes VPS variant.

### Symlink architecture

Three AI CLI tools share the same skills, instructions, and MCPs through a single source of truth:

```
~/.agents/skills/          ← Source of truth (this git repo)
│
├── ~/.claude/skills/*     ← Relative symlinks: ../../.agents/skills/<skill>
├── ~/.codex/skills/*      ← Relative symlinks: ../../.agents/skills/<skill>
└── ~/.gemini/antigravity/global_skills → ~/.agents/skills  (absolute symlink)
```

**Important: Gemini CLI does NOT use `~/.gemini/skills/` for shared skills.**

Gemini CLI discovers skills from `~/.agents/skills/` natively via the `global_skills` symlink in its antigravity data directory. Creating additional symlinks in `~/.gemini/skills/` causes "Skill conflict detected" warnings on every skill (each skill found twice). If `~/.gemini/skills/` is used at all, it should only be for Gemini-specific skills that do not exist in `~/.agents/skills/`.

### Instructions sharing

```
~/.claude/CLAUDE.md        ← Source of truth (real file)
├── AGENTS.md → CLAUDE.md  ← Per-repo symlinks (Codex reads AGENTS.md)
└── ~/.gemini/GEMINI.md → ../.claude/CLAUDE.md  ← Gemini reads this
```

All three tools read the same instructions. One file to maintain.

### MCP sharing

MCPs are configured separately in each tool's config file but share the same wrapper scripts in `~/.codex/mcp/`. The wrappers read API keys from 1Password (vault `Employee`) via `op read` at runtime. Prerequisite: `op` CLI installed and signed in (Touch ID or `op signin`).

| Tool | Config file | Wrapper type |
|------|-------------|-------------|
| Claude Code | `~/.claude.json` → `mcpServers` | 1Password wrappers (`op read`) |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers]` | 1Password wrappers (`op read`) |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` | 1Password wrappers (`op read`) |

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
