# Filled contract examples

These examples show concrete `v1` artifacts with real values instead of placeholder ellipses.

## Planner handoff example

```md
---
contract_type: planner-handoff
contract_version: v1
created_by: implementation-planner
status: ready
task_id: wave2-exemplar-workflow-review
parallelizable: false
worktree_required: true
---

# Planner handoff v1

## goal

- Turn the three exemplar skills into clearer portfolio examples without expanding scope beyond the assigned directories.

## files_in_scope

- skills/github-actions-failure-triage/SKILL.md
- skills/github-actions-failure-triage/references/triage-scenarios.md
- skills/workflow-contracts/SKILL.md
- skills/workflow-contracts/references/examples.md
- skills/review-comment-resolution/SKILL.md
- skills/review-comment-resolution/references/comment-disposition.md

## constraints

- Stay inside the assigned skill packages.
- Keep the existing shallow reference structure intact.
- Prefer direct edits to current files over new assets unless the new file materially improves the example surface.

## verification_commands

- `node skills/workflow-contracts/scripts/validate-contracts.mjs skills/workflow-contracts/assets/planner-handoff-v1.md`
- `git diff --check`

## acceptance_criteria

- Each exemplar skill has a concrete top-level example or appendix.
- The workflow-contracts examples clearly show filled frontmatter and body sections.
- Validation remains aligned with the contract spec.

## artifact_outputs

- Updated skill docs and references ready for follow-on review.
```

## Review outcome example

```md
---
contract_type: review-outcome
contract_version: v1
created_by: reviewer-name
status: revise
---

# Review outcome v1

## critical_issues

- The planner handoff template still uses placeholder ellipses under `## artifact_outputs`.

## evidence

- `assets/planner-handoff-v1.md` still shows `- ...` under `## artifact_outputs`, so the packaged template is not ready for direct handoff use.

## next_action

- Replace the placeholder artifact output with a concrete file list and re-run the contract validator on the touched template.
```

## Execution record example

```md
---
contract_type: execution-record
contract_version: v1
created_by: implementing-agent
status: done
task_id: wave2-exemplar-workflow-review
---

# Execution record v1

## goal

- Add concrete examples for the workflow-contracts skill and tighten the other two exemplar skills with minimal scope.

## changes_made

- Added a filled planner handoff and review outcome example.
- Added a reusable examples reference for the contract templates.
- Added a compact failure-bucket appendix and scenario matrix for GitHub Actions triage.
- Added an explicit unresolved-comment summary shape for review-comment resolution.

## verification_commands

- `node skills/workflow-contracts/scripts/validate-contracts.mjs skills/workflow-contracts/assets/execution-record-v1.md`
- `git diff --check`

## validation_results

- The example artifacts now show concrete values and preserve the required `v1` headings.

## remaining_blockers

- None for the scope of the exemplar update.

## next_action

- Review the updated skill docs and commit the wave 2 slice.
```
