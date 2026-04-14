---
name: cli-api-first-doctrine
description: "Use when a task targets an external service or remote system that could be handled through CLI, API, browser UI, scraping, or local wrappers. Enforces a CLI/API-first doctrine: prefer the simplest stable programmatic route, revalidate direct routes before fallback, stop and ask if the best route is blocked only by missing user-provided access, never fallback silently, and document only routes proven in real conditions in repo-local route memory when it exists. For service-specific workflows, see the relevant service skill."
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
7. Only document routes proven in real conditions.
8. Repo-local rules override this skill when they explicitly require a different route.

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

## Route Memory

If the repo has a local route-memory file such as `reference_effective_routes.md`, consult it first as a starting point.

Treat it as operational memory, not blind truth.

If a better route is proven in real conditions, update or propose updating that local file.

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
- write repo-local docs automatically when the repo has not opted into that pattern
- override explicit repo-local rules
- store repo-specific commands, endpoints, accounts, or credentials in global memory

## Anti-Patterns

Avoid:

- using the browser too early because it feels convenient
- treating an old ambiguous signal as decisive proof
- falling back without telling the user
- asking for access when the better route is impossible anyway
- forcing a repo to adopt local route memory
- confusing a doctrine skill with a service integration skill
