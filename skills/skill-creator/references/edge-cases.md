# Edge cases for Skill Creator

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Use an existing skill to solve a task right now instead of creating one."
- "Explain the history of agent tooling in general."
- "Review an implementation diff rather than authoring a skill."

## Common edge cases
- Do not add scripts or assets by default; add them only when deterministic validation or repeated logic clearly justifies them.
- If a skill already works well and only lacks measurement, prefer evals and references before rewriting the whole body.
- If the proposed metadata or directory convention conflicts with the active spec/tooling, resolve that compatibility gap first.

## Reminders
- If the request really matches this shape, the skill should activate: "Create a new skill for working with Cloudflare D1 migrations and include evals."
- If the request really matches this shape, the skill should activate: "Update an existing skill so it has better metadata, examples, and trigger coverage."
