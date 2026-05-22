---
name: github-actions-failure-triage
description: "Diagnose and minimally fix failing GitHub Actions runs in repositories already using GitHub Actions."
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

## Iron Law

> **No edits before reading the concrete failing evidence.**
>
> Read the exact failing run, job, step, and logs before touching any file.
> Speculative edits without evidence are the most common cause of wasted reruns.

## Routing boundary

Use the closest matching workflow:

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Failing GitHub Actions run, job, or check in a repo already on Actions | Yes | - |
| CircleCI migration planning, parity checks, or staged cutover | No | [`circleci-to-github-actions-migration`](../circleci-to-github-actions-migration/SKILL.md) |
| Broad CI migration planning, parity checks, or staged cutover between CI systems | No | dedicated migration plan in `plan-review` |
| PR review-comment adjudication and fix batching | No | [`review-comment-resolution`](../review-comment-resolution/SKILL.md) |
| Worktree or isolated branch setup for parallel changes | No | [`git-worktrees`](../git-worktrees/SKILL.md) |
| Root cause found; local reproduction with `act` is feasible | No | [`github-actions-local-repro`](../github-actions-local-repro/SKILL.md) |

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

**Announce at start:** "I'm using the github-actions-failure-triage skill to diagnose this run."

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
   - workflow linting with `action-validator` or `actionlint` when available
   - targeted rerun, check, or workflow verification where practical
7. Summarize the result using [`assets/triage-summary-template.md`](assets/triage-summary-template.md), including evidence, change made, validation, and any remaining blocker.
8. If the failure really belongs to migration design, review-comment handling, or admin-only settings, stop and hand off cleanly instead of stretching the skill.

## Quick decision appendix

Use this as the fast path once the failure bucket is known:

| Bucket | First safe move | Tightest fix | Rerun / escalation cue |
| --- | --- | --- | --- |
| Workflow syntax, trigger, or expression errors | Read the exact YAML and expression path that failed | Fix the broken key, trigger filter, or expression reference | Rerun only after the workflow parses cleanly |
| Permissions, token, secret, or variable issues | Confirm the expected names and scopes without reading secret values | Adjust repo-owned permissions or secret wiring | Escalate when the dependency lives in org-admin or environment policy |
| Runner or environment mismatch | Compare `runs-on`, image, labels, and shell assumptions | Switch to the correct runner or remove the environment-specific assumption | Escalate when the label or fleet health is outside repo control |
| Matrix or fan-out issues | Identify the single failing axis | Tighten include/exclude logic or branch-specific setup | Rerun the narrow matrix leg after the fix |
| Cache, artifact, job-output, or cross-job handoff failures | Compare the producer and consumer path or output name | Fix the exact path, name, or `needs` handoff | Rerun the downstream consumer after verifying the producer created the file |
| Reusable workflow or action interface issues | Inspect both caller and callee contracts together | Align inputs, secrets, outputs, or ref pins | Escalate only if the contract change needs broader coordination |
| Concurrency, cancellation, or dependency-order issues | Check `needs`, concurrency groups, and skip conditions | Remove the ordering bug or unsafe cancellation rule | Rerun after the dependency graph is corrected |
| Project, test, deployment, or runtime failures | Confirm the workflow is exposing a real repo bug | Fix the code or config surface that actually failed | Hand off instead of polishing workflow YAML |

## Guardrails

- **Must not** edit workflow files speculatively before reading the concrete failing evidence.
- **Must not** assume every failure is a YAML problem; the root cause may be a real project, test, deployment, or runtime bug.
- **Must not** collect, print, or store secret values.
- **Must not** absorb migration planning, PR review handling, or worktree setup into this skill.
- **Must not** rely on blind reruns as a substitute for diagnosis.
- **Must not** rerun a failure just to feel productive; a rerun only counts when it can change the evidence or verify a narrowly targeted fix.
- **Should** prefer the smallest change that explains the failure and preserves the surrounding workflow shape.
- **Should** distinguish flaky, pre-existing, and newly introduced failures before claiming a fix.
- **Should** escalate instead of guessing when the failure depends on org-admin controls, runner-fleet health, or broader CI redesign.

## Common rationalisations

| Rationalisation | Reality |
|---|---|
| "I'll just rerun it to see if it's flaky" | A rerun without evidence only wastes a run. Read the logs first. |
| "It's probably a YAML syntax issue" | Most failures are runner, secret, or project bugs — not YAML. Read the logs before assuming. |
| "It was working before the last merge, so it must be that" | Correlation is not causation. Anchor on the exact failing step. |
| "I'll fix something obvious while I read the logs" | Speculative fixes in parallel with investigation create confounding variables. |
| "The fix is small, I don't need to wait for the run" | A fix that seems small can pass locally and fail in CI for unrelated reasons. Wait for evidence. |

## Validation

- Run the repository's relevant validation commands for the touched surface.
- If workflow files changed, run workflow linting with `action-validator` or `actionlint` when available.
- Re-check the exact failing workflow, job, or check when practical instead of relying only on generic local validation.
- If the change touches artifact, cache, or output wiring, confirm both the producer and consumer paths before calling the fix complete.
- If the failure stayed ambiguous after reading the logs, prefer escalation or extra debug evidence over repeated reruns.
- If no change is made, provide a precise evidence-backed explanation of the root cause or blocker.
- If rerun or check access is unavailable, state the limitation and provide the exact evidence-backed next action for someone with access.
- Smoke test:
  - should trigger: "Diagnose why the deploy job started failing after a workflow edit."
  - should not trigger: "Reproduce this failing Actions job locally with act." (→ `github-actions-local-repro`)

## Examples

- "The `deploy` job on PR #182 fails on `Upload artifact` with `Artifact not found`; trace that run, fix the upload path, and do not touch the rest of the workflow."
- "A workflow started failing after `actions/checkout` was bumped; confirm whether the failure is in the action input, the checkout depth, or the repo script before changing anything else."
- "Only the `ubuntu-latest / node-20` matrix leg fails at the test step; isolate the failing job and keep the fix limited to that branch of the matrix."
- "A reusable workflow call started failing after an input rename; verify the caller and callee contract before editing unrelated jobs."

## Reference files

- [`references/evidence-checklist.md`](references/evidence-checklist.md) - intake fields and evidence to gather before editing
- [`references/failure-buckets.md`](references/failure-buckets.md) - common failure categories, symptoms, and first checks
- [`references/debug-and-escalation.md`](references/debug-and-escalation.md) - when to rerun, enable extra debugging, or hand off
- [`references/triage-scenarios.md`](references/triage-scenarios.md) - compact scenario matrix for validation and fast bucket recognition
- [`assets/triage-summary-template.md`](assets/triage-summary-template.md) - concise format for reporting root cause, fix, validation, and blockers
