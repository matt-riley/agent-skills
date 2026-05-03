# Examples for Example Skill

Replace these placeholders with concrete prompts that should trigger the real skill.

## Example 1 - Primary happy path

User says: "Help me `<primary task>`."

Expected behaviour:
- The response follows the skill's workflow instead of generic advice.
- The response uses the local guardrails and validation guidance captured in `SKILL.md`.

Key checks:
- Mentions the core workflow this skill owns.
- Mentions the main validation step.
- Stays inside this skill's boundary instead of spilling into a nearby skill.

## Example 2 - Adjacent but still in scope

User says: "I need `<adjacent in-scope variant>`."

Expected behaviour:
- The response still activates this skill because the distinguishing condition is present.

Key checks:
- Names the condition that keeps the request inside this skill.
- Avoids broadening the skill into unrelated nearby work.
