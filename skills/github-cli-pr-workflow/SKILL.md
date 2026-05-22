---
name: github-cli-pr-workflow
description: "Use when a branch needs GitHub CLI PR lifecycle work, like creating or updating a PR, watching checks for a pushed head SHA, or preparing PR handoff before review."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# GitHub CLI PR workflow

Use this skill when the main task is the PR lifecycle loop around a pushed branch: create or update the PR, monitor checks, and provide a clean handoff.

## Use this skill when

- The user asks to create a PR with `gh pr create` from an already prepared branch.
- The user asks to update PR metadata (title/body/base) with `gh`.
- The user asks to watch checks or workflow runs for the latest pushed commit.
- The user needs a concise PR status handoff before review-comment resolution starts.

## Do not use this skill when

- The main task is diagnosing why a workflow or check failed; route to [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md).
- The main task is adjudicating PR review comments and producing follow-up commits; route to [`review-comment-resolution`](../review-comment-resolution/SKILL.md).
- The main task is deciding merge vs PR vs keep vs discard; route to [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md).
- The main task is worktree setup or branch-lane isolation; route to [`git-worktrees`](../git-worktrees/SKILL.md) or [`worktrunk`](../worktrunk/SKILL.md).

## Iron Law

> **Always anchor PR check status to the current pushed head SHA.**
>
> Do not report check status from stale runs or earlier commits.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Create/update PR and monitor checks for a pushed branch | Yes | - |
| Failing run needs root-cause diagnosis | No | `github-actions-failure-triage` |
| Review comments need disposition and code fixes | No | `review-comment-resolution` |
| Need to choose integration option after implementation is done | No | `finishing-a-development-branch` |
| Need isolated worktree or parallel lane setup | No | `git-worktrees` or `worktrunk` |

## Inputs to gather

**Required before editing**

- Current branch name, target base branch, and whether the branch is already pushed.
- PR number or confirmation that no PR exists yet.
- The latest head SHA for the branch to anchor checks.
- Required checks or workflow expectations for the repository, if known.

**Helpful if present**

- Preferred PR title/body format.
- Linked issue numbers or release-note requirements.
- Whether review should start immediately or after checks pass.

## First move

1. Confirm the current branch and collect the current head SHA.
2. Confirm the branch is pushed to the expected remote.
3. Resolve whether the task is "create PR", "update PR", or "watch checks".

## Workflow

1. Ensure branch and remote context are correct.
2. Create or update the PR with `gh` using the intended base branch and summary.
3. Watch checks for the exact head SHA (`gh pr checks --watch` or SHA-scoped run listing).
4. Classify results as pass, fail, or blocked and report with PR URL + head SHA.
5. Route next step:
   - review comments pending -> `review-comment-resolution`
   - check failures need diagnosis -> `github-actions-failure-triage`
   - integration decision needed -> `finishing-a-development-branch`

## Outputs

- PR identifier (number and URL) and the exact head SHA assessed.
- Check/run status summary for that SHA (pass, fail, blocked, or still running).
- Explicit next-route recommendation when work moves to another skill.

## Guardrails

- **Must not** claim checks are green without referencing the current head SHA.
- **Must not** treat this skill as workflow-failure triage.
- **Must not** fold review-comment adjudication into this workflow.
- **Should** keep PR metadata edits scoped to the requested change.
- **Should** report blockers clearly when required checks are unavailable or still pending.

## Validation

- Confirm PR points at the intended base and head branch.
- Confirm reported check status corresponds to the current head SHA.
- Confirm handoff routing is explicit when transitioning to another workflow.

- Smoke test:
  - should trigger: "Create a PR from this branch and watch the latest checks."
  - should not trigger: "Help me choose whether to merge, PR, keep, or discard this branch." (→ `finishing-a-development-branch`)

## Examples

- "Create a PR from this branch and watch required checks before handoff."
- "Update PR #412 title/body and confirm whether checks are green on the latest commit."
- "Give me the current PR and check status for this branch, then tell me what workflow to run next."

## Reference files

- [`references/pr-lifecycle-commands.md`](references/pr-lifecycle-commands.md) - focused `gh` command sequence for create, update, and check-watch flows.
- [`references/routing-scenarios.md`](references/routing-scenarios.md) - route-to and route-away scenarios to avoid overlap with adjacent skills.

