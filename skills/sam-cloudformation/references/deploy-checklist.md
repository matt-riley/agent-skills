# Deploy checklist

Use this quick reference when the failure is in the SAM template or CloudFormation stack lifecycle.

## Quick checks

- Confirm the template includes `AWSTemplateFormatVersion` and `Transform: AWS::Serverless-2016-10-31`.
- Run `sam validate --lint` before `sam deploy`.
- Prefer `!Sub` with `AWS::AccountId` and `AWS::Region` for portable ARNs.
- Read CloudFormation stack events to find the first broken resource.
- If the stack is in `UPDATE_ROLLBACK_FAILED`, inspect drift before using `aws cloudformation continue-update-rollback`.
- For SQS or DynamoDB event sources that need partial batch failure handling, set `FunctionResponseTypes` intentionally.
- Prefer SAM/CloudFormation reference workflows for OIDC deploy auth rather than Terraform-shaped examples.

## Route away when

- The Lambda binary, runtime, or zip layout is the real blocker.
- IAM role assumption fails before the stack starts changing.
- Terraform owns the infrastructure instead of SAM or CloudFormation.
