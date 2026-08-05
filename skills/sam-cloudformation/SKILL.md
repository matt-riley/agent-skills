---
name: sam-cloudformation
description: "Use when AWS SAM templates, CloudFormation stacks, or SAM deploys fail on YAML, transforms, resource wiring, or rollback state, or when the deploy caller gets AWS sts:AssumeRole or sts:AssumeRoleWithWebIdentity AccessDenied — not when the Lambda binary itself or Terraform-owned infrastructure is the primary blocker."
license: GNU GPL v3
metadata:
  version: 2.0.0 # x-release-please-version
  category: ci
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# SAM CloudFormation

Use this skill when the failure lives in the SAM template, CloudFormation stack lifecycle, deployment-role/resource wiring, or the OIDC AssumeRole step that gates the deploy, and you need a deployment-oriented fix path that stays specific to SAM and CloudFormation.

## Use this skill when

- An AWS SAM template fails validation, linting, or deployment.
- A CloudFormation stack is drifting, rolling back, or stuck in a rollback state during a SAM deploy.
- SAM or CloudFormation YAML has schema, transform, event, or resource-property errors.
- Resource wiring in a SAM template needs correction, especially IAM ARNs, events, or dynamic references.
- A GitHub Actions SAM deployment needs correct CloudFormation/SAM auth and deployment patterns rather than Terraform-shaped examples.
- A CI log shows `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity` for the deployment role, so the deploy never reaches CloudFormation.
- GitHub Actions OIDC auth for the deploy is failing on the trust policy, provider, audience, subject condition, or a session-tag contract.
- A CircleCI-to-GitHub-Actions migration may have left deploy roles or trust policies specific to CircleCI callers.

## Do not use this skill when

- The main issue is the Go Lambda binary, runtime, handler, or zip layout.
- The infrastructure is Terraform-managed rather than SAM/CloudFormation-managed.
- The core problem is a generic GitHub Actions workflow failure with no SAM-specific evidence yet.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| SAM template authoring, validation, deploy, or CloudFormation stack-state issues | Yes | - |
| OIDC or AssumeRole `AccessDenied` blocking the deploy auth step | Yes | see [`references/oidc-assumerole-triage.md`](references/oidc-assumerole-triage.md) |
| Lambda binary, runtime, bootstrap, or handler issue | No | [`aws-lambda-go-deployment`](../aws-lambda-go-deployment/SKILL.md) |
| Infrastructure is owned by Terraform instead of SAM/CloudFormation | No | [`terraform-skill`](../terraform-skill/SKILL.md) |
| Generic workflow-run diagnosis before the SAM deploy step is understood | No | [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) |

## Inputs to gather

**Required before editing**

- The failing SAM template snippet and the deploy or validate command being run.
- Current stack status plus recent CloudFormation stack events.
- The exact validation, lint, or deployment error message.
- The relevant IAM role, event source, and resource configuration blocks tied to the failure.
- When the deploy fails at auth: the exact `AccessDenied` line, the target role's trust policy, the OIDC provider, and the caller's repo/ref/event shape — full list in [`references/oidc-assumerole-triage.md`](references/oidc-assumerole-triage.md).

**Helpful if present**

- `sam validate --lint` output.
- The GitHub Actions deploy step or local shell command that invoked `sam deploy`.
- Drift evidence for resources in rollback or stuck-update states.
- The reference repo or known-good SAM/CloudFormation deployment pattern being followed.

**Only investigate if encountered**

- Nested stack interactions.
- Stack policy overrides.
- Cross-account deployment wiring after auth is already proven correct.

## First move

1. Confirm the template is really SAM by checking for `AWSTemplateFormatVersion` plus `Transform: AWS::Serverless-2016-10-31`.
2. Run or inspect `sam validate --lint` before changing deployment flow.
3. Separate template/schema errors, stack-state problems, and auth failures. If the deploy never got past `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`, start from [`references/oidc-assumerole-triage.md`](references/oidc-assumerole-triage.md) and do not touch the template yet.

## Workflow

1. Verify the SAM transform headers are present and that the failing resources actually belong in a SAM/CloudFormation template.
2. Run `sam validate --lint` before `sam deploy`; fix schema and property errors there first.
3. Check resource wiring carefully:
   - prefer dynamic ARNs with `!Sub` plus `AWS::AccountId` and `AWS::Region`
   - avoid hardcoded account or region values when the template should stay portable
4. Inspect CloudFormation stack events when deployment fails; use the event history to anchor the first broken resource instead of retrying blindly.
5. If the stack is stuck in `UPDATE_ROLLBACK_FAILED`, inspect resource drift before retrying. When the drifted resource is stable and understood, use `aws cloudformation continue-update-rollback` to recover the stack.
6. For SQS or DynamoDB event source mappings that need partial batch failure reporting, set `FunctionResponseTypes` intentionally instead of assuming the default behavior is sufficient.
7. For GitHub Actions auth and deploy wiring, prefer patterns from a direct SAM/CloudFormation reference repo. Do not port Terraform OIDC workflow patterns directly because the deploy-role contract and permission scope differ.
8. If the deploy fails at auth with `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`, resolve the trust, provider, audience, subject, or session-tag contract first using [`references/oidc-assumerole-triage.md`](references/oidc-assumerole-triage.md); only return to the template once auth succeeds.
9. Route away immediately when the real problem is Lambda packaging or Terraform ownership.

## Outputs

- A narrowed diagnosis of whether the failure is template syntax, transform/schema validation, resource wiring, stack rollback state, or OIDC deploy-auth trust.
- The smallest justified SAM/CloudFormation configuration change or recovery action.
- A clean handoff to `aws-lambda-go-deployment`, `terraform-skill`, or `github-actions-failure-triage` when another skill owns the blocker.

## Guardrails

- Never skip `sam validate --lint` and jump straight to repeated `sam deploy` retries.
- Never hardcode account or region ARNs when `!Sub`, `AWS::AccountId`, and `AWS::Region` should be used.
- Never treat `UPDATE_ROLLBACK_FAILED` as a retry-only problem; inspect drift and recovery options first.
- Do not borrow Terraform workflow auth patterns for SAM deploys without checking a direct SAM/CloudFormation reference first.
- Never diagnose stack rollback or drift before resolving an explicit AssumeRole denial, and never widen trust-policy conditions further than the real repo, ref, and audience require.

## Validation

- Confirm the template includes `AWSTemplateFormatVersion` and `Transform: AWS::Serverless-2016-10-31` when SAM resources are present.
- Run `sam validate --lint` and fix reported schema or property issues before considering the change complete.
- Re-check the relevant CloudFormation stack events after the change to verify the first failing resource or rollback blocker is resolved.
- If event source mappings were touched, confirm `FunctionResponseTypes` is set when partial batch failure handling is required.
- When the failure was an AssumeRole denial, confirm the denied action matches the trust-policy path you fixed and re-read the auth step to verify IAM auth now succeeds before widening to stack triage.
- Smoke test:
  - should trigger: "Our SAM deploy rolls back because the template has invalid resource wiring and the stack is now stuck in UPDATE_ROLLBACK_FAILED."
  - should trigger: "GitHub Actions fails in configure-aws-credentials with AccessDenied on sts:AssumeRoleWithWebIdentity for our deployment role."
  - should not trigger: "The Go Lambda zip is missing the `bootstrap` binary and fails before the template is the problem." (→ `aws-lambda-go-deployment`)

## Examples

- "Fix this SAM template validation error and keep the change limited to the CloudFormation resource wiring."
- "Our stack is stuck in UPDATE_ROLLBACK_FAILED after a SAM deploy; check drift and the safest recovery step before changing anything else."
- "Review this GitHub Actions SAM deployment and align it to a real SAM/CloudFormation auth pattern instead of a Terraform-style role flow."
- "Trace why this GitHub Actions deployment role denies AssumeRoleWithWebIdentity and fix the trust policy instead of debugging the stack."
- "We migrated from CircleCI to GitHub Actions and now the deploy role denies OIDC callers; audit the trust policy for CircleCI-only conditions."

## Reference files

- [`references/deploy-checklist.md`](references/deploy-checklist.md) - quick checks for SAM transforms, linting, stack rollback recovery, event-source handling, and route-away cues.
- [`references/oidc-assumerole-triage.md`](references/oidc-assumerole-triage.md) - full triage path for `sts:AssumeRole` / `sts:AssumeRoleWithWebIdentity` `AccessDenied`: trust-policy conditions, provider and audience checks, CircleCI migration leftovers, session tags, and onward routing.
