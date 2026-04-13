# Catalog Translation Mode

Use this mode when the user wants to translate locale message catalogs such as `fr.json` to `en.json` without keeping a recurring prompt in notes.

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

Default rule: keep the translator prompt as small and task-focused as possible.

Do not turn the translator prompt into a mini-orchestration document.
Do not stuff it with evaluation, polling, or recovery rules.

Use the proven direct instruction pattern:

`Traduis fr.json en anglais comme un natif pour en.json, en adaptant aussi toutes les references, formulations et codes culturels pour qu'ils soient naturels et immediatement comprehensibles pour la communaute anglophone.`

Only two prompt adaptations are allowed by default:

1. adapt the target language, target file, and target community name
2. add one short sentence making it explicit that the model/agent addressed must do the translation itself and must not rely on translation APIs, browser translation, programmatic translation scripts, or second-opinion delegation to generate the copy

Everything else belongs to the orchestrator, not to the translator prompt.

Examples of the community-name substitution:

- communaute anglophone
- communaute germanophone
- communaute lusophone bresilienne
- communaute thaiophone
- communaute sinophone traditionnelle

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

Default orchestration rule:

- spawn one translator subagent per target locale
- launch all remaining target locales in parallel by default
- keep every translator on inherited conversation settings with no model or reasoning override

Do not shrink this into waves by default just because earlier runs looked quiet.
Quiet is not the same thing as dead.

Warm-up rule:

- 2 to 5 minutes of visible inactivity is normal
- less than 10 minutes of inactivity is not, by itself, a failure signal
- do not recadre, interrupt, or restart a translator merely because it looks frozen for a few minutes

Failure rule:

- only treat a translator as potentially dead after more than 10 minutes with no observable activity, no new step, and no local progress
- once that threshold is crossed, replace the translator rather than nudging it with extra instructions

Default orchestrator behavior:

1. define the source-of-truth catalog and structural invariants
2. spawn one translator subagent per target locale immediately
3. keep the translator prompt minimal; do not add orchestration boilerplate to it
4. let the translators run without recadrage unless the failure rule is met
5. as each locale lands locally, verify it on disk before accepting it
6. run the evaluator/correction loop for that locale
7. keep the orchestrator alive until every locale has completed translation, verification, evaluation, and any required corrections

Operational acceptance rule:

- a subagent final message is evidence, not acceptance
- acceptance requires local file presence plus local verification output recorded by the orchestrator
- if a verifier reports many mismatches, inspect representative keys directly before concluding the catalog is bad

Environment-limit rule:

- if spawning all target locales hard-fails because of a usage limit, quota limit, or agent-creation failure, report that environment limit explicitly
- do not silently redesign the translation brief or switch to another translation method because of that limit

Resumption and traceability rule:

- Codex threads are designed to persist and be resumed, but do not rely on UI attachment alone after closing the app or terminal
- the orchestrator must keep a run registry with at least locale, agent id, and status
- if the environment exposes a session or transcript path, record it too
- this registry is what lets a later session recover the translation run even if the visual parent/child attachment is gone

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
- the verifier should not fail valid English contractions such as `We've` or `You're`
- the verifier should not raise a false blocker when a target locale replaces a placeholder-plus-suffix source pattern with a valid ICU message that preserves the same runtime variable and meaning

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

- do not overload translator prompts with orchestration instructions; the extra instructions diluted the main task
- do not use a translation API or script as a shortcut when the user expects native AI-written, culturally adapted copy
- do not rely on the bundled verifier alone when it conflicts with direct ICU/runtime reasoning; the original verifier over-reported issues on strings like `Voir les {count} résultat{count, plural, one {} other {s}}`
- do not treat a translator as dead just because it stayed quiet for a few minutes; short freezes are often warm-up periods rather than real failure
- do not accept a locale from the subagent's final text alone; verify the file on disk locally first
- do not let the orchestrator stop after spawning translators; it must stay alive until the entire translation/evaluation/correction run is finished
- do not lose track of spawned subagents; keep locale-to-agent traceability so a later session can recover the run
- do not let model or reasoning-effort overrides leak into spawned translators unless explicitly authorized by the user
