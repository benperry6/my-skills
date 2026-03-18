---
name: my-personal-gemini-design
description: "[My Personal Skill] Design assistant for frontend development. Checks shadcn/ui components first, consults Gemini for aesthetic proposals, validates via web-design-guidelines, and integrates into the codebase. Use when creating new visual components, pages, or UI overhauls."
---

# Gemini Design Assistant

Design assistant workflow for creating visually polished frontend components. Orchestrates shadcn/ui component discovery, Gemini-powered design generation, fallback handling, and quality validation before integrating into the codebase.

## Activation Criteria

### When to activate
- Creating a new visual component (hero section, pricing card, dashboard layout, etc.)
- Building a new page from scratch
- UI overhaul or visual redesign of existing components
- Migrating a design mockup or screenshot to code

### When NOT to activate
- CSS fixes (adjusting a color, fixing alignment)
- Adding a form field to an existing form
- Adjusting padding, margins, or spacing
- Updating text content or copy
- Bug fixes that happen to involve UI code
- Adding a simple button or link

## Step 1 — shadcn/ui First

Before generating any design, check whether shadcn/ui components already cover the need. This avoids reinventing existing, well-tested UI primitives.

### Discovery commands

```bash
# Search for components matching the need
npx shadcn@latest search -q "keyword"

# Get API docs and examples for a specific component
npx shadcn@latest docs <component>

# Check what's already installed in the project
npx shadcn@latest info --json
```

### Decision
- If a shadcn component covers the need directly, use it as the base and skip Gemini consultation.
- If shadcn components cover parts of the need, list them for Gemini to compose.
- If no shadcn component applies, proceed to Gemini with a note that custom markup is acceptable.

### Critical Rules (enforced in ALL generated code)

These rules apply to every component produced by this workflow, whether from Gemini output or manual construction:

1. **Semantic colors only** — `bg-primary`, `text-muted-foreground`, `border-border`. Never raw values like `bg-blue-500` or `text-emerald-600`.
2. **`FieldGroup` + `Field` for forms** — Never raw `div` with `Label` for form layout.
3. **`gap-*` for spacing** — Never `space-x-*` or `space-y-*`. Use `flex` with `gap-*`.
4. **`data-icon` for icons in buttons** — `data-icon="inline-start"` or `data-icon="inline-end"`. No sizing classes on icons inside components.
5. **`cn()` for conditional classes** — Never manual template literal ternaries for className.
6. **Full Card composition** — Always use `CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter`. Never dump everything in `CardContent`.
7. **`Separator` instead of `<hr>` or border divs** — Use the shadcn Separator component.
8. **`Badge` instead of custom styled spans** — For status labels, tags, counts.
9. **`Skeleton` for loading states** — No custom `animate-pulse` divs.
10. **`sonner` for toasts** — Use `toast()` from `sonner`, not custom notification markup.

## Step 2 — Gemini Consultation

Call Gemini CLI with a structured design prompt. Gemini acts as a senior UI/UX designer producing JSX code.

### Tool detection

If the environment variable `$GEMINI_CLI=1` is set (meaning this skill is running inside Gemini itself), **skip this step entirely**. Gemini can use its own design capabilities directly without calling itself. Only consult Gemini externally from Claude Code or Codex.

### Prompt template

Construct the prompt by filling in the bracketed placeholders with project-specific values:

```
You are a senior UI/UX designer specializing in modern web interfaces.
Generate a [COMPONENT_TYPE] component for a [TECH_STACK] project.

DESIGN SYSTEM:
[Insert project's design system: colors, fonts, spacing, existing patterns]

SHADCN COMPONENTS TO USE:
[List components identified in Step 1]

REQUIREMENTS:
[Insert user's request]

RULES:
- Use ONLY the shadcn components listed above as building blocks
- Use semantic color tokens (bg-primary, text-muted-foreground, border-border)
- Mobile-first responsive design
- Include hover/focus states and smooth transitions (duration-200)
- Ensure accessible: proper contrast, focus rings, aria labels
- Use gap-* for spacing, never space-*
- Use cn() for conditional classes

OUTPUT FORMAT:
Return ONLY the JSX code for the component with imports.
Do NOT include:
- Business logic or state management
- API calls or data fetching
- Type definitions (the calling tool handles these)
- Explanations or commentary — just the code
```

### Execution

```bash
# Build the prompt (substitute actual values for placeholders)
DESIGN_PROMPT="You are a senior UI/UX designer..."

# Execute with model preference and fallback
GEMINI_MODEL=gemini-3.1-pro-preview gemini -p "$DESIGN_PROMPT" > /tmp/gemini-design.txt 2>&1
status=$?

if [ "$status" -ne 0 ]; then
  if rg -q 'ModelNotFoundError|Requested entity was not found|does not have access|code: 404' /tmp/gemini-design.txt; then
    gemini -p "$DESIGN_PROMPT" > /tmp/gemini-design.txt 2>&1
  fi
fi
```

### Output discipline

These rules are non-negotiable when executing `gemini -p`:

1. **ALWAYS use `run_in_background: true`** — Gemini takes 15s to 2+ minutes. Background execution lets it run to natural completion.
2. **ALWAYS redirect output to `/tmp/gemini-design.txt`** — Prevents context overflow and makes selective reading possible.
3. **NEVER truncate output** — No `| head`, `| tail`, or any pipe that limits stdout. These kill the process via SIGPIPE before the design is produced, while reporting a misleading exit code 0.
4. **NEVER pipe through other commands** — No `| jq`, `| grep`, or any post-processing pipe. Write to file, then read the file.

## Step 3 — Fallback Chain

Handle Gemini rate limits gracefully with Antigravity proxy fallback.

### Rate limit detection

After the Gemini CLI call, check for rate limit indicators:

```bash
# Check exit code and stderr/stdout for rate limit signals
if rg -q '429|quota|rate.limit|RESOURCE_EXHAUSTED' /tmp/gemini-design.txt; then
  echo "Rate limited — falling back to Antigravity proxy"
  FALLBACK=true
fi
```

### Antigravity fallback

If rate limited, route the same prompt through the local Antigravity proxy:

```bash
if [ "$FALLBACK" = "true" ]; then
  curl -s -X POST http://localhost:8045/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"gemini-3.1-pro-preview\",
      \"messages\": [{\"role\": \"user\", \"content\": $(echo "$DESIGN_PROMPT" | jq -Rs .)}]
    }" > /tmp/gemini-design.txt 2>&1

  # Check if Antigravity is reachable
  if rg -q 'Connection refused|connection refused|ECONNREFUSED' /tmp/gemini-design.txt; then
    echo "BLOCKED: Gemini CLI rate limit reached. Antigravity proxy is offline."
    echo "Open Antigravity Manager and activate the proxy, then retry."
    exit 1
  fi
fi
```

### Full fallback chain summary

```
1. gemini -p (with GEMINI_MODEL=gemini-3.1-pro-preview)
   -> Success: proceed to Step 4
   -> Model not found: retry with default model
   -> Rate limited (429 / quota / RESOURCE_EXHAUSTED):
      2. POST to http://localhost:8045/v1/chat/completions
         -> Success: proceed to Step 4
         -> Connection refused:
            STOP. Display message:
            "Gemini CLI rate limit reached. Antigravity proxy is offline.
             Open Antigravity Manager and activate the proxy, then retry."
```

## Step 4 — Quality Gate

Claude Code evaluates the Gemini output before integrating it into the codebase. This is a three-part validation.

### 4a. UI/UX compliance

Invoke the `web-design-guidelines` skill on the generated code to check:
- Accessibility (contrast ratios, focus management, aria attributes)
- Responsive behavior (mobile-first, breakpoint usage)
- Interaction states (hover, focus, active, disabled)
- Layout best practices (semantic HTML, logical ordering)

### 4b. shadcn compliance

Verify the generated code against the Critical Rules from Step 1:
- [ ] Semantic colors only (no raw `bg-blue-500`, `text-red-600`, etc.)
- [ ] Correct component composition (`CardHeader`/`CardTitle`/`CardContent`/`CardFooter`)
- [ ] `gap-*` for spacing (no `space-x-*` or `space-y-*`)
- [ ] `data-icon` on icons in buttons (no `size-4` or `w-4 h-4` on icons)
- [ ] `cn()` for conditional classes
- [ ] `FieldGroup` + `Field` for any form sections
- [ ] `Separator` instead of `<hr>` or border divs
- [ ] `Badge` for status/tag elements
- [ ] `Skeleton` for loading states
- [ ] `sonner` for toast notifications

### 4c. Codebase coherence

Verify the output integrates cleanly with the existing project:
- [ ] TypeScript types match the project's type conventions
- [ ] Import paths use the project's alias (`@/`, `~/`, etc.)
- [ ] Component naming follows the project's convention (PascalCase, file naming)
- [ ] No duplicate components (check if similar components already exist)
- [ ] Props interface matches how the component will be consumed
- [ ] `"use client"` directive present if the component uses hooks/state/events (check `isRSC` from shadcn info)

### Decision matrix

| Gemini Output Quality | Action |
|------------------------|--------|
| Good — passes all checks | Use as-is, integrate directly |
| Mostly good — minor issues (wrong import paths, missing types, naming mismatch) | Adapt: fix imports, add types, adjust naming to match project conventions |
| Mediocre — wrong component choices, poor composition, accessibility issues | Discard entirely and build manually using the shadcn components identified in Step 1 |
| Off-topic — doesn't match the request | Discard and re-prompt with more specific requirements, or build manually |

### Integration

After the quality gate passes:
1. Create the component file in the project's component directory
2. Add TypeScript types/interfaces
3. Wire up any necessary imports in parent components
4. Add `"use client"` directive if needed (based on `isRSC` from shadcn info)
5. Test the component renders correctly

## Output Discipline (Global)

These rules apply to ALL external tool calls in this workflow:

1. **`run_in_background: true`** for any Gemini CLI or Codex call
2. **Redirect to file** — always `/tmp/gemini-design.txt` (or similar named file for parallel calls)
3. **NEVER truncate** — no `| head`, `| tail`, `| head -N`
4. **NEVER pipe** — no `| jq`, `| grep`, `| sed`. Write to file, then read
5. **Read selectively** — use the Read tool on the output file, optionally with offset/limit for large outputs

## Workflow Summary

```
User requests new visual component / page / UI overhaul
  |
  v
Step 1: shadcn/ui discovery
  - Search for matching components
  - Get docs and examples
  - List components to use as building blocks
  |
  v
Step 2: Gemini consultation (skip if $GEMINI_CLI=1)
  - Build structured design prompt with project context
  - Execute via gemini -p (background, to file)
  - Wait for completion, read output
  |
  v
Step 3: Fallback chain (if rate limited)
  - Detect 429 / quota / RESOURCE_EXHAUSTED
  - Try Antigravity proxy at localhost:8045
  - STOP if proxy offline
  |
  v
Step 4: Quality gate
  - 4a: web-design-guidelines compliance
  - 4b: shadcn Critical Rules compliance
  - 4c: Codebase coherence (types, imports, naming)
  - Decision: use / adapt / discard
  |
  v
Integration into codebase
```
