# Edge cases for Docker Compose Dev

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write a Kubernetes deployment manifest."
- "Explain what containers are."
- "Add a database migration for a new table."

## Common edge cases
- If the repo has no compose files, stop and report that instead of inventing a stack.
- If a lighter local test path already exists, only use compose when the real multi-service backend is actually needed.
- Do not use this skill for production deployment orchestration.

## Reminders
- If the request really matches this shape, the skill should activate: "Spin up the app plus database locally with Docker Compose so I can reproduce production-like behavior."
- If the request really matches this shape, the skill should activate: "Help me bring up the compose stack and verify the service is healthy."
