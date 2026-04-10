# Catalog Translation Mode

Use this mode when the user wants to translate locale message catalogs such as `fr.json` -> `en.json` without keeping a recurring prompt in notes.

This mode exists to make translation execution reusable, native-sounding, and verifiable.

Treat this as one end-to-end workflow:

- translation
- independent evaluation
- correction
- re-evaluation until acceptance

## 1. Goal

The goal is not literal translation.

The goal is:

- a structurally identical target catalog
- that reads as if it were written natively for the target language community
- while preserving product meaning, variables, and runtime behavior

Important production lesson:

- deterministic scripts are allowed for scaffolding, parsing, verification, and audit only
- translation services, translation APIs, browser translation, or scripts that translate text are not allowed as the source of the translated copy unless the user explicitly authorizes that lower-quality trade-off
- the model/agent doing the target locale must produce the language itself and adapt references, formulations, examples, and cultural codes for that target community

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
- outsource translation quality to a programmatic translator when the user requested AI-native/culturally adapted copy
- change business logic embedded in the intended meaning
- break placeholders, HTML/Markdown fragments, or ICU message syntax
- bury market or billing rules inside translation copy

## 3. Reusable translation instruction

When the user asks for catalog translation, use a reusable instruction equivalent to:

`Translate the source locale catalog into the target locale like a native speaker. Adapt references, formulations, and cultural codes so the result is natural and immediately understandable for the target language community. Do not translate literally. Preserve keys, placeholders, ICU syntax, and structural parity with the source catalog.`

Also include, unless the user has explicitly authorized machine translation:

`Do not call translation APIs, browser translation, or programmatic translation scripts to produce the copy. You may use scripts only to scaffold JSON, compare keys, validate placeholders/ICU/markup, and audit the finished file.`

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

## 5. Orchestration at scale

For one or two target locales, a single execution pass can be enough.

For many target locales, do not run one giant sequential session and do not launch every locale in parallel at once.

For very large catalogs, do not default to one whole-file translation agent per locale.
If a locale file is long enough to force heavy context loading or long silent execution windows, prefer stable section-level handoffs instead.

Do not assume the theoretically ideal wave size is safe in the current tool environment. Calibrate it from the previous wave's observed behavior:

- if a pilot wave of 3 to 4 locales completed with files on disk and local verification, reuse 4 as the next wave size
- if a wave times out twice, returns no files, or hits agent/thread limits, stop and reduce the wave size or change the handoff strategy before launching more agents
- if an agent is closed or cannot be messaged, do not keep routing work to it; start a fresh, narrowly scoped correction agent or re-plan
- if a whole-file translator stalls for about 10 minutes with no completion and no observable local progress, treat it as blocked instead of "probably still finishing"
- when re-launching a blocked locale, replace the contaminated or half-trusted target file with a fresh scaffold from the canonical source before resuming section-level translation work
- do not count a subagent as complete until the orchestrator verifies the target file exists locally and passes the structural checks

Reusable orchestration:

1. One orchestrator agent defines:
   - the source-of-truth catalog
   - protected invariants
   - glossary and naming rules
   - verification rules
   - the exact wave size and timeout/stop rule for the current environment
2. Run a pilot batch on 3 to 4 representative locales.
   - use one translator subagent per locale
3. Review the pilot results.
4. Adjust the translation brief if needed.
5. Scale through small parallel batches of about 4 to 6 locales per wave.
   - in each wave, launch one translator subagent per locale
   - do not assign multiple locales to the same translator subagent
   - keep model/reasoning settings inherited from the parent conversation unless the user explicitly authorizes overrides
6. After each translation wave, launch one independent evaluator subagent per locale in that wave.
   - do not assign multiple locales to the same evaluator subagent
   - do not let a locale be evaluated by the same agent/session that generated it
7. If an evaluator finds issues, route that locale into a separate correction loop.
   - the evaluator reports findings
   - the orchestrator decides whether the locale passes or needs correction
   - a translator or dedicated fixer subagent corrects the locale
   - every corrected locale is re-evaluated
   - the evaluator does not fix the locale it reviewed
8. Run one final global verification pass across all produced catalogs and the codebase.

For very large catalogs or unstable agent environments, use a section-first pattern:

1. scaffold the target file from the canonical source catalog
2. assign one locale file to one translator agent at a time
3. ask that agent to translate only an explicit list of top-level sections
4. verify the file locally after each section batch
5. continue with a fresh agent or the same agent only if the current run is clearly healthy

Good section boundaries are usually top-level keys such as:

- `common`, `nav`, `hero`, `pricing`
- `auth`, `upload`, `onboarding`
- `dashboard`, `settings`, `addCard`
- `api`, `email`, `metadata`, `legal`
- `admin`, `promotion`, `chatbot`

Operational acceptance rule for each wave:

- subagent final messages are useful evidence, not acceptance
- acceptance requires local file presence plus local verification output recorded by the orchestrator
- if a verifier reports many mismatches, inspect representative keys directly before concluding the catalog is bad; the verifier may be wrong around hybrid ICU/plural-suffix patterns
- if direct inspection proves a verifier false positive, improve the verifier or document the adjudication before scaling the next wave

Why this pattern:

- long single-agent translation runs drift in tone and rigor as context grows
- all-at-once parallelism makes inconsistencies harder to catch and fix
- a pilot batch lets the system fail small before it fails wide

## 6. Independent evaluation is mandatory

Do not let the same agent or same session both generate and quality-check the translated catalogs.

For qualitative review, use an independent evaluator agent.

Preferred order:

1. a different engine
2. otherwise a different agent/session with a clean slate

The evaluator should review:

- naturalness and immediacy for the target language community
- cultural adaptation quality
- tone consistency with the product
- obvious awkward literal translation artifacts
- structural integrity when needed

Execution rule:

- one evaluator subagent reviews one locale at a time
- evaluators may run in parallel across a wave
- do not batch many locales into one evaluator if the goal is precise language-by-language judgment
- evaluators report findings; they do not directly edit the locale they reviewed

Independent delegation is required.

If the environment cannot provide one translator subagent and one separate evaluator subagent, or an equivalent separation across engines or clean sessions, stop and notify the user instead of pretending the same agent can independently validate its own translation.

This separation exists because long-running generators tend to become lenient about their own output.
Use generator/evaluator separation as a reusable harness rule, not as an ad hoc preference.

## 7. Correction loop is separate

If evaluation finds problems, do not let the evaluator become the fixer for that same locale.

Reusable loop:

1. evaluator produces findings
2. orchestrator triages them
3. translator/fixer agent applies corrections
4. locale returns to evaluation after every correction
5. the loop repeats until the locale is explicitly accepted

This preserves the harness separation:

- translator/fixer generates
- evaluator evaluates
- orchestrator routes

## 8. Verification pass is mandatory

After translation, run a verification pass.

Minimum checks:

- missing keys in the target catalog
- extra keys in the target catalog
- placeholder parity
- ICU/message syntax parity
- obvious broken escaping or markup
- hardcoded user-facing strings outside the message system

Adjudication rule:

- structure scripts are deterministic aids, not judges of copy quality
- if a script flags a placeholder/ICU mismatch on a source string that mixes a simple placeholder with a plural suffix helper, verify whether the target uses a runtime-valid ICU form with the same variable before failing the locale
- if the target deliberately uses locale-specific ICU plural categories, verify the message compiles and preserves meaning before rejecting it purely for option-key differences
- never hide unresolved script findings; report whether each finding is a real blocker, an accepted locale-specific adaptation, or a tool false positive

Reusable scripts bundled with this skill:

- `python3 ~/.agents/skills/my-personal-internationalization/scripts/verify_catalog.py --source path/to/fr.json --target path/to/en.json`
- `python3 ~/.agents/skills/my-personal-internationalization/scripts/scan_hardcoded_strings.py --root path/to/app/src`
- `python3 ~/.agents/skills/my-personal-internationalization/scripts/run_catalog_audit.py --source path/to/fr.json --target path/to/en.json --code-root path/to/app/src`

The hardcoded-string audit should inspect likely leak zones such as:

- components and pages
- onboarding flows
- legal pages
- emails
- shared/public pages
- support/chatbot/help surfaces
- API error messages

Important:

- `verify_catalog.py` is a structural gate
- `scan_hardcoded_strings.py` is heuristic and meant to produce review candidates
- `run_catalog_audit.py` gives a reusable one-command audit for real translation waves

## 9. Expected outcome

A successful run of this mode produces:

- a native-sounding target locale catalog
- structural parity with the reference locale
- a short audit result listing any remaining hardcoded user-facing strings outside the catalog system
- a clear distinction between:
  - translation complete
  - locale declared but not fully production-ready

Locale acceptance is not subjective.
Use `references/evaluator-rubric.md` and keep the locale in the correction loop until it receives an explicit `PASS`.

## 10. Lost N Found-derived rule worth reusing

When a project uses one core source catalog as the canonical reference, keep that pattern explicit.

Example reusable pattern:

- `fr.json` is the structurally complete reference catalog
- `en.json` is translated as natural anglophone copy, not as a literal mirror
- the codebase is audited afterward so untranslated hardcoded strings do not survive outside `messages/`

Additional production lessons from the first real Lost N Found translation run:

- do not spawn a single broad agent to create every missing catalog; it drifted toward programmatic translation and became hard to verify
- do not use a translation API or script as a shortcut when the user expects native AI-written, culturally adapted copy
- do not rely on the bundled verifier alone when it conflicts with direct ICU/runtime reasoning; the original verifier over-reported issues on strings like `Voir les {count} résultat{count, plural, one {} other {s}}`
- do not continue a stalled wave after repeated empty `wait_agent` results; stop, summarize, and re-plan
- do not keep two "stuck but maybe finishing" whole-file translators alive while opening the next wave; close them and relaunch on smaller section scopes
- do not forget that closed subagents cannot receive follow-up correction requests; start fresh correction agents with a narrow file scope instead
- do not let model or reasoning-effort overrides leak into spawned translators unless explicitly authorized by the user
