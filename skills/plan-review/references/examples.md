# Examples for Plan review

Use these as concrete patterns when the skill should activate.

## Example 1 - Approval Gated Plan

User says: "Create and review an implementation plan with named reviewers, and do not move to implementation until everyone approves."

Expected behaviour:
- The response drafts or updates the plan, gathers repo context, uses the reviewer prompt consistently, and blocks implementation until unanimous approval.
Key checks:
- Mentions plan artifact or plan revision.
- Mentions reviewer set or unanimous approval.
- States implementation should wait for approval.

## Example 2 - Strong Plan Criteria

User says: "Review this plan for feasibility, validation coverage, and scope discipline."

Expected behaviour:
- The response checks repo fit, validation commands, risks, and scope boundaries rather than only rephrasing the plan.
Key checks:
- Mentions validation strategy.
- Mentions scope or risk control.
- Focuses on executable plan quality.
