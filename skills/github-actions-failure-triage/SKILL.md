---
name: github-actions-failure-triage
description: Diagnose and minimally fix failing GitHub Actions runs in repositories already using GitHub Actions.
metadata:
  category: ci
  audience: general-coding-agent
  maturity: stable
---

# GitHub Actions failure triage

Use this skill when a repository already uses GitHub Actions and the task is to diagnose or minimally fix a failing workflow run, job, or check.

## Use this skill when

- The user asks why a GitHub Actions run, job, or check is failing.
- A workflow started failing after a workflow edit, action version bump, runner change, cache change, matrix change, or reusable workflow change.
- A post-migration GitHub Actions regression needs diagnosis, but the repository is already on GitHub Actions.
- The likely best outcome is a targeted fix, a precise explanation, or a clean escalation path rather than a broad CI redesign.

## Do not use this skill when

- The main task is CI-platform migration planning, parity mapping, or retirement of another CI system.
- The main task is handling PR review comments, pushing a fix batch, or waiting for post-push checks.
- The main task is worktree or branch isolation for parallel work.
- The user is asking for greenfield CI design or a broad GitHub Actions redesign with no concrete failing run to anchor on.
- The primary action required is changing org-admin settings, runner fleet configuration, branch protection, or environment policy rather than diagnosing a repository-owned failure.

## Routing boundary

Use the closest matching workflow:

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Failing GitHub Actions run, job, or check in a repo already on Actions | Yes | - |
| CI migration planning, parity checks, or staged cutover between CI systems | No | dedicated migration plan in `plan-review` |
| PR review-comment adjudication and fix batching | No | [`review-comment-resolution`](../review-comment-resolution/SKILL.md) |
| Worktree or isolated branch setup for parallel changes | No | [`git-worktrees`](../git-worktrees/SKILL.md) |

## Inputs to gather

**Required before editing**

- A concrete failure anchor such as a run URL, run ID, job name, job ID, or failed check name.
- The exact failing attempt, head SHA, branch or ref, and triggering event.
- The failing step logs plus enough surrounding context to understand what ran before the failure.
- The workflow file at the failing commit, plus any called reusable workflow or referenced action version involved in the failing path.

**Helpful if present**

- Matrix values for the failing job.
- Runner details such as GitHub-hosted vs self-hosted and the effective labels or image.
- Artifact names, cache keys, and relevant job outputs.
- Whether the failure is new, flaky, branch-specific, or already failing on the base branch.

**Only investigate if encountered**

- Secret and variable names, scopes, and inheritance behavior.
- Concurrency groups, cancellation behavior, and `needs` ordering.
- Debug rerun settings or extra logging surfaces.

Do not collect secret values. Only confirm whether the expected names, scopes, and inheritance behavior are present.

## First move

1. Anchor the exact failing run, attempt, job, step, SHA, branch or ref, and event.
2. Read the failed-step logs and surrounding setup context before editing anything.
3. Map the failure to the exact workflow file, called reusable workflow, action version, or repository script that ran for that commit.

## Workflow

1. Gather the required evidence using the checklist in [`references/evidence-checklist.md`](references/evidence-checklist.md).
2. Classify the failure using [`references/failure-buckets.md`](references/failure-buckets.md) before proposing a fix.
3. Form the smallest root-cause hypothesis that explains the failing step with evidence.
4. Decide whether the right next action is:
   - a small workflow fix
   - a code or config fix outside the workflow file
   - a targeted rerun or debug pass
   - an explanation-only outcome
   - escalation or handoff
5. Apply the smallest justified change only after the evidence supports it.
6. Validate as narrowly as possible:
   - relevant repository checks for the touched surface
   - workflow linting such as `actionlint` when available or already expected
   - targeted rerun, check, or workflow verification where practical
7. Summarize the result using [`assets/triage-summary-template.md`](assets/triage-summary-template.md), including evidence, change made, validation, and any remaining blocker.
8. If the failure really belongs to migration design, review-comment handling, or admin-only settings, stop and hand off cleanly instead of stretching the skill.

## Guardrails

- **Must not** edit workflow files speculatively before reading the concrete failing evidence.
- **Must not** assume every failure is a YAML problem; the root cause may be a real project, test, deployment, or runtime bug.
- **Must not** collect, print, or store secret values.
- **Must not** absorb migration planning, PR review handling, or worktree setup into this skill.
- **Must not** rely on blind reruns as a substitute for diagnosis.
- **Should** prefer the smallest change that explains the failure and preserves the surrounding workflow shape.
- **Should** distinguish flaky, pre-existing, and newly introduced failures before claiming a fix.
- **Should** escalate instead of guessing when the failure depends on org-admin controls, runner-fleet health, or broader CI redesign.

## Validation

- Run the repository's relevant validation commands for the touched surface.
- If workflow files changed, run workflow linting such as `actionlint` when available.
- Re-check the exact failing workflow, job, or check when practical instead of relying only on generic local validation.
- If no change is made, provide a precise evidence-backed explanation of the root cause or blocker.
- Before considering the skill package complete, confirm that:
  - `SKILL.md` has the required frontmatter and sections
  - every support file is linked directly from this file
  - the next action is obvious within a few seconds of reading it

## Examples

- "The deploy job on my PR is failing with a missing artifact. Can you figure out why without rewriting the whole workflow?"
- "Our workflow started failing after I bumped `actions/checkout`. Diagnose it before making broad CI changes."
- "One matrix variant keeps failing in GitHub Actions even though the others pass."
- "This reusable workflow call started failing after an input or ref change. Investigate the contract mismatch."
- "Post-migration, this GitHub Actions check is red. Triage whether it's the workflow or the application."

## Reference files

- [`references/evidence-checklist.md`](references/evidence-checklist.md) - intake fields and evidence to gather before editing
- [`references/failure-buckets.md`](references/failure-buckets.md) - common failure categories, symptoms, and first checks
- [`references/debug-and-escalation.md`](references/debug-and-escalation.md) - when to rerun, enable extra debugging, or hand off
- [`assets/triage-summary-template.md`](assets/triage-summary-template.md) - concise format for reporting root cause, fix, validation, and blockers
