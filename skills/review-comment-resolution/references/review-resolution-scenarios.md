# Review resolution scenarios

Use these compact scenarios to keep review-comment routing, disposition, and handoff behavior consistent.

| Scenario | Correct disposition | Expected move |
| --- | --- | --- |
| Reviewer flags a real null-check bug in the touched code path. | valid | Fix the smallest root cause, then run the relevant validation. |
| Reviewer suggests a naming/style tweak with no correctness impact. | not actionable yet | Defer the naming concern to a follow-up and explain that it is not merge-blocking for this batch. |
| The real blocker is a failed workflow job, not the review comment itself. | not actionable yet | Route to `github-actions-failure-triage` before editing review feedback. |
| Another fix in the branch already removed the commented line. | superseded | Avoid duplicating work and note that the concern is already covered. |
| The comment asks for a broader architecture change the user did not request. | not actionable yet | Escalate or defer instead of widening the review-fix batch. |
| The comment has a real bug plus an unrelated style nit. | partially valid | Fix the bug, skip the extra style-only ask, and explain the narrower change. |

## Maintenance loop

- Update this file whenever the review-resolution routing, disposition categories, or escalation boundary changes.
- If the workflow starts expecting a new handoff or validation step, add one scenario before expanding `SKILL.md`.
