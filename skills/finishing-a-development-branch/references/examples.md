# Examples

Each example walks through the full decision boundary: verify tests, check worktree cleanliness, present all four options, execute the chosen one.

## Example 1: Merge locally (Option 1)

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

## Example 2: Push and create PR (Option 2)

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

## Example 3: Keep as-is (Option 3)

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

## Example 4: Discard (Option 4)

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