# CircleCI to GitHub Actions rollout checklist

## Before translation

- [ ] Inventory CircleCI workflows, jobs, filters, caches, artifacts, and contexts.
- [ ] Identify required status checks and deployment gates.
- [ ] Confirm owner for CI secrets and environment protections.

## During translation

- [ ] Preserve trigger coverage (push, pull request, tags, schedules, manual dispatch).
- [ ] Preserve stage boundaries (build/test/package/deploy) unless intentionally changed.
- [ ] Define explicit workflow and job permissions.
- [ ] Map every CircleCI context to a concrete GitHub Actions secret or environment secret.
- [ ] Recreate cache keys and artifact publishing behavior.
- [ ] Keep branch and tag filters equivalent.

## Staged rollout

- [ ] Run GitHub Actions in parallel with CircleCI on representative branches.
- [ ] Compare success/failure behavior and artifact outputs.
- [ ] Validate required checks in branch protection settings.
- [ ] Validate environment approvals and deployment protections.

## Cutover

- [ ] Switch required checks to GitHub Actions workflow/job names.
- [ ] Remove or disable CircleCI-triggered checks only after parity is proven.
- [ ] Retain rollback path (ability to re-enable CircleCI temporarily) until stable.

## Post-cutover

- [ ] Remove stale CircleCI-only docs and references.
- [ ] Archive migration notes and parity evidence for future audits.
- [ ] Monitor first production-bound runs for regressions.
