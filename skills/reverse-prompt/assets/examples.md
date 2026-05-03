# Reverse prompt examples

Use these examples to keep the skill grounded in repository-local execution rather than generic prompt-writing advice.

## Prompt matrix

| Input prompt | Expected mode | Expected outcome |
| --- | --- | --- |
| `Improve this prompt only: audit @skills/README.md and tell me the best next prompt to use.` | `rewrite-and-return` | Return a concise execution brief for auditing `@skills/README.md`, plus assumptions and the recommended next phase. |
| `Rewrite this rough ask into the best executable prompt for this repository: add a skill that improves prompts before implementation.` | `rewrite-and-return` | Return a repository-shaped brief for creating a new skill, without starting the work. |
| `Before you start, sharpen my prompt into goal, constraints, deliverables, approval rule, and exact files, then move into planning mode: add a reverse-prompt skill under @skills/.` | `rewrite-and-proceed` | Produce the improved brief, note assumptions, then continue into planning. |
| `Reverse-prompt this request for this repo, then execute it: fix the TypeScript issues around @skills/.` | `rewrite-and-proceed` | Produce the improved brief, note assumptions, then continue with implementation-oriented work. |
| `Improve this prompt and then do the work: compare @instructions/ and @skills/README.md for overlap.` | `rewrite-and-proceed` | Produce the improved brief, then route into research or analysis rather than returning only a prompt. |
| `Improve this prompt and do it: update the broken workflow.` | blocked after rewrite | Return the improved brief plus a blocker because the target workflow is not known well enough to act safely. |

## Before/after sketches

### Return only

**Before**

`Improve this prompt: audit @skills/README.md`

**After**

- Goal: audit `@skills/README.md` for the requested concern
- Constraints: keep the output concise and repository-grounded
- Deliverables: a recommended next prompt or execution brief
- Approval rule: the rewritten prompt is specific enough to execute without broad clarification
- Exact files or directories: `@skills/README.md`
- Recommended next phase: `research`

### Return and proceed

**Before**

`Before you start, sharpen my prompt and then implement it: fix the TypeScript issues around @skills/`

**After**

- Goal: fix the TypeScript issues affecting `@skills/`
- Constraints: keep the change low-churn and convention-aligned
- Deliverables: code changes plus validation results
- Approval rule: relevant checks pass and the targeted issue is resolved
- Exact files or directories: `@skills/`
- Recommended next phase: `implement`

### Blocked

**Before**

`Improve this prompt and do it: update the broken workflow`

**After**

- Return a tighter execution brief
- Surface the blocker: the target workflow is not identified
- Recommend the next phase only after the workflow target is known
