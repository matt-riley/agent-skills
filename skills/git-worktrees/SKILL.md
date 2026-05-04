---
name: git-worktrees
description: Set up and manage isolated git worktrees for parallel tasks, agent lanes, and safer branch isolation. Use when worktree setup or recovery is the real need, not generic planning or implementation guidance.
license: Proprietary
compatibility: git repositories with worktree support; useful for human or multi-agent parallel work where isolated checkouts reduce conflicts.
metadata:
  owner: mattriley
  version: 1.1.0 # x-release-please-version
  maturity: stable
---

# Git worktrees

## Use this skill when

- You need isolated workspaces for parallel changes in the same repository.
- Multiple agents or contributors may work concurrently and branch-switch churn would be risky or slow.
- You want safer experimentation while keeping the primary checkout stable.
- The user explicitly asks for a separate checkout, isolated lane, or worktree-based cleanup or recovery.

## Do not use this skill when

- You only need a single quick edit on the current branch.
- The repository is not in a usable Git state for worktree operations.
- A disposable clone is explicitly preferred over shared object storage with the main repository.
- The real task is planning, implementation, or code review and worktree setup is only incidental.

## Inputs to gather

**Required before editing**

- The base ref to branch from, such as `origin/main` or the active feature branch.
- A task identifier suitable for branch and directory naming.
- Whether the worktree is temporary, long-lived, or tied to a PR or issue.

**Helpful if present**

- Existing branch naming conventions.
- Preferred worktree root location for the repository.
- Local cleanup expectations for stale worktrees.

**Only investigate if encountered**

- Submodule, sparse checkout, or filesystem constraints that affect worktree behavior.
- Branch-name collisions because the same branch is already checked out elsewhere.
- Recovery needs for stale registrations, missing directories, or removal blocked by local changes.

## First move

1. Inspect current worktrees and branch state.
2. Pick names using repository conventions or the defaults in `assets/naming-examples.md`.
3. Create or recover the isolated worktree before making task changes.

## Workflow

1. Check the current repository state with `git worktree list` and branch visibility with `git branch --all`.
2. Fetch and verify the intended base ref before branching from it.
3. Choose a worktree path and branch name that match the task and repository conventions.
4. Create a dedicated branch and worktree for the task.
5. Perform all edits, tests, and commits inside that worktree rather than the primary checkout.
6. If the worktree is stale, misconfigured, or ready to retire, follow `references/recovery-and-cleanup.md`.
7. After the task is merged or no longer needed, clean up the worktree deliberately.

## Guardrails

- **Must** use one active worktree per independent task when isolation is the reason this skill was selected.
- **Must** verify the current directory and branch before applying changes.
- **Must not** remove a worktree without checking for uncommitted changes first.
- **Should** use consistent naming defaults, but adapt to repository conventions when they differ.
- **Should** run the task's validation commands from inside the worktree that owns the changes.
- **May** keep long-lived worktrees for release or maintenance branches when the workflow benefits.

## Validation

- Confirm `git worktree list` shows the expected paths and branches.
- Confirm `git status` reflects the intended branch and checkout inside the worktree.
- Run relevant repository checks from inside the worktree used for the task.
- Verify the worktree is clean before removal and prune stale metadata afterward when needed.

## Examples

- `Set up a separate worktree for this bug fix so it does not collide with release prep.`
- `Create one worktree per agent for parallel PR work, then clean them up safely afterward.`
- `Recover a worktree that points to the wrong branch without losing local edits.`

## Reference files

- Read `assets/naming-examples.md` when you need default branch and path naming patterns.
- Read `references/recovery-and-cleanup.md` when a worktree is stale, on the wrong branch, or ready to be removed.
