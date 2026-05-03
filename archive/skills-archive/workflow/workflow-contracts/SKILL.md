---
name: workflow-contracts
description: Use versioned structured markdown contracts for planning handoffs, review outcomes, and execution records.
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Workflow contracts

Use this skill when a task needs a durable, handoff-friendly artifact for planning, review, or implementation in this Copilot setup.

## Use this skill when

- You are turning planning or research results into a reusable implementation handoff.
- A reviewer needs to return an explicit `approve|revise|blocked` decision.
- Implementation work needs a compact execution record with validation and blockers.
- The surrounding workflow needs stable headings and frontmatter instead of ad hoc prose.

## Do not use this skill when

- A one-off chat response is enough and no durable artifact is needed.
- The main task is inventing a new workflow instead of using the existing `v1` contracts.
- You need a client-specific parser, hook, or enforcement layer rather than a reusable artifact template.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Create or consume a structured plan, review, or execution artifact in this repo | Yes | - |
| Create or revise a reusable skill package | No | [`skill-creator`](../skill-creator/SKILL.md) |
| Write global policy that should always apply even when no artifact is produced | No | global instructions or a scoped instruction file |

## Inputs to gather

**Required before editing**

- Which phase the artifact serves: planning, review, or implementation.
- The target artifact path or durable destination.
- The current goal or `task_id`.
- The files, directories, or surfaces that must survive the handoff.
- The constraints, evidence, or validation commands that the next phase must retain.

**Helpful if present**

- The prior research memo, plan, or implementation note being converted.
- Reviewer names or roles.
- Existing legacy artifacts that need to be mapped into `v1`.

**Only investigate if encountered**

- Older ad hoc artifact shapes that the current task depends on.
- Client-specific automation or enforcement expectations outside this repository's current tooling.

## First move

1. Choose the matching `v1` template from `assets/`.
2. Keep the template's frontmatter keys and stable headings unchanged unless `references/contract-spec.md` is being revised too.
3. Fill only the fields supported by concrete evidence, commands, or decisions.

## Workflow

1. Pick the correct template:
   - planner handoff
   - review outcome
   - execution record
2. Set the required frontmatter fields:
   - `contract_type`
   - `contract_version`
   - `created_by`
   - `status`
3. Populate the contract-specific fields from [`references/contract-spec.md`](references/contract-spec.md).
4. During migration, accept legacy prose as input but prefer `v1` structured markdown for all new or revised artifacts.
5. If a legacy artifact must feed the next phase, map it into the `v1` headings before handing it off.
6. Validate the finished artifact with [`references/checklist.md`](references/checklist.md).
7. Hand off the artifact with an explicit next action instead of assuming the next agent will infer it from chat history.

## Outputs

- A populated `v1` contract artifact using one of the templates in `assets/`:
  - planner handoff
  - review outcome
  - execution record
- Required frontmatter and headings from [`references/contract-spec.md`](references/contract-spec.md).
- An explicit status plus a concrete next action for the next phase.

## Guardrails

- **Must** keep the stable field names and required headings from the contract spec.
- **Must** make the status explicit instead of burying approval or blockers in prose.
- **Must not** invent a third artifact shape during the migration window.
- **Must not** stretch this skill into a new parser, framework, or orchestration layer.
- **Should** keep artifacts short, phase-specific, and directly usable by the next step in the workflow.

## Validation

- Confirm the artifact uses the correct template and `contract_version: v1`.
- Confirm all shared frontmatter keys are present.
- Confirm the contract-specific headings exist and are populated with concrete content.
- Confirm any commands, evidence, or blockers are explicit enough that the next phase does not need to reconstruct them from chat history.
- Confirm the next action is obvious within a few seconds of reading the artifact.
- Run [`scripts/validate-contracts.mjs`](scripts/validate-contracts.mjs) when available to check required frontmatter, status values, and headings mechanically.

## Examples

- "Turn this approved plan into a `v1` planner handoff artifact."
- "Rewrite these review notes as a review-outcome contract with an explicit status."
- "Record the current implementation wave in an execution record before switching tasks."

## Reference files

- [`references/contract-spec.md`](references/contract-spec.md) - required frontmatter keys and headings for each `v1` contract
- [`references/terminology.md`](references/terminology.md) - shared terms used across planning, review, and execution
- [`references/rollout-and-compatibility.md`](references/rollout-and-compatibility.md) - migration rules, cutover conditions, and legacy-artifact handling
- [`references/checklist.md`](references/checklist.md) - final artifact validation checklist
- [`assets/planner-handoff-v1.md`](assets/planner-handoff-v1.md) - template for planner-to-executor handoffs
- [`assets/review-outcome-v1.md`](assets/review-outcome-v1.md) - template for machine-decidable reviewer responses
- [`assets/execution-record-v1.md`](assets/execution-record-v1.md) - template for implementation and verification handoffs
- [`scripts/validate-contracts.mjs`](scripts/validate-contracts.mjs) - local validator for `v1` contract artifacts
