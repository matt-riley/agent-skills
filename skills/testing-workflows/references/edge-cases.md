# Edge cases for Testing Workflows

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Design an entirely new test framework."
- "Explain TDD in theory only."
- "Review a finished implementation diff."

## Common edge cases
- If the issue is pure code generation drift, address that before spending time on unrelated test debugging.
- If optional databases are unavailable, prefer skip behaviour over treating every missing backend as a hard failure.
- Do not use this skill for HTTP integration-only work when the dedicated integration-testing-http skill is a better fit.

## Reminders
- If the request really matches this shape, the skill should activate: "Run the tests for this Go project and help me debug the failure in the right order."
- If the request really matches this shape, the skill should activate: "I changed repositories and handlers; what tests should I add before merging?"
