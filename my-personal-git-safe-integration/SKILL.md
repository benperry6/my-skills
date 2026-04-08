---
name: my-personal-git-safe-integration
description: "[My Personal Skill] Use when a repository deploys from a production branch such as main, and code changes must be integrated safely. Enforces branch-per-task, PR, minimum verification, explicit preview-vs-production status, squash merge, branch cleanup, and post-merge sync."
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
- If branch pushes create preview deployments, always verify the preview state and say explicitly whether the change is in preview only or already in production.
- Never say "deployed" without saying `preview` or `production`.

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
9. If the repo creates branch previews, verify the preview deployment or pipeline state.
10. Before ending the task, say explicitly:
   - `État: preview seulement (pas en production)` when the branch preview is ready but `main` has not been updated.
   - `État: en production` only after the production branch has been updated and the production deployment is verified.
11. If the preview is ready and production is not updated, ask explicitly whether to pass the change to production.
12. Merge with `squash merge` only.
13. Delete the branch after merge.
14. Checkout the production branch and sync it with remote.
15. If the repo auto-deploys, verify the resulting production deployment or pipeline state.

## Output expected from the agent
Before merge, summarize:
- what changed
- what was verified
- preview status
- final state line: `État: preview seulement (pas en production)`
- whether production still needs an explicit go-ahead

After merge, summarize:
- merged branch name
- final squash commit title
- verification result
- production deployment status if relevant
- final state line: `État: en production`

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
