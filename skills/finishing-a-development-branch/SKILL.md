---
name: finishing-a-development-branch
description: "Use when implementation work is complete and you need to decide how to integrate the branch — merging locally, creating a PR, keeping the branch, or discarding the work."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
---

# finishing-a-development-branch

## Use this skill when

- Implementation work on a feature or fix is complete (all code changes made)
- All local tests pass consistently
- You need to decide the final integration path: merge, PR, keep, or discard
- A worktree or isolated branch exists and needs lifecycle resolution
- The agent needs a structured, repeatable decision boundary before handing off

## Do not use this skill when

- Tests are still failing or not yet run
- Implementation is incomplete or blocked
- The task is mid-flight and still under active development
- No tests exist and you have not established pass/fail status (fix or establish tests first)
- The user has already decided the integration method; skip directly to executing it

## Iron Law

> **TESTS MUST PASS BEFORE OPTIONS 1–3 ARE PRESENTED**
>
> If tests are failing, do not present Options 1–3 (merge, PR, keep) — fix or report the failure first. The skill enforces this boundary: verify test status, present options only on green, handle blockers if red. **Exception:** Option 4 (Discard) is always available when the user explicitly wants to abandon the failing branch.

## Routing boundary

| Signal | Route |
|--------|-------|
| Tests passing, ready to integrate | → Present Four Options |
| Tests failing or not run | → Fix or report; do not present options |
| User rejects all four options or requests custom flow | → Clarify intent; escalate if outside standard paths |
| Worktree is dirty (uncommitted changes) | → Commit/stage first, then proceed |

## Inputs to gather

- **Branch and base:** What feature/fix branch? What is the target base branch (main/develop)?
- **Test status:** Which tests are relevant? Have they all passed locally?
- **Worktree context:** Is this isolated in a git worktree or the main checkout?
- **Delivery preference:** Any organizational or project convention about PR vs. merge?
- **Audience:** Who reviews this? (PR needed if code review is required; otherwise merge is faster)

## First move

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

Then:

1. Verify worktree is clean (no uncommitted tracked changes; ignore untracked files)
2. Run all relevant tests locally and confirm they pass
3. If tests fail → fix and retest, report the failure, do not proceed to options
4. If tests pass → proceed to Four Options section

## Workflow

### Verify tests pass first

Before presenting any option, confirm:
- All tests that apply to the changed files have run
- All tests pass consistently
- There are no known flaky tests masking failures

If tests are not passing or cannot be run → stop, fix the failure, and report it. Do not present the options below.

### Four Integration Options

1. **Merge locally** — `git checkout <base>`, `git pull`, `git merge <feature>`, verify tests, `git branch -d <feature>`, cleanup worktree

2. **Push and create PR** — push branch, `gh pr create` with summary and test plan, keep worktree

3. **Keep as-is** — report branch and worktree location, no cleanup

4. **Discard** — require typed "discard" confirmation, force-delete branch, cleanup worktree

### Worktree cleanup rules

- **Option 1 (Merge locally):** Clean up worktree after successful merge
- **Option 2 (Push and create PR):** Keep worktree active for follow-up review cycles or user iteration
- **Option 3 (Keep as-is):** Keep worktree as-is; report location and remind user of cleanup task
- **Option 4 (Discard):** Clean up worktree immediately after confirmation

## Guardrails

1. **Tests are the gate** — Do not present options if tests are failing, blocked, or not run. Announce the blocker and stop.

2. **No false progress** — Do not mark the task done until the integration option is executed and verified (branch pushed, merged, or explicitly kept/discarded).

3. **Dirty worktree safety** — Before any integration action, verify the working tree is clean. If there are uncommitted changes, halt and ask the user to commit or stash.

4. **Branch existence** — Confirm the feature branch still exists and has the expected commits before starting an integration action.

5. **Base branch freshness** — Before merging locally, pull the latest base branch to avoid silent conflicts or divergence.

6. **PR creation safety** — Before `gh pr create`, confirm the branch is already pushed to the remote and is reachable from `origin`.

7. **Confirmation for destructive actions** — Require explicit typed confirmation (the word "discard") for Option 4 to prevent accidental data loss.

8. **Cleanup idempotency** — Worktree cleanup commands should succeed even if the worktree is partially cleaned or already removed; use `mr_worktree_remove` with appropriate safety checks.

## Validation

After presenting and executing an option, validate:

- **Option 1 validation:** Base branch is updated; feature branch is deleted locally; tests pass on base; worktree is removed
- **Option 2 validation:** Branch is pushed; PR exists and links to the right base; PR title and summary are clear; worktree persists
- **Option 3 validation:** Branch and worktree locations are reported clearly; user acknowledges; no cleanup yet
- **Option 4 validation:** User typed "discard"; branch is force-deleted; worktree is removed; no residual files

- Smoke test:
  - should trigger: "Tests pass; help me decide whether to merge, PR, keep, or discard this branch."
  - should not trigger: "Create a PR and watch checks for this ready branch." (→ `github-cli-pr-workflow`)

## Examples

Each example below walks through the full decision boundary: verify tests, check worktree cleanliness, present all four options, execute the chosen one.

### Example 1: Merge locally (Option 1)

```
Work complete on feature/auth-jwt:
- Tests pass: 247 passed
- Ready to integrate

Announce: "I'm using the finishing-a-development-branch skill to complete this work."

Verify tests: ✓ All 247 tests passing
Verify worktree clean: ✓ No uncommitted changes
No blockers.

Presenting Four Integration Options:

1. Merge locally → git checkout main && git pull && git merge feature/auth-jwt
2. Push and create PR
3. Keep as-is
4. Discard

User selects: 1

Action:
$ git checkout main
$ git pull
$ git merge feature/auth-jwt
$ npm test  # retest on main
Tests pass: ✓
$ git branch -d feature/auth-jwt
$ mr_worktree_remove auth-jwt
Worktree cleaned up

✓ Integration complete: main now includes auth-jwt; branch removed.
```

### Example 2: Push and create PR (Option 2)

```
Work complete on fix/linting-errors:
- Tests pass: All 890 tests passing
- Ready for review

Announce: "I'm using the finishing-a-development-branch skill to complete this work."

Verify tests: ✓ All 890 tests passing
Verify worktree clean: ✓ No uncommitted changes
No blockers.

Presenting Four Integration Options:

1. Merge locally
2. Push and create PR → gh pr create --title "fix: resolve linting errors" --body "Fixes..."
3. Keep as-is
4. Discard

User selects: 2

Action:
$ git push origin fix/linting-errors
$ gh pr create --title "fix: resolve linting errors" --body "Resolves #123. Tests: 890 passed." --base main
PR created: https://github.com/owner/repo/pull/456

✓ Integration in progress: PR #456 created; worktree remains active for feedback cycles.
```

### Example 3: Keep as-is (Option 3)

```
Work complete on explore/experimental-feature:
- Tests pass but feature incomplete for production
- User wants to preserve branch for later

Announce: "I'm using the finishing-a-development-branch skill to complete this work."

Verify tests: ✓ All applicable tests passing
Verify worktree clean: ✓ No uncommitted changes
No blockers.

Presenting Four Integration Options:

1. Merge locally
2. Push and create PR
3. Keep as-is → Branch and worktree stay; cleanup later
4. Discard

User selects: 3

✓ Integration paused: Branch explore/experimental-feature and worktree remain active.
   Worktree path: .worktrees/experimental-feature
   Branch: origin/explore/experimental-feature (not pushed; local only)
   Next step: User pushes when ready, or deletes via Option 4 later.
```

### Example 4: Discard (Option 4)

```
Work incomplete on experiment/failed-approach:
- Tests failing; approach not viable
- Ready to abandon

Announce: "I'm using the finishing-a-development-branch skill to complete this work."

Verify tests: ✗ 12 tests failing; approach not viable
Blocker: Tests failing — Options 1–3 are unavailable (merge, PR, keep all require passing tests).
Exception: Option 4 (Discard) is available when the user explicitly wants to abandon.

Presenting available option:

4. Discard → Type "discard" to confirm; branch and worktree removed

(Options 1–3 are blocked until tests pass.)

User selects: 4 and types: discard

Action:
$ git branch -D experiment/failed-approach
$ mr_worktree_remove failed-approach --deleteBranch
Worktree cleaned up; branch removed

✓ Integration complete: Branch and worktree discarded; workspace clean.
```

## Guardrails in practice

- **Test failure blocks options:** If tests fail, announce the failure and ask user to fix or confirm discard intent (Option 4).
- **Dirty worktree blocks action:** If worktree has uncommitted changes, halt and ask user to commit first.
- **Confirmation for destructive action:** Option 4 requires explicit typed confirmation.
- **No premature cleanup:** Only cleanup worktree for Options 1 and 4; keep for 2 and 3.

## Integration

**Called by:** Any multi-step implementation workflow after all tasks complete and before final handoff.

**Pairs with:**
- [`git-worktrees`](../git-worktrees/SKILL.md) — cleanup via `mr_worktree_remove`
- [`worktrunk`](../worktrunk/SKILL.md) — prefer `wt merge` for Option 1 when Worktrunk is installed
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — use for Option 2 PR creation/update and check-watch handoff after pushing
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — after Option 2 receives feedback

**Activates:** When implementation is complete and tests pass; agent is deciding final branch fate.

**Deactivates:** After user confirms one of four options and execution is complete (merge verified, PR created, branch kept, or discarded).

## Reference files

- [`git-worktrees`](../git-worktrees/SKILL.md) — worktree lifecycle management and cleanup via `mr_worktree_remove`
- [`worktrunk`](../worktrunk/SKILL.md) — `wt merge` for Option 1 when Worktrunk is installed
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — handling review feedback cycles after Option 2 (PR creation)
