# Reset Policy

## Three reset modes

### 1. Curate

Use when some existing scratch is probably worth preserving.

Behavior:

- inspect what exists
- keep only the pieces that are clearly reusable
- still bootstrap durable docs before continuing implementation

### 2. Snapshot then reset

Use when the current work is probably bad, but recoverability still matters.

Behavior:

- create a recoverable snapshot first
- delete the scratch implementation
- recreate only the docs-first bootstrap

### 3. Hard delete

Use only when the user explicitly says the scratch work is disposable.

Behavior:

- delete the premature implementation
- do not spend time defending or curating it
- rebuild from docs-first

## Rule

Never choose hard delete on your own.

Hard delete requires explicit user approval.

Once explicit hard delete is approved, do not keep ghost copies in the working tree and do not continue the old tickets by inertia.
