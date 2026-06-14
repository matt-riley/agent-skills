---
name: rpi-workflow
description: "Apply a Research -> Plan -> Implement -> Validate workflow for non-trivial work in agent-compatible coding harnesses, keeping progress durable across turns and sessions via workspace `plan.md` and `files/` artifacts."
license: GNU GPL v3
metadata:
  version: 1.4.0 # x-release-please-version
  owner: mattriley
  maturity: draft
  kind: task
---

# Research -> Plan -> Implement -> Validate (RPI-V)

## Use this skill when

- The task is non-trivial and benefits from explicit phase boundaries with durable artifacts.
- Work spans multiple files, decisions, or validation steps and is safer executed one phase at a time.
- The user wants end-to-end disciplined execution rather than only planning, only review, or a narrow specialist workflow.

## Do not use this skill when

- The task is a tiny fix or direct answer where the full ceremony costs more than it saves.
- The user wants only a plan or plan revision → use `plan-review`; only implementation review → use `implementation-review`; only a contract-shaped execution brief or definition of done → use `reverse-prompt`; or a narrower specialist workflow that another skill covers better.
- The repo already imposes a stricter required workflow and the job is to follow that process.

## Inputs to gather

### Required before starting

- The concrete outcome the user wants.
- The current repository or target working directory.
- The relevant local instructions, conventions, and constraints for the touched area.
- Whether the user expects plan approval before implementation.

### Helpful if present

- Existing `plan.md` content for the current workspace or task branch.
- Prior research, checkpoints, or handoff notes already saved under a workspace `files/`
  directory.
- Existing tests, build commands, lint commands, or release checks for the area being changed.
- Known risk areas such as migrations, code generation, auth, or production-facing behavior.

### Only investigate if encountered

- Legacy `/share` or `thoughts/shared/...` artifacts from older sessions.
- Large context pressure that requires checkpointing or a phase boundary reset.
- Parallel-agent coordination details such as worktrees or isolated lanes.

## First move

1. Decide whether the task truly needs the full RPI-V workflow or a narrower skill.
2. Read the minimum relevant instructions and inspect the codebase without making changes.
3. Create or refresh a workspace `plan.md` with the problem, scope, phase list, and validation
   approach.
4. If research needs to persist beyond the current turn, save concise notes under a workspace
   `files/` directory before moving on.

## Workflow

### 1. Research

- Stay read-only; prefer targeted searches and a small set of relevant files over loading broad context.
- Identify the exact files, commands, constraints, and open questions that should shape the plan.
- Save research notes to `files/` only when they help later phases or a future handoff (e.g. `files/research-<topic>.md`).

### 2. Plan

- Use `plan.md` as the primary planning artifact: concrete phases, files to touch, verification commands, success criteria, and notable risks or approvals.
- If the user wants plan approval, stop after updating `plan.md` and route through `plan-review` before editing code.

### 3. Implement

- Implement one meaningful phase at a time; run planned checks before advancing.
- Keep `plan.md` aligned with reality when scope, sequencing, or risks change.
- Use `files/` for checkpoints or handoffs when context gets crowded or work continues later (e.g. `files/checkpoint-<topic>.md`).

### 4. Validate

- Run the most relevant verification first (targeted), then broaden as needed.
- Compare the result against `plan.md`; call out intentional or accidental deviations.
- Record follow-ups or residual risks; save a handoff note in `files/` only when evidence needs to persist (e.g. `files/validation-<topic>.md`).

## Outputs

- A workspace `plan.md` and any necessary `files/` notes that capture the research, plan, implementation phases, and validation path.
- Implementation progress delivered one meaningful phase at a time against the documented plan.
- A validation summary comparing the final result to the plan, including residual risks, deviations, or follow-up work that must persist.


## Workflow

See the body and references for the Research -> Plan -> Implement -> Validate phases.

## Examples

See references and the skill body for rpi-workflow examples.

## Reference files

See the references/ directory and linked files in the main content.

## Guardrails

- **Must not** make code changes during the research phase.
- **Must not** treat legacy `/share` or `thoughts/shared/...` paths as the default artifact model; use workspace-local artifacts instead.
- **Must not** skip validation because the implementation appears straightforward.
- **Should** keep artifacts lean: `plan.md` for the executable plan, `files/` for research, checkpoints, and durable notes that need to persist.
- **Should** pause for approval when the user asked for plan gating, reviewer gating, or similar governance.
- **Should** prefer narrower specialist skills when a task collapses to a smaller problem after research.
- **May** reuse older shared artifacts for compatibility when a workflow already started that way, but convert back to workspace-local artifacts where practical.

## Validation

- Run the most relevant checks from `plan.md`, starting targeted and broadening when risk requires it.
- Compare the final state against the plan and call out any intentional or accidental deviations.
- Update `plan.md` or a concise `files/` handoff only when the evidence needs to persist beyond the final response.
- End with validation status, residual risks, and the next step.

## Reference files

- Read `references/examples.md` for concrete activation examples and expected behavior.
- Read `references/edge-cases.md` when the task is a near miss, becomes smaller than expected, or
  needs a mid-workflow reset.
- Read `references/prompts.md` when you want phase-by-phase starter prompts that match the native
  workspace-artifact workflow.
