# Packaging checklist

Use this quick reference when the failure is likely in the Lambda artifact rather than the stack.

## Quick checks

- Build for Lambda, not the local host: `GOOS=linux` and `GOARCH=amd64` or `arm64`.
- Prefer `sam build --use-container` for reproducible Linux builds.
- For custom runtimes, the deployed executable should be named `bootstrap`.
- If the template uses a handler path instead, confirm `Handler` matches the packaged executable path.
- Prefer `provided.al2` or `provided.al2023` for Go Lambda functions.
- Check CloudWatch for `INIT_START` and `START` before assuming the handler code is wrong.

## Route away when

- `sam validate --lint` or stack events point to template or CloudFormation failures.
- The deploy workflow fails on `AccessDenied` during AssumeRole or OIDC auth.
- The binary does not compile before packaging starts.
