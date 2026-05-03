# Edge cases for Code Generation

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Design a new protobuf schema from scratch."
- "Explain what code generation is."
- "Run the unit tests and debug the failure only after the app already builds."

## Common edge cases
- If the repo has no generate target, identify the actual generator command instead of assuming make generate exists.
- If the repo ignores generated output or regenerates it in CI, validate locally without assuming the files belong in Git.
- If generator tooling is missing, document the install/recovery path but do not rewrite generated files manually.
- If no generator-backed inputs changed, do not force unnecessary regeneration as the first step.

## Reminders
- If the request really matches this shape, the skill should activate: "I changed sqlc queries and templ files; regenerate whatever is needed before I test."
- If the request really matches this shape, the skill should activate: "The build is failing in generated packages. Can you first figure out the repo's generation workflow and whether output should be committed?"
