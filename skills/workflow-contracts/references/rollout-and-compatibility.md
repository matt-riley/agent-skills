# Rollout and compatibility

Use these rules during the `v1` migration.

## Current rollout rules

1. Define the `v1` planner handoff, review outcome, and execution record templates before teaching other agents or skills to rely on them.
2. Prefer `v1` structured markdown for all new or revised artifacts.
3. Accept legacy prose artifacts as input during migration, but map them into the `v1` headings before handing them off downstream.
4. Do not make `v1` the default expectation in always-on instructions until:
   - the templates exist
   - the planner, research, and skill-authoring surfaces are updated
   - at least one end-to-end dry run succeeds
5. If mixed old/new artifact shapes start causing confusion, pause instruction cleanup and finish the contract migration first.

## Cutover checkpoint

The first-wave cutover is ready only when:

- all three `v1` templates exist
- downstream agent or skill docs point to them
- one dry-run planning-to-review or planning-to-execution flow succeeds with no missing required fields
- the remaining always-on guidance does not duplicate the moved artifact-shape rules
