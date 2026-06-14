# Decision Rules, Guardrails, Validation, and Integration

## Guardrails in Practice

- **Test failure blocks options:** If tests fail, announce the failure and ask user to fix or confirm discard intent (Option 4).
- **Dirty worktree blocks action:** If worktree has uncommitted changes, halt and ask user to commit or stash.
- **Confirmation for destructive action:** Option 4 requires explicit typed confirmation.
- **No premature cleanup:** Only cleanup worktree for Options 1 and 4; keep for 2 and 3.

## Four Integration Options (High Level)

1. **Merge locally** — `git checkout <base>`, `git pull`, `git merge <feature>`, verify tests, `git branch -d <feature>`, cleanup worktree
2. **Push and create PR** — push branch, `gh pr create` with summary and test plan, keep worktree
3. **Keep as-is** — report branch and worktree location, no cleanup
4. **Discard** — require typed "discard" confirmation, force-delete branch, cleanup worktree

### Worktree Cleanup Rules

- **Option 1 (Merge locally):** Clean up worktree after successful merge
- **Option 2 (Push and create PR):** Keep worktree active for follow-up review cycles or user iteration
- **Option 3 (Keep as-is):** Keep worktree as-is; report location and remind user of cleanup task
- **Option 4 (Discard):** Clean up worktree immediately after confirmation

## Validation (After Action)

- **Option 1 validation:** Base branch is updated; feature branch is deleted locally; tests pass on base; worktree is removed
- **Option 2 validation:** Branch is pushed; PR exists and links to the right base; PR title and summary are clear; worktree persists
- **Option 3 validation:** Branch and worktree locations are reported clearly; user acknowledges; no cleanup yet
- **Option 4 validation:** User typed "discard"; branch is force-deleted; worktree is removed; no residual files

- Smoke test:
  - should trigger: "Tests pass; help me decide whether to merge, PR, keep, or discard this branch."
  - should not trigger: "Create a PR and watch checks for this ready branch." (→ `github-cli-pr-workflow`)

## Integration

**Called by:** Any multi-step implementation workflow after all tasks complete and before final handoff.

**Pairs with:**
- [`git-worktrees`](../git-worktrees/SKILL.md) — cleanup via `mr_worktree_remove`
- [`worktrunk`](../worktrunk/SKILL.md) — prefer `wt merge` for Option 1 when Worktrunk is installed
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — use for Option 2 PR creation/update and check-watch handoff after pushing
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — after Option 2 receives feedback

**Activates:** When implementation is complete and tests pass; agent is deciding final branch fate.

**Deactivates:** After user confirms one of four options and execution is complete (merge verified, PR created, branch kept, or discarded).

See main SKILL.md for the concise workflow and Guardrails summary. Long examples are in `examples.md`; routing and inputs details in `routing-boundaries.md`.