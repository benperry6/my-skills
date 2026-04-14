# Subagent Orchestration Checklist

Use this before trusting a delegated run.

## Before Spawn

- [ ] delegation is materially justified
- [ ] each worker owns one bounded unit of work
- [ ] the acceptance rule is defined before spawning
- [ ] the worker prompt is task-only and does not contain orchestration boilerplate
- [ ] any model or reasoning override is explicitly justified or user-authorized
- [ ] a durable run registry path has been chosen

## Spawn and Tracking

- [ ] every worker attempt is recorded immediately
- [ ] the registry records `unit_id`, `phase`, `attempt`, `agent_id`, `status`, `started_at`, and `last_observed_at`
- [ ] transcript/session paths are recorded when discoverable
- [ ] local artifact paths are recorded when they materially help recovery
- [ ] replacement attempts link back to the prior attempt via `replacement_of`

## Supervision

- [ ] the orchestrator supervises on a measured cadence rather than busy-polling
- [ ] inactivity under 10 minutes is not treated as death by default
- [ ] workers are not interrupted only because they looked quiet for a few minutes
- [ ] any provider-specific override to the default inactivity threshold is explicit

## Resume and Recovery

- [ ] a resumed session reloads the registry before making life/death assumptions about detached workers
- [ ] local artifacts are inspected before any respawn decision
- [ ] recorded timestamps are checked against the inactivity threshold before replacing a detached worker
- [ ] the registry is updated after every recovery attempt and respawn
- [ ] detached UI state is not treated as proof of failure

## Completion

- [ ] each delegated unit reaches an explicit terminal state
- [ ] stale `running` or `waiting` markers are cleared when the real state changes
- [ ] the orchestrator stays active until the full delegated workflow is complete or a durable handoff is written
- [ ] user-facing completion claims are tied to the real acceptance rule, not to worker messages alone
