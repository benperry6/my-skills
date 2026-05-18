# Anthropic Article Findings

This file distills the article `Harness design for long-running application development` into reusable findings.

It is meant to stay faithful to the article's structure and conclusions, while remaining usable as an engineering reference.

## 1. The article's core claim

Harness design materially changes what frontier coding models can achieve.

The article is not arguing only for better prompts.
It is arguing that system-level orchestration choices can change:

- quality
- completeness
- runtime correctness
- design originality
- resilience on long runs

## 2. Two recurring failure modes in naive long runs

### Context degradation

Long tasks can drift as context fills.

Observed article-level problems:

- coherence loss
- premature wrap-up near the perceived context limit
- "context anxiety"

Key takeaway:

- compaction preserves continuity, but not always a true fresh start
- hard resets with structured handoff artifacts can solve problems that compaction alone does not

Important nuance:

- this is model-dependent
- one model may need hard resets badly, while a stronger later model may not

## 3. Self-evaluation is structurally weak

Agents are usually too lenient when grading their own work.

This is especially visible on subjective tasks such as design, but it also matters on coding tasks with real bugs.

Key takeaway:

- separate the producer from the judge
- tune the evaluator to be skeptical
- external critique gives the generator something concrete to iterate against

## 4. Subjective quality becomes more usable when made gradable

For design, the article showed that vague aesthetic judgment was too unstable.

Anthropic improved outcomes by creating explicit criteria:

- design quality
- originality
- craft
- functionality

Important takeaways:

- explicit criteria outperform generic "make it good"
- weighting matters
- the wording of criteria can materially shape output character
- evaluator calibration matters, including few-shot examples

## 5. The coding analogue is planner / generator / evaluator

The article maps the generator/evaluator loop from design onto full-stack coding.

Role split:

- planner
  - expands a short prompt into a richer product spec
  - should stay high-level enough to avoid downstream lock-in from bad low-level choices
- generator
  - builds the product in chunks
- evaluator
  - verifies behavior, catches bugs, and grades against explicit criteria

The article's main lesson is not "always use three agents."
It is "separate the roles that require different judgment patterns."

## 6. Sprint contracts are a bridge between spec and implementation

Before each sprint, the generator and evaluator aligned on a sprint contract.

Purpose:

- translate a high-level spec into testable chunk-level expectations
- define what done means before code is written

Key takeaway:

- this reduces ambiguity
- it also creates a clean surface for QA

## 7. File-based artifacts matter

The article used files for inter-agent communication and handoff.

Why this matters:

- artifacts outlive one session
- they reduce reliance on fragile conversational memory
- they make re-entry and auditing easier

Typical artifact classes implied by the article:

- product spec
- sprint contract
- QA feedback
- handoff/progress state

## 8. Evaluator quality is not automatic

The evaluator did not start strong.

Anthropic had to iterate on the evaluator prompt because early QA behavior was:

- too forgiving
- too superficial
- too weak on edge cases

Key takeaway:

- evaluator quality is itself an engineering problem
- building a skeptical evaluator is a real tuning loop

## 9. Evaluator overhead is conditional, not universal

One of the article's strongest practical findings is that evaluator value depends on where the task sits relative to model capability.

If the current model can already do the task well solo, evaluator overhead may be wasteful.
If the task is near the reliability frontier, evaluator overhead can be extremely valuable.

Practical implication:

- evaluator is not a permanent yes/no doctrine
- it is a conditional lever

## 10. Simplification is part of harness design

The article explicitly warns against freezing a complex harness forever.

Key principle:

- every harness component encodes an assumption about what the model cannot do alone
- as models improve, those assumptions can become stale

Practical implication:

- keep the simplest solution that still works
- periodically remove components and measure the effect

## 11. Cost and latency are real architectural constraints

The article gives concrete evidence that richer harnesses can be far more expensive and slower than solo runs.

Practical implication:

- harness quality gains are real
- but the overhead is real too
- good harness design includes a decision about when the extra cost is justified

## 12. Faithful takeaway for daily use

The most faithful operational reading of the article is:

1. do not trust naive single-agent execution on difficult work by default
2. do not overbuild the harness by default either
3. separate roles when failure modes justify it
4. use explicit artifacts and contracts
5. keep evaluator behavior skeptical and explicit
6. periodically simplify the harness as models improve
