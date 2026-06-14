---
name: grill-me
description: "Use when the user wants to be interviewed or stress-tested about a plan, design, or decision — or when the user explicitly says 'grill me'. Not for domain-doc maintenance; route to grill-with-docs when CONTEXT.md or ADRs should be updated."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# Grill me

Use this skill to relentlessly interrogate a plan or design until every branch of the decision tree is resolved. Pure interrogation — no documentation side-effects.

## Use this skill when

- The user wants to be grilled, stress-tested, or interviewed about a plan or design.
- The user explicitly says "grill me" and does not mention domain docs, CONTEXT.md, or ADRs.
- The user wants to think through a decision tree before committing to a direction.

## Do not use this skill when

- The plan touches domain concepts that should be captured in CONTEXT.md or ADRs — route to `grill-with-docs`.
- The request is under-specified and needs sharpening before interrogation — route to `reverse-prompt`.
- A completed `/plan` needs formal reviewer approval — route to `plan-review-loop`.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| User says "grill me" about a plan, no domain-doc intent | Yes | - |
| User wants interrogation AND domain language / ADR maintenance | No | `grill-with-docs` |
| User's request is too vague to interrogate | No | `reverse-prompt` |
| Completed `/plan` needs Jason/Freddy review | No | `plan-review-loop` |

## Inputs to gather

**Required before starting**

- The plan, design, or decision the user wants stress-tested.

**Helpful if present**

- Prior conversation context about the feature.
- The repository codebase for verification of claims.

## First move

1. Read the plan or design the user has presented.
2. Identify the first unresolved decision branch.
3. Ask the first question, providing your recommended answer using the `ask_user` tool

## Workflow

1. **Ask one question at a time.** Walk down each branch of the design tree, resolving dependencies between decisions sequentially. For each question, provide your recommended answer.
2. **Wait for feedback** on each question before continuing to the next.
3. **Explore instead of asking** when a question can be answered by examining the codebase.
4. **Repeat** until all branches are resolved and you have reached a shared understanding.

## Outputs

- A shared understanding of the plan or design, with all decision branches resolved.

## Guardrails

- Ask questions one at a time. Never dump a wall of questions.
- Provide your recommended answer with every question.
- Explore the codebase when it can answer a question directly — do not ask the user what the code already tells you.
- Do not create or update any documentation files (CONTEXT.md, ADRs). If domain-doc maintenance is needed, tell the user to use `grill-with-docs` instead.

## Validation

- Confirm the skill activates on "grill me" prompts without domain-doc intent.
- Confirm it routes to `grill-with-docs` when the user mentions CONTEXT.md, ADRs, or domain language maintenance.
- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/grill-me/SKILL.md`.
- Smoke test:
  - should trigger: "Grill me on my plan to refactor the notification service."
  - should not trigger: "Grill me on this design and build up CONTEXT.md as we go." (→ `grill-with-docs`)

## Examples

- "Grill me on this plan to split the monolith into two services."
- "Stress-test my design for the new caching layer — I want to make sure I haven't missed anything."
- "Interview me about this migration approach before I start implementing."

## Reference files

- [references/interrogation-patterns.md](references/interrogation-patterns.md) — lightweight interrogation patterns: question sequencing, when to explore vs. ask, session completion criteria
