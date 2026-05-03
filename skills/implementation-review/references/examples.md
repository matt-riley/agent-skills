# Examples for Implementation review

Use these as concrete patterns when the skill should activate.

## Example 1 - Review With Panel

User says: "Please review this implementation with named reviewers and do not consider it done until every reviewer approves."

Expected behaviour:
- The response identifies the review target, gathers validation context, uses the reviewer panel consistently, and blocks completion until all required reviewers approve.
Key checks:
- Mentions reviewer set or approval gate.
- Mentions validation status before approval.
- Treats requested changes as blocking.

## Example 2 - Review Focus

User says: "Do a code review focused on correctness and regression risk, not style nitpicks."

Expected behaviour:
- The response scopes the review to material issues such as correctness, validation gaps, rollout safety, and regressions.
Key checks:
- Focuses on materially important issues.
- Avoids style nitpicks as the primary output.
- Mentions validation or rollout safety.
