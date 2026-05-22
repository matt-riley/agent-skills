# Triage scenarios

Use these as quick validation cases when checking whether the skill still routes cleanly.

| Scenario | Expected bucket | First move | Expected outcome |
| --- | --- | --- | --- |
| A workflow fails to parse after a YAML edit | Workflow syntax, trigger, or expression errors | Read the exact file and expression path that failed | Fix the malformed key or expression, then rerun once the file parses |
| A job gets `403` on a repository-owned secret | Permissions, token, secret, or variable issues | Confirm the expected secret or permission scope without printing values | Fix the repo wiring or escalate if the missing scope is org-admin managed |
| A job fails only on a self-hosted runner with a missing tool | Runner or environment mismatch | Compare `runs-on`, image labels, and shell assumptions against the failing step | Fix the runner requirement or escalate if fleet ownership sits outside the repo |
| Only one matrix leg fails on `ubuntu-latest / node-20` | Matrix or fan-out issues | Isolate the failing axis and compare setup branches | Tighten the matrix or axis-specific setup, then rerun the narrow leg |
| Downstream deployment cannot find an artifact | Cache, artifact, job-output, or cross-job handoff failures | Compare producer and consumer artifact paths | Fix the exact path or output contract, then rerun the consumer job |
| A reusable workflow rejects an input name | Reusable workflow or action interface issues | Inspect both caller and callee contracts together | Align the interface or pin the correct action ref |
| A downstream job is skipped after an upstream job is canceled by concurrency rules | Concurrency, cancellation, or dependency-order issues | Check concurrency groups, `cancel-in-progress`, and `needs` conditions together | Fix the dependency or concurrency rule, then rerun the blocked path once |
| The workflow is passing but the application deploy is broken | Project, test, deployment, or runtime failures | Confirm the workflow is only exposing a repo bug | Hand off to the code or config surface that actually failed |
