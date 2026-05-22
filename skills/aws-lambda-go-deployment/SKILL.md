---
name: aws-lambda-go-deployment
description: "Use when deploying or debugging Go-based AWS Lambda packaging, bootstrap, runtime, or handler issues — not when the main failure is SAM stack wiring, IAM OIDC auth, or a generic GitHub Actions run failure."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# AWS Lambda Go deployment

Use this skill when a Go Lambda fails because the binary, runtime, package layout, or event wiring is wrong and you need the smallest deployment-focused fix before widening into SAM, IAM, or CI triage.

## Use this skill when

- A Go AWS Lambda fails to deploy, package, or start correctly.
- `sam build` or a manual zip step is producing the wrong binary layout for a Go function.
- The function is missing `bootstrap`, uses the wrong handler name, or was built for macOS instead of Linux.
- You need to check Lambda Function URL or API Gateway wiring after confirming the Go binary should boot.
- CloudWatch Logs need inspection to separate init/runtime failures from application-code failures.

## Do not use this skill when

- The main problem is SAM template YAML, CloudFormation stack behavior, or IAM role wiring.
- The failure is `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`.
- The core issue is a plain Go compile or test failure before Lambda packaging begins.
- The primary failure is a GitHub Actions workflow problem rather than the Lambda deployment path itself.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Go Lambda packaging, runtime, bootstrap, or handler problems | Yes | - |
| SAM template YAML, CloudFormation stack rollback, or IAM resource wiring | No | [`sam-cloudformation`](../sam-cloudformation/SKILL.md) |
| Deploy workflow fails on AssumeRole or OIDC auth | No | [`iam-oidc-triage`](../iam-oidc-triage/SKILL.md) |
| Go code does not compile before packaging | No | [`go-build-and-test`](../go-build-and-test/SKILL.md) |
| CI workflow structure or runner behavior is failing | No | [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) |

## Inputs to gather

**Required before editing**

- Target Lambda architecture (`amd64` or `arm64`) and whether the function runs on Graviton.
- Build path: `sam build`, Makefile, or manual `go build` plus zip.
- Runtime and handler settings from the SAM template or deployment config.
- The exact error from Lambda, SAM, or CloudWatch Logs.

**Helpful if present**

- `sam build` output or Docker build logs.
- The built artifact layout (`bootstrap`, handler path, zip contents).
- Function URL or API Gateway event configuration.
- Recent CloudWatch log lines around `INIT_START` and `START`.

**Only investigate if encountered**

- Cross-account deploy wiring.
- Downstream API Gateway integration responses after the function starts successfully.
- Provisioned concurrency or alias-specific rollout details.

## First move

1. Classify the failure as build-time, package-layout, runtime-startup, or event-wiring.
2. Confirm the target runtime, architecture, and executable name before changing code.
3. Prefer `sam build --use-container` or an equivalent Linux build path before trusting a local macOS binary.

## Workflow

1. Confirm the Lambda runtime contract first: for Go functions prefer `provided.al2` or `provided.al2023`, not deprecated `go1.x`.
2. Build for the real Lambda target: use `sam build --use-container` for reproducible Linux builds, or manually cross-compile with `GOOS=linux` and `GOARCH=amd64` (or `arm64` on Graviton).
3. Verify the artifact layout matches the runtime expectation:
   - zipped custom-runtime binaries should be named `bootstrap`
   - SAM `Handler` values must match the deployed executable path when that path is used instead of `bootstrap`
4. Inspect the built zip or `.aws-sam` output before redeploying so you know whether the executable, permissions, and path are correct.
5. If deployment succeeds but invocation fails, read CloudWatch Logs and look for `INIT_START` and `START` before assuming an application-code bug.
6. If the binary boots, then check Function URL or API Gateway wiring, event payload shape, and template event definitions.
7. Route away immediately when the real blocker is SAM stack configuration, IAM OIDC auth, CI orchestration, or a plain Go build failure.

## Outputs

- A clear diagnosis of whether the failure is packaging, runtime selection, artifact layout, or event wiring.
- The corrected build/deploy assumptions for Linux architecture, executable naming, and runtime choice.
- A clean handoff to `sam-cloudformation`, `iam-oidc-triage`, `go-build-and-test`, or `github-actions-failure-triage` when this skill is not the right owner.

## Guardrails

- Never trust a macOS-built Go binary to run in Lambda; cross-compile for Linux or build in a SAM container.
- Never keep `go1.x` as the target runtime for new or repaired Go Lambda deployments.
- Never assume a code bug before checking CloudWatch init/start logs for startup evidence.
- Do not stretch this skill into SAM stack repair or IAM trust-policy debugging once those are the primary blocker.

## Validation

- Confirm the runtime is `provided.al2` or `provided.al2023` and the target architecture matches the deployed function.
- Confirm the deployment artifact contains the expected executable name (`bootstrap` or the configured handler path).
- Re-run the narrowest available build or packaging command and verify the artifact layout before redeploying.
- If the function is deployed, inspect CloudWatch logs for `INIT_START` and `START` to confirm whether the runtime got far enough to execute code.
- Smoke test:
  - should trigger: "Our Go Lambda was built on macOS and now fails in AWS with an exec-format or missing-bootstrap style startup error."
  - should not trigger: "The deploy job fails before deployment because GitHub Actions gets AccessDenied on AssumeRoleWithWebIdentity." (→ `iam-oidc-triage`)

## Examples

- "Package this Go Lambda for SAM so it runs on Lambda instead of failing at startup with a missing `bootstrap`."
- "We switched a Go function to Lambda arm64 and now the binary will not start; check the runtime, GOARCH, and zip layout."
- "This Go Lambda deploys, but the Function URL returns errors; verify the binary boots before checking the event wiring."

## Reference files

- [`references/packaging-checklist.md`](references/packaging-checklist.md) - quick checks for Linux cross-compilation, runtime choice, artifact naming, and route-away cues.
