# Trust policy checklist

Use this quick reference when an OIDC caller gets AWS AssumeRole access denied.

## Quick checks

- Anchor the exact denied action: `sts:AssumeRole` or `sts:AssumeRoleWithWebIdentity`.
- Confirm the role trust policy allows the right action for the caller path.
- Check `token.actions.githubusercontent.com:aud == sts.amazonaws.com`.
- Check `token.actions.githubusercontent.com:sub` against the real repository, ref, and event pattern.
- Audit migration leftovers from CircleCI, including provider setup, thumbprints, and trust conditions like `runtime = "CircleCI"`.
- Confirm required session tags or transitive tags are actually sent by the caller.
- Only after auth works should you widen into stack, deploy, or Terraform debugging.

## Route away when

- AssumeRole succeeds and the remaining failure is in SAM or CloudFormation.
- The plan or apply itself fails in Terraform after auth is working.
- The workflow is failing before the IAM auth step or for non-IAM reasons.
