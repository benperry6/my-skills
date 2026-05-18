# Personal Source-Ingest Naming and Workspace Convention

Use this reference when creating, recovering, or renaming source-ingest skills for Ben's personal skill repo.

## Verified convention

Personal skills in `benperry6/my-skills` should use the `my-personal-*` prefix in both:

- the directory name
- the `name:` field in `SKILL.md` frontmatter

For the source-ingest family, the current names are:

- `my-personal-knowledge-source-ingest` — generic parent workflow
- `my-personal-seo-geo-source-ingest` — SEO/GEO specialization
- `my-personal-hermes-agent-source-ingest` — Hermes VPS / AI agents specialization

Descriptions for these personal skills should begin with `[My Personal Skill]`.

## Recovery/verification pattern

When a source-ingest skill appears missing on the active branch:

1. Fetch and inspect `origin/main` before concluding it does not exist.
2. Prefer selective checkout/recovery of the relevant skill directories when a full merge would introduce unrelated conflicts.
3. Validate all recovered/renamed skills by checking frontmatter name matches directory name and description begins with `[My Personal Skill]`.
4. Commit and push only the relevant skill rename/recovery changes.

## Workspace convention

The Hermes/agents source-ingest skill uses a vault workspace, not a new GitHub repo by default:

`/home/hermes/vault/ops/hermes-agent-source-ingest`

Recommended workspace files/directories:

- `README.md`
- `PROJECT_BRIEF.md`
- `ARCHITECTURE.md`
- `PROJECT_STATE.md`
- `BACKLOG.md`
- `sources/inbox/`
- `sources/processed/`
- `learnings/atomic/`
- `learnings/hypotheses/`
- `learnings/syntheses/`
- `decisions/`
- `drafts/skill-specs/`

Keep GitHub as source of truth for code and skills. Use vault for durable knowledge, decisions, hypotheses, and source-ingest backlog unless the workflow becomes executable tooling.
