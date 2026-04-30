# Verified Learning

Only durable learnings proven in real behavior belong here.

Do not add:

- theory
- guesses
- doc-only claims
- unverifiable assumptions

Promote entries here only after the behavior is verified locally or in the real target environment.

## 2026-03-30T00:00:00Z — Cloudflare wrapper read path verified

- Provider: `Cloudflare`
- Local path: `~/.codex/mcp/cloudflare-wrapper.sh`
- Auth source: 1Password item `Cloudflare` in vault `Employee` (field `api_token`), accessed via `op read "op://Employee/Cloudflare/api_token"`
- Verified behavior:
  - `GET /user/tokens/verify` returned an active token
  - `GET "/zones?per_page=3"` returned a successful zone listing
- Operational meaning:
  - Cloudflare should be treated as programmatically accessible on this machine for read-first administration
  - Browser fallback is not the default for Cloudflare here
