# Runtime Incident Schema

Use `runtime-learning.json` as the structured source of truth for runtime incidents.

Use `runtime-learning.md` as the human-readable mirror.

## Why both formats exist

JSON is for:

- deterministic parsing
- later comparison
- trigger triage
- promotion decisions

Markdown is for:

- quick human review
- repo diffs
- readable handoff between sessions

## File contract

- `runtime-learning.json` = array of incident objects
- `runtime-learning.md` = append-only human-readable mirror of those incidents
- `runtime-incident.schema.json` = machine-readable contract for one runtime incident object

## Required fields

Each runtime incident should include at least:

- `timestamp`
- `kind`
- `topic`
- `summary`
- `status`
- `confidence`
- `evidence`
- `canonical_change_candidate`

## Recommended fields

- `record_id`
- `failed_path`
- `repaired_path`
- `notes`
- `source_skill`
- `source_session`
- `agent`
- `target_files`
- `extensions`

## Example object

```json
{
  "record_id": "8d6dd6c39f5b2f52",
  "timestamp": "2026-04-15T10:02:00+00:00",
  "kind": "runtime",
  "topic": "gemini-cli-fallback",
  "summary": "The documented Gemini invocation failed; `-m auto` succeeded and produced valid JSON output.",
  "status": "repaired",
  "confidence": "medium",
  "failed_path": "gemini -m pro -p '...' --output-format json",
  "repaired_path": "gemini -m auto -p '...' --output-format json",
  "evidence": [
    "exit code 0 on repaired path",
    "expected JSON payload written to output file"
  ],
  "notes": [
    "Canonical guidance may need update if this remains true across future runs"
  ],
  "source_skill": "my-personal-second-opinion",
  "source_session": "session-abc123",
  "agent": "codex",
  "target_files": [
    "references/runtime-learning.md"
  ],
  "extensions": {
    "vendor": "Gemini CLI",
    "hook": "on_repair_success"
  },
  "canonical_change_candidate": true
}
```

## Status vocabulary

Keep the vocabulary explicit and finite:

- `observed`
- `repaired`
- `unresolved`
- `promoted`

## Confidence vocabulary

- `low`
- `medium`
- `high`

Do not overstate confidence.

## Promotion handoff

Promotion decisions should read this schema and decide whether the incident stays:

- runtime-only
- promoted into verified learning
- escalated into a canonical `SKILL.md` update

The `extensions` object is the approved place for skill-specific fields.

If the target skill defines:

- `references/runtime-extensions.schema.json`

the shared helper should validate `extensions` against that schema before writing the runtime incident.

## Runtime de-duplication

The shared helper may generate a stable `record_id` for runtime incidents.

Use it to avoid appending the same incident repeatedly across repeated runs.

Default behavior:

- the helper computes `record_id` from a stable subset of the runtime incident
- if the same `record_id` is already present in `runtime-learning.json`, the helper skips the duplicate append

If a downstream skill needs stronger control over what counts as "the same incident", it may pass a stable override through:

- `extensions.learning_fingerprint`

That value becomes the deduplication seed for the generated `record_id`.

## Producer-grade batch append behavior

The shared helper may accept a batch payload instead of one runtime incident per subprocess invocation.

Recommended payload shapes:

- a JSON array of incident objects
- or an object with a top-level `records` array

Behavior expectations:

- validate each runtime incident against the shared schema
- validate `extensions` against the target skill's extension schema when present
- de-duplicate within the existing runtime store before writing
- write the updated JSON store and Markdown mirror once per batch
- optionally persist the resulting files through git when the caller explicitly enables git persistence

## Machine-readable contract

The Markdown explanation in this file is descriptive.

The executable contract is:

- `references/runtime-incident.schema.json`

Intended use:

- downstream adapters can map their native runtime records into this shape
- future smoke tests can validate incident objects against it
- the shared loop can evolve its helper scripts without relying only on prose

Current scope:

- the JSON Schema validates a **single incident object**
- `runtime-learning.json` remains an array of such objects
- a full file-level schema or validator can be added later if needed
