---
name: my-personal-second-opinion
description: "[My Personal Skill] Use when Claude Code needs a second opinion, verification, or deeper research on technical matters. Routes to Codex (OpenAI), Gemini (Google), or both in parallel depending on context. Also use for multimodal analysis (audio/video) where Gemini has unique capabilities. Triggers on explicit user requests ('ask Codex', 'ask Gemini', 'second opinion') AND proactively when a question is critical and would benefit from multiple independent perspectives."
---

# Second Opinion — Multi-Engine Verification Agent

Unified skill for getting independent second opinions from external AI engines (Codex / Gemini), either individually or in parallel.

## Engines Available

| Engine | CLI Command | Strengths |
|--------|------------|-----------|
| **Codex** (OpenAI) | `codex exec --dangerously-bypass-approvals-and-sandbox` | Code, architecture, computer use |
| **Gemini** (Google) | `gemini -p` | Audio/video native, deep reasoning, 1M token context |

## Routing Decision

### When to use BOTH in parallel
- Critical architectural decisions
- Security-sensitive code review
- Complex debugging with no clear root cause
- When the user explicitly asks for both / "second opinion"
- Any decision with significant consequences (money, data, production)

### When to use Gemini ONLY
- Audio analysis (Gemini supports native audio, Codex does not)
- Video analysis (Gemini supports native video, Codex does not)
- When the user explicitly says "ask Gemini"

### When to use Codex ONLY
- When the user explicitly says "ask Codex"
- Quick code pattern verification where speed matters

### Default (no explicit request)
- Use BOTH in parallel — they are at parity on benchmarks, two perspectives are better than one

## CLI Usage

### Codex
```bash
codex exec --dangerously-bypass-approvals-and-sandbox "Your query here"
```
- Config already set: `model = "gpt-5.4"`, `model_reasoning_effort = "xhigh"`
- No need to pass `-m` or `-c` flags — defaults from `~/.codex/config.toml` apply
- Subcommand `exec` is REQUIRED for non-interactive use
- `--dangerously-bypass-approvals-and-sandbox` enables full access

### Gemini
```bash
gemini -p "Your query here"
```
- `-p` flag = headless/non-interactive mode (prints response to stdout)
- Do NOT pass `--model` — use Auto routing (Gemini 3 Pro models return 404 in headless mode as of CLI v0.32.1, known bug)
- Auto routing selects: `gemini-3-flash-preview` (simple) / `gemini-2.5-pro` (complex)
- In interactive mode, Auto routing uses `gemini-3.1-pro` / `gemini-3-flash` — headless mode IDs differ
- Auth: OAuth personal (already configured)

### Output integrity — NEVER truncate, NEVER limit
These rules are non-negotiable when executing `codex exec` or `gemini -p`:

1. **NEVER truncate output**: no `| head`, `| tail`, `| head -N`, or any pipe that truncates stdout. These tools produce verbose startup logs (Codex: ~70 lines of MCP startup alone) before the actual answer. Truncating kills the process via SIGPIPE before the review is produced, while reporting a misleading exit code 0.

2. **ALWAYS use `run_in_background: true`**: Codex and Gemini take as long as they need (30s to several minutes). Background execution lets them run to natural completion — the timeout does NOT kill background processes, so there is no risk of interruption. Do NOT set an arbitrary timeout.

3. **Redirect output to a file**: prevents context overflow and makes it easy to read selectively.

Correct pattern:
```bash
# Bash tool params: run_in_background: true (no timeout needed)
codex exec --dangerously-bypass-approvals-and-sandbox "..." > /tmp/codex-review.txt 2>&1
# When notified of completion, use Read tool on the file
```

## Execution Pattern

### Sequential (single engine)
```bash
# Bash tool params: run_in_background: true
# Codex
codex exec --dangerously-bypass-approvals-and-sandbox "Context: ... Question: ..." > /tmp/codex-review.txt 2>&1

# Gemini
gemini -p "Context: ... Question: ..." > /tmp/gemini-review.txt 2>&1
```

### Parallel (both engines)
Launch BOTH via the Bash tool in a single message (two parallel Bash calls, both with `run_in_background: true`):
- Call 1: Codex query → output to file
- Call 2: Gemini query → output to file
- Then synthesize both responses, highlighting agreements and divergences

## Prompt Template (same for both engines)

```
Context: [Project name] ([tech stack]).
Working directory: [pwd]
Relevant docs: CLAUDE.md files at root and in .claude/ directories.
Repository evidence: [paths/lines from prior search]

Task: [specific question]

Constraints: [any constraints]

Please return:
(1) Decisive answer
(2) Supporting citations (file paths:line numbers)
(3) Risks/edge cases
(4) Recommended next steps/tests
(5) Open questions — list any uncertainties explicitly
```

## Search-First Checklist

Before querying ANY engine:
- [ ] `rg <token>` in repo for existing patterns
- [ ] Skim relevant `CLAUDE.md` (root, .claude/*) for project norms
- [ ] `git log -p -- <file/dir>` if history matters
- [ ] Note findings in the prompt as "Repository evidence"

## Output Discipline

### Single engine response
Present the engine's structured reply directly:
1. Decisive answer
2. Citations
3. Risks/edge cases
4. Next steps
5. Open questions

### Parallel response synthesis
When both engines respond, present:
1. **Consensus** — what both engines agree on
2. **Divergences** — where they disagree, with each engine's reasoning
3. **Synthesis** — Claude Code's own recommendation considering both perspectives
4. **Risks** — combined risks from both analyses
5. **Next steps** — unified action items

## Performance Expectations

- **Codex**: 30s to 2 minutes typical
- **Gemini**: 15s to 1 minute typical
- **Best practice**: Launch queries early, work on other analysis while waiting
- **Parallel execution**: Both finish within ~2 minutes max

## Verification Checklist

After receiving responses, verify:
- [ ] Compatible with current library versions (not outdated patterns)
- [ ] Follows the project's directory structure
- [ ] Matches authentication/database patterns in use
- [ ] Considers project-specific constraints from CLAUDE.md
- [ ] No hallucinated file paths or APIs

## Key Principles

1. **Independence**: Each engine provides unbiased analysis without seeing the other's response
2. **Evidence-Based**: Require citations, not just opinions
3. **Synthesis over copy-paste**: Claude Code synthesizes and adds its own judgment
4. **Transparency**: Always tell the user which engine(s) were consulted
5. **Pragmatism**: Don't use parallel queries for trivial questions — reserve for decisions that matter

## Why Claude Code always executes (never the consulting engine)

Even when Claude Code adopts an approach proposed by Codex or Gemini, **Claude Code remains the sole executor**. The consulting engines are advisors, never implementers.

### The architect analogy
An architect consults structural engineers and soil experts — he integrates their expertise, but he draws the final plans because he holds the overall project vision. Same here: Claude Code holds the accumulated session context, project conventions, and user preferences.

### Why not delegate execution to the engine with the best idea?

1. **Lost context**: Codex/Gemini operate in headless mode — they don't carry the session history, prior decisions, CLAUDE.md rules, or project memory that Claude Code has built up
2. **Convention blindness**: They don't know the project's patterns (naming, structure, auth, DB) unless we explicitly pass everything — which is fragile and incomplete
3. **No real-time quality control**: If Codex writes code, Claude Code can't supervise mid-execution — only review after the fact
4. **Debugging complexity**: Mixed authorship ("who wrote this and why?") makes future maintenance harder
5. **Gemini limitation**: `gemini -p` is text in/out only — no filesystem access in headless mode

### The correct workflow
1. Second opinion → receive proposals from Codex/Gemini
2. User chooses which approach to follow
3. Claude Code writes the implementation plan based on the chosen approach
4. **Propose the execution choice to the user** — Claude Code is recommended, but the user decides (see "Execution Choice" below)
5. Execute with the chosen engine

Claude Code is the recommended executor for the reasons above, but the user always gets the final say — see the mandatory proposal in "Execution Choice" below.

## Execution Choice — Who implements?

When the second-opinion phase is complete and implementation work follows, **always propose the choice to the user** before executing. Never assume one executor by default.

### The proposal (MANDATORY before any execution)

Simply ask:

```
Qui exécute ? Claude Code ou Codex ?
```

That's it. No pros/cons, no justifications. The user decides.

### How to recommend

| Situation | Recommander | Pourquoi |
|-----------|-------------|----------|
| Multi-file refactor, architecture | Claude Code | Contexte cross-fichiers critique |
| Security-sensitive code | Claude Code | Pas de marge d'erreur |
| Bien scopé, 1-3 fichiers | Codex | Efficace, context package facile |
| Tokens Claude limités | Codex | Utiliser l'autre allowance |
| Boilerplate, tests | Codex | Tâche mécanique |
| Correction post-review Codex | Claude Code | Connaît déjà les findings |

### Why this matters
The user pays for both subscriptions. The choice has real trade-offs in quality, speed, and token usage. Making it explicit avoids assumptions and lets the user optimize.

## Delegated Execution Mode (explicit user override)

**By default, Claude Code always executes.** But the user can explicitly delegate execution to Codex when needed — typically when Claude Code token limits are reached and the user wants to use their Codex allowance instead.

### Trigger phrases
- "Codex exécute ça" / "Codex handle this"
- "Délègue à Codex" / "Delegate to Codex"
- "Fais faire ça par Codex" / "Have Codex do this"
- "J'ai plus de tokens, passe à Codex" / "I'm out of tokens, switch to Codex"

### Why this exists
The user pays for both Claude Code and Codex subscriptions. When Claude Code's token allowance is exhausted, it makes sense to leverage the Codex allowance for implementation work rather than waiting for limits to reset.

### Context Package Protocol
Since Codex has none of Claude Code's session context, Claude Code MUST prepare a comprehensive context package before delegating. This is the critical step that determines quality.

**Claude Code prepares and passes to Codex:**

1. **Project identity**: name, stack, repo structure
2. **Conventions**: extracted from CLAUDE.md, existing code patterns (naming, file structure, import style, error handling patterns)
3. **Relevant file contents**: the actual content of files Codex will need to read or modify — Codex can read files itself, but explicitly providing them in the prompt ensures it starts with the right context
4. **The task**: precise description of what to implement, with acceptance criteria
5. **Boundaries**: which files to create/modify, which files NOT to touch
6. **Schema/types**: relevant type definitions, DB schema, API contracts so Codex doesn't invent its own

**Prompt template for delegated execution:**
```
You are executing a task in an existing project. Follow these conventions exactly.

PROJECT: [name] — [stack]
WORKING DIRECTORY: [pwd]

CONVENTIONS:
- [extracted from CLAUDE.md and codebase patterns]

RELEVANT FILES (current content):
--- [file path 1] ---
[content]
--- [file path 2] ---
[content]

TASK:
[precise description with acceptance criteria]

BOUNDARIES:
- Create/modify ONLY: [list of files]
- Do NOT touch: [list of files]
- Follow existing patterns in the files above — do not introduce new patterns

AFTER COMPLETING:
- Run: [test command if applicable]
- Show: the diff of all changes made
```

### Execution command
```bash
codex exec --dangerously-bypass-approvals-and-sandbox "[full context package prompt]"
```

### Post-execution review (MANDATORY)
After Codex finishes, Claude Code MUST:
1. **Read all modified files** to verify the changes
2. **Check convention compliance** — naming, structure, patterns match the project
3. **Run tests** if applicable
4. **Fix minor issues** directly (typos, import paths, style inconsistencies)
5. **Report to user**: what Codex did, what Claude Code adjusted, any concerns

### Limitations to communicate to user
- **No Gemini equivalent**: `gemini -p` cannot modify files — delegated execution is Codex-only
- **Larger tasks = more risk**: the bigger the task, the more likely Codex will deviate from project conventions despite the context package
- **No interactive correction**: Codex runs in one shot — if it goes wrong, Claude Code fixes after the fact
- **Recommended scope**: single files or small focused tasks (one function, one component, one test file) — not multi-file architectural changes

### When to recommend delegated execution vs. waiting
- **Delegate**: well-scoped tasks with clear boundaries, boilerplate-heavy work, test writing, single-file implementations
- **Wait for Claude Code**: multi-file refactors, architecture changes, security-sensitive code, anything requiring deep project context across many files

## Relationship to old `codex` skill

This skill **supersedes** the standalone `codex` skill. All second-opinion functionality should go through `second-opinion`. The `codex` skill can be removed.
