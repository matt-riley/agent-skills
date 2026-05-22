---
name: terraform-skill
description: "Use when writing, reviewing, or debugging Terraform/OpenTofu — modules, tests, CI/CD, security scans, or state operations."
metadata:
  category: terraform
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# Terraform skill

Use this skill when working with Terraform or OpenTofu infrastructure code. It diagnoses the failure mode first, then loads only the relevant reference file rather than preloading all context.

## Use this skill when

- Creating or reviewing Terraform/OpenTofu configurations or modules
- Setting up or debugging tests (native `terraform test`, Terratest, mock providers)
- Structuring multi-environment deployments or choosing module patterns
- Implementing or debugging IaC CI/CD pipelines
- Configuring or migrating remote state backends
- Choosing state organization for multi-team environments
- Performing security scans or compliance checks on Terraform code

## Do not use this skill when

- The question is basic HCL syntax already in model knowledge — answer directly
- The question is about a cloud provider API unrelated to Terraform (link to provider docs instead)
- The question is about CI/CD for a non-IaC project — use `circleci-to-github-actions-migration` or `github-actions-failure-triage`

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Terraform/OpenTofu module authoring, review, or debugging | Yes | — |
| GitHub Actions workflow for a non-Terraform project | No | `circleci-to-github-actions-migration` or `github-actions-failure-triage` |
| Security scan failures on non-IaC code | No | `secret-scan-triage` |
| General code navigation or LSP usage | No | `code-intelligence` |
| Root-cause debugging a specific Terraform failure | Yes (diagnose failure mode first) | `systematic-debugging` if the failure is not IaC-specific |

## Inputs to gather

**Required before starting**
- Terraform/OpenTofu version (determines which features are available — see Feature Guard Table in `references/code-patterns.md`)
- Backend type (S3, Azure, GCS, Terraform Cloud, local)
- Provider list and approximate versions
- Execution path (local CLI, CI/CD, Terraform Cloud/Enterprise)
- Criticality of the target environment (prod / non-prod)

**Helpful if present**
- Existing `versions.tf` and `.terraform.lock.hcl`
- CI configuration files (`.github/workflows/`, `.circleci/config.yml`)
- Current error output or `terraform plan` output
- Existing module structure

**Only investigate if encountered**
- Multi-team state sharing patterns (check `references/state-management.md`)
- Sentinel/OPA policy configurations
- Atlantis or Terraform Cloud run triggers

## First move

1. Establish the version floor — check the runtime version against the Feature Guard Table in `references/code-patterns.md` before emitting any feature-specific HCL.
2. Diagnose the failure mode using the routing table below, then load only the matching reference file.
3. Emit the Response Contract before generating any HCL, CI changes, or state operations.

## Workflow

**Diagnose the failure mode first — load only the matching reference file:**

| Failure mode | Symptoms | Load |
| --- | --- | --- |
| Identity churn | Resource addresses shift after refactor, `count` index churn, missing `moved` blocks | `references/code-patterns.md` |
| Secret exposure | Secrets in defaults, state, logs, or CI artifacts | `references/security-compliance.md`, `references/code-patterns.md`, `references/state-management.md` |
| Blast radius | Oversized stacks, shared prod/non-prod state, unsafe applies | `references/state-management.md`, `references/module-patterns.md` |
| CI drift | Local plan ≠ CI plan, unpinned versions, no reviewed artifact | `references/ci-cd-workflows.md`, `references/code-patterns.md` |
| Compliance gaps | No policy stage, no approval model, no evidence retention | `references/security-compliance.md`, `references/ci-cd-workflows.md` |
| Testing blind spots | Plan-only computed values, set-type `[0]` indexing | `references/testing-frameworks.md` |
| State corruption/recovery | Stuck lock, backend migration, drift reconciliation | `references/state-management.md` |
| Provider upgrade risk | Breaking-change bump, unpinned modules | `references/code-patterns.md`, `references/module-patterns.md` |
| Provider lifecycle | Removing a provider with resources still in state | `references/state-management.md` |
| Navigation/safe rename | Cannot locate symbol definitions/refs semantically | `references/code-intelligence-lsp.md` |

**Then follow these steps:**

1. Capture execution context: runtime version, exact providers, backend type, execution path, environment criticality.
2. Diagnose failure mode using the table above.
3. Load only the matching reference file — do not preload all references.
4. Propose fix with risk controls and tradeoffs.
5. Generate artifacts: HCL, `moved`/`import`/`removed` blocks, CI changes, policy rules.
6. Validate with risk-tier commands (`fmt -check`, `validate`, `plan -out`, policy check).
7. Emit the Response Contract.

## Outputs

- HCL changes: resource blocks, `moved`/`import`/`removed` blocks, `versions.tf`, variable and output contracts
- CI/CD workflow files: GitHub Actions, GitLab CI, Atlantis configuration
- Policy rules: OPA Rego, Sentinel
- Response Contract (mandatory on every response):
  1. Assumptions and version floor
  2. Risk category addressed (identity churn / secret exposure / blast radius / CI drift / compliance gaps / state corruption / provider upgrade risk / testing blind spots)
  3. Chosen remediation and tradeoffs
  4. Validation plan — exact commands
  5. Rollback notes for destructive or state-mutating changes

## Guardrails

- Always emit the Response Contract — never omit version floor or risk category
- Never generate `for_each` keyed on a computed attribute (`.id`, `.arn`) — keys must be known at plan time
- Never claim `sensitive = true` keeps a value out of state — use `ephemeral` (1.10+) or `write_only` (1.11+) for state exclusion
- Never use DynamoDB for S3 state locking on Terraform 1.10+ — use `use_lockfile = true`
- Never rename a resource without a `moved` block (requires 1.1+)
- Never emit a feature above the version floor without an explicit version guard comment
- Always check the terraform-ls Capability Matrix (`references/code-intelligence-lsp.md`) before claiming an LSP operation is available
- Do not load all reference files speculatively — load only what the diagnosed failure mode requires

## Validation

- Run `terraform fmt -check && terraform validate && terraform plan -out=tfplan` in order
- Run `trivy config .` or `checkov -d .` for security scans
- Smoke-test trigger: "Create a Terraform module for an AWS S3 bucket with versioning and encryption" — skill should activate
- Smoke-test near-miss: "Set up a GitHub Actions workflow for a Node.js project" — skill should not activate

- Smoke test:
  - should trigger: "Debug this Terraform module and plan failure in our AWS stack."
  - should not trigger: "Diagnose a failing GitHub Actions job in a non-Terraform repo." (→ `github-actions-failure-triage`)

## Examples

- "Review this Terraform configuration — it has a public S3 bucket and a security group open to 0.0.0.0/0"
- "I'm upgrading the AWS provider from 4.x to 5.x, what breaking changes and `moved` blocks do I need?"
- "Set up a GitHub Actions pipeline for Terraform with Infracost, plan review, and protected applies on main"

## Reference files


| [`PROVENANCE.md`](PROVENANCE.md) | Skill provenance, changelog, and authorship |
- [`references/code-patterns.md`](references/code-patterns.md) — count vs for_each, `moved` blocks, write-only args, Feature Guard Table (17 features with version floors and LLM error patterns)
- [`references/module-patterns.md`](references/module-patterns.md) — architecture principles, naming conventions, variable/output contracts, provider alias passing
- [`references/state-management.md`](references/state-management.md) — S3/Azure/GCS/TFC backends, native lock-file, migration, multi-team isolation, disaster recovery
- [`references/testing-frameworks.md`](references/testing-frameworks.md) — static analysis, native `terraform test` (1.6+), Terratest, mock providers (1.7+)
- [`references/ci-cd-workflows.md`](references/ci-cd-workflows.md) — GitHub Actions, GitLab CI, Atlantis, Infracost, OIDC trust correctness table, drift detection
- [`references/security-compliance.md`](references/security-compliance.md) — Trivy/Checkov, secrets handling, state-file hardening, IAM least-privilege, compliance mappings
- [`references/quick-reference.md`](references/quick-reference.md) — command cheat sheets, decision flowcharts, Terraform vs OpenTofu comparison, troubleshooting
- [`references/code-intelligence-lsp.md`](references/code-intelligence-lsp.md) — terraform-ls capability matrix, position-anchored LSP calls, degradation gate, manual rename protocol
