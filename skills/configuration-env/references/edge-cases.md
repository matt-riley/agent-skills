# Edge cases for Configuration Env

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Set up Docker Compose for local Postgres."
- "Write a secrets manager from scratch."
- "Explain the theory behind environment variables."

## Common edge cases
- If the repo has no `.env.example`, use the README or config loader as the source of truth instead of inventing variable names.
- If the real issue is a repo-owned runtime config file rather than an env var, stay in scope: missing Worker bindings, `wrangler` config drift, and similar startup-contract problems still belong here.
- If the service has no `/health` endpoint, validate configuration with the closest existing startup check instead of assuming one exists.
- Do not use this skill for secret rotation policy or cloud IAM design; keep it focused on application configuration and environment loading.

## Reminders
- If the request really matches this shape, the skill should activate: "The server will not start locally; help me verify the env vars and .env setup."
- If the request really matches this shape, the skill should activate: "I need to bootstrap a new developer environment from .env.example and validate it safely."
