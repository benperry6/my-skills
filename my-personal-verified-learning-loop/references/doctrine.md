# Verified Learning Doctrine

This reference exists to keep self-improving skills disciplined.

## 1. Separate the layers

There are three different things people often collapse together:

- runtime incident memory
- verified reusable doctrine
- task-specific or project-specific memory

Keep them separate.

Runtime incident memory says:

- this failed
- this was tried
- this repair path appeared to work
- more validation may still be needed

Verified reusable doctrine says:

- this has been proven enough to guide future runs by default

Project memory says:

- this mattered in a specific repository, business, or session

Do not merge them into one file.

## 2. Learning from behavior, not vibes

A skill should learn from:

- observed failure
- observed repair
- observed success
- observed artifact

It should not learn from:

- a plausible guess
- a nice-sounding interpretation of the docs
- a single unverified claim from an upstream source

## 3. Self-modification is allowed

Self-modification is not the problem.

The real problem is self-modification without:

- evidence
- scope control
- layer separation
- auditability

So the rule is not "never self-modify."
The rule is "self-modify only under a verified learning contract."

## 4. Promotion discipline

Promote only what is durable.

Questions to ask before promotion:

- did the repaired path actually run successfully?
- is the evidence local and inspectable?
- is this likely to remain useful across future runs?
- does this change canonical guidance, or only incident memory?

If the answer to the last question is "incident memory only", do not touch `SKILL.md`.

## 5. Smallest-correct-target rule

Update the smallest surface that captures the new truth.

Examples:

- a transient provider quirk may belong only in `runtime-learning.md`
- a stable new invocation path may belong in `verified-learning.md`
- a changed default workflow may justify a `SKILL.md` update
- a repaired helper path may justify a helper-script patch plus verified note

## 6. Preserve specialization

Shared doctrine should govern:

- confidence thresholds
- promotion rules
- evidence requirements
- write-back discipline

It should not erase:

- skill-specific success conditions
- skill-specific references
- skill-specific operating constraints

The shared loop governs how a skill learns, not what that skill is about.
