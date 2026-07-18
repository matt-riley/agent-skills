---
name: git-worktrees
description: "Set up and manage isolated git worktrees for parallel tasks, agent lanes, and safer branch isolation. Use when worktree setup or recovery is the real need, not generic planning or implementation guidance."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  category: git
  audience: general-coding-agent
  maturity: stable
  kind: task
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
- The task is only PR lifecycle work (create/update PR and watch checks) on an already prepared branch; route to [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md).

## Inputs to gather

**Required before editing**

- Base ref to branch from (for example `origin/main`).
- Task identifier suitable for branch and directory naming.
- Whether this worktree is temporary, long-lived, or tied to a PR/issue.

**Helpful if present**

- Existing branch naming conventions.
- Preferred worktree root location for the repository.
- Local cleanup expectations for stale worktrees.
- Repo shape details such as monorepo package paths, submodules, sparse checkout, or nested worktrees.

**Only investigate if encountered**

- Submodule, sparse checkout, or filesystem constraints that affect worktree behavior.
- Branch-name collisions because the same branch is already checked out elsewhere.
- Recovery needs for stale registrations, missing directories, or removal blocked by local changes.
- Detached HEADs or platform-specific filesystem constraints.

## First move

0. Check if Worktrunk is installed: `wt --version`. If available (exit code 0), prefer `wt` commands throughout this workflow — see [Worktrunk command equivalents](references/worktrunk-commands.md).
1. Inspect current worktrees and branch state (`git worktree list` and `git branch --all`).
2. Pick names using repository conventions or the defaults in `assets/naming-examples.md`.
3. Create or recover the isolated worktree before making task changes.

## Workflow

### With Worktrunk installed (`wt --version` succeeds)

1. Fetch and verify the intended base ref.
2. Create worktree: `wt switch --create <branch> --base <ref>` — fires `post-start` hooks automatically (deps install, dev server, etc).
3. Perform all edits, tests, and commits inside that worktree.
4. Commit with LLM message (if configured): `wt step commit`.
5. Merge when ready: `wt merge [target]` — squashes, rebases, validates via pre-merge hooks, fast-forwards, and cleans up. Add `--no-squash` if `[commit.generation]` is not configured.
6. Or: push and open PR, then `wt remove` after the PR is merged.

See [Worktrunk command equivalents](references/worktrunk-commands.md) and the `worktrunk` skill for hooks, LLM commits, and parallel agent recipes.

### Without Worktrunk (raw git fallback)

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
- **Should** keep branch names and worktree paths aligned so the branch name still makes sense if the worktree path is copied or recreated later.
- **Should** verify the repository root before creating the worktree in monorepos or nested checkouts.
- **Should** run the task's validation commands from inside the worktree that owns the changes.
- **May** keep long-lived worktrees for release or maintenance branches when the workflow benefits.
- **Should** use `wt switch --create` / `wt remove` instead of `git worktree add` / `git worktree remove` when Worktrunk is installed, so project hooks fire and worktree lifecycle is tracked.

## Validation

- Confirm `git worktree list` shows the expected paths and branches.
- Confirm `git status` reflects the intended branch and checkout inside the worktree.
- Run relevant repository checks from inside the worktree used for the task.
- Verify the worktree is clean before removal and prune stale metadata afterward when needed.

- Smoke test:
  - should trigger: "Create a parallel worktree for a refactor without touching my main checkout."
  - should not trigger: "Configure wt hooks and parallel lanes for this repo." (→ `worktrunk`)

## Examples

- "Create `.worktrees/feature-auth-refactor` from `origin/main` for a migration lane, then keep the main checkout untouched until the branch is ready."
- "Set up one worktree per agent for parallel PR work, then remove the clean worktree only after `git status` passes."
- "Recover a worktree that points at the wrong branch without losing local edits."

## Reference files

- [Naming conventions and scheme](references/naming-conventions.md)
- [Naming defaults and examples](assets/naming-examples.md)
- [Recovery and cleanup guide](references/recovery-and-cleanup.md)
- [Worktrunk command equivalents](references/worktrunk-commands.md)

## Integration

**Pairs with:**
- [`worktrunk`](../worktrunk/SKILL.md) — use `wt switch --create` / `wt merge` / `wt remove` instead of raw git commands when Worktrunk is installed; the `worktrunk` skill covers hooks, LLM commits, and merge pipeline
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — after pushing from a worktree, use this for PR creation/update and check-watch workflow
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — after pushing a branch from a worktree, address PR review comments in the same worktree before cleanup
- [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) — if a pushed branch fails CI, diagnose the failure before removing the worktree
- [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) — when implementation in a worktree is complete, use this to decide how to integrate (merge, PR, keep, or discard)
