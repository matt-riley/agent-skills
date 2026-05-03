# Edge cases for Ci Images

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write me a Dockerfile for a Go app."
- "Explain what CI means in software delivery."
- "Set up docker compose for local development."

## Common edge cases
- Do not use this skill for general Dockerfile authoring or docker-compose setup; those are different workflows.
- If the repository has no container publishing path, stop after documenting the missing release contract instead of inventing one.
- If CI commands differ from the documented local equivalents, prefer the repository source of truth and update the checklist.

## Reminders
- If the request really matches this shape, the skill should activate: "I changed generation and Docker tags; can you tell me if CI and image publishing are ready?"
- If the request really matches this shape, the skill should activate: "Before I cut a release, run the local equivalents of the CI checks and verify image tags."
