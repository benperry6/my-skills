# Run Registry Contract

Use one durable JSON registry per delegated run.

The exact filename is flexible.
The contract is not.

## Required top-level fields

- `run_id`
- `objective`
- `workspace`
- `created_at`
- `updated_at`
- `units`

## Required per-attempt fields

Every worker attempt entry should include at least:

- `unit_id`
- `phase`
- `attempt`
- `agent_id`
- `status`
- `started_at`
- `last_observed_at`

Recommended additional fields:

- `provider`
- `nickname`
- `last_progress_at`
- `transcript_path`
- `artifact_paths`
- `replacement_of`
- `notes`

## Status vocabulary

Use explicit statuses such as:

- `pending`
- `running`
- `waiting`
- `recovered`
- `replaced`
- `completed`
- `accepted`
- `rejected`
- `failed`
- `blocked`

Pick one vocabulary and keep it consistent within the run.

## Example structure

```json
{
  "run_id": "catalog-2026-04-13",
  "objective": "Translate and review 18 locale catalogs",
  "workspace": "/path/to/project",
  "created_at": "2026-04-13T07:10:00Z",
  "updated_at": "2026-04-13T14:31:00Z",
  "units": [
    {
      "unit_id": "locale:th",
      "current_phase": "evaluator",
      "terminal": false,
      "attempts": [
        {
          "phase": "translator",
          "attempt": 1,
          "agent_id": "agent_123",
          "provider": "codex",
          "status": "completed",
          "started_at": "2026-04-13T07:11:00Z",
          "last_observed_at": "2026-04-13T07:18:00Z",
          "last_progress_at": "2026-04-13T07:17:32Z",
          "transcript_path": "/path/to/subagents/locale-th.jsonl",
          "artifact_paths": [
            "/path/to/messages/th.json"
          ],
          "notes": "Initial translation landed on disk"
        },
        {
          "phase": "evaluator",
          "attempt": 1,
          "agent_id": "agent_456",
          "provider": "codex",
          "status": "running",
          "started_at": "2026-04-13T07:19:00Z",
          "last_observed_at": "2026-04-13T07:24:00Z",
          "last_progress_at": "2026-04-13T07:23:41Z",
          "transcript_path": "/path/to/subagents/locale-th-eval.jsonl",
          "artifact_paths": [],
          "notes": "Quota reset confirmed; evaluation re-run in progress"
        }
      ]
    }
  ]
}
```

## Update rules

Update the registry after each of these events:

- spawn
- observation
- recovery attempt
- respawn
- local verifier result
- evaluator verdict
- final acceptance or rejection

## Resume rules

On resume:

1. load the registry first
2. find all non-terminal units
3. inspect their latest attempt timestamps and artifacts
4. recover or replace from that evidence

Do not rebuild state from memory if the registry exists.

## Handoff rule

If the orchestrator cannot finish in the current session, the final message for that session should include:

- the registry path
- which units remain non-terminal
- the latest known blocker or next step

That turns session closure into a clean pause instead of an opaque interruption.
