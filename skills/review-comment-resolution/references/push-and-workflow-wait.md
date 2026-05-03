# Push and workflow wait

Use this sequence after the fixes are ready locally.

## 1. Validate before committing

Run the repository's relevant checks for the touched surface first, such as:

- targeted tests
- typecheck
- lint or build commands the branch normally depends on

Do not create the commit first and hope CI will explain obvious local failures.

## 2. Stage only the intended fix set

Before committing:

- inspect the staged diff
- confirm unrelated local changes are excluded
- confirm the batch matches the review comments you decided to fix

## 3. Commit cleanly

Create a focused commit message that describes the review-fix batch rather than every individual comment.

If the environment expects signed commits, use the repository's configured signing flow.

## 4. Push the correct branch

Verify:

- the current branch is the intended PR branch
- the push target is correct
- the new head commit is the one you just created

Avoid force-push unless the workflow explicitly requires it.

## 5. Wait for workflows or checks

After the push:

- get the new head commit SHA for the branch you pushed
- use the available GitHub tools, API, or CLI to list checks or workflow runs for that SHA
- if `gh` is available, `gh pr checks --watch` or `gh run list --commit <sha>` are reasonable starting points
- identify the workflows or checks triggered for the new head commit
- poll every 10-30 seconds or use a built-in watch mode until they finish instead of stopping after the push
- distinguish required checks from optional informational ones when the platform exposes that detail
- treat `success`, `failure`, `cancelled`, and `skipped` as terminal states only after all relevant runs have landed there

## 6. Handle failures deliberately

If a workflow fails:

- inspect the failing job or check output
- fetch job details or logs using the available GitHub tools or CLI before deciding what failed
- fix failures caused by your changes when they are in scope
- call out unrelated or pre-existing failures clearly instead of claiming success

The task is only complete when the intended fixes are pushed and the resulting checks have either passed or been reported with a precise blocker.
