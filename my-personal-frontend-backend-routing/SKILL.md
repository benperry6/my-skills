---
name: my-personal-frontend-backend-routing
description: "[My Personal Skill] Automatically routes frontend work to Claude Code and backend work to Codex CLI. Detects file type via heuristics, delegates to the specialized tool with a context package, and reviews the output. Use when a task spans both frontend and backend. For route-repair learnings, use my-personal-verified-learning-loop."
---

# Frontend/Backend Routing

Automatically delegates backend work to Codex and frontend work to Claude Code, regardless of which tool the user started in. Zero manual switching.

When a task spans both frontend and backend, this skill detects the nature of each sub-task via heuristics, delegates to the specialized tool with a full context package, and reviews the output for coherence.

---

## Tool Detection — Who Am I?

Before routing, detect which tool is currently orchestrating. Use environment variables:

```bash
if [ "${CLAUDECODE:-}" = "1" ]; then
  # Running inside Claude Code
  # Strength: frontend (UI components, pages, CSS, design systems)
  CURRENT_TOOL="claude-code"
elif [ "${CODEX_CI:-}" = "1" ]; then
  # Running inside Codex CLI
  # Strength: backend (API, workers, models, migrations, infra)
  CURRENT_TOOL="codex"
elif [ "${GEMINI_CLI:-}" = "1" ]; then
  # Running inside Gemini CLI
  # Strength: general — delegates both frontend and backend
  CURRENT_TOOL="gemini"
fi
```

If none of these are set, assume the current tool handles everything directly (no delegation).

---

## Heuristic Classification

The AI judges the nature of each file or sub-task based on these principles. There are NO hardcoded file paths — the classification is semantic, based on what the code does.

### Backend Indicators

A file or task is **backend** if it involves:

- **API endpoints**: route handlers, controllers, REST/GraphQL resolvers
- **Server actions**: Next.js server actions, Remix loaders/actions (the server-side logic, not the form UI)
- **Database**: models, schemas, migrations, ORM queries, seed scripts
- **Workers/jobs**: background workers, queue consumers, cron jobs, scheduled tasks
- **Server-side services**: business logic services, email senders, payment processing, external API integrations
- **Infrastructure**: Dockerfiles, docker-compose, Terraform, Ansible, systemd units, nginx configs, CI/CD pipelines
- **CLI scripts**: management commands, data scripts, tooling
- **Authentication/authorization**: auth middleware, permission checks, token validation, session management
- **Middleware**: request/response interceptors, rate limiting, CORS, logging
- **Environment config**: server-side env parsing, secrets management, config loaders

### Frontend Indicators

A file or task is **frontend** if it involves:

- **UI components**: JSX, TSX, Vue SFC, Svelte components, React components
- **Pages/layouts**: page components, layout wrappers, navigation structures
- **CSS/styles**: CSS, SCSS, Tailwind utility classes, CSS modules, styled-components, CSS-in-JS
- **HTML templates**: Jinja, EJS, Handlebars, Pug (the template structure, not the data)
- **Visual assets**: SVGs, icons, images, fonts
- **Animations/transitions**: CSS transitions, Framer Motion, GSAP, Lottie
- **Responsive design**: media queries, breakpoint logic, mobile-first layouts
- **Client-side interactivity**: event handlers, form validation (client-side), state management, hooks
- **Form rendering**: form components, input components, select dropdowns (the UI, not the server processing)
- **Design system components**: buttons, cards, modals, toasts, tooltips, tabs, accordions

### Ambiguous Cases

Some files contain both frontend and backend logic. Common examples:

- **Next.js pages with server actions**: the page component is frontend, the server action is backend
- **API route files in Next.js** (`app/api/`): these are backend despite living in a frontend framework
- **Full-stack form handlers**: the form UI is frontend, the submission processing is backend
- **tRPC routers**: the router definition is backend, the client hooks are frontend

**Resolution strategy**: The orchestrating tool handles what it is good at and delegates the rest. If the split is unclear or the task is small enough, do it yourself — do NOT delegate trivially small sub-tasks (under ~10 lines of change).

---

## Routing Table

| Currently in... | Frontend file/task | Backend file/task |
|---|---|---|
| **Claude Code** | Execute directly | Delegate to Codex |
| **Codex** | Delegate to Claude Code | Execute directly |
| **Gemini** | Delegate to Claude Code | Delegate to Codex |

**Key principle**: each tool does what it does best. Claude Code excels at UI/UX, visual polish, component architecture. Codex excels at backend logic, API design, data modeling, infrastructure.

---

## Delegation Commands

### To Codex (for backend work)

```bash
# Bash tool params: run_in_background: true
codex exec --dangerously-bypass-approvals-and-sandbox "[context package prompt]" > /tmp/codex-delegate.txt 2>&1
```

- Runs in the same working directory as the orchestrator
- Config defaults apply from `~/.codex/config.toml`: model = "gpt-5.4", model_reasoning_effort = "xhigh"
- The entire context package is passed as the prompt string (see Context Package Protocol below)
- Output is redirected to file — NEVER into the conversation context

### To Claude Code (for frontend work)

```bash
# Bash tool params: run_in_background: true
claude -p "[context package prompt]" \
  --output-format json \
  --permission-mode acceptEdits \
  --max-turns 8 \
  --tools Read,Edit,Write \
  > /tmp/claude-delegate.txt 2>&1
```

- Runs in the same working directory as the orchestrator
- `-p` = headless/non-interactive mode (pipe mode, no TTY needed)
- Prompt goes immediately after `-p`; do not put flags before supplying the prompt text incorrectly
- Default safe recipe for frontend edits is `acceptEdits` + `--tools Read,Edit,Write`
- Use `--add-dir` when the target files are outside Claude's launch directory
- Do not set `--max-turns` below `5` for file edits; Claude often needs an initial read before a successful write
- For route debugging, prefer `--output-format stream-json --verbose` so the trace shows the actual tool sequence instead of failing silently
- Do not rely on `--no-session-persistence` to suppress plugin/session bootstrap in the current environment; it only works with `--print`, and in practice the SessionStart hooks still fire here
- Output is redirected to file — NEVER into the conversation context

### Important constraints

- Always use `run_in_background: true` on the Bash tool call
- Always redirect output to a file (`> /tmp/xxx-delegate.txt 2>&1`)
- NEVER truncate output: no `| head`, no `| tail`, no `| grep`
- NEVER pipe output through anything — raw redirect only
- One delegation at a time (do not launch both Codex and Claude Code simultaneously for the same task)
- If the Claude Code route itself had to be debugged or repaired, invoke `my-personal-verified-learning-loop` and persist the learning before resuming the user task

---

## Context Package Protocol

When delegating, the orchestrating tool MUST prepare a complete context package. The delegate has NO prior context — it starts from zero. The context package is the ONLY information it receives.

### Required sections

1. **Project identity**: stack, framework, language, key conventions
2. **File contents**: actual content of every file the delegate will need to read or modify, or tightly scoped excerpts when a full file would be too large (do NOT rely on the delegate discovering the right section by itself)
3. **Shared types/interfaces**: type definitions, schemas, or contracts used across frontend and backend
4. **Design system** (if frontend delegation): colors (hex values), fonts (family + weight), spacing conventions, existing component patterns to follow
5. **Task description**: precise instructions with clear acceptance criteria
6. **Boundaries**: explicit list of files to create/modify, and files NOT to touch

### Prompt template

```
You are executing a task in an existing project. Follow these conventions exactly.

PROJECT: [name] — [stack summary, e.g. "Next.js 14 + FastAPI + PostgreSQL"]
WORKING DIRECTORY: [absolute path from pwd]

CONVENTIONS:
[extracted from CLAUDE.md/AGENTS.md — coding style, naming, patterns]
[e.g. "Use snake_case for Python, camelCase for TypeScript"]
[e.g. "All API responses use {data, error, message} shape"]
[e.g. "Components use shadcn/ui + Tailwind v3"]

RELEVANT FILES (current content or targeted excerpts):
--- [file path 1] ---
[full file content OR the exact excerpt with line anchors]
--- [file path 2] ---
[full file content OR the exact excerpt with line anchors]
--- [file path 3] ---
[full file content OR the exact excerpt with line anchors]

SHARED TYPES/INTERFACES:
--- [types file path] ---
[content of shared type definitions]

TASK:
[precise description of what needs to be done]
[acceptance criteria — what "done" looks like]
[any edge cases to handle]

BOUNDARIES:
- Create/modify ONLY: [explicit list of file paths]
- Do NOT touch: [explicit list of files that must remain unchanged]
- Follow existing patterns — do not introduce new libraries, patterns, or conventions

AFTER COMPLETING:
- Show the diff of all changes made
- List any concerns, assumptions, or questions
```

### Guidelines for preparing the context package

- **Read before you delegate**: always read the files the delegate will need BEFORE constructing the prompt. Include their actual content when they are reasonably sized; for large files, include only the exact excerpts and anchors needed for the edit.
- **Be specific, not vague**: "Add a loading state to the UserTable component" is better than "improve the user table".
- **Include neighboring files**: if the delegate needs to match patterns from similar files, include those files too.
- **Over-include rather than under-include**: it is better to give the delegate too much context than too little. A delegate with incomplete context produces bad code.
- **Shared contracts are critical**: if frontend and backend share types, API shapes, or validation rules, include them in BOTH delegations.
- **For large frontend files, give search anchors**: include the exact function names, strings, selectors, or grep hits to edit. Otherwise Claude Code may waste turns on a full-file `Read` that exceeds the token cap before it narrows down.

---

## Gemini Design Integration

When Claude Code handles a frontend task and the task involves one of these:

- A **new visual component** (not a tweak to an existing one)
- A **new page** or major page section
- A **UI overhaul** or redesign of an existing page

Then invoke the `my-personal-gemini-design` skill to get an aesthetic proposal BEFORE or DURING implementation. The Gemini design output informs the implementation — it does not replace it.

**Skip the design skill** for:
- Small CSS fixes (color change, spacing adjustment, font weight)
- Adding a field to an existing form
- Bug fixes in UI behavior
- Copy/text changes
- Adding a button or link to an existing component

---

## Post-Delegation Review

After the delegate finishes (output file available), the orchestrating tool MUST:

1. **Read the output file** (`/tmp/codex-delegate.txt` or `/tmp/claude-delegate.txt`) to understand what was done
2. **Read all files produced or modified** by the delegate — use `git diff` or read the files directly
3. **Verify coherence**:
   - Types match between frontend and backend (no mismatched field names, no missing fields)
   - Imports are correct (no broken imports, no unused imports)
   - Naming is consistent with the rest of the project (no sudden switch from camelCase to snake_case)
   - No new dependencies were introduced without justification
   - Code follows the project's existing patterns
4. **Fix minor discrepancies directly**: typos, import paths, style inconsistencies, missing semicolons — fix these yourself without re-delegating
5. **Report to user**:
   - What was done and by which tool
   - Summary of changes (files modified, key decisions made)
   - Any adjustments the orchestrator made after review
   - Any concerns or items that need the user's attention

---

## Error Handling

If the delegate fails (process crash, timeout, non-zero exit, or produces clearly broken output):

1. **Check for partial changes**: run `git status` and `git diff` to see if the delegate made any file changes before failing
2. **Report the failure clearly**:
   - What was attempted (the task description)
   - What the delegate produced (error message, partial output)
   - What remains to be done
   - Whether partial changes should be kept or reverted
3. **Do NOT auto-retry**: the failure may indicate a problem with the task description, the context package, or the delegate's capabilities. Let the user decide whether to:
   - Retry with a modified context package
   - Handle the task directly in the current tool
   - Abandon the delegation and do it manually

**Common failure modes**:
- Delegate cannot find files → context package was missing file contents
- Claude Code cannot find target files → the target lived outside the launch directory and needed `--add-dir` or a repo-local path
- Claude Code exits with `error_max_turns` on a trivial edit → the turn budget was too low for the normal `Write -> Read -> Write` sequence
- Claude Code tries to `Read` a very large file and gets a token-cap error → the context package should have supplied exact excerpts/anchors instead of expecting a whole-file read
- Claude Code appears to ignore the prompt in headless mode → the prompt placement after `-p` or the CLI invocation shape was wrong
- Claude Code seems "stuck in bootstrap" even with `--no-session-persistence` → that flag is not a reliable way to suppress SessionStart hooks in this environment
- Delegate introduces wrong patterns → conventions section was incomplete
- Delegate times out → task was too large, split it into smaller sub-tasks
- Delegate produces syntax errors → shared types/interfaces were missing

If the route itself was repaired during debugging:

1. stop treating it as a one-off local fix
2. invoke `my-personal-verified-learning-loop`
3. record the repaired path and evidence
4. patch this skill if the canonical delegation recipe changed
5. only then retry or resume the original delegated task

---

## Output Discipline

Same rules as the `my-personal-second-opinion` skill — these are non-negotiable:

- **`run_in_background: true`** for ALL delegation calls (Bash tool parameter)
- **Redirect ALL output to file**: `> /tmp/codex-delegate.txt 2>&1` or `> /tmp/claude-delegate.txt 2>&1`
- **NEVER truncate**: no `| head`, no `| tail`, no `| head -c`
- **NEVER pipe through anything**: no `| grep`, no `| jq`, no `| sed`
- **NEVER embed delegate output in the conversation**: read the file, summarize the relevant parts, but do not paste hundreds of lines into the chat
- **Clean up temp files** after the task is complete: `rm -f /tmp/codex-delegate.txt /tmp/claude-delegate.txt`

---

## Usage Examples

### Example 1: User asks Claude Code to add a new API endpoint + its frontend form

1. Claude Code classifies: the API endpoint is **backend**, the form is **frontend**
2. Claude Code reads relevant files (existing endpoints for patterns, shared types, existing forms)
3. Claude Code delegates the API endpoint to Codex with a full context package
4. While waiting, Claude Code builds the frontend form directly
5. When Codex finishes, Claude Code reviews the endpoint code, verifies types match the form, fixes any discrepancies
6. Claude Code reports to user: "Built the form in `components/NewUserForm.tsx`. Codex created the endpoint in `api/routes/users.py`. I adjusted the response type to match the form's expected shape."

### Example 2: User asks Codex to fix a broken dashboard page

1. Codex classifies: dashboard page is **frontend**
2. Codex reads the page file and related components
3. Codex delegates to Claude Code with the page content, design system info, and the bug description
4. When Claude Code finishes, Codex reviews the changes for correctness
5. Codex reports to user: "Delegated the dashboard fix to Claude Code. The issue was a missing null check in the data mapping. Claude Code also improved the loading state."

### Example 3: Task is ambiguous — Next.js server action

1. The user asks to "add server-side validation to the contact form"
2. The current tool reads the file — it contains both a React form component and a server action
3. The form validation logic is interleaved with the UI — splitting would be artificial
4. Decision: handle it directly, no delegation (the task is cohesive enough)
