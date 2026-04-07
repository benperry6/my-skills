# Catalog Translation Mode

Use this mode when the user wants to translate locale message catalogs such as `fr.json` -> `en.json` without keeping a recurring prompt in notes.

This mode exists to make translation execution reusable, native-sounding, and verifiable.

## 1. Goal

The goal is not literal translation.

The goal is:

- a structurally identical target catalog
- that reads as if it were written natively for the target language community
- while preserving product meaning, variables, and runtime behavior

## 2. Default doctrine

Treat one locale catalog as the structural reference.

Reusable default:

- the reference locale must be structurally complete
- the target locale should stay iso-structured with the reference locale
- the target wording should sound native, not translated
- formulations, examples, references, and cultural codes may be adapted when that improves immediate comprehension
- placeholders, ICU plurals, interpolation variables, and key structure must remain valid

Do not:

- translate literally when the result sounds unnatural
- change business logic embedded in the intended meaning
- break placeholders, HTML/Markdown fragments, or ICU message syntax
- bury market or billing rules inside translation copy

## 3. Reusable translation instruction

When the user asks for catalog translation, use a reusable instruction equivalent to:

`Translate the source locale catalog into the target locale like a native speaker. Adapt references, formulations, and cultural codes so the result is natural and immediately understandable for the target language community. Do not translate literally. Preserve keys, placeholders, ICU syntax, and structural parity with the source catalog.`

Adapt the target-language community explicitly when relevant:

- anglophone
- german-speaking
- brazilian portuguese
- traditional chinese

## 4. Execution workflow

1. Identify the structurally complete source catalog.
2. Confirm the target catalog path and whether it already exists.
3. Translate key by key while preserving exact key structure.
4. Keep runtime tokens intact:
   - placeholders like `{name}`
   - ICU blocks
   - links, markup, HTML fragments, and escaped characters unless a localized variant is explicitly intended
5. Keep tone and positioning aligned with the product, not with the source language's sentence rhythm.
6. If the source contains culture-bound references that would feel foreign or confusing in the target locale, adapt them.
7. If the source contains business-specific entities that must remain unchanged, keep them unchanged.

## 5. Verification pass is mandatory

After translation, run a verification pass.

Minimum checks:

- missing keys in the target catalog
- extra keys in the target catalog
- placeholder parity
- ICU/message syntax parity
- obvious broken escaping or markup
- hardcoded user-facing strings outside the message system

The hardcoded-string audit should inspect likely leak zones such as:

- components and pages
- onboarding flows
- legal pages
- emails
- shared/public pages
- support/chatbot/help surfaces
- API error messages

## 6. Expected outcome

A successful run of this mode produces:

- a native-sounding target locale catalog
- structural parity with the reference locale
- a short audit result listing any remaining hardcoded user-facing strings outside the catalog system
- a clear distinction between:
  - translation complete
  - locale declared but not fully production-ready

## 7. Lost N Found-derived rule worth reusing

When a project uses one core source catalog as the canonical reference, keep that pattern explicit.

Example reusable pattern:

- `fr.json` is the structurally complete reference catalog
- `en.json` is translated as natural anglophone copy, not as a literal mirror
- the codebase is audited afterward so untranslated hardcoded strings do not survive outside `messages/`
