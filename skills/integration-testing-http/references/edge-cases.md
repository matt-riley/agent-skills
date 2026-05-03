# Edge cases for Integration Testing HTTP

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write a unit test for a pure function."
- "Design a brand new API without tests."
- "Review implementation approval workflow."

## Common edge cases
- If the change is domain logic only, the test strategy may belong in testing-workflows rather than integration-testing-http.
- If the repo has no integration suite, stop and identify the nearest existing test harness instead of inventing one.
- If a generated API client or spec is involved, coordinate with http-api-openapi or code-generation rather than treating the route in isolation.

## Reminders
- If the request really matches this shape, the skill should activate: "I changed an HTTP handler and need to extend the end-to-end integration tests."
- If the request really matches this shape, the skill should activate: "Run the HTTP integration tests and help me debug a failing middleware/auth case."
