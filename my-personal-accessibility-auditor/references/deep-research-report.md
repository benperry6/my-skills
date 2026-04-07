# CLI Accessibility Testing Tools & WCAG 2.2 Audit Best Practices
## Source: ChatGPT Deep Research — 2026-03-09

---

## CLI Accessibility Testing Tools (2026)

**axe-core CLI (@axe-core/cli)** – Latest *axe-core CLI* is version **4.11.1** (Feb 2026). Install globally with:
```bash
npm install -g @axe-core/cli
```
Note: *axe-cli* requires Chrome and a WebDriver (e.g. browser-driver-manager). Usage is simply:
```bash
axe https://example.com [options]
```
By default it outputs a summary; use `--save filename.json` or `--stdout` to get full JSON results. You can target multiple pages (`axe site.com other.com`), or specific DOM scopes with CSS filters: `--include "main"` and `--exclude ".footer"`. Common flags include `--rules` or `--tags` to restrict tests, and `--disable` to skip rules. Use `--exit` (`-q`) to have the process return a nonzero exit code when violations are found. The JSON results include arrays of violations, passes, incomplete, etc. In general, axe catches most programmatic issues (missing `alt`, contrast failures, form labels, ARIA misuse, etc.), but it **cannot verify context or subjective criteria** (e.g. meaningful alt text, correct reading order, cognitive clarity). Human review is needed for any flag to confirm the actual user impact.

**Pa11y CLI** – Current version **v9.1.1** (Feb 2026). Install with:
```bash
npm install -g pa11y
```
Run it like:
```bash
pa11y [options] <URL>
```
By default Pa11y uses the HTML_CodeSniffer runner (WCAG2AA ruleset), but you can specify the *axe* engine with `--runner axe` (or combine runners). It outputs a summary by default, or use `--reporter json` (or `csv`, `html`, etc.) to get detailed JSON. Key options: `--standard` (WCAG2A/AA/AAA), `--level` (error/warning/notice), and `--threshold N` to set a max allowed issue count (above threshold it exits 2). Pa11y's default exit code is 2 if any (error) issues are found. Unlike axe's focus on deep rule sets, Pa11y provides a quick CLI wrapper and built‑in reporting. It flags similar issues (missing alt, contrast, labels, etc.), but note: HTML_CodeSniffer (default) may not catch everything axe finds, and vice versa. Pa11y is very configuration-driven – for example, you can ignore specific codes or notices, or set `--level=warning` to fail on warnings too.

**Lighthouse (CLI)** – Google Lighthouse (v10+ in 2026) can run headless audits. Install with:
```bash
npm install -g lighthouse
```
Run an accessibility-only audit via:
```bash
lighthouse https://example.com --only-categories=accessibility --output=json --output-path=report.json
```
This produces a JSON report. The `categories.accessibility.score` is a 0–100 score (100 is best) that reflects a weighted average of individual checks. Internally Lighthouse uses the axe-core ruleset for many checks. In the JSON, look under `categories.accessibility` and `audits` for each test. By default Lighthouse always exits 0 unless it crashes; to enforce a pass threshold you must parse the JSON. The score is calculated by summing each audit's weight times pass(=1) or fail(=0) (for example, "image-alt" might be 10 points, "button-name" 3 points, etc.), so failing high-weight audits hurts the score more. Importantly, audits flagged as "manual" do not count toward the numeric score, so some issues (like focus order or semantic meaning) won't lower the score.

**WAVE API** – There is **no official free CLI** for WAVE (WebAIM). WAVE's functionality is provided by a paid API. The WAVE API works via HTTP: you submit a GET like `http://wave.webaim.org/api/request?key=YOURKEY&url=https://example.com`, and you get back a JSON (or XML) report. A typical usage would be:
```bash
curl "http://wave.webaim.org/api/request?key=YOURKEY&url=https://example.com" -o wave.json
```
There is a cost per analysis, and results include WAVE's error and alert codes.

**New Tools (2025–2026)** – The landscape has not seen many brand-new open-source CLI scanners; the leaders remain axe-core, Pa11y, Lighthouse, and the IBM Equal Access Checker. One notable addition is Microsoft's *Accessibility Insights CLI* (part of the AISuite), which offers `npx axic` to run checks (it's based on axe-core plus extra rulesets). However, for most projects axe, Pa11y, or Lighthouse suffice.

**IBM Equal Access Checker (Accessibility Checker)** – IBM provides a CLI via its **Accessibility Checker** (formerly "IBM Equal Access Checker"). Install via NPM (`npm install accessibility-checker`), and run with the `achecker` CLI (or via `npx achecker`). For example, create a text file list of URLs or HTML files, then execute:
```bash
npx achecker path/to/list.txt
```
This scans the listed pages against IBM's ACT rule library. It outputs JSON, CSV, or HTML. It integrates with Node test frameworks (Puppeteer, Selenium, Jest, etc.). Version is in the 4.x series (as of early 2026 ~v4.0.12). Like axe, it finds many code-level issues (alt text, ARIA, labels, etc.) and flags possible form/authentication issues, but it still cannot judge *meaning*.

**Deque's Other Tools** – Beyond axe-core, Deque offers commercial tools (Accessibility Insights/Attest). The free CLI integrations are mainly axe and Pa11y. Deque's *axe-puppeteer* integration provides the `AxePuppeteer` class to run axe inside Puppeteer. They also have *Attest CLI* (part of WorldSpace Attest) which supports custom rulesets and various report formats (HTML, JUnit, etc.). But these require licensed products.

---

## What Automated Tools Cannot Catch

Automated scanners have inherent limits. Studies show they only **fully detect ~13%** of WCAG success criteria reliably; roughly 45% are *partially detectable* and ~42% are **undetectable** by any scan. In practice:

- **Fully Automatable Criteria (mostly tech-checks)** include things like: *color contrast ratios (1.4.3, 1.4.11)*, *page `<title>` present (2.4.2)*, *language attribute (3.1.1)*, *skip-links or landmarks (2.4.1)*, *autocomplete attributes (1.3.5)*, and *minimum touch target size (2.5.8)*. Scans can reliably flag those (e.g. catch every missing `alt`, measure contrast, find no `<title>`, etc.). These often return a pass/fail that just needs human context-checking.

- **Partially Detectable Criteria** (scanners flag possible issues, but need human review). Typical examples: *missing or generic alt text* (1.1.1) – a tool can see no `alt` or vague "image" alt, but cannot know if `alt="photo"` is meaningful; *form input purpose (labels/instructions)* (1.3.1) – scanners catch missing `label` or `aria-label` but not whether the provided label is clear; *keyboard access (2.1.1)* – tools can check `tabindex` or event handlers, but cannot simulate a real user's tab sequence; *link purpose (2.4.4)* – tools flag "click here" or empty links, but can't ensure surrounding text makes it clear. In short, anything requiring understanding of **context, content quality, or user intent** falls here.

- **Not Detectable by Tools (must test manually)** include all cases needing subjective judgment. For example: proper **captioning of video** (1.2.2) – scans can't verify accuracy or sync; *audio descriptions* (1.2.5); *consistency of navigation or help across pages* (3.2.3, 3.2.6); *error suggestions* (3.3.3) and *helpful labels/instructions* (3.3.2) – tools cannot assess clarity of instructions; *focus order in dynamic content*; overall *readability* or *visual clarity* beyond contrast; or *multiple navigation mechanisms* (2.4.5) – it requires human testing. In other words, **all design, context, writing, and user-flow criteria** cannot be fully automated.

To summarize: tools reliably check technical, programmatic requirements (code structure, color math, missing attributes). They flag hints (like "no alt") but can't confirm semantic correctness. Anything about *user understanding, content accuracy, or dynamic behavior* must be tested manually (screen readers, keyboard walks, or user testing).

---

## Browser Automation Recipes for Accessibility

Modern headless browser APIs (Puppeteer, Playwright or raw CDP) let you script a lot of checks:

- **Keyboard Navigation**: Use `page.keyboard.press('Tab')` (and `Shift+Tab`) to simulate tabbing through the page. After each tab, inspect `document.activeElement` to verify the expected focus order or trapping. You can loop until focus returns to start to detect traps. Check for skip-links by finding `<a href="#...">` elements and programmatically clicking them, then verifying focus jumps to the main content. Also verify focused element has a visible outline (or compute style `:focus` outline) to ensure *focus visibility*.

- **Screen Reader Output**: Use the DevTools Accessibility API. In Puppeteer, you can call `const snapshot = await page.accessibility.snapshot();` which returns the AX tree of the page. You can then traverse `snapshot.children` to inspect names/roles. This helps validate ARIA roles/names (e.g. form labels, landmarks). Alternatively, use CDP directly:
  ```js
  const client = await page.target().createCDPSession();
  const { nodes } = await client.send('Accessibility.getFullAXTree');
  ```
  Inspecting the AX tree lets you see what a screen reader would announce (node.role and node.name) and catch missing names.

- **Color Contrast**: Compute styles on text elements and measure their contrast ratio. There are JS libraries (e.g. tinycolor2 or wcag-contrast) to calculate the 4.5:1 or 3:1 ratio. You can automate checking each text element. However, mind dynamic backgrounds or overlays – automation may miss complex cases.

- **Prefers-reduced-motion / Color-scheme**: Puppeteer and Playwright support `emulateMediaFeatures`. For example, to test dark mode and reduced motion:
  ```js
  await page.emulateMediaFeatures([
    { name: 'prefers-color-scheme', value: 'dark' },
    { name: 'prefers-reduced-motion', value: 'reduce' }
  ]);
  ```
  This ensures your page responds to those preferences.

- **Dynamic Focus Management**: For modals or SPAs, after triggering a modal/opening a view, assert that focus moves into the new content. Also test Tabbing inside the modal does not escape it. Conversely, on SPA route changes, ensure focus shifts to the new page's main heading.

- **ARIA Roles and Attributes**: Use the accessibility snapshot or DOM inspection to validate roles. You could also run axe in page context (via `axe.run()`) for full ARIA validation, or use CDP's AX tree to confirm every `role` node has a valid `name` property.

---

## WCAG 2.2 and Legal Context

**WCAG 2.2 vs 2.1:** WCAG 2.2 (W3C Rec Dec 2024) adds *9 new success criteria*. Key new AA-level requirements include:
- **2.4.11 Focus Not Obscured (Minimum)** (AA): Focusable elements must not be hidden behind fixed content.
- **2.5.7 Dragging Movements (AA)**: Functionality using dragging must have a non-drag alternative.
- **2.5.8 Target Size (Minimum)** (AA): Touch targets must be at least 24×24px.
- **3.3.8 Accessible Authentication (Minimum)** (AA): Authentication must avoid cognitive tests or provide alternatives.
Additional AAA criteria include enhanced focus appearance, consistent help, and redundant entry prevention.

**WCAG 3.0 Status:** As of March 2026, WCAG 3.0 is *not finalized*; it remains a Working Draft. The W3C expects it will be a major rewrite taking several years. Organizations should continue to align with WCAG 2.x for now, but track WCAG 3 developments.

**Common Violations (Top 10):** Real-world audits and studies show certain WCAG failures are extremely common:
- ~98% of pages fail color-contrast (1.4.3)
- ~80% had unclear link text (2.4.4)
- ~75% have missing image alt text (1.1.1)
- ~62% had unlabeled form controls (3.3.2)
- ~56% missing alt text (WebAIM Million 2025)
- ~48% missing form labels
- ~45% with empty (non-descriptive) links/buttons
- Missing page `<title>` (2.4.2), missing `lang` attribute (3.1.1), and missing focus indicators round out the top barriers.

**Legal Standards:** Many laws map to WCAG AA:
- U.S. *Section 508* (federal) currently cites WCAG 2.0 AA, and *ADA Title II* is moving to require WCAG 2.1 AA by 2026.
- The European Accessibility Act (EAA) requires compliance by June 28, 2025 with EN 301 549 (which references WCAG 2.1 AA).
- Industry guidance now treats **WCAG 2.2 as the current recommended standard**: published Oct 2023 and is being pushed as the compliance target for ADA, Section 508, EAA, etc.

---

## Optimal Accessibility Audit Workflow

A **robust audit** combines automated tooling and expert manual testing in sequence. Best practice is **manual evaluation first, then scans as QA**. Accessibility experts should perform a full manual audit (screen reader walkthrough, keyboard/navigation testing, code inspection, etc.) **covering all WCAG criteria**. Then use automated scans (axe, Pa11y, WAVE) as a *review layer* – to ensure no overlooked issues in code are missed. This order is crucial: **scans alone find only ~13% of issues**, so we cannot rely on them to set scope.

**Tool Order:** A common approach is:
1. **Run broad scans early** (axe CLI, Pa11y, Lighthouse) across the site to flag obvious low-hanging issues.
2. **Fix or mitigate critical issues**, then proceed to manual exploration.
3. **Manual testing** – keyboard navigation, screen-reader checks, mobile emulation, forms, ARIA, etc.
4. **Use scans again after manual auditing** to catch anything code-level missed.

**Combining Results:** Export all tools' results as JSON/CSV and merge into categories by WCAG criterion or page.

**Prioritizing Findings:** Assign **severity levels** (high/medium/low or P0/P1/P2) based on user impact and policy priority. A standard is to mark any Level A/AA failure that blocks core functionality or affects many users as **high priority**.

**Remediation Guidance:** For each issue, give clear, *actionable steps*: e.g. "Add meaningful `alt` text to `<img>` (WCAG 1.1.1)"; "Increase text/background contrast to ≥4.5:1 (WCAG 1.4.3)". Include example code or screenshots.

**Report Format:** A typical structure: **Issue → Impact (level) → WCAG ref → Code snippet or screenshot → Recommendation**. Reports are frequently delivered as PDF or HTML.

---

## Integration and CI/CD Patterns

- **Running axe-core in Node:** You can use *axe-core* programmatically with Puppeteer via axe-puppeteer:
  ```js
  const puppeteer = require('puppeteer');
  const { AxePuppeteer } = require('axe-puppeteer');
  (async() => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://example.com');
    const results = await new AxePuppeteer(page).analyze();
    console.log(results.violations);
    await browser.close();
  })();
  ```
  Alternatively, inject axe-core:
  ```js
  await page.addScriptTag({ path: require.resolve('axe-core') });
  const results = await page.evaluate(async () => {
    return await new Promise(res => axe.run(document, {}, (err, r) => res(r)));
  });
  ```

- **Exit Codes & CI:** Each tool has its own exit-code behavior:
  - **axe-core CLI:** Use `--exit` to make any failure return code 1. Otherwise it always exits 0 by default.
  - **Pa11y:** Exit code 2 if any issue of level>="error" (default), or below threshold. You can configure `--threshold` or `--level` to adjust this.
  - **Lighthouse:** Exits 0 unless there's a crash or a score threshold is manually checked.
  - **IBM Checker:** By default, `npx achecker` returns nonzero if any violations above configured level.

For CI/CD integration, it's common to fail the build on any critical accessibility errors. But because automated tools miss many issues, some teams only block on certain criteria (e.g. color contrast or missing alt) and log others for manual review.
