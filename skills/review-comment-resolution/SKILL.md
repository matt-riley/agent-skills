---
name: review-comment-resolution
description: Apply pull request review feedback by assessing comments, fixing valid concerns, pushing the branch, and waiting for checks. Use when reviewer feedback must be carried through to completion, not just reviewed.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes access to the repository, review-comment context, git, and a way to inspect branch checks or workflow runs.
metadata:
  owner: mattriley
  version: 1.1.0 # x-release-please-version
  maturity: stable
---

# Review comment resolution

## Use this skill when

- The user asks you to address pull request review comments or reviewer feedback.
- Review comments exist as GitHub review threads, PR comments, copied text, or linked comment URLs.
- The task includes deciding which comments are valid concerns before making changes.
- The expected outcome is updated code plus a pushed commit whose resulting checks or workflows have been observed to completion.

## Do not use this skill when

- The task is only to review, summarize, or classify comments without changing code; use `implementation-review` when evaluation is the real deliverable.
- The comments are really bug reports, issue triage, or general design questions outside a concrete review surface.
- You cannot access the branch, PR, or comment context needed to judge the concern.
- The user explicitly instructs you to apply every review comment exactly as written without assessment.

## Inputs to gather

**Required before editing**

- The PR number, branch, or comment source to inspect.
- The unresolved or in-scope review comments to address.
- The repository's validation commands for the touched surface.
- Whether you can push to the current branch and whether checks are expected to run on that push.

**Helpful if present**

- Review thread URLs or comment IDs.
- The base branch and head branch of the PR.
- Existing branch-protection or required-check expectations.
- Whether you should post follow-up replies for comments you decide not to fix.

**Only investigate if encountered**

- Whether a separate worktree would make the feedback pass safer or less conflict-prone; use `git-worktrees` when isolation is the real need.
- Whether comments were superseded by later commits or overlapping fixes.
- Whether failing checks are pre-existing rather than introduced by the review-fix batch.

## First move

1. Fetch the in-scope review comments and map each one to its file, code context, and current relevance.
2. Classify each comment before editing anything.
3. Start with the valid or partially valid comments that have the highest correctness or merge-blocking impact.

## Workflow

1. Inventory the review comments and group them by file, concern, or shared root cause.
2. Use `references/comment-disposition.md` to classify each comment as valid, partially valid, not valid, superseded, or not actionable yet.
3. Inspect the code and nearby tests before accepting or rejecting the concern.
4. Fix the accepted concerns in small coherent batches, preserving runtime behavior unless the comment is explicitly about behavior.
5. Re-run the relevant validation commands for the touched surface.
6. Prepare a concise rationale for comments you intentionally do not fix so the result can be explained clearly.
7. Stage and commit only the intended review-comment fixes.
8. Push the branch, then use `references/push-and-workflow-wait.md` to watch checks or workflows on the new head commit until they reach terminal states.
9. If a failure was introduced by your changes and is in scope, fix it before considering the task complete.

## Guardrails

- **Must not** assume every review comment is correct without checking the actual code and context.
- **Must not** dismiss reviewer concerns casually; keep evidence for any comment you choose not to fix.
- **Must not** mix unrelated cleanup into the review-comment fix batch.
- **Must not** force-push, merge, or resolve/dismiss comments unless the surrounding workflow clearly calls for it.
- **Must** state the limitation and stop after local validation/commit guidance when the current harness cannot push or inspect checks.
- **Should** prefer the smallest change that addresses the real concern rather than the literal wording of a comment if the wording is imprecise.
- **Should** keep accepted and rejected comment reasoning easy to summarize after the push.

## Validation

- Run the repository's relevant validation commands before committing.
- Verify the staged diff only contains the intended review-comment fixes.
- Confirm the pushed branch matches the branch or PR under review.
- Wait for checks or workflows on the new head commit to finish.
- If any run fails, inspect whether the failure was introduced by your changes and address it when it is in scope.

## Examples

- `Address the open review comments on this PR, but only fix the ones that are actually valid.`
- `Go through the reviewer feedback, decide what needs changing, push the fixes, and wait for CI.`
- `Resolve the latest PR review comments on this branch and tell me which ones you intentionally did not fix.`

## Reference files

- Read `references/comment-disposition.md` when you need a concrete rubric for accepting, narrowing, or rejecting comments.
- Read `references/push-and-workflow-wait.md` when the fixes are ready locally and you need the commit/push/check-wait sequence.
