# Verification Benchmarks

Use this file after hardening changes have been proposed or implemented.

The goal is to prove behavior, not to "inspect the code and assume it works".

## Safety Rules

- Prefer staging or development for burst tests
- Do not run noisy or high-volume tests against production without explicit approval
- Start with low concurrency and narrow scopes
- Capture observable evidence: status codes, headers, logs, screenshots, or provider events

## Benchmark Families

### 1. Challenge gating

Use when checking auth, form, or chatbot protection.

What to verify:

- a legitimate flow still works
- the anonymous or risky flow is challenged when expected
- invisible-by-default behavior stays low-friction
- challenge failure produces the intended fallback behavior

### 2. Rate limiting

Use when protecting public APIs, auth, or noisy endpoints.

Example burst test:

```bash
seq 1 20 | xargs -I{} -P 5 curl -s -o /dev/null -w "%{http_code}\n" https://example.com/api/endpoint
```

What to verify:

- early requests succeed normally
- later requests are limited as intended
- the limit resets as expected
- false positives are acceptable or can be rolled back fast

### 3. Cache bypass on dynamic routes

Use when proxy or cache rules are involved.

What to verify:

- dynamic API routes are not cached unintentionally
- dashboard or preview routes do not leak stale or private data
- public static assets still cache normally

### 4. Admin or internal surface access

Use when Access, Zero Trust, or edge guards are involved.

What to verify:

- unauthorized access is blocked before origin when intended
- authorized access still works
- emergency rollback is documented

### 5. Server-truth validation

Use when the protection depends on prior steps or client state.

What to verify:

- forged client state does not bypass the control
- replayed tokens fail when they should
- the server derives truth from trusted state, not user-controlled hints

## Evidence Standard

A change counts as verified only if at least one of these is captured:

- concrete HTTP responses
- provider-side logs or events
- app-side logs tied to the protection
- browser-visible behavior in the real product

Code inspection alone is not enough.
