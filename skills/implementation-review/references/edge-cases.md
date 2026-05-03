# Edge cases for Implementation review

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Create an implementation plan for a feature."
- "Explain how pull request reviews work in general."
- "Write new code for the feature instead of reviewing it."

## Common edge cases
- If the implementation is still changing, freeze the reviewed revision before asking for approval.
- If the user asks only for review comments, do not silently escalate to approval-gated completion unless requested.
- If validation is missing, report that gap explicitly rather than implying readiness.

## Reminders
- If the request really matches this shape, the skill should activate: "Review the current implementation and tell me if it is ready to merge."
- If the request really matches this shape, the skill should activate: "Run an implementation review with named reviewers and block until every reviewer approves."
