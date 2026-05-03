# Contract spec

Use the stable frontmatter keys and headings from this spec. Do not rename fields ad hoc.

## Shared frontmatter

Every `v1` contract uses these keys:

- `contract_type`
- `contract_version`
- `created_by`
- `status`

## Planner handoff

Use for planner-to-executor or research-to-executor handoffs.

Required frontmatter:

- shared frontmatter
- `task_id`
- `parallelizable`
- `worktree_required`

Status values:

- `draft`
- `ready`
- `blocked`

Required headings:

- `## goal`
- `## files_in_scope`
- `## constraints`
- `## verification_commands`
- `## acceptance_criteria`
- `## artifact_outputs`

## Review outcome

Use for reviewer responses that must be machine-decidable without re-reading free-form prose.

Required frontmatter:

- shared frontmatter

Status values:

- `approve`
- `revise`
- `blocked`

Required headings:

- `## critical_issues`
- `## evidence`
- `## next_action`

## Execution record

Use for implementation-phase handoffs and verification summaries.

Required frontmatter:

- shared frontmatter
- `task_id`

Status values:

- `in_progress`
- `blocked`
- `done`

Required headings:

- `## goal`
- `## changes_made`
- `## verification_commands`
- `## validation_results`
- `## remaining_blockers`
- `## next_action`

## Extension rule

Optional sections may be added after the required headings when a task genuinely needs them, but the required headings must stay present and in the same names.
