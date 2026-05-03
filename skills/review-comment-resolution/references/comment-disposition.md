# Comment disposition

Use this guide before changing code so reviewer feedback is handled deliberately rather than mechanically.

## Valid

Treat a comment as valid when:

- the reviewer identified a real bug, correctness gap, unsafe assumption, or missing test
- the concern still applies to the current diff
- the requested direction is compatible with the repository's patterns

Action:

- fix it directly
- keep the change as small as possible
- add or adjust validation when the concern is regression-prone

## Partially valid

Treat a comment as partially valid when:

- the underlying concern is real, but the suggested fix is too broad or slightly off
- the comment points at a symptom rather than the root cause

Action:

- fix the real problem, not necessarily the exact wording of the suggestion
- be ready to explain the narrower implementation choice afterward

## Not valid

Treat a comment as not valid when:

- the code already handles the concern correctly
- the suggestion would break established behavior or conflict with repository conventions
- the reviewer likely missed adjacent context, tests, or constraints

Action:

- do not make the change
- keep a concise evidence-backed rationale for the final summary or follow-up reply if needed

## Superseded

Treat a comment as superseded when:

- the code has already changed since the comment was written
- another fix in the batch already addresses the concern

Action:

- avoid duplicating the change
- note that the concern is already covered by the current head state

## Not actionable yet

Treat a comment as not actionable yet when:

- it depends on missing product direction or broader architectural approval
- it requires a scope increase that the user did not ask for
- it belongs in a follow-up issue rather than this review-fix batch

Action:

- avoid speculative implementation
- record the blocker or follow-up recommendation clearly
