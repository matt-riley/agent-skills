# Failure buckets

Use this guide to classify the failure before editing anything.

| Bucket | Common symptoms | First checks |
| --- | --- | --- |
| Workflow syntax, trigger, or expression errors | Workflow fails to parse, never triggers as expected, or errors on expressions or unknown keys | Check the exact workflow YAML, trigger filters, `if:` conditions, and expression references |
| Permissions, token, secret, or variable issues | 403s, missing secret messages, permission denied errors, or reusable workflow auth failures | Inspect `permissions`, secret and variable names, inheritance behavior, and whether the workflow path actually has the scopes it needs |
| Runner or environment mismatch | Missing tools, wrong shell behavior, path issues, unavailable labels, or self-hosted-only failures | Check `runs-on`, runner image or labels, shell assumptions, and whether the failing tool exists on that runner |
| Matrix or fan-out issues | Only one axis fails, wrong include or exclude behavior, or unsupported version combinations | Inspect matrix expansion, job naming, and any axis-specific expressions or setup logic |
| Cache, artifact, job-output, or cross-job handoff failures | Missing artifacts, wrong paths, cache misses, empty uploads, or downstream jobs cannot find prior outputs | Verify upload and download names, exact paths, job `needs`, output wiring, and whether the producer job actually created the expected files |
| Reusable workflow or action interface issues | Caller and callee disagree on inputs, secrets, outputs, or refs; action inputs are rejected | Inspect `workflow_call` inputs and secrets, `uses:` refs, action version docs, and the caller or callee contract |
| Concurrency, cancellation, or dependency-order issues | Runs are canceled unexpectedly, jobs are skipped, or outputs are missing because prerequisites never ran | Check concurrency groups, `cancel-in-progress`, `needs`, and skip conditions |
| Project, test, deployment, or runtime failures | Tests fail honestly, deploy contracts are wrong, or application code is broken even though workflow plumbing is fine | Confirm whether the workflow only exposed a repository bug and route the fix to the actual code or config surface |

## Notes on recurring high-signal buckets

### Artifact and path mismatches

Treat artifact failures as a contract problem, not just an upload or download problem. Check:

- artifact name
- exact upload path
- exact download path
- whether a reusable workflow expects a different root layout than the producer created
- whether the downstream job is reading the same directory shape the upstream job actually wrote

### Reusable workflow contract mismatches

When a reusable workflow is involved, inspect both sides:

- caller `with:` inputs
- caller `secrets:` or `secrets: inherit`
- callee `workflow_call` contract
- any assumptions about working directory, artifact root, or output names

### Workflow vs application failures

Do not stop at "the workflow failed." Decide whether the failing step proves:

- the workflow wiring is broken
- the workflow is fine but the underlying code or deploy contract is broken
- the failure is external or flaky and needs escalation or careful rerun strategy
