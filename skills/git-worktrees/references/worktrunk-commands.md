# Worktrunk command equivalents

Quick mapping from raw `git worktree` commands to Worktrunk (`wt`) equivalents.

Use `wt` when it is installed (`wt --version`) — it fires hooks, tracks lifecycle, and provides richer status than raw git.

| Task | Raw git | Worktrunk |
|------|---------|-----------|
| Create worktree | `git worktree add -b feat .worktrees/feat origin/main && cd .worktrees/feat` | `wt switch --create feat` |
| Create from specific base | `git worktree add -b feat .worktrees/feat origin/release` | `wt switch --create feat --base origin/release` |
| List worktrees | `git worktree list` | `wt list` (adds CI status, ahead/behind, agent markers) |
| List with full status | n/a | `wt list --full` (CI, line diffs, LLM summaries) |
| Remove worktree + branch | `git worktree remove .worktrees/feat && git branch -d feat` | `wt remove` (from inside worktree) or `wt remove feat` |
| Merge + cleanup | manual: squash, rebase, ff, branch delete | `wt merge [target]` (one command) |
| Commit with AI message | n/a | `wt step commit` |
| Squash commits | manual | `wt step squash` |
| View live agent state | n/a | `wt list` (shows 🤖/💬 markers) |
| Switch to existing worktree | `cd <path>` | `wt switch <branch>` |
| Switch interactively | n/a | `wt switch` (opens picker with diff preview) |
| PR checkout | `gh pr checkout 123` | `wt switch pr:123` |

## Notes

- Worktrunk computes worktree paths from a template in `~/.config/worktrunk/config.toml`. The default is a sibling directory (`../repo.branch-name`). For agent harness compatibility, set: `worktree-path = "{{ repo_path }}/.worktrees/{{ branch | sanitize }}"`..
- `wt merge` defaults to squash mode, which requires `[commit.generation]` config. Pass `--no-squash` when not configured.
- All `wt` commands accept `-C <path>` to set the working repository root.
- See the `worktrunk` skill for hooks, LLM commit setup, and parallel agent recipes.
