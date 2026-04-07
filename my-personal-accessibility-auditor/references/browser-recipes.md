# Browser Automation Recipes for Accessibility Testing

These recipes use Claude Code's browser automation (claude-in-chrome) or can be run via Puppeteer/Playwright.

---

## Keyboard Navigation Testing

### Tab Order Verification
```javascript
// Simulate tabbing through the page and record focus order
async function testTabOrder(page) {
  await page.keyboard.press('Tab');
  const focusOrder = [];
  let prevElement = '';

  for (let i = 0; i < 100; i++) {
    const focused = await page.evaluate(() => {
      const el = document.activeElement;
      return {
        tag: el.tagName,
        id: el.id,
        text: el.textContent?.slice(0, 50),
        role: el.getAttribute('role'),
        ariaLabel: el.getAttribute('aria-label'),
        tabIndex: el.tabIndex,
        visible: el.offsetWidth > 0 && el.offsetHeight > 0
      };
    });

    const key = `${focused.tag}#${focused.id}`;
    if (key === prevElement) break; // Looped back to start

    focusOrder.push(focused);
    prevElement = key;
    await page.keyboard.press('Tab');
  }

  return focusOrder;
}
```

### Focus Visibility Check
```javascript
// Check if focused element has visible focus indicator
async function checkFocusVisibility(page) {
  await page.keyboard.press('Tab');

  const hasVisibleFocus = await page.evaluate(() => {
    const el = document.activeElement;
    const style = getComputedStyle(el);
    const outline = style.outline;
    const boxShadow = style.boxShadow;
    const border = style.border;

    // Check for visible focus indicator
    const hasOutline = outline !== 'none' && outline !== '0px none';
    const hasBoxShadow = boxShadow !== 'none';
    const hasBorderChange = border !== 'none'; // simplified

    return {
      element: el.tagName + (el.id ? '#' + el.id : ''),
      outline,
      boxShadow,
      hasVisibleFocus: hasOutline || hasBoxShadow
    };
  });

  return hasVisibleFocus;
}
```

### Skip Link Test
```javascript
// Verify skip link exists and works
async function testSkipLink(page) {
  // Tab once — skip link should be first focusable element
  await page.keyboard.press('Tab');

  const skipLink = await page.evaluate(() => {
    const el = document.activeElement;
    const href = el.getAttribute('href');
    const text = el.textContent?.toLowerCase();

    return {
      exists: text?.includes('skip') || text?.includes('main content'),
      href,
      text: el.textContent,
      tag: el.tagName
    };
  });

  if (skipLink.exists && skipLink.href) {
    // Activate skip link
    await page.keyboard.press('Enter');

    // Check if focus moved to main content
    const afterSkip = await page.evaluate(() => {
      const el = document.activeElement;
      return {
        tag: el.tagName,
        id: el.id,
        role: el.getAttribute('role'),
        isMain: el.tagName === 'MAIN' || el.getAttribute('role') === 'main'
      };
    });

    return { skipLink, afterSkip };
  }

  return { skipLink, error: 'No skip link found' };
}
```

### Focus Trap Detection (Modals)
```javascript
// Test that modal traps focus and Escape releases it
async function testModalFocusTrap(page, modalTriggerSelector) {
  // Open modal
  await page.click(modalTriggerSelector);
  await page.waitForTimeout(500);

  // Check focus moved into modal
  const focusInModal = await page.evaluate(() => {
    const el = document.activeElement;
    const modal = el.closest('[role="dialog"], [aria-modal="true"], .modal');
    return { inModal: !!modal, element: el.tagName + '#' + el.id };
  });

  // Tab through modal — should stay inside
  const focusedElements = [];
  for (let i = 0; i < 20; i++) {
    await page.keyboard.press('Tab');
    const el = await page.evaluate(() => {
      const el = document.activeElement;
      const modal = el.closest('[role="dialog"], [aria-modal="true"], .modal');
      return { inModal: !!modal, id: el.id, tag: el.tagName };
    });
    focusedElements.push(el);
  }

  const escapedModal = focusedElements.some(e => !e.inModal);

  // Test Escape closes modal
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  const afterEscape = await page.evaluate(() => ({
    modalStillOpen: !!document.querySelector('[role="dialog"]:not([hidden]), [aria-modal="true"]:not([hidden])'),
    focusReturned: document.activeElement.id
  }));

  return { focusInModal, escapedModal, afterEscape };
}
```

---

## Screen Reader Simulation

### Accessibility Tree Inspection
```javascript
// Get the full accessibility tree (Puppeteer)
async function getAccessibilityTree(page) {
  const snapshot = await page.accessibility.snapshot();
  return snapshot;
}

// Find elements with missing accessible names
function findMissingNames(node, path = '') {
  const issues = [];
  const currentPath = path + '/' + (node.role || 'unknown');

  // Interactive elements that MUST have names
  const needsName = ['button', 'link', 'textbox', 'combobox',
                      'checkbox', 'radio', 'slider', 'tab'];

  if (needsName.includes(node.role) && !node.name) {
    issues.push({
      role: node.role,
      path: currentPath,
      issue: `${node.role} has no accessible name`
    });
  }

  // Images that need alt
  if (node.role === 'img' && !node.name) {
    issues.push({
      role: 'img',
      path: currentPath,
      issue: 'Image has no alt text'
    });
  }

  if (node.children) {
    for (const child of node.children) {
      issues.push(...findMissingNames(child, currentPath));
    }
  }

  return issues;
}
```

### Heading Hierarchy Check
```javascript
// Verify heading levels are hierarchical (no skipped levels)
async function checkHeadingHierarchy(page) {
  const headings = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
      level: parseInt(h.tagName[1]),
      text: h.textContent.trim().slice(0, 80),
      visible: h.offsetWidth > 0 && h.offsetHeight > 0
    }));
  });

  const issues = [];

  // Check for missing h1
  if (!headings.some(h => h.level === 1)) {
    issues.push('No h1 found on page');
  }

  // Check for multiple h1s
  const h1Count = headings.filter(h => h.level === 1).length;
  if (h1Count > 1) {
    issues.push(`Multiple h1 elements found (${h1Count})`);
  }

  // Check for skipped levels
  for (let i = 1; i < headings.length; i++) {
    const prev = headings[i - 1].level;
    const curr = headings[i].level;
    if (curr > prev + 1) {
      issues.push(`Skipped heading level: h${prev} → h${curr} ("${headings[i].text}")`);
    }
  }

  return { headings, issues };
}
```

### Landmark Regions Check
```javascript
// Verify ARIA landmarks exist
async function checkLandmarks(page) {
  const landmarks = await page.evaluate(() => {
    const required = {
      main: document.querySelector('main, [role="main"]'),
      navigation: document.querySelector('nav, [role="navigation"]'),
      banner: document.querySelector('header, [role="banner"]'),
      contentinfo: document.querySelector('footer, [role="contentinfo"]')
    };

    return Object.entries(required).map(([name, el]) => ({
      landmark: name,
      found: !!el,
      element: el ? el.tagName : null,
      ariaLabel: el?.getAttribute('aria-label') || null
    }));
  });

  const missing = landmarks.filter(l => !l.found);
  return { landmarks, missing };
}
```

---

## Color Contrast Testing

### Programmatic Contrast Check
```javascript
// Check contrast ratio of text elements
async function checkContrast(page) {
  const results = await page.evaluate(() => {
    function luminance(r, g, b) {
      const [rs, gs, bs] = [r, g, b].map(c => {
        c = c / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }

    function contrastRatio(l1, l2) {
      const lighter = Math.max(l1, l2);
      const darker = Math.min(l1, l2);
      return (lighter + 0.05) / (darker + 0.05);
    }

    function parseColor(str) {
      const match = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      if (!match) return null;
      return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
    }

    const textElements = document.querySelectorAll('p, span, a, button, label, h1, h2, h3, h4, h5, h6, li, td, th');
    const failures = [];

    textElements.forEach(el => {
      if (el.offsetWidth === 0 || el.offsetHeight === 0) return;

      const style = getComputedStyle(el);
      const fg = parseColor(style.color);
      const bg = parseColor(style.backgroundColor);

      if (!fg || !bg) return;
      if (bg[0] === 0 && bg[1] === 0 && bg[2] === 0 && style.backgroundColor.includes('0)')) return; // transparent

      const fgLum = luminance(...fg);
      const bgLum = luminance(...bg);
      const ratio = contrastRatio(fgLum, bgLum);

      const fontSize = parseFloat(style.fontSize);
      const isBold = parseInt(style.fontWeight) >= 700;
      const isLargeText = fontSize >= 24 || (fontSize >= 18.66 && isBold);
      const required = isLargeText ? 3.0 : 4.5;

      if (ratio < required) {
        failures.push({
          text: el.textContent.trim().slice(0, 50),
          selector: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
          ratio: Math.round(ratio * 100) / 100,
          required,
          fg: style.color,
          bg: style.backgroundColor,
          fontSize: `${fontSize}px`,
          isBold
        });
      }
    });

    return failures;
  });

  return results;
}
```

---

## Media Feature Emulation

### Test Reduced Motion and Dark Mode
```javascript
// Test prefers-reduced-motion
await page.emulateMediaFeatures([
  { name: 'prefers-reduced-motion', value: 'reduce' }
]);

// Verify animations are disabled
const animationsDisabled = await page.evaluate(() => {
  const elements = document.querySelectorAll('*');
  const animated = [];
  elements.forEach(el => {
    const style = getComputedStyle(el);
    if (style.animationName !== 'none' || style.transitionDuration !== '0s') {
      animated.push({
        element: el.tagName + '#' + el.id,
        animation: style.animationName,
        transition: style.transitionDuration
      });
    }
  });
  return animated;
});

// Test prefers-color-scheme: dark
await page.emulateMediaFeatures([
  { name: 'prefers-color-scheme', value: 'dark' }
]);
// Then run contrast check again to verify dark mode contrast
```

---

## ARIA Validation

### Check for Common ARIA Mistakes
```javascript
async function validateARIA(page) {
  return await page.evaluate(() => {
    const issues = [];

    // 1. Interactive elements with redundant roles
    document.querySelectorAll('button[role="button"], a[role="link"]').forEach(el => {
      issues.push({
        type: 'redundant-role',
        element: el.outerHTML.slice(0, 100),
        fix: `Remove role="${el.getAttribute('role')}" — native element already has this role`
      });
    });

    // 2. aria-hidden on focusable elements
    document.querySelectorAll('[aria-hidden="true"] a, [aria-hidden="true"] button, [aria-hidden="true"] input').forEach(el => {
      if (el.tabIndex >= 0) {
        issues.push({
          type: 'hidden-focusable',
          element: el.outerHTML.slice(0, 100),
          fix: 'Focusable element inside aria-hidden container — add tabindex="-1" or remove aria-hidden'
        });
      }
    });

    // 3. Missing aria-label on icon buttons
    document.querySelectorAll('button').forEach(el => {
      if (!el.textContent.trim() && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')) {
        issues.push({
          type: 'empty-button',
          element: el.outerHTML.slice(0, 100),
          fix: 'Add aria-label="[description]" to button with no text content'
        });
      }
    });

    // 4. aria-expanded without toggling
    document.querySelectorAll('[aria-expanded]').forEach(el => {
      const controls = el.getAttribute('aria-controls');
      if (controls && !document.getElementById(controls)) {
        issues.push({
          type: 'broken-aria-controls',
          element: el.outerHTML.slice(0, 100),
          fix: `aria-controls references "${controls}" which doesn't exist in the DOM`
        });
      }
    });

    return issues;
  });
}
```
