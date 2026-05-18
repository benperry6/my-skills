# Codex JSONL source-location and identity validation

Use this reference when Ben asks to ingest a Codex/Claude/agent session export from Drive or another file store.

## Durable lesson

Do not ingest a plausible-looking session archive just because it is topically related. For agent-session JSONL, source identity matters: filename, internal timestamps, first/last messages, and any embedded local session path can prove that a candidate is a different session.

## Minimum identity checks

Before moving a session from `sources/inbox/` to processed/validated status:

1. Confirm the requested filename or user-approved replacement.
2. Confirm the file is visible in the intended storage location or document why it is not.
3. Inspect the JSONL structure enough to identify:
   - first meaningful user message;
   - last assistant message;
   - internal session path or rollout filename if present;
   - rough topical match to the user's described source.
4. If any identity signal points to a different date/session, treat it as `needs-confirmation`, not as validated.

## Drive search pattern for missing session exports

When a requested Drive file is not found by exact name, try a bounded escalation before blocking:

- exact filename query;
- filename fragments: date prefix, UUID fragments, `rollout`, `.jsonl`;
- root listing if Ben said “at Drive root”;
- `sharedWithMe` and shared/all drives where available;
- full-text fragments for the exact rollout string and UUID;
- local search under `/home/hermes` and the relevant vault workspace.

Do not expose OAuth tokens or credential file contents. If checking scopes/auth state, summarize only the presence/absence of access and redact any secret values as `[REDACTED]`.

## Handling plausible but unconfirmed candidates

If a candidate is topically close but not identity-confirmed:

1. Store it under the workspace inbox with a `needs-confirmation-` prefix.
2. If you already extracted it, keep the extraction next to it with the same prefix.
3. Create a short source-location attempt note under `sources/inbox/` with:
   - requested filename;
   - search methods used;
   - exact non-match result summary;
   - candidate found and why it is not validated;
   - required next user action.
4. Mark parse/ingest/verification tasks as blocked or cancelled, not completed.
5. Ask Ben to either approve the candidate or provide/share the exact source.

## Decision rule

A related Codex session can be useful later, but it must not be silently substituted for the requested source. Substitution requires explicit user approval or a clear user-provided equivalence statement.