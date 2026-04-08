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

## F. Explicit locale selector doctrine

Use the selector as the durable, intentional language-control surface.

### F1. What the selector should show

Recommended default:

- current locale in the closed trigger
- native language names in the selector list
- optional flag or language marker when it materially improves scanning
- optional currency or market label when locale and market are materially linked in the product

Reusable default pattern:

- trigger: `flag + native language name + currency/market label when relevant`
- menu row: `flag + native language name`, with secondary `currency/market label` when relevant

### F2. How the selector should order options

Default rule:

- order options from one central locale registry
- prefer business-priority or acquisition-priority ordering over blind alphabetical ordering when the product has a real rollout strategy

For search-led products, ordering by the prioritized search-market opportunity list is a valid default.

### F3. What a selector click means

An explicit selector click means:

- "set my language preference to this locale"

Persist it durably:

- authenticated: profile/manual preference
- anonymous: explicit guest preference storage

Do not treat explicit selector usage as session-only behavior.

### F4. What navigation should do after a selector click

After a selector click:

- navigate to the equivalent localized route
- preserve path
- preserve query string
- preserve hash
- preserve any deliberate tracking/state parameters the product wants to keep

Only fall back to the homepage if there is no valid localized equivalent.
