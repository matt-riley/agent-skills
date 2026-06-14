---
name: agentic-eval
description: "Use when designing or implementing an evaluation loop for AI agent outputs — reflection loops, evaluator-optimizer pipelines, LLM-as-judge scoring, or rubric-based iteration. Not when running an existing test suite or reviewing a completed artifact without iterating."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: reference
---

# Agentic Evaluation

Use this skill when you are designing or implementing an evaluation loop that lets an agent assess and improve its own outputs through iteration — not when you are running a pre-existing test suite or doing a one-off review with no refinement cycle.

The core pattern is: **Generate → Evaluate → Critique → Refine → Output**, looping until a convergence condition is met or a max-iteration budget is exhausted.

## Use this skill when

- Implementing a self-critique or reflection loop that feeds output quality back into generation.
- Building an evaluator-optimizer pipeline that separates generation from evaluation responsibilities.
- Designing LLM-as-judge scoring to compare or rank multiple candidate outputs.
- Adding rubric-based scoring with weighted dimensions to iterative generation.
- Setting iteration limits, convergence checks, or structured evaluation output contracts.
- The task requires measurable improvement across runs, not just a single-shot best effort.

## Do not use this skill when

- You are running an existing test suite to verify code — use `verification-before-completion`.
- You are diagnosing a specific failure or bug, not evaluating output quality — use `systematic-debugging`.
- The goal is writing test coverage (unit tests, integration tests) — use `test-driven-development`.
- You are reviewing a completed artifact once without a refinement loop (a single code review, an editorial pass, a PR check).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Designing a reflection loop with a score threshold and max iterations | Yes | — |
| Implementing LLM-as-judge comparison of two candidate outputs | Yes | — |
| Running `npm test` to confirm a fix works | No | `verification-before-completion` |
| Tracing why a specific assertion fails | No | `systematic-debugging` |
| Writing Jest or pytest test coverage for a module | No | `test-driven-development` |
| Reviewing a PR diff once, no iteration | No | `review-comment-resolution` |

## Inputs to gather

**Required before starting**

- The skill or agent behavior to evaluate.
- The target metric: trigger accuracy, refusal rate, or behavioral assertion coverage.

**Helpful if present**

- Existing evals or trigger-queries files to extend.

## First move

1. Identify the skill or behavior to evaluate.
2. Check whether a `trigger-queries.json` already exists; if so, load it to understand scope.
3. Open the relevant reference file based on the evaluation type.

## Navigation

The three evaluation strategy patterns (outcome-based, LLM-as-judge, rubric-based) and full Python examples are in `references/patterns.md`.

The implementation checklist — criteria, threshold, loop wiring, convergence, logging — is in `assets/eval-checklist.md`.

For a new implementation, start with the checklist to confirm your setup is complete, then use the patterns reference to choose and adapt an evaluation strategy.

## Workflow

See the body and references for agentic evaluation design and loop steps.

## Examples

See references and the skill body for agentic-eval examples.

## Reference files

See the references/ directory and linked files in the main content.

## Guardrails

- Always set a `max_iterations` bound (3–5 is a safe default) before wiring up a refinement loop. Unbounded loops stall agents.
- Require structured output (JSON) from the evaluation step so the optimize step has a reliable signal to act on. Free-text critique is fragile.
- Add a convergence check: if the score does not improve between iterations, stop early. Oscillating loops that never converge waste budget.
- Log the full iteration trajectory. Evaluation loops are hard to debug post-hoc without a history of inputs, outputs, scores, and critiques.
- Define evaluation criteria before generating any output. Criteria added mid-loop drift and make scores incomparable across iterations.
- Keep the evaluate step isolated from the generate step. Blending them makes it hard to replace the evaluator or diagnose score instability.
- Handle evaluation parse failures gracefully — if the LLM judge returns malformed JSON, fall back to a safe default (treat as failing) rather than crashing the loop.

## Validation

- should trigger: "I want to add a reflection loop to my code-generation agent so it self-critiques and reruns until the score exceeds 0.85"
- should not trigger: "Run the test suite and tell me if the build passes"
- should not trigger: "Why is this specific assertion failing in my TypeScript tests?"

After implementing an evaluation loop, confirm:

- [ ] `max_iterations` is set and respected by the loop
- [ ] Evaluate step returns structured output (JSON or equivalent)
- [ ] Convergence check exits early when score does not improve
- [ ] All iterations are logged with input, output, score, and critique
- [ ] Parse-failure fallback is present on the evaluate step
- [ ] Criteria are defined before any generation begins

## Examples

- "Add a self-critique loop to my report-generation agent that retries up to three times if the rubric score is below 0.8."
- "Implement an evaluator-optimizer where a separate LLM judge scores code clarity and the generator rewrites until it passes."
- "Build a rubric-based evaluator with accuracy, completeness, and style dimensions that returns a weighted score as JSON."

## Reference files

- `references/patterns.md` — The three evaluation strategy patterns (outcome-based, LLM-as-judge, rubric-based) with annotated Python examples and a best-practices table.
- `assets/eval-checklist.md` — Implementation checklist: setup, loop wiring, convergence, logging, and safety items to confirm before shipping.
