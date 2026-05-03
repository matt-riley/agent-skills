# Reviewer prompt template

Use this template when the user asks for implementation review, named reviewer models, or unanimous approval before changes are considered done.

## Reviewer prompt

```text
Review the current implementation and diff for correctness, repo fit, validation coverage, regression risk, rollout safety, and scope discipline.

Return exactly:
1. Verdict: APPROVE or REQUEST_CHANGES
2. Required changes
3. Optional suggestions
4. Approval rationale

Focus on materially important issues only. Do not nitpick style.

Context:
- Repo: <repo>
- User goal: <goal>
- Constraints: <constraints>
- Review target: <branch / PR / commit / diff path>
- Validation status: <tests, build, lint, manual checks>
- Plan or requirements: <path or summary, if available>
- Approval rule: all required reviewers participate in every round; the implementation is not final until every required reviewer approves
```

## Consolidation rules

- Treat `REQUEST_CHANGES` as blocking.
- Merge duplicate findings across reviewers before revising the code or summary.
- Preserve reviewer-specific concerns when they are materially different.
- After revising the implementation, send the updated revision back to the full reviewer set.
