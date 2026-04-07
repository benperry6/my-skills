# CLI Tools Reference

## axe-core CLI (v4.11.x)

### Installation
```bash
npm install -g @axe-core/cli
# Requires Chrome + WebDriver
# Install browser-driver-manager if needed:
npm install -g browser-driver-manager
npx browser-driver-manager install chrome
```

### Full Command Reference
```bash
# Basic scan
axe https://example.com

# JSON output to stdout
axe https://example.com --stdout

# Save to file
axe https://example.com --save results.json

# Fail on violations (for CI)
axe https://example.com --exit

# Multiple pages
axe https://example.com https://example.com/about https://example.com/contact --stdout

# Scope to specific DOM area
axe https://example.com --include "main" --exclude ".cookie-banner,.chat-widget"

# WCAG 2.2 AA only
axe https://example.com --tags wcag2aa,wcag22aa --stdout

# Specific rules only
axe https://example.com --rules color-contrast,image-alt,label

# Disable specific rules
axe https://example.com --disable color-contrast

# With timeout (ms)
axe https://example.com --timeout 60000
```

### JSON Output Structure
```json
{
  "violations": [
    {
      "id": "color-contrast",
      "impact": "serious",
      "description": "Ensures contrast ratio is sufficient",
      "help": "Elements must have sufficient color contrast",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.11/color-contrast",
      "tags": ["wcag2aa", "wcag143"],
      "nodes": [
        {
          "html": "<p class='muted'>Some text</p>",
          "target": [".muted"],
          "failureSummary": "Fix any of the following: ..."
        }
      ]
    }
  ],
  "passes": [...],
  "incomplete": [...],
  "inapplicable": [...]
}
```

### What axe Catches vs Misses
**Catches:** Missing alt, contrast failures, form labels, ARIA misuse, empty buttons/links, missing lang, missing title, duplicate IDs, missing landmarks
**Misses:** Meaningful alt text quality, reading order, cognitive clarity, focus order logic, content equivalence, video captions accuracy

---

## Pa11y (v9.1.x)

### Installation
```bash
npm install -g pa11y
```

### Full Command Reference
```bash
# Basic scan (HTML_CodeSniffer runner)
pa11y https://example.com

# Use axe runner (recommended for broader coverage)
pa11y https://example.com --runner axe

# Use both runners
pa11y https://example.com --runner htmlcs --runner axe

# JSON output
pa11y https://example.com --reporter json > results.json

# Other formats
pa11y https://example.com --reporter csv
pa11y https://example.com --reporter html

# Set standard
pa11y https://example.com --standard WCAG2AA

# Set level (error, warning, notice)
pa11y https://example.com --level error

# Set failure threshold
pa11y https://example.com --threshold 5  # allow up to 5 issues

# Ignore specific codes
pa11y https://example.com --ignore "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail"

# Wait for page load (ms)
pa11y https://example.com --wait 2000

# With actions (login, click, etc.)
# Use a config file for complex scenarios
```

### Pa11y Config File (.pa11yci)
```json
{
  "defaults": {
    "runner": ["axe", "htmlcs"],
    "standard": "WCAG2AA",
    "level": "error",
    "reporter": "json",
    "wait": 1000
  },
  "urls": [
    "https://example.com",
    "https://example.com/about",
    {
      "url": "https://example.com/dashboard",
      "actions": [
        "set field #email to user@test.com",
        "set field #password to testpass",
        "click element #login-btn",
        "wait for url to be https://example.com/dashboard"
      ]
    }
  ]
}
```

Run with: `pa11y-ci`

### Exit Codes
- `0` — no issues
- `1` — Pa11y error (not a11y issue)
- `2` — accessibility issues found above threshold

---

## Lighthouse (v10+)

### Installation
```bash
npm install -g lighthouse
```

### Full Command Reference
```bash
# Accessibility only, JSON output
lighthouse https://example.com \
  --only-categories=accessibility \
  --output=json \
  --output-path=results.json \
  --chrome-flags="--headless=new"

# Multiple output formats
lighthouse https://example.com \
  --only-categories=accessibility \
  --output=json,html \
  --output-path=./report

# Custom viewport
lighthouse https://example.com \
  --only-categories=accessibility \
  --screenEmulation.width=375 \
  --screenEmulation.height=667 \
  --output=json

# With throttling disabled (faster)
lighthouse https://example.com \
  --only-categories=accessibility \
  --throttling-method=provided \
  --output=json
```

### Score Interpretation
The accessibility score (0-100) is a weighted average:
- High-weight audits: `image-alt` (10pts), `label` (7pts), `button-name` (7pts)
- Lower-weight: `html-has-lang` (3pts), `document-title` (3pts)
- "Manual" audits don't affect score (focus-order, logical-tab-order, etc.)

**Score thresholds:**
- 100: All automated checks pass
- 90-99: Minor issues
- 70-89: Significant issues
- <70: Critical accessibility problems

### Parsing Lighthouse JSON
Key paths in the JSON:
```
categories.accessibility.score          → 0.0 to 1.0
categories.accessibility.auditRefs      → list of audit IDs and weights
audits["image-alt"].score               → 0 or 1
audits["image-alt"].details.items       → failing elements
audits["color-contrast"].details.items  → failing elements with ratios
```

---

## IBM Equal Access Checker (v4.x)

### Installation
```bash
npm install accessibility-checker
```

### Usage
```bash
# Create a file with URLs to scan
echo "https://example.com" > urls.txt
echo "https://example.com/about" >> urls.txt

# Run scan
npx achecker urls.txt

# Output formats: json, csv, html
npx achecker urls.txt --outputFormat json
```

### Integration with Node.js
```javascript
const { getCompliance } = require('accessibility-checker');

async function audit(url) {
  const result = await getCompliance(url, 'audit-label');
  const { report } = result;
  console.log('Violations:', report.results.filter(r => r.level === 'violation'));
  console.log('Needs review:', report.results.filter(r => r.level === 'potentialviolation'));
}
```
