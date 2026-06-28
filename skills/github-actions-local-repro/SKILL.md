---
name: github-actions-local-repro
description: Use when a GitHub Actions failure needs local reproduction with act before pushing, especially for workflow logic or step-level regressions, but not when the failure depends on org-managed runner or secret policy.
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: ci
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# GitHub Actions local repro

Use this skill when you need to reproduce a GitHub Actions failure locally with `act` to shorten debug loops and avoid speculative workflow edits.

## Use this skill when

- A GitHub Actions job is failing and local reproduction could confirm root cause before another push.
- You need to debug workflow conditions, step ordering, shell commands, or job wiring.
- The repository already has Docker support needed to run `act`.
- The fastest path is reproducing one failing job or event locally, then making a narrow fix.

## Do not use this skill when

- The failure depends on org-managed runner fleet behavior, protected environments, or hosted-only credentials.
- The main task is migration planning rather than debugging a concrete failing run.
- The user already provided definitive failing evidence and asked for a direct fix without a local repro loop.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Concrete Actions failure where local job execution is feasible | Yes | - |
| Failure tied to org policy, runner fleet labels, or protected environment gates | No | `github-actions-failure-triage` |
| Main goal is CircleCI migration or parity rollout | No | `circleci-to-github-actions-migration` (archived) |

## Inputs to gather

- Workflow file path, event type, and failing job name.
- Branch or commit containing the failing workflow.
- Required local secrets placeholders (never real secret values in logs).
- Any matrix value or environment variable needed to target the failing leg.

## First move

1. Confirm `action-validator` and `act` are available, then lint the target workflow file first.
2. Reproduce the exact failing job locally with the smallest command that matches CI behavior.
3. Capture the first failing step and error output before editing files.

## Workflow

1. Map the failing GitHub run to local `act` inputs: event, workflow file, job, matrix axis, and env.
2. Run `action-validator` against the target workflow and resolve syntax/schema failures before local execution.
3. Run a narrow local reproduction first (`act <event> -j <job>`), adding only required flags.
4. Compare local failure output to the hosted run to ensure the same failing step is being exercised.
5. Apply the smallest fix that addresses the reproduced failure.
6. Re-run the same local command until the failing step passes.
7. If local reproduction diverges because of hosted-only services or policies, stop and hand off with evidence.

## Outputs

- Exact `act` command used for reproduction.
- Failing step evidence and root-cause summary.
- Minimal patch tied to the reproduced failure.
- Clear note when local repro is not representative and must be escalated.

## Guardrails

- Do not assume local success guarantees hosted success; call out known environment gaps.
- Do not print secret values; use placeholder secret files or masked env values.
- Do not broaden the change scope beyond the reproduced failing path.
- Do not keep iterating if the failure cannot be represented locally after a focused attempt.

## Validation

- Confirm the same `act` command that failed now passes for the previously failing step.
- Re-run `action-validator` for every changed workflow file.
- Run repository checks relevant to changed files.
- Verify workflow syntax/lint expectations already used in the repo.

- Smoke test:
  - should trigger: "Reproduce the failing Actions job locally with act before I push again."
  - should not trigger: "Read the workflow logs and find the root cause first." (→ `github-actions-failure-triage`)

## Examples

- "Reproduce this `pull_request` failure for job `lint-and-test` with `act` and patch only what breaks in that job."
- "The `build` job started failing after a workflow edit; run it locally with `act`, isolate the failing step, and fix minimally."

## Reference files

- [`references/act-command-patterns.md`](references/act-command-patterns.md) - safe command patterns for targeting events, jobs, and matrix legs with `act`
