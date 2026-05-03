# Worktree and branch naming examples

These are defaults, not fixed requirements. Prefer repository conventions when they differ.

## Default pattern

- Worktree path: `.worktrees/<task-id>`
- Branch name: `task/<task-id>`

## Task ID guidelines

Choose task IDs that are:

- lowercase
- filesystem-safe
- stable over the task lifetime
- short but descriptive

## Example mappings

| Scenario | Task ID | Worktree path | Branch name |
| --- | --- | --- | --- |
| Bug fix from issue tracker | `issue-812-auth-timeout` | `.worktrees/issue-812-auth-timeout` | `task/issue-812-auth-timeout` |
| CI migration spike | `gha-cache-parity` | `.worktrees/gha-cache-parity` | `task/gha-cache-parity` |
| Release hotfix | `hotfix-v2-4-1-login` | `.worktrees/hotfix-v2-4-1-login` | `task/hotfix-v2-4-1-login` |
| Docs-only update | `docs-api-onboarding` | `.worktrees/docs-api-onboarding` | `task/docs-api-onboarding` |

## Alternative branch prefixes

If the repository uses a different branch taxonomy, keep `<task-id>` and swap the prefix:

- `agent/<task-id>`
- `feature/<task-id>`
- `chore/<task-id>`
- `fix/<task-id>`
