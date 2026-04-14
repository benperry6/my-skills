---
name: cli-api-first-doctrine
description: "Use when a task targets an external service or remote system that could be handled through CLI, API, browser UI, scraping, or local wrappers. Enforces a CLI/API-first doctrine: prefer the simplest stable programmatic route, revalidate direct routes before fallback, stop and ask if the best route is blocked only by missing user-provided access, never fallback silently, and treat persistence of proven routes as a completion gate. For service-specific workflows, see the relevant service skill."
---

# CLI/API-First Doctrine

This skill governs route selection for external systems.

It is a doctrine skill.
It does not implement service-specific business logic.
It does not replace repo-local rules.

## Use This Skill When

Use this skill when a task targets an external service or remote system and multiple route families may exist, such as:

- direct CLI
- direct API
- local wrapper script
- SDK call
- browser UI
- scraping or page parsing

Typical prompts:

- connect to X
- fetch data from X
- automate X
- sync X with Y
- check this in the admin
- can you do this via API
- why did you use the browser

## Core Rules

1. Prefer the simplest, most stable, fastest, most robust programmatic route available now.
2. Prefer direct CLI or API over browser/UI whenever realistically possible.
3. Do not treat an old ambiguous failure as proof that a direct route is unavailable.
4. Revalidate the best direct route in the current environment before fallback.
5. If the best route exists but is blocked only by access or input the user can provide, stop and ask before fallback.
6. Never fallback silently.
7. Treat a proven reusable route as incomplete until its persistence status is resolved.
8. Document only routes proven in real conditions.
9. If a repo-local route-memory file exists, update it. If none exists, create the smallest acceptable local route-memory surface unless repo-local rules clearly forbid it.
10. If no acceptable persistence surface can be written now, say so explicitly and do not act as if the route is durably handled.
11. Repo-local rules override this skill when they explicitly require a different route.

## Decision Procedure

### 1. Identify the target

Determine:

- which external system is targeted
- whether the task is read, verify, write, trigger, administer, export, or audit
- which route families are realistically possible

### 2. Rank routes

Default order:

1. direct CLI or direct API already available
2. local script or stable programmatic wrapper
3. other stable replayable programmatic route
4. browser-assisted route
5. manual UI or scraping-only fallback

This is a default order, not a blind rule.

### 3. Revalidate the best direct route

Before declaring the best direct route unavailable, retest it in the current environment.

Do not rely only on:

- an old 401 or 403
- an expired token incident
- an old missing-scope result
- a previous session failure
- a browser-first habit
- an assumption that the endpoint is not exposed

Use the smallest safe verification possible first:

- auth check
- whoami or status endpoint
- list or read call
- dry-run
- lightweight metadata call

### 4. Classify the blocker

#### Case A: blocked only by user-provided access

Examples:

- missing API key
- missing env vars
- missing OAuth token
- missing account access
- missing scope the user can grant
- missing credential file
- missing identifier the user can provide

In this case, stop and ask before fallback.

Use this structure:

- best route: `<route>`
- missing: `<exact access/input>`
- if you provide it: `<next action>`
- otherwise I will use: `<fallback route>`

Do not silently move to a worse route in this case.

#### Case B: not realistically available even with user help

Examples:

- no API exists for the needed action
- the provider does not expose the operation programmatically
- the route is broken upstream in a way the user cannot unblock here
- the action requires a browser surface no programmatic interface can reach
- the CLI/API path was disproven now after revalidation

In this case:

- say briefly why the preferred route is not practicable
- use the next-best route
- keep the fallback proportional to the task

Use this structure:

- preferred route: `<route>`
- blocked because: `<reason>`
- using instead: `<fallback route>`

### 5. After a route succeeds, resolve persistence before closure

Once a route is proven in real conditions and is likely to be reusable:

1. Decide whether the route is specific to this one run or operationally reusable.
2. If it is reusable and a repo-local route-memory file already exists, update it in the same task.
3. If it is reusable and no such file exists, create the smallest acceptable local route-memory file unless repo-local rules clearly forbid that.
4. If repo-local rules forbid write-back, or the correct persistence surface is still unclear, stop and say that explicitly instead of treating the task as fully closed.
5. Never rely on chat memory alone for a proven reusable route.

Use this structure when persistence is blocked:

- route proven: `<route>`
- persistence blocked by: `<reason>`
- task status: `route proven but not durably persisted`
- next step needed: `<exact write surface or access needed>`

## Route Memory

If the repo has a local route-memory file such as `reference_effective_routes.md`, consult it first as a starting point.

Treat it as operational memory, not blind truth.

If a better route is proven in real conditions, update that local file in the same task whenever repo-local rules allow it.

If no local route-memory file exists, create the smallest acceptable one for that repo unless repo-local rules clearly forbid it.

Do not treat "I will remember it later" or "it is in chat history" as acceptable persistence.

Document only:

- subject
- objective
- effective route
- prerequisites
- proof of success
- limits or traps
- fallback

Do not store repo-specific routes in this global skill.

## What This Skill Must Not Do

This skill must not:

- execute service-specific business logic by itself
- invent credentials
- assume a token is valid without checking
- fallback silently to browser or scraping
- treat transient chat memory as a substitute for durable route memory
- write broad repo-local documentation when a narrow route-memory update would do
- override explicit repo-local rules
- store repo-specific commands, endpoints, accounts, or credentials in global memory

## Anti-Patterns

Avoid:

- using the browser too early because it feels convenient
- treating an old ambiguous signal as decisive proof
- falling back without telling the user
- proving a reusable route and then closing the task without persisting it
- asking for access when the better route is impossible anyway
- creating an oversized documentation system when a minimal route-memory file is enough
- confusing a doctrine skill with a service integration skill
