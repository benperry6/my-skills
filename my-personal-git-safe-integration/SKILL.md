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

## Preview deploys blocked by third-party hostname allowlists

Recurring pattern across projects that use a hosting platform with per-deploy ephemeral URLs (Vercel `*.vercel.app`, Netlify `*.netlify.app`, Cloudflare Pages `*.pages.dev`, etc.) **and** a third-party service with a hostname allowlist (Turnstile / reCAPTCHA / hCaptcha site keys, Stripe webhook allowlists, OAuth redirect URIs, strict CORS, CSP `connect-src`, SSO callbacks, …).

**Problem.** Protected flows (login, signup, checkout, OAuth, any challenge-gated action) cannot be exercised on preview URLs because the ephemeral hostname is not on the allowlist. Tests break silently or only on previews.

**Wrong fix — never do this.** Adding the platform apex (`vercel.app`, `netlify.app`, `pages.dev`) to the allowlist. Every tenant on that platform can then host a site under that apex, embed the widget / site key, and harvest valid tokens to replay against **your** backend. This defeats the point of the allowlist entirely.

**Right fix — stable branded preview URL under a domain you own.**
1. Pick a subdomain on a domain already covered by the allowlist (or add the apex). Example: `preview.<prod-domain>`. Most allowlists (Turnstile, CSP host-source, OAuth) cover subdomains automatically when the apex is present.
2. Add the **non-wildcard** domain to the hosting platform project: `preview.<prod-domain>`. Keep it non-wildcard on purpose (see constraint below).
3. DNS: CNAME `preview` → platform canonical target (Vercel: `cname.vercel-dns.com`). Proxy / CDN **off** during cert validation, otherwise ACME HTTP-01 fails.
4. Cert: HTTP-01 auto-provisions for specific hostnames. Don't use a wildcard (`*.preview.<prod-domain>`) — wildcards require DNS-01, which requires DNS control by the platform. Subdomain NS delegation is typically refused by platform APIs (Vercel accepts only apex as a managed DNS zone), and delegating the apex is too invasive for this use case.
5. CI: after each preview deploy, alias it to the stable URL. For Vercel:
   ```yaml
   on: { deployment_status: {} }
   jobs:
     alias:
       if: github.event.deployment_status.state == 'success' && github.event.deployment.environment != 'Production'
       steps:
         - run: npx vercel@latest alias set "$DEPLOY_HOST" preview.<prod-domain> --token "$VERCEL_TOKEN" --scope <team-slug>
   ```
6. Token: create a **long-lived, team-scoped** platform token via the provider dashboard (not via the local CLI, which issues short-TTL interactive tokens). Store as a repo secret. Minimum scope, no account-wide access.

**Trade-off to accept.** Single stable URL = "latest preview wins". For two PRs in flight simultaneously, manually realias the non-current one with `<platform> alias set`. Automating per-branch aliasing would require wildcard certs → requires DNS control delegation → usually not worth the infra cost for a 1 % usage case.

**Don't try** (tried and documented so future sessions skip the dead ends):
- Adding the platform apex to the allowlist — permissive, insecure.
- Wildcard custom domain (`*.preview.<prod-domain>`) on platforms without DNS control over the subdomain — DNS-01 challenge will fail (Vercel: `dns_pretest_cns_not_using_vercel_ns_error`).
- Subdomain-level NS delegation to the hosting platform on Hobby / free plans — the platform's DNS zone API usually refuses subdomains (Vercel: `invalid_name`).
- Using the local CLI auth token as the CI secret — typically expires within hours to days; the workflow will start failing silently at renewal time.

**State reporting impact.** When this setup exists in a project, the `État:` preview line should name the stable URL (e.g., `https://preview.<prod-domain>`), not the raw ephemeral URL. The ephemeral URL stays active in parallel and cannot be disabled on free / Hobby tiers; it's simply ignored for manual testing.
