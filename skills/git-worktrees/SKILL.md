---
name: git-worktrees
description: "Set up and manage isolated git worktrees for parallel tasks and agent lanes, and configure or operate Worktrunk (wt) for worktree lifecycle, hooks, LLM commits, and parallel agent workflows. Use when worktree setup, recovery, or wt configuration is the real need, not generic planning or implementation guidance."
license: GNU GPL v3
metadata:
  version: 3.0.0 # x-release-please-version
  owner: mattriley
  category: git
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Git worktrees

Owns the whole worktree lifecycle: raw `git worktree` when that is all that is available, and Worktrunk (`wt`) configuration, hooks, LLM commits, merge pipeline, and parallel agent lanes when `wt` is installed.

## Use this skill when

- You need isolated workspaces for parallel changes in the same repository.
- Multiple agents or contributors may work concurrently and branch-switch churn would be risky or slow.
- You want safer experimentation while keeping the primary checkout stable.
- The user explicitly asks for a separate checkout, isolated lane, or worktree-based cleanup or recovery.
- The user asks how to configure Worktrunk (`wt config`, `~/.config/worktrunk/config.toml`, `.config/wt.toml`).
- The user wants LLM-generated commit messages or branch summaries from `wt`.
- The user needs to author or debug `wt` hooks (`post-start`, `pre-merge`, and the rest).
- The user is setting up parallel agent lanes with `wt switch --create --execute=…`.
- The user asks about `wt merge`, `wt step`, the merge pipeline, shell integration, or worktree path layout.

## Do not use this skill when

- You only need a single quick edit on the current branch.
- The repository is not in a usable Git state for worktree operations.
- A disposable clone is explicitly preferred over shared object storage with the main repository.
- The real task is planning, implementation, or code review and worktree setup is only incidental.
- The task is only PR lifecycle work (create/update PR and watch checks) on an already prepared branch; route to [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md).
- Implementation is complete and the question is how to integrate the branch; route to [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md).

## Inputs to gather

**Required before editing**

- Base ref to branch from (for example `origin/main`).
- Task identifier suitable for branch and directory naming.
- Whether this worktree is temporary, long-lived, or tied to a PR/issue.
- For `wt` work: whether the need is config setup, hook authoring, or a parallel agent lane, and whether config already exists (`wt config show`).

**Helpful if present**

- Existing branch naming conventions.
- Preferred worktree root location for the repository.
- Local cleanup expectations for stale worktrees.
- Repo shape details such as monorepo package paths, submodules, sparse checkout, or nested worktrees.
- Project type (Node, Rust, Python, and so on) for hook examples.
- Whether LLM commit generation is wanted and which LLM tool is available.

**Only investigate if encountered**

- Submodule, sparse checkout, or filesystem constraints that affect worktree behavior.
- Branch-name collisions because the same branch is already checked out elsewhere.
- Recovery needs for stale registrations, missing directories, or removal blocked by local changes.
- Detached HEADs or platform-specific filesystem constraints.

## First move

0. Check if Worktrunk is installed: `wt --version`. If available (exit code 0), prefer `wt` commands throughout this workflow — see [Worktrunk command equivalents](references/worktrunk-commands.md). If it fails and the user asked for `wt` specifically, suggest `brew install worktrunk`; otherwise fall back to raw git.
1. Inspect current worktrees and branch state (`git worktree list` and `git branch --all`, or `wt list`).
2. Pick names using repository conventions or the defaults in `assets/naming-examples.md`.
3. Create or recover the isolated worktree before making task changes.

## Workflow

### With Worktrunk installed (`wt --version` succeeds)

Configure first — always when the ask is config, hooks, or LLM commits; once per user or project otherwise.

1. `wt config show` — inspect active config and file locations. `wt config create` scaffolds the user config, `wt config create --project` the project config.
2. Set `worktree-path` in the user config. An inside-repo `.worktrees/` template keeps agent harness worktree managers compatible. All keys and defaults: [config reference](references/config-reference.md).
3. Add a `[commit.generation]` block if LLM commit messages are wanted — see [LLM commit setup](references/llm-commits-setup.md).
4. Author project hooks in `.config/wt.toml` for install, dev server, DB, and CI gates — see [hooks reference](references/hooks-reference.md).
5. Optional: `[list] summary = true` in the user config for branch summaries.

Then run the lifecycle.

6. Fetch and verify the intended base ref.
7. Create the worktree: `wt switch --create <branch> --base <ref>` — fires `post-start` hooks automatically (deps install, dev server, and so on).
8. Perform all edits, tests, and commits inside that worktree.
9. Commit with an LLM message (if configured): `wt step commit`.
10. Merge when ready: `wt merge [target]` — squashes, rebases, validates via pre-merge hooks, fast-forwards, and cleans up. Add `--no-squash` if `[commit.generation]` is not configured. Stage-by-stage detail: [merge pipeline](references/merge-pipeline.md).
11. Or: push and open a PR, then `wt remove` after the PR is merged.
12. For parallel agent lanes, use `wt switch --create <lane> --execute=<agent>` — see [parallel agent recipes](references/parallel-agents-recipes.md).

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
- **Must** check `wt --version` before using any `wt` command; fall back to raw git if Worktrunk is not installed.
- **Must not** bypass project hooks (`post-start`, `pre-merge`) without explicit justification.
- **Should** use consistent naming defaults, but adapt to repository conventions when they differ.
- **Should** keep branch names and worktree paths aligned so the branch name still makes sense if the worktree path is copied or recreated later.
- **Should** verify the repository root before creating the worktree in monorepos or nested checkouts.
- **Should** run the task's validation commands from inside the worktree that owns the changes.
- **Should** use `wt switch --create` / `wt remove` instead of `git worktree add` / `git worktree remove` when Worktrunk is installed, so project hooks fire and worktree lifecycle is tracked.
- **Should** use `wt merge` for squash + rebase + cleanup in preference to manual git steps.
- **Should** configure `[commit.generation]` before relying on `wt step commit` for LLM messages.
- **May** keep long-lived worktrees for release or maintenance branches when the workflow benefits.
- **May** use `--no-squash` when commit granularity matters for the PR.

## Validation

- Confirm `git worktree list` (or `wt list`) shows the expected paths and branches.
- Confirm `git status` reflects the intended branch and checkout inside the worktree.
- Run relevant repository checks from inside the worktree used for the task.
- Verify the worktree is clean before removal and prune stale metadata afterward when needed.
- After config or hook changes, confirm the round trip:

```sh
wt config show                    # confirms settings loaded
wt switch --create test-wt-check  # creates worktree, fires hooks
wt list                           # confirms branch with status markers
wt remove test-wt-check           # cleans up
```

- Smoke test:
  - should trigger: "Create a parallel worktree for a refactor without touching my main checkout."
  - should trigger: "Configure wt hooks and parallel lanes for this repo."
  - should not trigger: "Review the finished diff for merge readiness." (→ `implementation-review`)

## Examples

- "Create `.worktrees/feature-auth-refactor` from `origin/main` for a migration lane, then keep the main checkout untouched until the branch is ready."
- "Set up one worktree per agent for parallel PR work, then remove the clean worktree only after `git status` passes."
- "Recover a worktree that points at the wrong branch without losing local edits."
- "Set up LLM commit messages for this repo: inspect `wt config show`, add a `[commit.generation]` block, then verify on a throwaway worktree that `wt merge` generates the message."
- "Add a `post-start` hook that runs `npm ci` and starts the dev server on the worktree's assigned port."
- "Configure two parallel agent lanes with `wt switch --create agent-lane-1 --execute=…` and confirm both show status markers in `wt list`."

## Reference files

- [Naming conventions and scheme](references/naming-conventions.md)
- [Naming defaults and examples](assets/naming-examples.md)
- [Recovery and cleanup guide](references/recovery-and-cleanup.md)
- [Worktrunk command equivalents](references/worktrunk-commands.md)
- [Worktrunk config reference](references/config-reference.md) — complete config key reference with defaults
- [Worktrunk hooks reference](references/hooks-reference.md) — all hook types, template variables, filters, pipeline syntax
- [Worktrunk LLM commit setup](references/llm-commits-setup.md) — commit generation config for Claude Code, Codex, llm CLI, aichat
- [Worktrunk merge pipeline](references/merge-pipeline.md) — `wt merge` pipeline, flags, and `wt step` sub-commands
- [Worktrunk parallel agent recipes](references/parallel-agents-recipes.md) — one-shot alias pattern, dev server per worktree, DB per worktree, cold-start elimination

## Integration

**Pairs with:**
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — after pushing from a worktree, use this for PR creation/update and check-watch workflow
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — after pushing a branch from a worktree, address PR review comments in the same worktree before cleanup
- [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) — if a pushed branch fails CI, diagnose the failure before removing the worktree
- [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) — when implementation in a worktree is complete, use this to decide how to integrate (merge, PR, keep, or discard)
