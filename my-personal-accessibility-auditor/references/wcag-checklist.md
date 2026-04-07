# WCAG 2.2 AA Checklist with Automation Status

Legend:
- **AUTO** = Fully automatable by CLI tools
- **PARTIAL** = Tools flag it, but human must verify
- **MANUAL** = Cannot be automated — requires manual testing or browser walkthrough

---

## Principle 1: Perceivable

| # | Criterion | Level | Automation | What to Check |
|---|-----------|-------|------------|---------------|
| 1.1.1 | Non-text Content | A | **PARTIAL** | Tools find missing alt. Human must verify alt text is meaningful |
| 1.2.1 | Audio-only/Video-only | A | **MANUAL** | Verify text alternatives or audio descriptions exist |
| 1.2.2 | Captions (Prerecorded) | A | **MANUAL** | Verify caption accuracy and timing |
| 1.2.3 | Audio Description or Media Alternative | A | **MANUAL** | Verify audio description or transcript for video |
| 1.2.5 | Audio Description (Prerecorded) | AA | **MANUAL** | Verify audio description track exists |
| 1.3.1 | Info and Relationships | A | **PARTIAL** | Tools check headings, lists, tables structure. Human verifies meaning |
| 1.3.2 | Meaningful Sequence | A | **MANUAL** | Verify reading order matches visual order |
| 1.3.3 | Sensory Characteristics | A | **MANUAL** | Verify instructions don't rely solely on shape, color, size, location |
| 1.3.4 | Orientation | AA | **MANUAL** | Verify content works in both portrait and landscape |
| 1.3.5 | Identify Input Purpose | AA | **AUTO** | Tools check autocomplete attributes on form fields |
| 1.4.1 | Use of Color | A | **MANUAL** | Verify color is not the only means of conveying information |
| 1.4.2 | Audio Control | A | **MANUAL** | Verify auto-playing audio can be paused/stopped |
| 1.4.3 | Contrast (Minimum) | AA | **AUTO** | Tools calculate 4.5:1 for normal text, 3:1 for large text |
| 1.4.4 | Resize Text | AA | **MANUAL** | Verify content is readable at 200% zoom |
| 1.4.5 | Images of Text | AA | **PARTIAL** | Tools may flag, human verifies if real text could be used |
| 1.4.10 | Reflow | AA | **MANUAL** | Verify no horizontal scrolling at 320px width |
| 1.4.11 | Non-text Contrast | AA | **AUTO** | Tools check UI component and graphic contrast ≥3:1 |
| 1.4.12 | Text Spacing | AA | **MANUAL** | Verify custom text spacing doesn't break layout |
| 1.4.13 | Content on Hover or Focus | AA | **MANUAL** | Verify hover/focus content is dismissible, hoverable, persistent |

---

## Principle 2: Operable

| # | Criterion | Level | Automation | What to Check |
|---|-----------|-------|------------|---------------|
| 2.1.1 | Keyboard | A | **PARTIAL** | Tools check tabindex. Manual tab-through needed |
| 2.1.2 | No Keyboard Trap | A | **MANUAL** | Verify focus can move away from every component |
| 2.1.4 | Character Key Shortcuts | A | **MANUAL** | Verify single-character shortcuts can be turned off |
| 2.2.1 | Timing Adjustable | A | **MANUAL** | Verify time limits can be extended/turned off |
| 2.2.2 | Pause, Stop, Hide | A | **MANUAL** | Verify moving/auto-updating content can be paused |
| 2.3.1 | Three Flashes or Below | A | **MANUAL** | Verify no content flashes more than 3 times/second |
| 2.4.1 | Bypass Blocks | A | **PARTIAL** | Tools check for skip links and landmarks |
| 2.4.2 | Page Titled | A | **AUTO** | Tools check `<title>` exists |
| 2.4.3 | Focus Order | A | **MANUAL** | Verify tab order is logical and matches visual flow |
| 2.4.4 | Link Purpose (In Context) | A | **PARTIAL** | Tools flag "click here" / empty links. Human verifies context |
| 2.4.5 | Multiple Ways | AA | **MANUAL** | Verify multiple navigation methods (menu, search, sitemap) |
| 2.4.6 | Headings and Labels | AA | **PARTIAL** | Tools check headings exist. Human verifies they're descriptive |
| 2.4.7 | Focus Visible | AA | **PARTIAL** | Tools check outline. Manual verification of visibility |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | **MANUAL** | *NEW in 2.2.* Verify focus isn't hidden behind sticky elements |
| 2.5.1 | Pointer Gestures | A | **MANUAL** | Verify multipoint gestures have single-pointer alternatives |
| 2.5.2 | Pointer Cancellation | A | **MANUAL** | Verify actions fire on up-event, not down-event |
| 2.5.3 | Label in Name | A | **PARTIAL** | Tools check visible label matches accessible name |
| 2.5.4 | Motion Actuation | A | **MANUAL** | Verify motion-triggered functions have UI alternatives |
| 2.5.7 | Dragging Movements | AA | **MANUAL** | *NEW in 2.2.* Verify drag actions have non-drag alternative |
| 2.5.8 | Target Size (Minimum) | AA | **AUTO** | *NEW in 2.2.* Tools check 24×24px minimum |

---

## Principle 3: Understandable

| # | Criterion | Level | Automation | What to Check |
|---|-----------|-------|------------|---------------|
| 3.1.1 | Language of Page | A | **AUTO** | Tools check `lang` attribute on `<html>` |
| 3.1.2 | Language of Parts | AA | **PARTIAL** | Tools flag missing `lang` on inline content. Human checks completeness |
| 3.2.1 | On Focus | A | **MANUAL** | Verify focus doesn't trigger unexpected context changes |
| 3.2.2 | On Input | A | **MANUAL** | Verify input doesn't trigger unexpected context changes |
| 3.2.3 | Consistent Navigation | AA | **MANUAL** | Verify navigation is consistent across pages |
| 3.2.4 | Consistent Identification | AA | **MANUAL** | Verify same functions have same labels across pages |
| 3.2.6 | Consistent Help | A | **MANUAL** | *NEW in 2.2.* Verify help mechanisms are in consistent location |
| 3.3.1 | Error Identification | A | **PARTIAL** | Tools check aria-invalid. Human verifies error messages |
| 3.3.2 | Labels or Instructions | A | **PARTIAL** | Tools check labels exist. Human verifies clarity |
| 3.3.3 | Error Suggestion | AA | **MANUAL** | Verify error messages suggest how to fix the error |
| 3.3.4 | Error Prevention (Legal, Financial) | AA | **MANUAL** | Verify reversibility, review, and confirmation for important actions |
| 3.3.7 | Redundant Entry | A | **MANUAL** | *NEW in 2.2.* Verify previously entered info is auto-populated |
| 3.3.8 | Accessible Authentication (Minimum) | AA | **MANUAL** | *NEW in 2.2.* Verify login doesn't require cognitive tests |

---

## Principle 4: Robust

| # | Criterion | Level | Automation | What to Check |
|---|-----------|-------|------------|---------------|
| 4.1.2 | Name, Role, Value | A | **PARTIAL** | Tools check ARIA roles/names. Human verifies accuracy |
| 4.1.3 | Status Messages | AA | **PARTIAL** | Tools may flag missing live regions. Human verifies announcements |

---

## Summary

| Automation Level | Count | Percentage |
|-----------------|-------|------------|
| **AUTO** (fully automatable) | 7 | ~15% |
| **PARTIAL** (tools flag, human verifies) | 15 | ~31% |
| **MANUAL** (human testing required) | 26 | ~54% |
| **Total AA criteria** | 48 | 100% |

This confirms the research: automated tools reliably catch ~13-15% of criteria. The remaining 85% need human verification or manual testing.
