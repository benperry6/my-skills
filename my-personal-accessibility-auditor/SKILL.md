---
name: my-personal-accessibility-auditor
description: "[My Personal Skill] When the user wants to audit a website or web application for accessibility compliance. Also use when the user mentions 'accessibility audit,' 'WCAG,' 'a11y,' 'screen reader,' 'keyboard navigation,' 'color contrast,' 'accessibility check,' 'ADA compliance,' 'EAA compliance,' or 'Section 508.' Runs real CLI tools (axe-core, Pa11y, Lighthouse) and browser automation checks."
metadata:
  version: 1.0.0
---

# Accessibility Auditor

You are an expert accessibility engineer. You audit web applications against WCAG 2.2 AA using **real CLI tools and browser automation** — not just advice.

## Before Auditing

Gather this context (ask if not provided):

### 1. Target
- What URL(s) to audit? (single page, list of pages, or full site)
- Is it a SPA (React/Vue/Angular) or server-rendered?
- Is authentication required to access pages?

### 2. Scope
- Which WCAG level? (A, AA, AAA — default: AA)
- Any specific concerns? (keyboard nav, screen readers, contrast, forms)
- Legal context? (ADA, EAA/European Accessibility Act, Section 508)

### 3. Context
- Is this a pre-launch audit, a regression check, or a full compliance audit?
- Are there known accessibility issues already?
- What browsers/devices are target users on?

---

## Audit Workflow

```dot
digraph audit {
  "1. Automated Scans" -> "2. Parse & Triage Results";
  "2. Parse & Triage Results" -> "3. Browser Manual Checks";
  "3. Browser Manual Checks" -> "4. Generate Report";
  "4. Generate Report" -> "5. Remediation Guidance";
}
```

**Critical principle:** Automated tools only catch ~13% of WCAG criteria reliably. ~45% are partially detectable, ~42% require manual testing. Always combine automated scans with browser-based manual checks.

---

## Phase 1: Automated Scans

Run these three tools in sequence. Each catches issues the others miss.

### 1a. axe-core CLI

```bash
# Install if needed
npm list -g @axe-core/cli || npm install -g @axe-core/cli

# Run scan with JSON output
axe <URL> --stdout --exit > axe-results.json
```

Key flags:
- `--include "main"` — scope to main content area
- `--exclude ".cookie-banner"` — skip known non-content elements
- `--tags wcag2aa,wcag22aa` — restrict to WCAG 2.2 AA rules
- `--exit` (`-q`) — return nonzero exit code if violations found
- Multiple pages: `axe page1.com page2.com --stdout`

### 1b. Pa11y

```bash
# Install if needed
npm list -g pa11y || npm install -g pa11y

# Run with axe runner for broader coverage
pa11y <URL> --runner axe --reporter json > pa11y-results.json
```

Key flags:
- `--standard WCAG2AA` — set standard (default)
- `--level error` — only errors (or `warning` for more)
- `--threshold 0` — fail on any issue
- `--runner axe` — use axe engine instead of HTML_CodeSniffer (recommended: run both)

### 1c. Lighthouse Accessibility

```bash
# Install if needed
npm list -g lighthouse || npm install -g lighthouse

# Run accessibility-only audit
lighthouse <URL> --only-categories=accessibility --output=json --output-path=lighthouse-results.json --chrome-flags="--headless=new"
```

The `categories.accessibility.score` is 0-100 (weighted average). Audits marked "manual" don't affect the score — those need Phase 3.

### Interpreting Results

After running all three, read the JSON files and triage:

| Severity | axe impact | Pa11y level | Action |
|----------|-----------|-------------|--------|
| **Critical** | critical | error | Fix before launch |
| **Serious** | serious | error | Fix in current sprint |
| **Moderate** | moderate | warning | Fix in next sprint |
| **Minor** | minor | notice | Backlog |

**For detailed CLI reference and flags:** See [references/cli-tools.md](references/cli-tools.md)

---

## Phase 2: Parse & Triage

After running automated scans, analyze the JSON results:

1. **Deduplicate** — axe and Pa11y often flag the same issues. Group by WCAG criterion.
2. **Count by criterion** — Which WCAG criteria have the most violations?
3. **Identify patterns** — Same issue across many pages = systemic (fix in component). One page = isolated fix.
4. **Flag false positives** — Some "needs review" items are fine. Note them but don't ignore.

### Top 10 Most Common Violations (by frequency in real-world audits)

| # | Issue | WCAG | % of sites failing |
|---|-------|------|--------------------|
| 1 | Low color contrast | 1.4.3 | ~98% |
| 2 | Missing image alt text | 1.1.1 | ~75% |
| 3 | Unclear link text | 2.4.4 | ~80% |
| 4 | Unlabeled form controls | 3.3.2 | ~62% |
| 5 | Missing page title | 2.4.2 | ~28% |
| 6 | Missing language attribute | 3.1.1 | ~18% |
| 7 | Empty buttons | 4.1.2 | ~27% |
| 8 | Missing focus indicators | 2.4.7 | ~80%+ |
| 9 | Incorrect ARIA usage | 4.1.2 | ~40% |
| 10 | Touch target too small | 2.5.8 | ~50% |

---

## Phase 3: Browser Manual Checks

Automated scans miss critical issues. Use browser automation (claude-in-chrome) for these checks.

### 3a. Keyboard Navigation

Test these using the browser:
1. **Tab through the entire page** — Is every interactive element reachable?
2. **Focus visibility** — Can you SEE where focus is at all times?
3. **Focus order** — Does tab order match visual order (left→right, top→bottom)?
4. **Skip link** — Is there a "Skip to main content" link that works?
5. **Focus traps** — Can you tab INTO and OUT OF modals/dropdowns?
6. **No keyboard traps** — Can you reach every part of the page and leave it?

### 3b. Screen Reader Simulation

Check the accessibility tree via browser:
- Do all images have meaningful alt text (not just "image" or filename)?
- Do form inputs have associated labels?
- Are headings hierarchical (h1 → h2 → h3, no skipped levels)?
- Do ARIA landmarks exist (main, nav, banner, contentinfo)?
- Are live regions (toasts, alerts) announced?

### 3c. Visual Checks

- **Color contrast** — Text on backgrounds meets 4.5:1 (normal) or 3:1 (large/bold)
- **Reduced motion** — Do animations respect `prefers-reduced-motion`?
- **Dark mode** — Does `prefers-color-scheme: dark` maintain contrast?
- **Zoom to 200%** — Is content still readable and functional?
- **Text spacing** — Can text spacing be increased without clipping?

### 3d. Forms & Dynamic Content

- **Error messages** — Are they clear, specific, and programmatically associated?
- **Required fields** — Are they indicated both visually AND with `aria-required`?
- **Modals** — Does focus move into modal on open and return to trigger on close?
- **Single-page navigation** — Does focus move to new content on route change?
- **Autocomplete** — Do fields have appropriate `autocomplete` attributes?

### 3e. WCAG 2.2 New Criteria

These are NEW in 2.2 — automated tools may not fully cover them yet:

| Criterion | What to Check |
|-----------|---------------|
| **2.4.11 Focus Not Obscured** | Is the focused element ever hidden behind sticky headers, footers, or floating elements? |
| **2.5.7 Dragging Movements** | Can every drag-and-drop interaction be done WITHOUT dragging? (e.g., use buttons or menus instead) |
| **2.5.8 Target Size (24px min)** | Are all clickable targets at least 24×24 CSS pixels? |
| **3.3.8 Accessible Authentication** | Can login work WITHOUT cognitive tests? (no CAPTCHA without alternative) |

**For detailed browser automation recipes:** See [references/browser-recipes.md](references/browser-recipes.md)

**For the full WCAG 2.2 checklist with automation status:** See [references/wcag-checklist.md](references/wcag-checklist.md)

---

## Phase 4: Generate Report

### Report Structure

```markdown
# Accessibility Audit Report
**URL:** [target]
**Date:** [date]
**Standard:** WCAG 2.2 Level AA
**Tools:** axe-core v4.11.x, Pa11y v9.1.x, Lighthouse v10.x, Manual testing

## Executive Summary
- **Overall Score:** [Lighthouse score]/100
- **Total Issues:** [N] ([critical] critical, [serious] serious, [moderate] moderate, [minor] minor)
- **Top Barrier:** [most impactful issue]
- **Recommendation:** [PASS / CONDITIONAL PASS / FAIL]

## Automated Scan Results
| Tool | Issues Found | Critical | Serious |
|------|-------------|----------|---------|
| axe-core | N | N | N |
| Pa11y | N | N | N |
| Lighthouse | score/100 | — | — |

## Findings by WCAG Criterion

### [WCAG Ref] — [Criterion Name] — [SEVERITY]
- **What:** [Description of the issue]
- **Where:** [Page URL + CSS selector or element description]
- **Impact:** [Who is affected and how]
- **Fix:**
  ```html
  <!-- Before -->
  <img src="photo.jpg">

  <!-- After -->
  <img src="photo.jpg" alt="Team members collaborating around a whiteboard">
  ```
- **WCAG Reference:** [link to Understanding doc]

[Repeat for each finding]

## Manual Testing Results

### Keyboard Navigation: [PASS/FAIL]
[Details of keyboard testing findings]

### Screen Reader: [PASS/FAIL]
[Details of AT testing findings]

### Visual Checks: [PASS/FAIL]
[Details of visual testing findings]

## Remediation Priority

### Immediate (this week)
- [ ] [Critical fix 1]
- [ ] [Critical fix 2]

### Short-term (this sprint)
- [ ] [Serious fix 1]
- [ ] [Serious fix 2]

### Ongoing (backlog)
- [ ] [Moderate improvement 1]
```

### Report Rules

1. **Every finding has a fix** — Not just "this is wrong" but "here's how to fix it"
2. **Show before/after code** — Developers need copy-pasteable solutions
3. **Link to WCAG Understanding docs** — For context on why it matters
4. **Be honest about pass/fail** — Don't soften. If it fails AA, say it fails
5. **Prioritize by user impact** — Not by tool severity alone

---

## Phase 5: Remediation Guidance

### Common Fixes (quick reference)

| Issue | Fix |
|-------|-----|
| Missing alt text | Add `alt="[descriptive text]"` or `alt=""` for decorative images |
| Low contrast | Increase to ≥4.5:1 (normal text) or ≥3:1 (large text, 18px+ or 14px+ bold) |
| Missing form label | Add `<label for="id">` or `aria-label="..."` |
| Empty link/button | Add text content or `aria-label` |
| Missing page title | Add `<title>` in `<head>` |
| Missing lang | Add `lang="en"` to `<html>` |
| No skip link | Add `<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>` |
| Focus not visible | Ensure `:focus` has visible outline (never `outline: none` without replacement) |
| Target too small | Ensure clickable area is ≥24×24px (padding counts) |
| Keyboard trap | Ensure Escape closes modals and returns focus to trigger element |

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Accessibility Check
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install -g @axe-core/cli pa11y
      - name: Start dev server
        run: npm run dev &
      - name: Wait for server
        run: npx wait-on http://localhost:3000
      - name: axe scan
        run: axe http://localhost:3000 --exit --tags wcag2aa,wcag22aa
      - name: Pa11y scan
        run: pa11y http://localhost:3000 --runner axe --threshold 0
```

### Exit Codes

| Tool | Behavior |
|------|----------|
| axe-core | Exits 0 by default. Use `--exit` to return 1 on violations |
| Pa11y | Exits 2 if issues found above threshold |
| Lighthouse | Always exits 0 (parse JSON to enforce threshold) |

---

## Sources

- **Full Deep Research source:** See [references/deep-research-report.md](references/deep-research-report.md)

---

## Related Skills

- **web-design-guidelines**: For Web Interface Guidelines compliance review
- **page-cro**: For conversion optimization that maintains accessibility
- **my-personal-technical-writer**: For writing accessible documentation
