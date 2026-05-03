# Reverse prompt brief template

Use this template when rewriting a rough ask into a concise execution brief.

## Canonical brief

```md
Goal:
- <what should happen>

Constraints:
- <behavioral, file, tooling, or rollout constraints>

Deliverables:
- <what the agent should produce>

Approval rule:
- <what must be true before the work is considered complete>

Exact files or directories:
- <@file or @dir references when known>

Assumptions:
- <safe assumptions the agent is making>

Validation or checks:
- <commands, tests, review gates, or other completion checks when known>

Recommended next phase:
- <research | plan | implement>
```

## Usage notes

- Prefer exact `@` file or directory references when they can be grounded safely.
- Keep the brief short enough that it can be reused directly in a follow-up prompt.
- If exact files are unknown but not blocking, say so plainly instead of inventing targets.
- If a blocker remains, keep it outside the brief body so it is easy to act on separately.
