---
name: iam-oidc-triage
description: "Use when GitHub Actions or another OIDC caller gets AWS sts:AssumeRole or sts:AssumeRoleWithWebIdentity AccessDenied — not when auth succeeds and the remaining failure is in SAM, CloudFormation, or Terraform execution."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: ci
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# IAM OIDC triage

Use this skill when an OIDC-federated caller cannot assume an AWS role and the priority is to prove or fix the IAM trust, provider, audience, subject, or tagging contract before investigating later workflow stages.

## Use this skill when

- A CI log shows `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`.
- GitHub Actions OIDC auth is failing because the trust policy, provider, audience, or subject condition may be wrong.
- A CircleCI-to-GitHub-Actions migration may have left IAM roles or trust policies specific to CircleCI callers.
- The role assumption path may require session tags or transitive tags that the caller is not sending.
- You need to prove whether IAM trust is the blocker before investigating deployment, plan, or stack behavior.

## Do not use this skill when

- The role assumption step already succeeds and the remaining failure is in SAM, CloudFormation, Terraform, or application code.
- The main problem is a generic GitHub Actions workflow failure before the IAM auth step.
- The infrastructure issue is a Terraform plan/apply problem rather than OIDC trust or AssumeRole access.
- The failure is Lambda packaging, runtime, or handler-specific.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| OIDC trust-policy, audience, subject, provider, or session-tag issue causing AssumeRole denial | Yes | - |
| Auth succeeds, but the SAM or CloudFormation stack then fails | No | [`sam-cloudformation`](../sam-cloudformation/SKILL.md) |
| Terraform-managed infrastructure fails during plan/apply after auth | No | [`terraform-skill`](../terraform-skill/SKILL.md) |
| The failure is earlier in the workflow or not IAM-related | No | [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) |
| Lambda packaging or runtime is broken after deployment auth | No | [`aws-lambda-go-deployment`](../aws-lambda-go-deployment/SKILL.md) |

## Inputs to gather

**Required before editing**

- The exact `AccessDenied` log line, including whether the failing action is `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`.
- The target IAM role trust policy and the configured OIDC provider.
- The caller identity shape: repository, ref, event type, expected `sub`, and audience.
- Any required session-tag or transitive-tag contract for the role.

**Helpful if present**

- The GitHub Actions auth step configuration.
- Previous CircleCI trust-policy snippets or migration notes.
- CloudTrail or AWS error context that confirms the denied principal and condition mismatch.
- The permission model for any follow-on role chaining.

**Only investigate if encountered**

- Permission boundaries or SCPs that alter an otherwise-correct trust policy.
- Multiple OIDC providers or duplicate audience settings.
- Cross-account role chaining after the first AssumeRole call succeeds.

## First move

1. Stop chasing later stack or plan failures until the IAM denial is explained.
2. Capture the exact failing action, target role, repo/ref context, and expected `sub`/`aud` claims.
3. Compare the role trust policy to the real caller context before proposing any broader workflow change.

## Workflow

1. Treat `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity` as the primary blocker; do not investigate plan drift or stack rollback first.
2. Verify the role trust policy conditions against the real GitHub caller:
   - `token.actions.githubusercontent.com:aud` should be `sts.amazonaws.com`
   - `token.actions.githubusercontent.com:sub` must match the repository and ref pattern that actually triggered the run
3. Check that the trust relationship and caller flow include the right action for the path in use, especially `sts:AssumeRoleWithWebIdentity` for OIDC federation.
4. Audit migration leftovers from CircleCI:
   - roles that still require CircleCI-specific trust conditions such as `runtime = "CircleCI"`
   - providers or thumbprints registered only for CircleCI callers
   - role names or session-tag expectations that still point at the old runtime
5. Check whether the role requires session tags or transitive tags such as `aws:RequestedRegion`; if so, verify the caller includes them.
6. Look for common mismatches: wrong audience, subject condition too narrow for PRs vs branches, missing provider registration, or an outdated OIDC thumbprint.
7. Only after the assume-role path is proven correct should you route onward to stack, deployment, or Terraform-specific debugging.

## Outputs

- An evidence-backed IAM root-cause hypothesis for the AccessDenied.
- The smallest trust-policy, provider, or caller-shape correction needed to unblock OIDC auth.
- A clean route to `sam-cloudformation`, `terraform-skill`, or `github-actions-failure-triage` once IAM is no longer the blocker.

## Guardrails

- Never diagnose Terraform plan drift or SAM stack behavior before resolving an explicit AssumeRole denial.
- Never widen trust-policy conditions more than necessary; match the real repo/ref and audience precisely.
- Never ignore CircleCI-specific trust conditions during a GitHub Actions migration audit.
- Do not collect secret values; inspect identity shape, trust conditions, and policy text only.

## Validation

- Confirm the denied action (`sts:AssumeRole` vs `sts:AssumeRoleWithWebIdentity`) matches the trust-policy path you are fixing.
- Confirm `token.actions.githubusercontent.com:aud` is `sts.amazonaws.com` and that `sub` matches the real repo/ref or PR pattern.
- Confirm any required session tags or transitive tags are present in the caller configuration.
- Re-read the failing auth step after the change and verify IAM auth now succeeds before widening to stack or plan triage.
- Smoke test:
  - should trigger: "GitHub Actions fails in configure-aws-credentials with AccessDenied on sts:AssumeRoleWithWebIdentity for our deployment role."
  - should not trigger: "The workflow assumes the role successfully, but `sam deploy` then rolls back on an invalid template property." (→ `sam-cloudformation`)

## Examples

- "Trace why this GitHub Actions deployment role denies AssumeRoleWithWebIdentity and fix the trust policy instead of debugging the stack."
- "We migrated from CircleCI to GitHub Actions and now the deploy role denies OIDC callers; audit the trust policy for CircleCI-only conditions."
- "Check whether this role's `sub`, `aud`, and session-tag requirements match the repo, branch, and event that triggered the workflow."

## Reference files

- [`references/trust-policy-checklist.md`](references/trust-policy-checklist.md) - quick checks for trust-policy conditions, CircleCI migration leftovers, session tags, and route-away cues.
