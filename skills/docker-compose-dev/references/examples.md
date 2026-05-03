# Examples for Docker Compose Dev

Use these as concrete patterns when the skill should activate.

## Example 1 - Compose Startup

User says: "I want a local stack with the app and its database using docker compose. What is the workflow?"

Expected behaviour:
- The response gives a compose-oriented bring-up flow, mentions common operations, and includes a health/verification step.
Key checks:
- Mentions compose bring-up commands or equivalent operations.
- Mentions verification of service health.
- Mentions troubleshooting or invariants for the stack.

## Example 2 - Compose Debug

User says: "The compose stack starts but the app cannot reach the database. What should I check?"

Expected behaviour:
- The response focuses on compose service health, networking, env/config, and service logs rather than generic app debugging only.
Key checks:
- Mentions compose-level debugging such as logs or service status.
- Mentions the database/backend dependency explicitly.
- Includes a concrete next-step checklist.
