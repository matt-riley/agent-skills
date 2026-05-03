# Edge cases for Database Migrations

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Design a brand new database schema from scratch."
- "Tune a slow SQL query without changing schema."
- "Explain what database normalization is."

## Common edge cases
- If the repo treats migrations as generated artifacts, follow that workflow instead of hand-authoring SQL blindly.
- If the repo is forward-only, do not promise a rollback step; describe the corrective-migration path instead.
- If the change is not persistent schema, prefer a different skill such as repository-adapters or testing-workflows.
- If state differs across environments, document the environment-specific risk before applying fixes.

## Reminders
- If the request really matches this shape, the skill should activate: "I need a new schema migration for an index and want the safe workflow for apply and recovery."
- If the request really matches this shape, the skill should activate: "Please help me troubleshoot a migration that is stuck halfway through."
