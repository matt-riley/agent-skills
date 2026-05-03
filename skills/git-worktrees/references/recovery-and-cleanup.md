# Git worktrees recovery and cleanup

Use this reference when a worktree is stale, misconfigured, or ready to retire.

## Quick diagnostics

```bash
git worktree list --porcelain
git status
git branch --all
```

## Common recovery cases

### Worktree path was deleted manually

1. Remove stale registration:
   ```bash
   git worktree prune
   ```
2. Confirm the list is clean:
   ```bash
   git worktree list
   ```

### Worktree exists but is on the wrong branch

1. Enter the worktree directory.
2. Check for uncommitted changes:
   ```bash
   git status
   ```
3. If clean, switch branch:
   ```bash
   git switch <expected-branch>
   ```
4. If not clean, commit or stash before switching.

### Branch already checked out in another worktree

Git blocks duplicate branch checkout across worktrees.

- Either create a new branch for this worktree:
  ```bash
  git switch -c <new-branch>
  ```
- Or use the existing worktree already attached to that branch.

### Failed removal due to uncommitted changes

1. Inspect pending changes:
   ```bash
   git status
   ```
2. Commit, stash, or intentionally discard changes.
3. Remove the worktree:
   ```bash
   git worktree remove <path>
   ```

## Safe cleanup sequence

1. Verify the branch has been pushed or merged if needed.
2. Ensure the worktree is clean with `git status`.
3. Remove the worktree path:
   ```bash
   git worktree remove <path>
   ```
4. Optionally delete the merged branch:
   ```bash
   git branch -d <branch>
   ```
5. Prune stale metadata:
   ```bash
   git worktree prune
   ```
