# Edge cases for Plan review

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Review the finished code diff."
- "Explain what project planning means."
- "Implement the feature now instead of planning it."

## Common edge cases
- If the user asks for a plan but not reviewer gating, still improve the plan, but do not invent approval rules they did not request.
- If the repo already has a current plan artifact, update that revision instead of starting from scratch.
- If requirements are still ambiguous, resolve the ambiguity in the plan before treating it as executable.

## Reminders
- If the request really matches this shape, the skill should activate: "Create a plan for this change and do not consider it final until the reviewers approve it."
- If the request really matches this shape, the skill should activate: "Review and harden my implementation plan with named reviewer models."
