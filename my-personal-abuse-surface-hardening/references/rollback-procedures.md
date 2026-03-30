# Rollback Procedures

Security hardening can break legitimate traffic.

Do not ship protection without a rollback path.

## Before Any Write Change

Capture the current state first:

- target account, business, project, or zone
- rule names or IDs
- current threshold values
- current route scopes
- current challenge behavior
- screenshots or read-only JSON snapshots when useful

## Typical Rollback Triggers

Rollback quickly when you see:

- legitimate users blocked
- conversion-critical flow degradation
- admin or preview access accidentally locked out
- sudden spike in `403`, challenge loops, or provider-side blocks
- cache behavior breaking dynamic or authenticated routes

## Rollback Order

Use the narrowest rollback first:

1. disable or narrow the newest edge rule
2. relax the newest rate limit or challenge threshold
3. bypass a single affected path temporarily
4. disable the provider-side change entirely if the narrow rollback fails
5. roll back app-side challenge logic only if provider rollback is insufficient

Do not undo unrelated protections just to clear one false positive.

## After Rollback

Re-verify:

- the legitimate flow works again
- the provider state matches the intended rollback
- the problem is recorded in `runtime-learning.md`

If the failure mode is understood and later fixed correctly, promote the repaired path to `verified-learning.md`.
