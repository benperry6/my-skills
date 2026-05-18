---
name: my-personal-qa-evaluator
description: "[My Personal Skill] Use when a completed implementation, sprint, or feature needs a skeptical QA evaluator before acceptance. Defines a fulfillment-first evaluation workflow: compare against the requested contract, gather real behavioral evidence, score against a calibrated rubric, and return a strict PASS / REWORK / BLOCK verdict without drifting into generic code review."
metadata:
  version: 0.1.0
---

# My Personal QA Evaluator

## Overview

This skill defines the evaluator role for non-trivial implementation work.

Use it after code exists and a real acceptance decision is needed.

It exists to answer:

- did the delivered work actually fulfill the requested contract?
- what was proven in real behavior versus merely inferred from reading code?
- is this ready to accept, does it need a small rework loop, or should it be rejected?

This skill is not a harness chooser.
It is not a generic code reviewer.
It is not an adversarial security reviewer.

It is the skeptical QA judge.

## Trigger Conditions

Use this skill when:

- a feature or sprint is finished and needs formal acceptance
- a long-running builder needs a separate evaluator
- the implementation looks plausible but must be proven
- a product flow needs browser/API/runtime checks, not just code reading
- you need a strict `PASS / REWORK / BLOCK` decision

Good fits:

- post-implementation acceptance for a non-trivial feature
- sprint acceptance in a planner / generator / evaluator harness
- verification of a user flow, integration, or runtime behavior
- checking whether the implementation matches the validated scope

Do not use this skill for:

- choosing the harness shape; use `my-personal-harness-engineering`
- cross-engine technical review by itself; use `my-personal-second-opinion`
- adversarial pre-PR grilling; use `challenge`
- worker supervision or recovery; use `my-personal-subagent-orchestration`

## Core Doctrine

1. Evaluate fulfillment first, elegance second.
2. Reading code is not proof of behavior.
3. The evaluator must be more skeptical than the builder.
4. Use explicit rubric criteria, not vague approval.
5. Behavioral evidence beats implementation theory.
6. If a critical behavior is unproven, do not give `PASS`.
7. Small fixable misses get `REWORK`, not false approval.
8. Major scope failure, architectural mismatch, or missing proof gets `BLOCK`.
9. The evaluator should not silently expand scope.
10. Calibration is part of the job: if the evaluator is too lenient, tighten the rubric rather than trusting vibes.

## Reference Map

Read only what the current task needs:

- `references/default-rubric.md`
  - the default weighted rubric and how to adapt it to a specific task
- `references/verdict-policy.md`
  - strict `PASS / REWORK / BLOCK` rules
- `references/evidence-workflow.md`
  - how to gather real behavioral evidence before judging
- `references/integration-boundaries.md`
  - how this skill composes with harness engineering, second opinion, and challenge
- `references/calibration-loop.md`
  - how to improve the evaluator over time when its judgment is too soft or too noisy

## Workflow

### 1. Lock the acceptance surface

Before judging, identify the source of truth:

- validated plan
- sprint contract
- user request
- acceptance checklist

If the contract is fuzzy, say so explicitly before scoring.

### 2. Gather behavioral evidence first

Use the strongest available evidence:

- automated tests
- browser behavior
- API responses
- database or side-effect inspection
- produced artifacts
- logs or command output

Do not default to code reading when behavior can be tested.

### 3. Score against an explicit rubric

Use `references/default-rubric.md`.

At minimum, evaluate:

- contract fulfillment
- behavioral evidence
- regression / collateral damage
- constraint adherence
- UX / operability sanity
- test adequacy

If the task has special constraints, adapt the rubric rather than pretending the default is perfect.

### 4. Return a strict verdict

Use only:

- `PASS`
- `REWORK`
- `BLOCK`

Then explain why.

Use `references/verdict-policy.md`.

### 5. Keep the output actionable

The evaluator output should contain:

- verdict first
- severity-ordered findings
- what is proven
- what is still unproven
- smallest next fix set
- next tests required before acceptance

### 6. Calibrate over time

If the evaluator keeps being too generous or too noisy:

- collect concrete examples of bad judgments
- update the rubric or verdict policy
- use `my-personal-verified-learning-loop` to promote durable improvements

## Output Standard

A correct evaluator run should leave behind:

- the acceptance contract used
- the evidence actually checked
- a rubric-based scorecard
- a strict verdict
- the smallest next action

If the result still depends on untested behavior, that must be said explicitly.
