# Edge cases for Observability Metrics

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Explain Prometheus from first principles."
- "Set up Docker Compose for local development."
- "Write a new logging framework."

## Common edge cases
- If the service intentionally hides metrics in local or test environments, document that behavior instead of assuming exposure is broken.
- If the endpoint requires auth, validate access control along with content.
- Do not use this skill for unrelated application business logic debugging.

## Reminders
- If the request really matches this shape, the skill should activate: "Validate the /health and /metrics endpoints after I changed observability code."
- If the request really matches this shape, the skill should activate: "I added a metric and need to confirm it appears locally without exposing sensitive data."
