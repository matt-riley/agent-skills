---
name: grill-with-docs
description: "Use when stress-testing a plan against the project's domain model, when domain terminology is fuzzy or inconsistent, or when the user says 'grill me' about a design that should produce or update CONTEXT.md and ADRs."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# Grill with docs

Use this skill to stress-test a plan or design through relentless interrogation while simultaneously maintaining the project's domain glossary (CONTEXT.md) and capturing architectural decisions (ADRs) as they crystallise.

## Use this skill when

- The user wants to be grilled or stress-tested on a plan that touches domain concepts.
- Domain terminology in the project is fuzzy, inconsistent, or undocumented.
- The user explicitly says "grill me" and mentions domain docs, CONTEXT.md, or ADRs.
- A plan exists but the shared understanding between user and agent is not yet solid, and domain language should be captured along the way.
- The user wants to build or update CONTEXT.md as part of planning.

## Do not use this skill when

- The user wants pure interrogation without any documentation side-effects — route to `grill-me`.
- The request is under-specified and needs sharpening before it can be interrogated — route to `reverse-prompt`.
- A completed `/plan` needs formal review by Jason/Freddy personas — route to `plan-review-loop`.
- The user wants to write standalone documentation (README, guide, runbook) — route to `doc-coauthoring`.
- The user wants a pre-edit file/test map — route to `context-map`.

## Routing boundary

| Situation                                                              | Use this skill? | Route instead      |
| ---------------------------------------------------------------------- | --------------- | ------------------ |
| User says "grill me on this plan" and the plan touches domain concepts | Yes             | -                  |
| User wants domain glossary built from scratch during planning          | Yes             | -                  |
| User wants pure interrogation, no doc maintenance                      | No              | `grill-me`         |
| User's request is too vague to interrogate                             | No              | `reverse-prompt`   |
| Completed `/plan` needs formal approval-gate review                    | No              | `plan-review-loop` |
| User wants a standalone document authored collaboratively              | No              | `doc-coauthoring`  |
| User needs to map files and tests before editing                       | No              | `context-map`      |

## Inputs to gather

**Required before starting**

- The plan, design, or feature the user wants stress-tested.
- The repository root where CONTEXT.md and `docs/adr/` should live.

**Helpful if present**

- An existing CONTEXT.md or CONTEXT-MAP.md in the repository.
- An existing `docs/adr/` directory with prior decisions.
- Prior conversation context about the feature being planned.

**Only investigate if encountered**

- Code that contradicts what the user says about how things work.
- Multiple bounded contexts in a monorepo (signalled by CONTEXT-MAP.md).

## First move

1. Check whether CONTEXT.md (or CONTEXT-MAP.md) and `docs/adr/` exist in the repository.
2. If CONTEXT.md exists, read it. If ADRs exist, scan them for decisions relevant to the plan.
3. Begin the interrogation: ask the first question about the plan, providing your recommended answer using the `ask_user` tool.

## Workflow

1. **Interrogate one question at a time.** Walk down each branch of the design tree, resolving dependencies between decisions sequentially. For each question, provide your recommended answer. Wait for the user's response before continuing.

2. **Explore before asking.** If a question can be answered by exploring the codebase, explore the codebase instead of asking the user.

3. **Challenge against the glossary.** When the user uses a term that conflicts with the existing language in CONTEXT.md, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

4. **Sharpen fuzzy language.** When the user uses vague or overloaded terms, propose a precise canonical term: "You're saying 'account' — do you mean the Customer or the User?"

5. **Discuss concrete scenarios.** Stress-test domain relationships with specific scenarios that probe edge cases and force precision about boundaries between concepts. See [references/session-playbook.md](references/session-playbook.md) for patterns.

6. **Cross-reference with code.** When the user states how something works, verify against the code. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

7. **Update CONTEXT.md inline.** When a term is resolved, update CONTEXT.md immediately — do not batch. Use the format in [references/context-format.md](references/context-format.md). Create CONTEXT.md lazily if it does not exist yet. Do not couple CONTEXT.md to implementation details; only include terms meaningful to domain experts.

8. **Offer ADRs sparingly.** Only offer to create an ADR when all three conditions are met: (a) hard to reverse, (b) surprising without context, (c) the result of a real trade-off. If any condition is missing, skip the ADR. Use the format in [references/adr-format.md](references/adr-format.md). ADRs live in `docs/adr/` with sequential numbering. Create the directory lazily if it does not exist yet.

## Outputs

- Updated or newly created CONTEXT.md with resolved domain terms.
- Zero or more ADRs in `docs/adr/` for qualifying decisions.
- A shared understanding of the plan, documented through the glossary and decision records.

## Guardrails

- Ask questions one at a time. Never dump a wall of questions.
- Provide your recommended answer with every question.
- Update CONTEXT.md inline as terms resolve. Do not batch documentation updates to the end.
- Do not add general programming concepts to CONTEXT.md — only project-specific domain terms.
- Do not offer an ADR unless all three conditions (hard to reverse, surprising, real trade-off) are met.
- Do not create CONTEXT.md or `docs/adr/` until you have something to write in them.
- Keep CONTEXT.md definitions to one sentence. Define what a term IS, not what it does.

## Validation

- Confirm that every term added to CONTEXT.md follows the format in [references/context-format.md](references/context-format.md).
- Confirm that every ADR created follows the format in [references/adr-format.md](references/adr-format.md) and meets all three offering criteria.
- Confirm that CONTEXT.md does not include implementation-specific terms.
- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/grill-with-docs/SKILL.md`.
- Smoke test:
  - should trigger: "Grill me on this plan to add order cancellation — I want the domain language documented."
  - should not trigger: "Sharpen this vague request into a proper brief before I start." (→ `reverse-prompt`)

## Examples

- "Grill me on this plan to refactor the notification system — build up CONTEXT.md as we go."
- "Stress-test my design for the new auth flow against the existing domain model in CONTEXT.md."
- "I need to work through the payment processing changes — interrogate me and capture any ADRs along the way."

## Reference files

- [references/context-format.md](references/context-format.md) — CONTEXT.md format specification: structure, rules, single vs. multi-context repos
- [references/adr-format.md](references/adr-format.md) — ADR format, offering criteria, qualifying categories, and optional sections
- [references/session-playbook.md](references/session-playbook.md) — interrogation patterns: scenario construction, contradiction surfacing, fuzzy-term resolution
- [assets/context-template.md](assets/context-template.md) — starter template for a new CONTEXT.md
