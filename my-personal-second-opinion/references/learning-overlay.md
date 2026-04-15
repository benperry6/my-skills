# Second Opinion Learning Overlay

Use this file when `my-personal-second-opinion` is evaluated against `my-personal-verified-learning-loop`.

The shared skill owns the base doctrine.
This file defines the second-opinion-specific overlay.

## Current status

`my-personal-second-opinion` is currently a temporary special implementation on the path to convergence.

That means:

- the runner remains the source of truth for orchestration, repair, and persistence behavior
- the shared loop remains the source of truth for doctrine, trigger vocabulary, confidence tiers, and promotion guardrails
- convergence should happen through an adapter layer first, not through immediate replacement of the runner with the shared helper

## Skill-specific triggers

In addition to the shared triggers, fire the learning loop when:

- a documented external-engine invocation path breaks
- a repaired external-engine path requires a new engine-specific fallback
- engine detection or "never consult yourself" safeguards materially change
- a post-implementation audit flow requires new manifest, transcript, or git-evidence handling
- a real behavior change alters the canonical fallback order for Codex, Claude, or Gemini

## Runtime hook usage

Active hooks for this skill:

- `on_failure`
  - when a documented engine path fails in `execute_attempt()` or `run_engine()`
- `on_repair_success`
  - when a later attempt succeeds after an earlier failure for the same target engine
- `on_user_correction`
  - when the user changes the required routing, current-engine assumption, or review scope in a reusable way
- `on_run_end`
  - when the final successful path differs materially from doctrine or unresolved invocation incidents would otherwise be lost

## Runtime incident extensions

When recording a runtime incident for this skill, prefer these `extensions` fields:

- `target_engine`
- `failure_classification`
- `failure_signature`
- `repair_strategy`
- `verified_models`
- `response_preview`
- `mode`
- `needs_web_research`

## Native-to-shared field mapping

Use this mapping when translating runner-native incidents into the shared runtime incident shape:

| Native runner field | Shared field | Notes |
| --- | --- | --- |
| `recorded_at` | `timestamp` | direct rename |
| `current_engine` | `agent` | direct rename |
| `working_directory` | `notes` or `extensions.working_directory` | keep visible for auditability |
| `failed_command` | `failed_path` | direct rename |
| `repaired_command` | `repaired_path` | direct rename |
| `target_engine` | `extensions.target_engine` | shared schema has no top-level equivalent |
| `failure_classification` | `extensions.failure_classification` | preserve native taxonomy |
| `failure_signature` | `extensions.failure_signature` | do not collapse into `failed_path` |
| `repair_strategy` | `extensions.repair_strategy` | preserve native fallback detail |
| `verified_models` | `extensions.verified_models` | preserve structured provider metadata |
| `response_preview` | `extensions.response_preview` | keep short native outcome trace |

## Native source-of-truth rules

During the adapter phase:

- native runner persistence remains authoritative
- native runner de-duplication remains authoritative
- any shared-compatible mirror must be derived from an already accepted native record, not from a parallel best-effort write path
- the bridge artifacts are `references/runtime-learning.shared.json` and `references/runtime-learning.shared.md`

This avoids downgrading the runner to the current capabilities of the shared helper.

## Promotion overrides

Use the shared promotion ladder, plus these second-opinion-specific rules:

- engine-failure incidents stay runtime-only unless the repaired path becomes reusable doctrine for future runs
- one-off prompt content or review outcomes never justify doctrine changes by themselves
- capacity-only incidents do not become verified learning unless repeated real behavior proves a different canonical fallback order
- current-engine detection, git-topology handling, or structured-output guidance may become verified learning when they materially change the canonical execution path

## Convergence boundary

Do not replace `second_opinion_runner.py` with the shared helper until the shared layer can support, at minimum:

- producer-grade structured incident capture
- machine-validated extensions
- batch append without subprocess-per-record
- native git-persist semantics
