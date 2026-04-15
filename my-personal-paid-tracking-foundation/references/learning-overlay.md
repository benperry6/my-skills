# Paid Tracking Learning Overlay

Use this file when `my-personal-paid-tracking-foundation` invokes `my-personal-verified-learning-loop`.

The shared skill owns the base doctrine.
This file defines the paid-tracking-specific overlay.

Machine-readable extension validation for this overlay lives in:

- `references/runtime-extensions.schema.json`

## Skill-specific triggers

In addition to the shared triggers, fire the learning loop when:

- a newly relevant vendor is not documented yet
- a documented vendor bootstrap flow no longer works
- a programmatic path became real where the skill still implied browser fallback
- the live permissions/scopes exposed by the vendor differ materially from the skill's current assumptions
- a Google account identity or approved-account rule had to change the real execution path
- a phase gate changed what counts as sufficient proof for this vendor flow

## Runtime hook usage

Active hooks for this skill:

- `on_failure`
  - when a documented vendor bootstrap or verification path fails
- `on_repair_success`
  - when a repaired or newly discovered vendor path succeeds
- `on_user_correction`
  - when the user clarifies the approved account, vendor choice, or business ownership boundary
- `on_run_end`
  - when the final path differs materially from the doctrine or unresolved vendor gaps would otherwise be lost

## Runtime incident extensions

When recording a runtime incident for this skill, prefer these `extensions` fields:

- `vendor`
- `phase`
- `operation`
- `auth_surface`
- `verification_surface`
- `approved_account`
- `browser_fallback_used`

## Promotion overrides

Use the shared promotion ladder, plus these paid-tracking-specific rules:

- a bootstrap learning may become `verified` after the strongest relevant phase-2 or phase-3 proof if bootstrap itself is the learned surface
- a data-flow or ingestion learning should not become `verified` until the strongest relevant phase-4 proof exists, unless the skill explicitly labels the proof as intentionally deferred
- account-specific or identity-specific quirks should stay runtime-only unless they reflect a reusable doctrine change
