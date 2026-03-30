# Provider Matrix

This file is the compact matrix of control families the skill already knows about.

Treat vendors already named here as examples, not a whitelist.
If a relevant provider or feature is missing, research the current official docs and API surface live, then record only verified behavior.

## Control Families

| Control family | Typical trigger | Candidate implementation layers | Notes |
| --- | --- | --- | --- |
| DNS and nameserver control | Domain onboarding, verification records, DNS centralization | Registrar API, provider DNS, edge DNS provider | Useful before any proxy or WAF decision |
| Proxy and edge filtering | Many public endpoints, anonymous traffic, serverless origin protection | Cloudflare proxy, hosting-native edge controls, CDN firewall layer | Use when requests should be filtered before origin |
| WAF managed rules | Commodity attack noise, scanners, generic probes | Cloudflare managed rules, provider-native firewall, app validation as fallback | Good first layer, not a substitute for app logic |
| WAF custom rules | Repeated probes, path traversal patterns, abusive request signatures | Provider firewall rules, reverse proxy rules | Scope narrowly to reduce false positives |
| Rate limiting | Auth, public APIs, costly anonymous endpoints, log endpoints | Edge rate limiting, gateway limits, app limits | Distributed runtimes often need edge enforcement |
| Bot challenge or CAPTCHA | Auth, enumeration risk, spammy forms, costly AI | Turnstile, CAPTCHA, provider bot challenge, app challenge fallback | Distinguish invisible default from visible fallback |
| Bot signal and browser heuristics | Scraping, commodity bots, suspicious headless traffic | Provider bot modes, JS detection, browser integrity checks, app anomaly detection | Useful before adding visible friction everywhere |
| DDoS protection | Volumetric bursts, network-level abuse | Edge or CDN DDoS layer, hosting-native mitigation | Usually provider-layer, not app-layer |
| Traffic segmentation and request filtering | Geo abuse, ASN abuse, country restrictions, suspicious paths | Provider firewall expressions, gateway policy, reverse-proxy allow or deny rules | Often useful for narrowing a rule before going broad |
| Cache rules and bypass | Dynamic APIs, dashboards, previews, auth pages | Provider cache rules, origin cache headers | Prevent stale or private data leakage |
| Transform or header rules | CSP, HSTS, cache behavior, request shaping | Provider transform rules, hosting config, app headers | Choose the narrowest effective layer |
| TLS, certificates, and transport enforcement | Admin surfaces, API trust boundaries, mixed legacy infra | Provider SSL or TLS settings, custom certificates, mTLS, origin transport policy | Relevant when the abuse or trust problem is transport-level |
| Zero Trust or Access | Admin, staging, preview, internal tools | Provider access controls, VPN, SSO gateway | Best for surfaces that should not be public at all |
| API protection | B2B APIs, machine traffic, schema-sensitive endpoints | API gateway, signed requests, mTLS, schema validation | Use when identity and payload guarantees matter |
| Surge control and waiting room | Launches, ticketing, high-demand drops, flash abuse | Provider waiting room, queueing layer, app-side queue fallback | More relevant for traffic spikes than for everyday bot noise |
| App-layer validation | Client-controlled state, payload abuse, replay | Server-truth checks, token design, sanitization, payload caps | Mandatory when provider layers cannot see product logic |
| Observability and rollback | False positives, change safety | Provider rule IDs, logs, metrics, internal alerts | Hardening without rollback is brittle |

## Known Provider Families

### Edge or provider layer

- Cloudflare
- Hosting-native edge controls such as Vercel or similar platform features
- Registrar or DNS-provider APIs
- CDN, WAF, and edge-security providers other than Cloudflare
- Reverse proxies and API gateways
- Access-control or identity-broker layers
- Provider-native queueing or waiting-room products where relevant

### App or code layer

- Server-side validation
- Existing auth gates
- Payload caps and sanitization
- Signed links or tokens
- Rate limiting implemented in durable shared storage
- Durable shared counters, queues, or worker-backed enforcement
- App-side anomaly checks when provider heuristics are not enough

## Selection Notes

- Choose the control family first, then choose the provider or implementation layer.
- Do not assume Cloudflare is mandatory.
- Prefer the provider already in the request path when it can solve the problem credibly.
- Do not assume code-only protection is enough on distributed serverless traffic.
- Do not assume provider-managed protection is enough when the abuse depends on product-specific state.
- Do not assume a feature exists on every plan or every provider tier.
- Do not freeze vendor capability claims when the live docs or API surface can be checked at runtime.
- Prefer read-only verification of provider access before any write action.
- Record newly verified provider behavior in the learning files instead of bloating the core skill.
- If the provider matrix does not clearly answer a case, read `programmatic-bootstrap.md` and research the live provider docs before deciding.
