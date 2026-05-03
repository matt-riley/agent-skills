# Edge cases for Stochastic multi-agent consensus

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Have three agents debate this together over several rounds."
- "Write a prompt contract for this project."
- "Explain what consensus means in philosophy."

## Common edge cases
- Use an odd sample size for binary decisions when possible.
- If the schema is too loose to aggregate mechanically, tighten it before launching agents.
- If one sample fails or goes off-topic, exclude it and report the effective N.
- For codebase lookup or evidence gathering, `explore` may be a better agent type than `general-purpose`.

## Reminders
- If the request really matches this shape, the skill should activate: "Poll several agents independently and tell me the consensus."
- If the request really matches this shape, the skill should activate: "Use stochastic consensus to compare these options and surface the outliers."
