# Edge cases for Research -> Plan -> Implement -> Validate (RPI-V)

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Just fix this one-line typo right now."
- "Explain what project management is."
- "Do an implementation review of the current diff only."

## Common edge cases
- For tiny one-line fixes, do not force the full RPI-V ceremony when it adds more overhead than value.
- If the user explicitly wants plan-only or review-only behaviour, combine with the more specific plan-review or implementation-review skills.
- If context grows too large, checkpoint in a workspace `files/` directory and continue rather than cramming every phase into one pass.
- If the workflow already started with legacy `/share` or `thoughts/shared/...` artifacts, you may read them, but prefer `plan.md` and `files/` for any new durable notes.

## Reminders
- If the request really matches this shape, the skill should activate: "This is a non-trivial refactor; use a research-plan-implement-validate workflow."
- If the request really matches this shape, the skill should activate: "I need a disciplined RPI-V pass on this feature, with artifacts and validation at each phase."
