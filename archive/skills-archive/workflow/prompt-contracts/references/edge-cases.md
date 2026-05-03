# Edge cases for Prompt contracts

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Just implement the fix right now and keep it simple."
- "Explain what a legal contract is."
- "Have multiple agents debate this design."

## Common edge cases
- If the user already provided a partial contract, normalize and tighten it instead of rewriting from scratch.
- If GOAL and CONSTRAINTS conflict, surface the contradiction explicitly before execution.
- If a FAILURE condition cannot be verified mechanically, label it `UNVERIFIABLE` rather than pretending it passed.
- If the task is tiny, use a minimal contract or say the full ceremony is unnecessary.

## Reminders
- If the request really matches this shape, the skill should activate: "Write a prompt contract for this change, including failure conditions."
- If the request really matches this shape, the skill should activate: "Define the success criteria and definition of done before we implement this."
