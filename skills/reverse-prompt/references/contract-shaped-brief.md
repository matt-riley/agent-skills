# Contract-shaped brief

Use this file when the user wants a sharper execution brief with explicit success criteria rather than a loose prompt.

## Template

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

## When to use it

- The user asks for a better prompt plus explicit success criteria.
- The user wants a definition of done before planning or implementation.
- The user asks for a reusable execution brief, not just free-form prompt cleanup.

## Guardrails

- Keep the brief concrete and testable.
- Preserve the user's actual objective instead of inventing new work.
- If a condition cannot be verified yet, say so explicitly rather than pretending it passed.
