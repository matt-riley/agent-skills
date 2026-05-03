# Edge cases for Agent chatrooms

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Poll 10 agents independently and tell me the consensus."
- "Explain how multi-agent systems work in general."
- "Just review this implementation yourself without extra agents."

## Common edge cases
- If the user names roles, use them exactly rather than normalizing them away.
- If the debate question is vague, sharpen the decision target before spawning agents.
- If one agent goes off the rails, exclude it from the synthesis and note the effective panel size.
- If the room converges after the first round, stop early instead of forcing extra turns.

## Reminders
- If the request really matches this shape, the skill should activate: "Let three agents debate this architecture decision and give me the synthesis."
- If the request really matches this shape, the skill should activate: "Use an agent chatroom to pressure-test this design from different roles."
