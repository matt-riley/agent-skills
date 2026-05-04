---
name: reverse-prompt
description: Sharpen or rewrite a rough request into a repository-grounded brief before research, planning, or implementation. Use when the user explicitly asks for a better prompt, a sharper request, a repo-grounded brief, or a contract-shaped execution brief before the next phase.
license: Proprietary
compatibility: Agent Skills-compatible coding agents; useful before research, planning, or direct implementation when a sharper brief would materially improve execution.
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: stable
---

# Reverse prompt

## Use this skill when

- The user explicitly asks to improve, rewrite, sharpen, or reverse-prompt a request.
- The user says "before you start" or similar and wants a repo-grounded brief before planning or implementation.
- The current ask is under-specified enough that a tighter brief would materially improve speed, correctness, or completion quality.
- The user wants prompt improvement as a precursor to research, planning, or implementation.
- The user wants a definition of done, success criteria, or failure checks expressed as a sharper execution brief before work starts.
- The best next step is to turn a rough ask into a reusable execution brief with grounded file, scope, and validation details.

## Do not use this skill when

- The request is already specific enough to execute directly without a prompt rewrite pass.
- The user wants direct implementation right now and has not asked for any prompt, brief, or execution-contract rewrite first.
- The task is generic prompt-writing advice with no repository grounding or execution context.
- The behavior should be an always-on instruction or extension policy instead of a situational workflow.

## Inputs to gather

**Required before rewriting**

- The user's actual objective.
- Scope boundaries or exclusions.
- Constraints on files, behavior, tools, or rollout.
- The expected deliverable.
- Any stated approval, review, or completion rule.

**Helpful if present**

- Exact files or directories worth naming in the rewritten brief.
- Existing scripts, tests, or review gates that should shape the brief.
- The most likely next phase after rewriting: `research`, `plan`, or `implement`.
- Nearby repo conventions or instructions that should be reflected explicitly.

**Only surface as blockers when needed**

- Missing target surfaces that cannot be safely inferred.
- Conflicting goals or constraints that materially change the work.
- Missing validation expectations for work that clearly needs a completion check.

## First move

1. Identify what structure is missing from the user's current ask.
2. Ground the rewrite in repository-local specifics that can be stated safely.
3. Decide whether this is `rewrite-and-return` or `rewrite-and-proceed` before doing deeper work.

## Workflow

1. Extract the user's intent, scope, constraints, deliverable, and completion signal.
2. Use `references/decision-rules.md` to choose `rewrite-and-return`, `rewrite-and-proceed`, or blocked.
3. Fill the brief shape from `references/brief-template.md`, adding exact file or directory mentions when they are known.
4. If the user wants explicit success criteria or a reusable definition of done, switch to the contract-shaped variant in `references/contract-shaped-brief.md`.
5. Keep assumptions and blockers explicit instead of hiding them inside the rewritten brief.
6. If the task is `rewrite-and-return`, deliver the improved brief, note assumptions or blockers, and recommend the next phase.
7. If the task is `rewrite-and-proceed`, use the improved brief internally and continue into the appropriate next phase immediately.
8. If a blocking ambiguity remains after rewriting, stop at the rewritten brief plus blocker instead of forcing execution.

## Guardrails

- **Must** sharpen the request faithfully instead of inventing new requirements.
- **Must** keep the rewrite grounded in the user's ask and repository context.
- **Must not** silently start work when prompt-help intent is explicit and execution intent is absent.
- **Must not** invent new requirements just to make the brief look more formal.
- **Should** use the contract-shaped brief variant when the user explicitly wants success criteria, constraints, and checks in the rewritten prompt.
- **Should** keep the rewritten brief concise enough that it can be reused directly in a follow-up prompt.
- **Should** prefer exact file or directory mentions when they can be grounded safely.

## Validation

- Re-read the rewritten brief and confirm the next action is obvious within a few seconds.
- Confirm the dual-mode behavior in `SKILL.md` matches `references/decision-rules.md`.
- Confirm the brief shape still covers goal, constraints, deliverables, approval rule, exact files when known, assumptions, validation or checks, and recommended next phase.
- Sanity-check against the examples in `assets/examples.md`.

## Examples

- `Reverse-prompt this request for this repo, then execute it: fix the failing handler tests under @pkg/api.`
- `Improve this prompt only: audit @skills/README.md and tell me the best next prompt to use.`
- `Before you start, sharpen my prompt into a repo-grounded brief and then move into a planning pass: add a new skill under @skills/.`

## Reference files

- Read `references/brief-template.md` when you need the canonical brief shape.
- Read `references/contract-shaped-brief.md` when the user wants success criteria, definition-of-done language, or a stricter execution brief.
- Read `references/decision-rules.md` when the choice between return-only, proceed, or blocker is unclear.
- Read `assets/examples.md` when you want before/after examples or a quick sanity check for mode selection.
