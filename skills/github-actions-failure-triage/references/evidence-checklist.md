# Evidence checklist

Gather this evidence before proposing workflow edits.

## Failure anchor

- run URL, run ID, job name, job ID, or failed check name
- exact attempt number when reruns are involved
- head SHA and branch or ref
- triggering event such as `push`, `pull_request`, `workflow_dispatch`, or `schedule`

## Failed-step evidence

- failing step name
- relevant log excerpt from the failing step
- nearby setup or prerequisite steps that explain how the failing step was reached
- whether the failure is deterministic, flaky, or only affecting one variant

## Source mapping

- exact workflow file at the failing commit
- called reusable workflow file or reference, if any
- action versions used on the failing path
- repository script, Make target, or package script invoked by the failing step

## Runtime context

- runner type: GitHub-hosted or self-hosted
- effective runner labels or image details when visible
- matrix values for the failing job
- `needs`, artifacts, caches, or job outputs relevant to the failing handoff

## Secrets and permissions

- expected permission scopes, secret names, and variable names
- whether reusable workflow inputs or secrets are passed explicitly or inherited

Do not collect secret values. Confirm names, scopes, and inheritance behavior only.

## Change framing

- whether the failure is new or pre-existing
- whether the base branch already fails the same surface
- smallest plausible change surface:
  - workflow YAML
  - called reusable workflow
  - repository code or config
  - no-edit diagnosis or escalation
