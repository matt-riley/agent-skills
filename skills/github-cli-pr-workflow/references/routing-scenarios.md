# Routing scenarios

Use this table to keep boundaries clear with nearby skills.

| User intent | Route |
| --- | --- |
| "Create a PR and wait for checks." | `github-cli-pr-workflow` |
| "Update PR title/body and confirm status." | `github-cli-pr-workflow` |
| "Why did this Actions job fail?" | `github-actions-failure-triage` |
| "Address reviewer comments and push fixes." | `review-comment-resolution` |
| "Decide merge vs PR vs keep vs discard." | `finishing-a-development-branch` |
| "Set up a worktree lane before starting." | `git-worktrees` or `worktrunk` |

## Escalation cues

- If checks fail and root cause is unknown, hand off immediately to `github-actions-failure-triage`.
- If comments are already open and need acceptance/rejection decisions, hand off to `review-comment-resolution`.
- If implementation is complete and branch fate is undecided, hand off to `finishing-a-development-branch`.
