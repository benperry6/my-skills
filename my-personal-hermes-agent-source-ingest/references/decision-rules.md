# Decision Rules for `my-personal-hermes-agent-source-ingest`

## User-Curation Rule

Ben-selected sources in the `Hermes & AI Agents Setup` topic are high-signal inputs. Treat them as likely useful, but not automatically correct.

High-signal changes the retention posture, not the truth standard.

## Status Rules

- `reject`: vague, unsafe, unrelated, non-actionable, already known with no enrichment, or conflicts with hard constraints.
- `duplicate`: already represented with same principle, action, and scope.
- `enrich`: improves an existing memory, vault note, skill, prompt rule, docs note, or workflow.
- `hypothesis`: plausible, testable, and relevant, but unverified for Ben's setup.
- `technique_candidate`: concrete tactic worth preserving but still thinly evidenced.
- `operator_verified`: Ben reports first-party validation for a scoped technique.
- `new_learning`: verified, reusable, durable Hermes/agent doctrine.
- `conflict`: contradicts current setup, explicit Ben preferences, or another retained rule.

## Verification Rule

Before saying a recommendation applies, check the relevant real source of truth:

- config for configuration claims
- repo/docs for feature or command claims
- vault notes for durable decisions/backlog
- skills for procedural workflows
- runtime/tool output for current system state

If verification is impossible or blocked, say so and downgrade to `hypothesis` unless the user supplied enough direct evidence.

## Safe-Apply Rule

Apply immediately only when all are true:

- small
- reversible
- local to Hermes VPS/setup
- no credentials or secrets
- no billing or new paid service
- no destructive action
- no cross-project impact
- no major architecture change

Otherwise, ask Ben before applying.

## Evidence Types

Record the evidence profile when it matters:

- official Hermes docs
- repo source code
- runtime verification
- Ben first-party report
- practitioner field report
- tool/repo example
- reasoned hypothesis
- unsupported assertion

Use evidence type to calibrate confidence and action.

## Promotion Rule

Promote to `new_learning` only when a candidate has:

- a clear action
- a clear target artifact or behavior
- direct verification or strong corroboration
- explicit boundary/failure mode
- durable relevance to Ben's Hermes/agent setup

## Rejection Baseline

Reject faster when a candidate is:

- abstract agent commentary
- motivational framing
- prompt cargo-culting without mechanism
- a vendor sales claim without usable detail
- unsafe credential practice
- MacBook-as-always-on-relay pattern
- UI claim that cannot be screen-verified
- outside this topic's Hermes/agent scope

## Reporting Rule

Every final answer after ingesting a source should include:

- core recommendation
- decision status
- verification performed
- action taken or why none
- next step, if any
