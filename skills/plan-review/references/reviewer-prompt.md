# Reviewer prompt template

Use this template when the user asks for plan review, named reviewer models, or unanimous plan approval.

## Reviewer prompt

```text
Review the current implementation plan for correctness, repo fit, validation coverage, rollout safety, and scope discipline.

Return exactly:
1. Verdict: APPROVE or REQUEST_CHANGES
2. Required changes
3. Optional suggestions
4. Approval rationale

Focus on materially important gaps only. Do not nitpick style.

Context:
- Repo: <repo>
- User goal: <goal>
- Constraints: <constraints>
- Plan revision: <revision or path>
- Approval rule: all required reviewers participate in every round; the plan is not final until every required reviewer approves
```

## Consolidation rules

- Treat `REQUEST_CHANGES` as blocking.
- Merge duplicate findings across reviewers before revising the plan.
- Preserve reviewer-specific concerns when they are materially different.
- After revising the plan, send the updated revision back to the full reviewer set.
