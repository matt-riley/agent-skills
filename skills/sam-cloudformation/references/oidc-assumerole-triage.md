# OIDC AssumeRole triage

Use this reference when the deployment fails at auth: an OIDC-federated caller
(usually GitHub Actions `configure-aws-credentials`) gets `AccessDenied` on
`sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`, before SAM or
CloudFormation has run anything.

Prove or fix the IAM trust, provider, audience, subject, or tagging contract
before investigating later stages. Do not diagnose stack rollback, drift, or
Terraform plan behavior while an explicit AssumeRole denial is unexplained.

## First move

1. Stop chasing later stack or plan failures until the IAM denial is explained.
2. Capture the exact failing action, target role, repo/ref context, and the
   expected `sub` and `aud` claims.
3. Compare the role trust policy to the real caller context before proposing any
   broader workflow change.

## Inputs to gather

**Required**

- The exact `AccessDenied` log line, including whether the failing action is
  `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`.
- The target IAM role trust policy and the configured OIDC provider.
- The caller identity shape: repository, ref, event type, expected `sub`, and
  audience.
- Any required session-tag or transitive-tag contract for the role.

**Helpful if present**

- The GitHub Actions auth step configuration.
- Previous CircleCI trust-policy snippets or migration notes.
- CloudTrail or AWS error context that confirms the denied principal and
  condition mismatch.
- The permission model for any follow-on role chaining.

**Only investigate if encountered**

- Permission boundaries or SCPs that alter an otherwise-correct trust policy.
- Multiple OIDC providers or duplicate audience settings.
- Cross-account role chaining after the first AssumeRole call succeeds.

## Triage workflow

1. Treat `AccessDenied` on `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`
   as the primary blocker.
2. Verify the role trust policy conditions against the real GitHub caller:
   - `token.actions.githubusercontent.com:aud` should be `sts.amazonaws.com`
   - `token.actions.githubusercontent.com:sub` must match the repository and ref
     pattern that actually triggered the run
3. Check that the trust relationship and caller flow include the right action for
   the path in use, especially `sts:AssumeRoleWithWebIdentity` for OIDC
   federation.
4. Audit migration leftovers from CircleCI:
   - roles that still require CircleCI-specific trust conditions such as
     `runtime = "CircleCI"`
   - providers or thumbprints registered only for CircleCI callers
   - role names or session-tag expectations that still point at the old runtime
5. Check whether the role requires session tags or transitive tags such as
   `aws:RequestedRegion`; if so, verify the caller includes them.
6. Look for common mismatches: wrong audience, subject condition too narrow for
   PRs versus branches, missing provider registration, or an outdated OIDC
   thumbprint.
7. Only after the assume-role path is proven correct should you continue into
   stack, deployment, or Terraform-specific debugging.

## Quick checks

- Anchor the exact denied action: `sts:AssumeRole` or
  `sts:AssumeRoleWithWebIdentity`.
- Confirm the role trust policy allows the right action for the caller path.
- Check `token.actions.githubusercontent.com:aud == sts.amazonaws.com`.
- Check `token.actions.githubusercontent.com:sub` against the real repository,
  ref, and event pattern.
- Audit migration leftovers from CircleCI, including provider setup, thumbprints,
  and trust conditions like `runtime = "CircleCI"`.
- Confirm required session tags or transitive tags are actually sent by the
  caller.

## Guardrails

- Never diagnose Terraform plan drift or SAM stack behavior before resolving an
  explicit AssumeRole denial.
- Never widen trust-policy conditions more than necessary; match the real
  repo/ref and audience precisely.
- Never ignore CircleCI-specific trust conditions during a GitHub Actions
  migration audit.
- Do not collect secret values; inspect identity shape, trust conditions, and
  policy text only.

## Validation

- Confirm the denied action (`sts:AssumeRole` versus
  `sts:AssumeRoleWithWebIdentity`) matches the trust-policy path you are fixing.
- Confirm `token.actions.githubusercontent.com:aud` is `sts.amazonaws.com` and
  that `sub` matches the real repo/ref or PR pattern.
- Confirm any required session tags or transitive tags are present in the caller
  configuration.
- Re-read the failing auth step after the change and verify IAM auth now succeeds
  before widening to stack or plan triage.

## Route onward when auth is no longer the blocker

- AssumeRole now succeeds and the failure is in the SAM template or
  CloudFormation stack lifecycle: return to the main
  [`sam-cloudformation`](../SKILL.md) workflow and the
  [deploy checklist](deploy-checklist.md).
- The infrastructure is Terraform-managed and the plan or apply itself fails
  after auth: route to [`terraform-skill`](../../terraform-skill/SKILL.md).
- The workflow is failing before the IAM auth step, or for non-IAM reasons:
  route to
  [`github-actions-failure-triage`](../../github-actions-failure-triage/SKILL.md).
- The blocker is Lambda packaging, runtime, or the handler after deployment auth
  works: route to
  [`aws-lambda-go-deployment`](../../aws-lambda-go-deployment/SKILL.md).
