---
name: to-issues
description: "Use when the user wants to turn a plan, spec, PRD, or approved idea into independently grabbable issue-tracker slices. Not when the work still needs a PRD, repository discovery, or a generic handoff artifact."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# To Issues

Use this skill when the goal is to break already-shaped work into issue-tracker tickets that can be picked up independently. Favor tracer-bullet vertical slices: thin end-to-end slices that are demoable or verifiable on their own, with explicit dependencies and a clear distinction between `AFK` work and `HITL` work.

## Use this skill when

- The user wants to turn a plan, spec, PRD, or approved feature idea into implementation issues.
- The next step is creating dependency-aware tickets rather than refining the product narrative.
- The work should be split into small vertical slices instead of broad layer-by-layer tasks.
- The output should either be published to the issue tracker or left as ready-to-paste issue bodies.

## Do not use this skill when

- The work still needs a PRD or broader product framing before it can be split into tickets — use [`to-prd`](../to-prd/SKILL.md).
- The codebase is not understood well enough to describe the slices responsibly — use [`acquire-codebase-knowledge`](../acquire-codebase-knowledge/SKILL.md).
- The user needs a reusable markdown handoff artifact rather than tracker-native issues — use [`workflow-contracts`](../workflow-contracts/SKILL.md).
- The ask is still too vague to tell whether issue slicing is the right next step — use [`reverse-prompt`](../reverse-prompt/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Break an existing plan or PRD into implementation tickets with dependencies | Yes | - |
| Create the product-facing requirements document before any ticket breakdown exists | No | [`to-prd`](../to-prd/SKILL.md) |
| Produce a structured markdown handoff for planning, review, or execution | No | [`workflow-contracts`](../workflow-contracts/SKILL.md) |
| Explore the repository because the current architecture is still unclear | No | [`acquire-codebase-knowledge`](../acquire-codebase-knowledge/SKILL.md) |
| Rewrite an under-specified ask before deciding whether tickets should exist yet | No | [`reverse-prompt`](../reverse-prompt/SKILL.md) |

## Inputs to gather

**Required before editing**

- The source material to break down: plan, spec, PRD, approved issue, or a clearly scoped feature brief.
- Whether the result should be published now or left as a reviewed draft.
- The target issue tracker context, including any known parent issue or epic link.

**Helpful if present**

- User stories or acceptance criteria already captured in the source material.
- Existing domain vocabulary, ADRs, or repository conventions for the affected area.
- Known issue template, labels, or triage conventions for the target project.

**Only investigate if encountered**

- Missing architectural context that changes where slice boundaries should fall.
- Existing issue comments, linked tickets, or parent issue notes that materially change dependencies.
- Missing permissions, labels, or tracker configuration needed for publication.

## First move

1. Read the source material and current conversation before asking for anything new.
2. Pull just enough repository context to make the slice boundaries and terminology credible.
3. Draft the first vertical-slice breakdown before asking the user to adjust granularity or dependencies.

## Workflow

1. Start from the source artifact already in context. If the user supplied an issue reference, fetch its body and comments before slicing.
2. Identify the outcomes, user stories, and scope boundaries that the issues need to cover.
3. Break the work into tracer-bullet vertical slices using [`references/slicing-guide.md`](references/slicing-guide.md):
   - each slice should cut through the necessary layers end-to-end
   - each slice should be demoable or verifiable on its own
   - prefer many thin slices over a few thick ones
4. For each slice, draft:
   - title
   - type: `AFK` or `HITL`
   - dependencies / blockers
   - user stories covered
   - a concise "What to build" summary
   - concrete acceptance criteria
5. Present the proposed breakdown as a numbered list and get explicit approval on:
   - granularity
   - dependencies
   - merge or split suggestions
   - `AFK` vs `HITL` classification
6. Iterate until the slice breakdown is approved.
7. If publication is requested, create issues in dependency order using [`assets/issue-template.md`](assets/issue-template.md) so blocker references point to real issue IDs. Apply only verified labels or tracker fields.

## Outputs

- An approved vertical-slice issue breakdown.
- One ready-to-paste issue body per slice using [`assets/issue-template.md`](assets/issue-template.md).
- Either published issues in dependency order or a complete draft set plus any explicit publication blocker.

## Guardrails

- Keep slices vertical, not horizontal. Do not create separate tickets like "database work", "API work", and "UI work" when one thin end-to-end slice would be more executable.
- Prefer `AFK` over `HITL` unless human review, design, or decision-making is genuinely required.
- Do not publish issues before the user approves the proposed breakdown.
- Do not invent labels such as `needs-triage`, project fields, or tracker conventions unless they are verified in the target project.
- Do not close or modify a parent issue as part of this skill.
- If the source material is still too fuzzy to slice responsibly, stop and route to [`to-prd`](../to-prd/SKILL.md) or [`reverse-prompt`](../reverse-prompt/SKILL.md) instead of guessing.

## Validation

- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/to-issues/SKILL.md`.
- Confirm every slice has a title, `AFK`/`HITL` type, dependency status, user-story coverage, and acceptance criteria.
- Confirm the proposed issues are thin vertical slices rather than layer-based tasks; use [`references/checklist.md`](references/checklist.md).
- Confirm the publish order matches dependency order and does not create circular blockers.
- Confirm any tracker labels, templates, or metadata are applied only when they are verified.
- should trigger: "Break this approved PRD into implementation issues and open them in dependency order."
- should not trigger: "Write the PRD for this feature before we decide how to split the work."

## Examples

- "Turn this implementation plan into independently grabbable GitHub issues, and show me the breakdown before you publish anything."
- "Break this PRD into thin vertical slices with blocker relationships and mark which ones need human review."
- "Use the current issue and repo context to draft issue bodies for the next implementation wave, but leave them as ready-to-paste markdown."

## Reference files

- [`assets/issue-template.md`](assets/issue-template.md) - starter issue body template for each approved slice.
- [`references/slicing-guide.md`](references/slicing-guide.md) - tracer-bullet slicing rules, `AFK` vs `HITL` guidance, and anti-patterns.
- [`references/checklist.md`](references/checklist.md) - final review checklist for slice quality, dependency order, and publication readiness.
