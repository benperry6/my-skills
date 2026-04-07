# Locale Decision Tree

Use this when implementing or auditing locale behavior.

## A. Determine `current locale`

1. Does the URL explicitly contain a supported locale?
   - Yes: use it as `current locale`
   - No: continue

2. Is there an authenticated manual preference?
   - Yes: use it
   - No: continue

3. Is there an authenticated auto-detected preference?
   - Yes: use it
   - No: continue

4. Is there an explicit guest preference?
   - Yes: use it
   - No: continue

5. Is there a supported browser/app language?
   - Yes: use it
   - No: continue

6. Fall back to the default locale.

Important:

- if the URL already contains a locale, do not silently replace it with a cookie or browser signal

## B. Determine `preferred locale`

For authenticated users:

1. manual preference
2. auto-detected preference
3. default locale

For anonymous users:

1. explicit guest preference
2. browser/app language
3. default locale

Important:

- a technical navigation cookie does not automatically count as explicit preference

## C. Show the mismatch banner?

Show the banner only if all are true:

1. `preferred locale` is known
2. `preferred locale !== current locale`
3. the current locale pair is not dismissed for the current session
4. the banner can be rendered safely

Recommended locale-pair key:

- `preferredLocale -> currentLocale`
- example: `it -> fr`

## C2. Default reusable banner pattern

Unless the project already validated a different pattern, reuse this default:

### Title

- `Switch to {preferredLanguageName}?`

### Subtitle

Use two short sentences:

- sentence 1 = current page language
- sentence 2 = preferred-language signal

Reusable defaults:

- browser: `This page is in {currentLanguageName}. Your browser prefers {preferredLanguageName}.`
- account: `This page is in {currentLanguageName}. Your account is set to {preferredLanguageName}.`
- guest cookie: `This page is in {currentLanguageName}. You usually browse in {preferredLanguageName}.`
- fallback: `This page is in {currentLanguageName}. Also available in {preferredLanguageName}.`

Important:

- localize both language names into the banner's own display language
- keep the wording short and direct
- do not put storage semantics inside the main CTA labels

### CTA hierarchy

- primary filled CTA: `Switch to {preferredLanguageName}`
- secondary ghost CTA: `Stay in {currentLanguageName}`
- independent close/X button

If `Stay in {currentLanguageName}` creates a durable preference, it should still look like a real button, not a plain text link.

### Layout defaults

- close button at top-right
- text above actions on mobile
- actions stacked vertically on mobile
- desktop may use a horizontal action row
- use visual language markers such as flags sparingly; default to CTA-only if needed

## D. What each user action means

### `Switch to {preferredLanguage}`

- interpret as: "I want to use the preferred language"
- persist as durable preference:
  - authenticated: profile
  - anonymous: explicit preference cookie
- navigate to the equivalent localized URL

### `Stay in {currentLanguage}`

- interpret as: "I want to use the current language"
- persist as durable preference:
  - authenticated: profile
  - anonymous: explicit preference cookie
- do not navigate away

### `Close`

- interpret as: "Not now"
- do not change durable preference
- dismiss for current session only
- scope dismiss by locale pair

## E. Preserve user context on switch

When switching locale, preserve:

- equivalent route/path
- query string
- hash/fragment
- any deliberate tracking or state parameters the product wants to retain

Do not send the user back to the homepage unless there is no valid localized equivalent.
