# AGENTS.md - my-skills

This repository stores reusable skills for AI agents.

## Personal Skill Conventions

Skills that are personal to this stack should follow these conventions:

- folder name starts with `my-personal-`
- `SKILL.md` frontmatter `name` matches the folder name
- `SKILL.md` frontmatter `description` starts with `[My Personal Skill]`

## Public Skills: No Durable Local Patches

Do not rely on local edits to public or upstream-managed skills as a durable fix.

Reason:

- installs or updates such as `npx skills add <repo>` may replace or refresh those skill files
- a local patch on a public skill can disappear on the next reinstall or upstream sync

Default rule:

- if the behavior change is personal to this stack, patch a `my-personal-*` skill instead
- if the behavior change should live in the public skill, contribute it upstream
- treat local edits to public skills as temporary debugging only, and remove them once the durable fix exists elsewhere

## README Rule For Strategic Personal Skills

Not every skill needs a human-facing presentation page.

But when a personal skill carries a real thesis, a reusable method, a strong point of view, or an important piece of the broader stack, it should also include a `README.md`.

Use that `README.md` to explain:

- why the skill exists
- what problem it solves
- the logic behind its creation
- where it sits in the broader workflow or stack
- what makes it strategically important

Keep the roles separate:

- `SKILL.md` = agent-facing execution contract
- `README.md` = human-facing presentation and rationale

Examples of skills that should usually have a `README.md`:

- foundational skills
- skills that encode a reusable framework
- skills that sit upstream of many others
- skills that carry a strong methodology or philosophy

Examples of skills that may not need a `README.md`:

- small utility skills
- narrow helper skills
- straightforward execution skills with no broader thesis

## Default Bias

If a new `my-personal-*` skill feels strategically important, default toward adding a `README.md`.

It is better for the repo to explain the important skills clearly than to leave them as opaque technical artifacts.
