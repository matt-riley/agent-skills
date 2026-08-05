---
name: grill-me
description: "Use when the user wants to be interviewed or stress-tested about a plan, design, or decision, including explicit requests to 'grill me'. If they also mention CONTEXT.md, ADRs, or a domain glossary, use the documentation mode; otherwise keep the session pure interrogation and do not create docs."
license: GNU GPL v3
metadata:
  version: 2.0.1 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Grill me

Use this skill to relentlessly interrogate a plan or design until every branch of the decision tree is resolved. Pure interrogation is the default. Switch to the explicit documentation mode only when the user signals domain-document intent by mentioning `CONTEXT.md`, ADRs, or a domain glossary; never create those files silently.

## Use this skill when

- The user wants to be grilled, stress-tested, or interviewed about a plan or design.
- The user explicitly says "grill me" and does not mention domain docs, `CONTEXT.md`, or ADRs.
- The user asks to grill a plan while explicitly asking to create or update `CONTEXT.md`, ADRs, or a domain glossary.
- The user wants to think through a decision tree before committing to a direction.

## Do not use this skill when

- The request is under-specified and needs sharpening before interrogation — route to [`reverse-prompt`](../reverse-prompt/SKILL.md).
- A completed plan needs formal reviewer-gated, multi-round approval — route to [`plan-review`](../plan-review/SKILL.md).
- The user wants standalone documentation (README, guide, or runbook) — route to [`doc-coauthoring`](../doc-coauthoring/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| User says "grill me" about a plan with no documentation intent | Yes | - |
| User says "grill me" and mentions `CONTEXT.md`, ADRs, or a domain glossary | Yes — documentation mode | - |
| User's request is too vague to interrogate | No | [`reverse-prompt`](../reverse-prompt/SKILL.md) |
| Completed plan needs Jason/Freddy or other reviewer-gated rounds | No | [`plan-review`](../plan-review/SKILL.md) |

## Inputs to gather

**Required before starting**

- The plan, design, or decision the user wants stress-tested.

**Helpful if present**

- Prior conversation context about the feature.
- The repository codebase for verification of claims.

**Only investigate if encountered**

- An existing `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` directory when the user explicitly asks for documentation mode.

## First move

1. Read the plan or design the user has presented.
2. If documentation mode was explicitly requested, check for existing `CONTEXT.md`/`CONTEXT-MAP.md` and `docs/adr/`; otherwise do not look for or create documentation artifacts.
3. Identify the first unresolved decision branch and ask one question, providing your recommended answer using the available user-input mechanism.

## Workflow

1. Ask one question at a time. Walk down each branch of the design tree, resolving dependencies between decisions sequentially; provide your recommended answer with every question.
2. Explore instead of asking when a question can be answered by examining the codebase.
3. In documentation mode, challenge terms against the existing glossary, sharpen fuzzy domain language, and cross-reference claims with code.
4. In documentation mode, update `CONTEXT.md` inline only after the user has explicitly requested that mode and a domain term is resolved; offer ADRs only for hard-to-reverse, surprising trade-offs.
5. Repeat until all branches are resolved and the user confirms shared understanding.

## Outputs

- A shared understanding of the plan or design, with all decision branches resolved.
- In documentation mode only: updated or newly created `CONTEXT.md` and zero or more qualifying ADRs.

## Guardrails

- Ask questions one at a time; never dump a wall of questions.
- Provide a recommended answer with every question.
- Explore the codebase when it can answer a question; do not ask the user what the code already tells you.
- Keep pure interrogation free of documentation side effects.
- Never create or update `CONTEXT.md`, `CONTEXT-MAP.md`, or ADRs unless the user explicitly signals documentation mode.
- In documentation mode, define only project-specific domain terms in `CONTEXT.md`, one sentence each, and use the formats in the reference files.

## Validation

- Confirm the skill activates on "grill me" prompts without domain-doc intent.
- Confirm the same trigger enters documentation mode when the user mentions `CONTEXT.md`, ADRs, or a domain glossary.
- Confirm vague requests route to `reverse-prompt` and reviewer-gated plan approval routes to `plan-review`.
- Run `node skills/skill-creator/scripts/validate-skill-library.mjs skills/grill-me/SKILL.md`.
- Smoke test:
  - should trigger: "Grill me on my plan to refactor the notification service."
  - should trigger in documentation mode: "Grill me and build CONTEXT.md as we go."
  - should not trigger: "Sharpen this vague request before I start." (→ `reverse-prompt`)

## Examples

- "Grill me on this plan to split the monolith into two services."
- "Stress-test my caching design before I commit to it."
- "Grill me on order cancellation and update CONTEXT.md as we resolve domain terms."

## Reference files

- [references/interrogation-patterns.md](references/interrogation-patterns.md) — lightweight question sequencing and completion guidance.
- [references/session-playbook.md](references/session-playbook.md) — scenario construction, contradiction surfacing, fuzzy-term resolution, and explicit documentation-mode patterns.
- [references/context-format.md](references/context-format.md) — `CONTEXT.md` format when documentation mode is explicitly requested.
- [references/adr-format.md](references/adr-format.md) — ADR format and offering criteria for qualifying decisions.
- [assets/context-template.md](assets/context-template.md) — starter template for a new `CONTEXT.md`, used only in documentation mode after the user requests it.
