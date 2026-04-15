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
