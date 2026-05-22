---
name: circleci-to-github-actions-migration
description: Use when a repository still depends on .circleci/config.yml jobs, workflows, or artifacts that need to be replaced or phased out with GitHub Actions — including incremental shadow runs, staged cutover, and parity checks.
metadata:
  category: migrations
  audience: general-coding-agent
  maturity: beta
---

# CircleCI to GitHub Actions migration

## Use this skill when

- You need to replace or phase out `.circleci/config.yml` with `.github/workflows/*`.
- The repo still depends on CircleCI jobs, filters, contexts, or artifacts that need a faithful GitHub Actions translation.
- You need an incremental rollout path with low-risk parity checks.

## Do not use this skill when

- The repository is already fully on GitHub Actions and you only need minor workflow tuning.
- You are designing a brand-new CI pipeline with no CircleCI behavior to preserve.
- You are migrating between other CI systems (for example, Jenkins to GitHub Actions).

## Inputs to gather

**Required before editing**

- `.circleci/config.yml` (jobs, workflows, filters, executors, contexts, caches, artifacts).
- Existing `.github/workflows/*.yml` files or reusable workflows already in use.
- Required secrets, protected environments, deployment gates, and branch protections.

**Helpful if present**

- Recent successful CircleCI runs for timing and artifact parity checks.
- Repository scripts for build, lint, test, package, and release.

**Only investigate if encountered**

- Downstream infra or release automation that expects CircleCI-specific artifacts or status contexts.

## First move

1. Read `.circleci/config.yml` end-to-end and create a concept map using `references/concept-mapping.md`.
2. Draft one representative GitHub Actions workflow from the Node.js example in `assets/workflow-skeleton.yml`, or replace that skeleton first if the repo is not Node-based.
3. Validate trigger, matrix, cache, and secret parity for that workflow before translating the rest.

## Permissions and secrets mapping

- Map each CircleCI `context` to the narrowest GitHub Actions secret scope that fits: repository secret, organization secret, or environment secret.
- Keep job `permissions` explicit and minimal; add `id-token: write` only when the migration truly uses OIDC.
- For deployment jobs, pair `environment:` with the secrets and approval gates that protect that environment.
- Document every secret source and the job or environment that consumes it before removing the CircleCI context.

## Workflow

1. Inventory CircleCI jobs, commands, workflows, filters, contexts, cache keys, and artifacts.
2. Translate concepts using `references/concept-mapping.md`.
3. Create or update GitHub Actions workflows with explicit triggers, `permissions`, runner choices, and concurrency.
4. Recreate branch/path filters, matrix strategy, caches, artifacts, and environment protections intentionally.
5. Keep deployment stages explicit instead of collapsing distinct environments into one opaque job.
6. Run a staged rollout using `assets/rollout-checklist.md` before deleting CircleCI configuration.

## Guardrails

- **Must** preserve behavior for triggers, required checks, artifacts, and deployment protections.
- **Must** define secret usage and job `permissions` explicitly.
- **Must** treat `assets/workflow-skeleton.yml` as a Node.js example, not a repo-generic template.
- **Should** migrate incrementally (shadow run or staged cutover) for multi-workflow repositories.
- **Should** keep workflows readable and deterministic rather than embedding heavy shell logic.
- **May** reuse existing reusable workflows where they preserve parity.

## Routing boundary

- Use this skill directly for single-repo CircleCI→GitHub Actions migration work where parity mapping and staged cutover are the main tasks.
- Escalate to [`ci-migration-orchestrator`](../../agents/ci-migration-orchestrator.agent.md) when migration execution needs phased rollout choreography, multi-workflow coordination, or cross-surface sequencing beyond this reusable playbook.

## Validation

- Run repository build/test/lint commands locally where practical before relying on workflow runs.
- Run `action-validator` on each new or modified GitHub Actions workflow before parity comparison.
- Compare CircleCI and GitHub Actions outcomes for the same branch or commit range.
- Confirm required checks, protected branches, and deploy approvals behave as expected.
- Only remove `.circleci/config.yml` after successful parity and rollout checks.

- Smoke test:
  - should trigger: "Translate .circleci/config.yml jobs into GitHub Actions with parity checks."
  - should not trigger: "Diagnose why the deploy workflow fails on ubuntu-latest." (→ `github-actions-failure-triage`)

## Examples

- "Migrate a `build-and-deploy` CircleCI workflow to GitHub Actions, keep `main` deploys gated, and preserve the existing cache keys."
- "Translate a CircleCI test matrix with contexts and artifacts into GitHub Actions without changing required checks."
- "Plan a low-risk CircleCI retirement with a shadow run, explicit permissions, and rollback checkpoints."

## Reference files

- [CircleCI to Actions concept mapping](references/concept-mapping.md)
- [Workflow skeleton](assets/workflow-skeleton.yml)
- [Rollout checklist](assets/rollout-checklist.md)
