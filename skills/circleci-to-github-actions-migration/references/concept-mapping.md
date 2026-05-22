# CircleCI to GitHub Actions concept mapping

Use this reference while translating `.circleci/config.yml` into `.github/workflows/*.yml`.

| CircleCI concept | GitHub Actions concept | Migration notes |
| --- | --- | --- |
| `workflows` | workflow files in `.github/workflows/` | You may split one CircleCI workflow into multiple workflow files when it improves trigger clarity. |
| `jobs` | `jobs.<job_id>` | Keep job boundaries aligned with existing stages unless there is a clear reason to merge or split. |
| `steps` | `steps` | CircleCI `run` maps to a shell `run` step; CircleCI `checkout` maps to `actions/checkout`. |
| `orbs` | reusable workflows or actions | Map each orb capability to a trusted action, reusable workflow, or explicit steps. |
| `commands` | composite actions, reusable workflows, or repeated steps | Start with inline steps; extract later only when repetition is meaningful. |
| `executors` | `runs-on`, `container`, `services` | Translate machine/docker choices intentionally; do not assume ubuntu-latest parity automatically. |
| `parallelism` | `strategy.matrix` or explicit split jobs | Choose matrix when the same job logic runs across variants. |
| `context` | repository/org/environment secrets and variables | Preserve least-privilege access; map each secret source deliberately. |
| `filters` on branches/tags | `on` filters and job `if` conditions | Keep branch and tag semantics explicit at workflow and job levels. |
| `requires` | `needs` | Keep dependency graph readable and equivalent. |
| `when` | job/step `if` expressions | Translate conditional semantics carefully, especially for tag and branch patterns. |
| `persist_to_workspace` / `attach_workspace` | artifacts or caches, or job outputs | Use artifacts for handoff and traceability; use caches only for reusable dependency data. |
| `save_cache` / `restore_cache` | `actions/cache` | Keep cache keys deterministic and scoped to dependency lockfiles or tool versions. |
| `store_artifacts` | `actions/upload-artifact` | Preserve retention expectations and artifact naming. |
| `schedule` triggers | `on: schedule` | Verify cron timezone expectations and frequency. |

## Common translation checks

- Confirm every required CircleCI stage has an explicit GitHub Actions equivalent.
- Ensure required status checks still map to the correct workflow/job names.
- Verify deploy protections, manual approvals, and secret scopes for each environment.

## Permissions and secrets mapping

- CircleCI `context` values usually map to GitHub Actions repository, organization, or environment secrets.
- Prefer the narrowest secret scope that satisfies the job; do not promote a secret to a broader scope just to make the migration easier.
- Declare job `permissions` explicitly in GitHub Actions; CircleCI permissions are implicit, but GitHub Actions defaults are not enough to document intent.
- Use `environment:` for deploy jobs that need approvals, protected secrets, or environment-specific credentials.
- If a CircleCI job relied on OIDC or cloud federation, add the matching GitHub Actions identity permission deliberately and keep it isolated to that job.
