---
name: my-personal-git-safe-integration
description: "[My Personal Skill] Use when a repository deploys from a production branch such as main, and code changes must be integrated safely. Enforces branch-per-task, PR, minimum verification, squash merge, branch cleanup, and post-merge sync."
---

# Git Safe Integration

Use this skill when a repo has a production branch, especially if pushing to it can trigger deployment.

## Mandatory rules
- Never commit or push directly to the production branch. Default to `main` unless repo rules say otherwise.
- Always create a short-lived branch for one logical task.
- Always run the repo's minimum verification before proposing merge.
- Always open a PR before integrating into the production branch.
- Always use `squash merge`.
- Always delete the branch after merge.
- Always sync local production branch after merge.

## Workflow
1. Identify the production branch from repo rules. Default to `main`.
2. Check Git state before starting:
   - current branch
   - tracked changes
   - untracked temp files
   - worktrees or stale branches that may interfere
3. If the worktree is dirty:
   - separate real work from temp noise
   - do not discard user work without explicit approval
   - clean or isolate temp noise before preparing integration
4. Create a short branch for the task.
   Example: `fix/cookie-banner-copy`
5. Do the work on that branch only.
6. Make intermediate commits on that branch as needed.
7. Before integration, run the repo's required verification.
   Minimum: the build command from repo rules.
   If relevant tests exist, run them too.
8. Open a PR into the production branch.
9. Merge with `squash merge` only.
10. Delete the branch after merge.
11. Checkout the production branch and sync it with remote.
12. If the repo auto-deploys, verify the resulting deployment or pipeline state.

## Output expected from the agent
Before merge, summarize:
- what changed
- what was verified
- what will go to production

After merge, summarize:
- merged branch name
- final squash commit title
- verification result
- deployment status if relevant

## Do not do
- Do not push directly to `main`.
- Do not ask the user to choose between merge, rebase, and squash.
- Do not treat a dirty worktree as safe.
- Do not mix unrelated changes in one PR.
- Do not rewrite shared history unless the user explicitly asks for it.

## Squash commit title
Use one clean final title:
- `fix: ...`
- `feat: ...`
- `refactor: ...`
- `docs: ...`
