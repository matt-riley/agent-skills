# Edge cases for Repository Adapters

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Design a new database schema migration."
- "Write an HTTP handler for this endpoint."
- "Explain repository patterns in abstract terms only."

## Common edge cases
- If the change really belongs in the domain service or schema migration layer, stop and redirect rather than forcing it into the adapter.
- If the repo has generated queries or ORM code, coordinate with code-generation rather than editing generated files directly.
- If the interface contract must change, update consumers deliberately instead of silently widening adapter behavior.

## Reminders
- If the request really matches this shape, the skill should activate: "Add a new repository method in the DB adapter and map DB errors to domain errors correctly."
- If the request really matches this shape, the skill should activate: "I changed a query and need to keep the adapter aligned with the domain interface."
