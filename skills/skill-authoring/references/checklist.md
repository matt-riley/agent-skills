# Skill checklist

Use this checklist before considering a skill complete.

## Structure

- `SKILL.md` exists.
- Frontmatter includes `name` and `description`.
- The `name` matches the parent directory name.
- If nearby skills use shared metadata fields, the new skill follows that local convention consistently.
- If the skill uses `metadata.kind`, the value matches the package behavior.
- The main file is concise and easy to scan.
- The package shape is predictable enough that a future scaffolding or validation tool would not need to guess where things belong.

## Activation and workflow

- The skill clearly says when to use it.
- The skill clearly says when not to use it, if overlap is likely.
- The description includes specific trigger phrases (not just a domain label) and leans toward over-triggering. It includes at least one disambiguator to avoid crowding adjacent skills.
- Inputs are clear enough for an agent to gather what it needs.
- The first move is obvious.
- The workflow is sequential and actionable.
- Outputs or end-state expectations are explicit enough for the skill kind.
- Section headings are stable enough to find the activation, workflow, validation, and support-file guidance quickly.

## Progressive disclosure

- Detailed mappings, checklists, or examples live in `references/` or `assets/` instead of bloating `SKILL.md`.
- Every support file is referenced from `SKILL.md`.
- Any scripts are optional and clearly documented.
- Support-file names and paths are explicit enough that a future tool could discover them without guessing.

## Quality

- The wording stays generic at the intended user level.
- Guardrails prevent common failure modes.
- Validation steps tell an agent how to check its own work.
- Task skills declare outputs, artifacts, or end-state expectations plus validation.
- Reference skills make the lookup value, examples, and support-file navigation obvious.
- Examples look like realistic user requests rather than abstract labels.
- The skill uses the smallest stable structure that still leaves room for future tool-assisted authoring.
- A two-prompt smoke-test (one request that should trigger the skill, one near-miss that should not) confirms the description alone distinguishes between them without needing to read the SKILL.md body.
