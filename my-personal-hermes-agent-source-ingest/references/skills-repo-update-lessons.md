# Skills Repo Update Lessons

Use these notes when maintaining Ben's `/home/hermes/.agents/skills` repo during Hermes/agent setup work.

## Plain-language reporting

When Ben asks what happened after a repo/setup issue, explain in normal language first:

- what was blocked
- why that mattered
- what you changed
- whether it is fixed now

Avoid leading with Git internals, symlink terminology, branch names, or commit hashes. Add those only after the simple explanation if they help verification.

## Branch freshness check

Do not conclude a skill is absent only because the active branch does not contain it.

Check:

- active branch
- `origin/main`
- other `origin/*` branches when relevant

A useful pattern is: search paths and content across origin branches for the skill name or core phrase before saying it does not exist.

## Selective recovery from `origin/main`

If the active branch is intentionally not `main`, and `origin/main` contains the desired skill but merging all of `main` would create broad unrelated conflicts, prefer the smaller safe move:

1. Abort any conflicted merge.
2. Check out only the needed skill directories from `origin/main`.
3. Validate the skill frontmatter and references.
4. Commit and push immediately, following the skills repo rule.

This preserves the active branch while recovering the missing class-level skill.
