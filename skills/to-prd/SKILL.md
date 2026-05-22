---
name: to-prd
description: "Use when the user wants a PRD synthesized from current repository and conversation context, especially for issue-tracker handoff. Not when doc-coauthoring, workflow-contracts, or codebase discovery is the better fit."
metadata:
  category: authoring
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# To PRD

Use this skill when the goal is to turn what is already known — repository context, current conversation, and agreed constraints — into a product requirements document. Start from synthesis, not interviews: gather only the missing details that would materially change the scope, user stories, or issue-tracker destination.

## Use this skill when

- The user wants a PRD, product spec, or issue-ready requirements document from the current context.
- The current conversation already contains enough signal to synthesize the problem, solution, user stories, and implementation/testing decisions.
- The PRD should reflect the repository's current vocabulary, architecture, and prior art instead of a blank-sheet brainstorm.
- The next step is handing the result to an issue tracker, triage queue, or review flow rather than starting implementation immediately.

## Do not use this skill when

- The user wants a broader documentation workflow with iterative co-authoring and reader feedback — use [`doc-coauthoring`](../doc-coauthoring/SKILL.md).
- The task needs an implementation handoff, review artifact, or execution contract rather than a product-facing PRD — use [`workflow-contracts`](../workflow-contracts/SKILL.md).
- The codebase is still poorly understood and repository-level discovery is the real blocker — use [`acquire-codebase-knowledge`](../acquire-codebase-knowledge/SKILL.md).
- The ask is mainly to sharpen or restructure a vague request before planning or implementation — use [`reverse-prompt`](../reverse-prompt/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Turn an already-discussed feature into a PRD body for issue tracking or review | Yes | - |
| Produce a reusable markdown handoff artifact for planning, review, or execution | No | [`workflow-contracts`](../workflow-contracts/SKILL.md) |
| Write or refactor a broad shared document with multi-round collaboration | No | [`doc-coauthoring`](../doc-coauthoring/SKILL.md) |
| Map the repository first because the system is not understood well enough to describe the work | No | [`acquire-codebase-knowledge`](../acquire-codebase-knowledge/SKILL.md) |
| Rewrite an under-specified ask into a clearer brief before deciding whether a PRD is even needed | No | [`reverse-prompt`](../reverse-prompt/SKILL.md) |
| Break an approved PRD into independently trackable tickets | No | [`to-issues`](../to-issues/SKILL.md) |

## Inputs to gather

**Required before editing**

- The feature or problem area the PRD is about.
- The repository surfaces, product constraints, and decisions already established in the conversation.
- Whether the output should be published to an issue tracker now or left as ready-to-paste markdown.

**Helpful if present**

- Existing domain vocabulary, ADRs, or design notes for the feature area.
- Similar modules, interfaces, or tests in the codebase that establish prior art.
- Known issue-template, label, or triage conventions for the target project.

**Only investigate if encountered**

- Missing architectural context that would materially change the proposed module boundaries.
- Missing publication details such as issue labels, templates, or permissions.
- Adjacent feature work whose scope boundary is unclear enough to affect the PRD's out-of-scope section.

## First move

1. Read the current conversation and the relevant repository surfaces before asking anything new.
2. Pull the domain terms, module boundaries, interfaces, and test prior art that should shape the PRD.
3. Start from [`assets/prd-template.md`](assets/prd-template.md), filling the user-facing sections first.

## Workflow

1. Synthesize the product frame from what is already known: user problem, target outcome, constraints, and confirmed boundaries.
2. Inspect the current implementation enough to name the major modules or surfaces likely to change. Prefer deep, stable module boundaries when the repository suggests them.
3. Draft `Problem Statement`, `Solution`, and `User Stories` from the user's perspective. Make the user-story list extensive enough to cover primary flows, edge cases, administrative or operator roles, and failure/recovery paths when they matter.
4. Draft `Implementation Decisions` from concrete repository evidence: modules, interface changes, schema or API implications, architectural choices, and notable interactions. Describe capabilities and contracts, not file paths or code snippets.
5. Draft `Testing Decisions` around external behavior: what makes a good test here, which surfaces should be tested, and the closest prior art in the codebase.
6. Make `Out of Scope` explicit. Put unresolved but non-blocking notes in `Further Notes`; if a gap is still blocking, say so instead of inventing certainty.
7. If issue-tracker publication is part of the request, publish using the project's verified issue workflow. If tracker vocabulary, labels, or permissions are missing, stop at a complete markdown artifact and surface the publication blocker explicitly.

## Outputs

- A completed PRD using [`assets/prd-template.md`](assets/prd-template.md).
- An extensive user-story list that covers the feature's main actors and meaningful edge cases.
- Implementation and testing decisions grounded in repository context and prior art.
- Either a published issue or a ready-to-paste PRD markdown artifact plus any explicit publication blocker.

## Guardrails

- Do not start with a broad interview. Synthesize from existing context first and ask only targeted questions that unblock the PRD materially.
- Keep `Problem Statement` and `Solution` user-facing; do not let them collapse into implementation notes.
- Do not include file paths or code snippets in `Implementation Decisions`.
- Do not invent issue labels such as `needs-triage` unless the project already defines them.
- Prefer repository vocabulary, current architecture, and known prior art over generic best-practice prose.
- If the task turns into repository discovery, route to [`acquire-codebase-knowledge`](../acquire-codebase-knowledge/SKILL.md) instead of stretching this skill.

## Validation

- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/to-prd/SKILL.md`.
- Confirm the PRD uses the section order from [`assets/prd-template.md`](assets/prd-template.md).
- Confirm `Problem Statement` and `Solution` are written from the user's perspective.
- Confirm `Implementation Decisions` and `Testing Decisions` are grounded in repository context and mention no file paths or code snippets.
- Confirm any publish step uses only verified issue-template or label conventions; otherwise leave the output as markdown plus a blocker note.
- should trigger: "Turn this feature discussion into a PRD and open an issue for it using what you can verify from the repo."
- should not trigger: "Help me rewrite this vague feature request before we decide whether it needs a PRD."

## Examples

- "Turn everything we know about the billing retry flow into a PRD and publish it to the repo's issue tracker."
- "Use the current conversation and the codebase to write a PRD for offline draft sync; don't interview me unless something is genuinely blocking."
- "Synthesize this feature discussion into a PRD with extensive user stories, implementation decisions, testing decisions, and out-of-scope items."

## Reference files

- [`assets/prd-template.md`](assets/prd-template.md) - starter PRD scaffold with the required section order.
- [`references/checklist.md`](references/checklist.md) - final quality and publication checklist before treating the PRD as done.
