# Cloudflare

Use this file when Cloudflare is already present or under consideration.

The goal here is not "use Cloudflare by default".
The goal is to use the currently verified programmatic path when Cloudflare is relevant, and to avoid unnecessary browser work.

## Verified Local Path On This Machine

Current verified path:

- Wrapper: `~/.codex/mcp/cloudflare-wrapper.sh`
- Auth source: 1Password item `Cloudflare` in vault `Employee` (field `api_token`), accessed via `op read "op://Employee/Cloudflare/api_token"`
- Access model: direct Cloudflare API via `curl`

Do not default to `wrangler` here.
`wrangler` may still be useful in a future context, but it is not the currently verified baseline on this machine.

## Read-Only Verification First

Before any write action, verify the programmatic path with read-only calls:

```bash
~/.codex/mcp/cloudflare-wrapper.sh GET /user/tokens/verify
~/.codex/mcp/cloudflare-wrapper.sh GET "/zones?per_page=20"
~/.codex/mcp/cloudflare-wrapper.sh GET "/zones?name=example.com"
```

Use `scripts/verify_cloudflare_api.sh` when you want the local wrapper path checked quickly before reasoning about Cloudflare changes.

## Wrapper Contract

Usage:

```bash
~/.codex/mcp/cloudflare-wrapper.sh <METHOD> <ENDPOINT> [JSON_BODY]
```

Examples:

```bash
~/.codex/mcp/cloudflare-wrapper.sh GET /user/tokens/verify
~/.codex/mcp/cloudflare-wrapper.sh GET "/zones?name=example.com"
~/.codex/mcp/cloudflare-wrapper.sh POST /zones/ZONE_ID/dns_records '{"type":"TXT","name":"_verify","content":"value"}'
```

The POST example is a shape example, not a blanket permission to write.
Read the current official docs for the exact product and endpoint before any write action.

## Cloudflare Product Families Worth Considering

Research the live docs and plan limits before assuming these are available or justified:

- DNS
- Proxy and edge filtering
- WAF managed rules
- WAF custom rules
- Rate limiting
- Bot challenge features
- Cache rules and bypass
- Transform rules
- SSL or TLS settings
- Access or Zero Trust controls
- API protection features

Not every plan exposes every feature in the same way.
Do not hardcode plan assumptions without verifying the current live docs and the actual zone state.

## Cloudflare Workflow

1. Verify the token and wrapper path.
2. Resolve the target zone.
3. Read the current official docs and API surface for the exact feature in scope.
4. Snapshot current state read-only before any write.
5. Apply changes only with explicit user approval.
6. Re-verify behavior with read-only checks and real traffic where appropriate.
7. Record the result in `runtime-learning.md` first, then promote to `verified-learning.md` after durable proof.

## Browser Fallback Rule

Use the browser only when:

- the API path is genuinely missing for the needed feature
- the account bootstrap has a real UI-only gap
- or the live API/docs check proves that programmatic control is insufficient

Do not open Cloudflare in the browser just because it is familiar.
