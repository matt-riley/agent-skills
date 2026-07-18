# Skill selection guide

This guide helps you choose among the active skills in `skills/*`.
Start with the skill whose deliverable most directly matches the user's request, then add overlays only when they contribute distinct operational knowledge.

`skills/<name>/SKILL.md` remains the source of truth for any individual skill's workflow, boundaries, and support files.

## Core defaults

Start with these when the request matches them directly:

- `testing-workflows` — default test/debug loop for Go changes and unexpected failures
- `implementation-review` — default finished-code review workflow
- `security-basics` — cross-cutting auth, request-handling, and data-exposure guardrails
- `code-generation` — prerequisite overlay when generated output may be stale

## Archived skills

One-shot migration skills live in `archived/`. They're still available but excluded from active discovery:

- `archived/aws-sdk-v2-to-v3-migration` — AWS SDK v2 to v3 migration
- `archived/circleci-to-github-actions-migration` — CircleCI to GitHub Actions migration
- `archived/mocha-to-jest-migration` — Mocha to Jest migration
- `archived/project-references-migration` — TypeScript Project References migration

## High-visibility operational guardrail

- `configuration-env` — keep this easy to find for startup failures, env drift, and deployment/config debugging, but do not force it into every task by default

## Local harness / personal environment

These skills depend on personal harness tooling and are **not portable to every agent environment**:

- `session-store-history` — cross-session recall via `session_store` (requires a read-only SQL tool and `session_store` access)
- `resolve-open-loops` — Lore `open_loop` / `assistant_goal` triage (requires Lore memory tools and the stabilisation-guard flow)

Load them only when the current harness exposes those tools; otherwise surface the limitation and use another evidence source.

## Families

### Governance and process

- `rpi-workflow` — full Research -> Plan -> Implement -> Validate discipline for non-trivial work
- `plan-review` — plan drafting, hardening, approval gates, and optional structured reviewer personas
- `plan-review-loop` — structured reviewer-persona loop (Jason and Freddy) that enforces unanimous approval over up to three rounds
- `reverse-prompt` — sharpen a rough ask into a repository-grounded execution brief or contract-shaped brief before work starts
- `implementation-review` — post-implementation review and approval
- `verification-before-completion` — mandatory pre-done checklist that blocks task completion until evidence passes
- `resolve-open-loops` — close or hand off deferred items, open questions, and unresolved decisions
- `workflow-contracts` — define and enforce explicit entry/exit contracts for multi-step workflows
- `agent-instructions` — create or update AGENTS.md, copilot-instructions.md, and per-path instruction guides when agent guidance is stale or missing

### Session history and recall

- `session-store-history` — search past sessions through `session_store` to answer prior-work, prior-approach, and session-to-ref tracing questions

### Writing and GitHub presence

- `writing-and-editing` — draft structured documents, audit prose readability, and review short metadata strings
- `github-presence` — improve GitHub profiles, org profile pages, repo presentation, and community-health surfaces

### TypeScript typing and config

- `tsc-error-triage` — root-cause-first triage for TypeScript compiler failures
- `tsconfig-hardening` — tighten or rationalize `tsconfig` safely and incrementally
- `schema-boundary-typing` — align runtime validation with truthful TypeScript boundary types
- `type-test-authoring` — add compile-time type regression tests for important APIs
- `typescript-any-eliminator` — systematically hunt and replace `any` types with precise inferred or explicit types

### JavaScript and TypeScript code health

- `knip` — find unused dependencies, exports, files, and unresolved imports with Knip in JS/TS projects
- `fallow` — audit JS/TS code health with the Fallow tool: dead code, duplication, circular dependencies, boundaries, and complexity

### CI and delivery workflows

- `github-actions-failure-triage` — diagnose existing failing GitHub Actions runs with evidence-first minimal fixes
- `github-actions-local-repro` — reproduce a GitHub Actions failure locally using act, Docker, or shell isolation
- `goreleaser-release-pipeline` — configure and operate a GoReleaser release pipeline with artifacts and changelogs
- `ci-images` — local CI parity and image-publishing workflows

### Testing, APIs, and delivery checks

- `integration-testing-http` — specialist overlay for endpoint, auth, request/response, and HTTP contract testing
- `http-api-openapi` — keep handler and spec changes in sync
- `test-driven-development` — strict TDD discipline: failing test → minimal pass → refactor
- `systematic-debugging` — structured root-cause debugging when immediate fixes are elusive
- `api-smoke-validation` — post-deploy smoke tests that verify key API endpoints are alive and correct

### Go development

- `go-build-and-test` — build, vet, and test Go packages with correct module and toolchain usage
- `go-cli-development` — develop, structure, and release Go CLI tools with cobra, goreleaser, and Homebrew
- `go-docker-builds` — containerize Go services with multi-stage Docker builds, scratch images, health checks, and CI
- `go-error-patterns` — apply idiomatic Go error wrapping, sentinel values, and `errors.As`/`errors.Is` patterns
- `aws-lambda-go-deployment` — package and deploy Go functions to AWS Lambda with the right runtime and IAM config

### Schema and persistence

- `database-migrations` — general database migration workflow
- `cloudflare-d1-migrations` — Cloudflare D1 migration workflow for Wrangler, local/preview/remote promotion, and recovery
- `cloudflare-d1-query-tuning` — Cloudflare D1 runtime query and repository-path tuning when schema or migration changes are out of scope
- `repository-adapters` — repository-layer adapter changes and DB error mapping

### Operations and runtime environment

- `docker-compose-dev` — local multi-service stack setup for prod-like development
- `observability-metrics` — `/health`, `/metrics`, and logging behavior validation

### Cloud and infrastructure

- `sam-cloudformation` — author, validate, and deploy SAM templates and CloudFormation stacks
- `terraform-skill` — write, plan, apply, and troubleshoot Terraform configurations and state
- `iam-oidc-triage` — diagnose and fix IAM OIDC trust policy failures for GitHub Actions, AWS, and GCP
- `secret-scan-triage` — identify, remediate, and prevent secret leaks caught by Trufflehog, GitGuardian, or similar scanners

### Frontend and site quality

- `astro-seo` — Astro-specific SEO implementation and audit work
- `make-interfaces-feel-better` — UI polish for existing interfaces
- `templ-templates` — server-side templ template authoring and regeneration workflows

### Git and branch workflow

- `review-comment-resolution` — apply PR feedback, push the fix branch, and wait for resulting checks
- `git-worktrees` — set up isolated worktrees for parallel tasks, agents, or safer branch isolation
- `finishing-a-development-branch` — complete all finishing steps on a feature branch before opening a PR
- `github-cli-pr-workflow` — create, review, and merge pull requests using the GitHub CLI
- `git-signing-troubleshoot` — diagnose and fix commit/tag signing failures (GPG, SSH, 1Password)
- `worktrunk` — operate the Worktrunk git workflow tool for step-commit, squash-rebase, and trunk management

### Research, knowledge, and discovery

- `find-skills` — discover an existing local catalog skill when skill lookup is the deliverable; do not use it as a wrapper around a directly requested task (experimental; explicit invocation preferred)
- `acquire-codebase-knowledge` — deep-map an existing codebase into seven structured docs covering stack, architecture, conventions, integrations, testing, and concerns
- `autoresearch` — execute an automated research pass across docs, code, and search to answer a question or validate a claim
- `code-tour` — create or follow a guided tour through an unfamiliar codebase
- `context-map` — produce a domain-driven context map of bounded contexts and their integration relationships
- `code-intelligence` — preferred routing layer for LSP, grep, and glob operations; always use LSP over text search when available
- `graphify` — turn a mixed document or code corpus into a persistent knowledge graph and graph-oriented exports; use direct analysis skills when no graph artifact is needed (experimental; explicit invocation preferred)

### AI agent development

- `agent-governance` — implement safety, policy, trust scoring, and audit patterns for AI agents that call external tools
- `agent-supply-chain` — add integrity manifests and promotion gates to agent plugin and tool pipelines
- `agentic-eval` — design and run behavioral evaluations for agent skills and trigger accuracy

### Writing, docs, and planning artifacts

- `doc-coauthoring` — co-author technical documentation with a domain expert in an iterative Q&A loop
- `to-prd` — generate a Product Requirements Document from a feature idea or conversation
- `to-issues` — convert a conversation, PRD, or plan into well-formed GitHub issues
- `skill-authoring` — design, write, and improve reusable skills in this catalog
- `skill-creator` — create or upgrade a skill with frontmatter, headings, evals, and validation

### Developer experience and tooling

- `neovim-config` — configure and extend a Neovim setup with plugins, keymaps, and LSP wiring
- `neovim-plugin-development` — develop, test, and release Neovim Lua plugins with plenary, CI, and docs
- `grill-me` — generate adversarial questions to stress-test your understanding of a codebase or design
- `grill-with-docs` — challenge an implementation against official docs to surface gaps and misnomers
- `ast-grep` — run structural code search and rewrite using ast-grep patterns
- `modern-web-guidance` — apply current web platform guidance for a specific framework or API decision

## Selection rules

- Prefer the sharpest direct match over a generic process wrapper.
- Prefer the skill whose `Use this skill when` most directly matches the requested deliverable.
- If a skill's `Do not use this skill when` would apply, do not load it just because adjacent concepts appear.
- Use `rpi-workflow` when the task is genuinely multi-phase and execution discipline matters, not as the first answer to every non-trivial request.
- Use `plan-review` when planning is the deliverable; use `implementation-review` when reviewing finished work is the deliverable.
- Use `writing-and-editing` when the main work is writing quality; use `github-presence` when the task is broader GitHub-surface setup or audit.
- Keep specialist skills when they preserve unique operational traps, recovery knowledge, or repo-contract checks.
- Treat `code-generation` as a prerequisite overlay unless regeneration itself is the main task.

## Quick chooser

| If the user asks for... | Start with... | Why |
| --- | --- | --- |
| a full research -> plan -> implement -> validate pass | `rpi-workflow` | Full lifecycle discipline is the primary need |
| a plan, plan hardening, or reviewer-gated planning | `plan-review` | Planning is the deliverable; implementation is not yet in scope |
| running a multi-reviewer approval loop on a completed /plan | `plan-review-loop` | Structured multi-round reviewer-persona loop with explicit verdict tokens is the main mechanism |
| a rough prompt that should be sharpened into an executable repo-grounded brief | `reverse-prompt` | Prompt critique or rewrite is the primary need before work starts |
| an explicit definition of done, success criteria, or a contract-shaped execution brief | `reverse-prompt` | Contract-shaped brief framing now lives with prompt sharpening |
| what they worked on before, whether they handled a topic already, or which session linked to a file / PR / issue | `session-store-history` | Cross-session recall from `session_store` is the main task |
| a structured technical document, prose audit, or metadata-string review | `writing-and-editing` | Writing work is the main deliverable |
| review or approval of code that already exists | `implementation-review` | Post-implementation review is the primary task |
| PR review feedback that must be fixed, pushed, and carried through CI/checks | `review-comment-resolution` | Applying reviewer feedback is the deliverable, not reviewing code from scratch |
| TypeScript compiler errors or strictness regressions | `tsc-error-triage` | Fix the highest-fanout type failure before patching leaf call sites |
| safer `tsconfig` tightening or cleanup | `tsconfig-hardening` | Configuration hardening is the primary risk |
| runtime validation that should match TypeScript types | `schema-boundary-typing` | Boundary truthfulness is the main need |
| compile-time type regression coverage | `type-test-authoring` | Protect inference and assignability contracts directly |
| a normal Go testing/debug loop | `testing-workflows` | Default testing entry point |
| HTTP request/response, auth, or endpoint contract testing | `testing-workflows` + `integration-testing-http` | Keep the default testing loop and layer the HTTP specialist |
| handler changes that must stay aligned with an OpenAPI spec | `http-api-openapi` | Spec/code synchronization is the main risk |
| a failing GitHub Actions run, job, or check | `github-actions-failure-triage` | Evidence-first CI diagnosis is the main task |
| CI image or local CI parity checks | `ci-images` | Focuses on CI/publishing workflows rather than app tests |
| a security or privacy guardrail review on auth, logging, or sensitive endpoints | `security-basics` | Cross-cutting safety review is the primary need |
| a database migration workflow (schema change, index, constraint) | `database-migrations` | Migration create/apply/rollback is the main risk |
| a Cloudflare D1 migration, D1 import, or local/preview/remote migration drift | `cloudflare-d1-migrations` | Wrangler and D1 environment semantics are the main risk |
| a slow Cloudflare D1 query or D1-backed repository path that must improve without schema or migration changes | `cloudflare-d1-query-tuning` | Runtime D1 tuning needs binding-aware repro steps and no-schema rewrite rules |
| database repository adapter changes or DB error mapping | `repository-adapters` | Adapter-boundary changes need repo/domain-layer care |
| generated code that feeds builds/tests (sqlc, templ, codegen) | `code-generation` | Regeneration prerequisite overlay |
| server-side templ templates or handler wiring | `templ-templates` | Generated-template authoring is the specialty |
| local multi-service stack setup via Docker Compose | `docker-compose-dev` | Local orchestration is the blocker |
| `/health`, `/metrics`, or logging verification | `observability-metrics` | Observability behavior is the main concern |
| env loading, `.env`, startup config drift, or repo-owned runtime config issues like missing Wrangler bindings | `configuration-env` | Operational configuration is the main problem |
| GitHub profile, org profile, repo README polish, or community health files | `github-presence` | GitHub-surface quality is the main task |
| Astro SEO work | `astro-seo` | Astro-specific SEO implementation and audit risks dominate |
| interface polish on an existing UI | `make-interfaces-feel-better` | Detail-level visual and interaction quality is the main problem |
| isolated parallel checkouts, agent lanes, or safer multi-branch task setup | `git-worktrees` | Worktree setup and isolation are the main problem |
| TDD, strict red-green-refactor cycle | `test-driven-development` | TDD discipline is the main ask |
| a bug that resists quick diagnosis | `systematic-debugging` | Root-cause methodology beats random patch attempts |
| post-deploy API smoke checks | `api-smoke-validation` | Smoke validation is the primary delivery gate |
| mapping or documenting an unfamiliar codebase | `acquire-codebase-knowledge` | Produces 7 structured knowledge docs in docs/codebase/ |
| a PRD from a feature idea or conversation | `to-prd` | PRD generation is the deliverable |
| converting a plan or PRD into GitHub issues | `to-issues` | Issue creation is the deliverable |
| Go build, vet, or test issues | `go-build-and-test` | Go module and toolchain handling is the speciality |
| building or releasing a Go CLI tool | `go-cli-development` | Go CLI structure, subcommands, flags, goreleaser, and Homebrew |
| containerizing a Go service for production | `go-docker-builds` | Multi-stage Docker builds, scratch images, health checks, and CI |
| Go error wrapping, sentinel errors, or errors.As/Is patterns | `go-error-patterns` | Idiomatic Go error handling is the focus |
| a GoReleaser release pipeline | `goreleaser-release-pipeline` | Release artifacts and changelogs are the main output |
| reproducing a GitHub Actions failure locally | `github-actions-local-repro` | Local repro beats remote re-run for diagnosis |
| SAM or CloudFormation template work | `sam-cloudformation` | SAM/CFN syntax, deploy, and stack management are the focus |
| Terraform write, plan, or apply work | `terraform-skill` | Terraform config, state, and provider patterns are the focus |
| IAM OIDC trust failures or GitHub Actions AWS auth | `iam-oidc-triage` | OIDC trust policy diagnosis is the speciality |
| secret scanning alerts or leak remediation | `secret-scan-triage` | Secret identification and rotation are the main risk |
| finishing, polishing, or PR-readying a feature branch | `finishing-a-development-branch` | Branch completion checklist is the deliverable |
| creating or merging a PR with the GitHub CLI | `github-cli-pr-workflow` | `gh` PR workflow is the primary tool |
| GPG, SSH, or 1Password commit signing failures | `git-signing-troubleshoot` | Signing configuration diagnosis is the speciality |
| running the Worktrunk git workflow | `worktrunk` | Worktrunk commands, squash-rebase, and trunk ops are the focus |
| TypeScript `any` elimination or type tightening | `typescript-any-eliminator` | Systematic any removal is the deliverable |
| finding unused dependencies, exports, files, or unresolved imports in a JS/TS repo | `knip` | Knip-based codebase health analysis is the main need |
| auditing JS/TS dead code, duplication, circular dependencies, or architecture boundaries with Fallow | `fallow` | Fallow tool is requested or the scope is broader than unused-import detection |
| writing or improving reusable skills | `skill-authoring` | Skill authorship is the primary task |
| creating a new skill or upgrading an existing one with correct frontmatter and evals | `skill-creator` | Skill creation/upgrade workflow with validation is the deliverable |
| adversarial questioning to stress-test a design | `grill-me` | Adversarial review is the main format |
| challenging an implementation against official docs | `grill-with-docs` | Doc-grounded critique is the main format |
| AI agent policy, tool allowlists, or audit trails | `agent-governance` | Runtime governance patterns are the speciality |
| AI agent plugin integrity or promotion gates | `agent-supply-chain` | Supply chain verification is the main risk |
| evaluating AI agent trigger accuracy or behavior | `agentic-eval` | Behavioral evaluation methodology is the focus |
| recovering a stalled, blocked, or dormant task from partial context | `resolve-open-loops` | Open-loop and stalled-task recovery is the main need |
| closing deferred items, open questions, or unresolved decisions | `resolve-open-loops` | Open-loop closure and handoff is the deliverable |
| defining or enforcing explicit entry/exit contracts for multi-step workflows | `workflow-contracts` | Contract-shaped workflow boundaries are the main risk |
| a mandatory pre-completion verification checklist | `verification-before-completion` | Evidence-gated sign-off is the main mechanism |
| creating or updating AGENTS.md, copilot-instructions.md, or per-path instruction guides | `agent-instructions` | Instruction-file setup and maintenance is the deliverable |
| co-authoring technical documentation with iterative Q&A | `doc-coauthoring` | Document structure and prose co-authorship is the main need |
| a pre-edit context map or survey of likely files and patterns | `context-map` | Contextual file-and-pattern mapping is the main deliverable |
| creating a guided code tour or narrative walkthrough | `code-tour` | Step-by-step `.tour` file creation is the deliverable |
| an automated research pass to answer a question or validate a claim | `autoresearch` | Autonomous iterative research is the main mechanism |
| structural code search, codemod rewrites, or ast-grep patterns | `ast-grep` | Syntax-aware search and rewrite is the speciality |
| modern web platform patterns, HTML, CSS, forms, or web API guidance | `modern-web-guidance` | Current web platform guidance prevents legacy patterns |
| Neovim config, plugins, LSP wiring, or startup behavior | `neovim-config` | Neovim Lua configuration is the speciality |
| developing a Neovim Lua plugin | `neovim-plugin-development` | Plugin structure, plenary tests, CI, and documentation |
| AWS Lambda Go packaging, bootstrap, or deployment | `aws-lambda-go-deployment` | Lambda runtime and IAM config for Go is the focus |
| code navigation, symbol lookup, or LSP vs grep routing decisions | `code-intelligence` | Routing layer for LSP over text search is the main value |

## Boundary reminders

Keep these boundaries crisp instead of broadening nearby skills:

- `git-worktrees` should own worktree setup and isolation for parallel or multi-branch work; do not bury worktree mechanics inside `rpi-workflow`, `plan-review`, or implementation skills.
- `review-comment-resolution` should own "apply review feedback and update the code/tests" work; keep it separate from `implementation-review`, which evaluates existing code rather than carrying feedback through to completion.
- `reverse-prompt` should own prompt and execution-brief sharpening; keep it separate from `plan-review`, which owns plan artifacts and approval gates.
- `writing-and-editing` should own reader-facing writing work; keep it separate from `github-presence`, which owns broader profile and repository-surface audits.
- `session-store-history` should own cross-session recall and session-to-ref/file tracing; keep it separate from current-workspace repo exploration, which should stay with repo-local search tools.
- `cloudflare-d1-query-tuning` should own runtime D1 query-shape and access-path tuning without schema changes; keep it separate from `cloudflare-d1-migrations` and from generic `repository-adapters` work when Cloudflare D1 runtime behavior is the main risk.
- `acquire-codebase-knowledge` should own deep seven-document codebase mapping; do not conflate it with narrow file reads, quick architecture sketches, or ad-hoc questions about single modules.
- `fallow` and `knip` are both JS/TS code-health tools but target different tools and scopes: prefer `knip` when the Knip tool is explicitly requested or the need is unused dependencies, exports, or unresolved imports; prefer `fallow` when the Fallow tool is requested or the analysis covers duplication, circular dependencies, complexity hotspots, architecture boundaries, or CI audit gates.
- `plan-review-loop` is distinct from `plan-review`; `plan-review` owns plan drafting and one-shot approval; `plan-review-loop` owns the explicit multi-round reviewer-persona loop with Jason and Freddy.
- `verification-before-completion` should block final task sign-off; keep it separate from `implementation-review`, which evaluates code quality rather than completion criteria.
- `agent-governance` owns runtime policy and trust enforcement; keep it separate from `security-basics`, which owns static auth and data-exposure guardrails.
- `code-intelligence` is a routing overlay that ensures LSP is used when available; it should not be selected as the primary skill for work that has a more specific match.
- `neovim-config` owns editing user-level Neovim configuration (init.lua, lazy.nvim specs, LSP wiring); `neovim-plugin-development` owns building, testing, and releasing Neovim Lua plugins — these are complementary but distinct surfaces.
- `go-build-and-test` owns Go build failures, toolchain mismatches, and CI-parity issues; `go-cli-development` owns CLI project structure, subcommand patterns, goreleaser, and Homebrew distribution — building vs authoring are different concerns.
- `go-docker-builds` owns production Dockerfiles for Go services; `docker-compose-dev` owns local multi-service development stacks — production images vs local dev environments are different workflows.

## Layering notes

- `plan-review` beats `rpi-workflow` when the user only wants a plan or plan approval.
- `reverse-prompt` can produce a contract-shaped execution brief, but it should not replace `plan-review` when the user wants a phased implementation plan.
- `integration-testing-http` is an overlay on `testing-workflows`, not a replacement for it.
- `http-api-openapi` is for contract synchronization, not generic HTTP testing.
- `cloudflare-d1-migrations` is the sharper match than `database-migrations` when Wrangler, `d1_databases`, or local/preview/remote D1 state is central to the task.
- `cloudflare-d1-query-tuning` is the sharper match than `repository-adapters` when the main risk is Cloudflare D1 runtime query performance without schema or migration changes.
- `code-generation` often pairs with schema, template, and API work, but usually should not be the only selected skill unless regeneration itself is the task.
- `configuration-env` and `docker-compose-dev` are situational operational helpers, not default entry points.
- `plan-review-loop` is the post-`/plan` structured approval loop; run it after `plan-review` creates the plan artifact.
- `verification-before-completion` pairs with any implementation skill; load it last, before signing off.
- `test-driven-development` and `systematic-debugging` layer onto `testing-workflows`; prefer the specialist when TDD discipline or structured root-cause methodology is the explicit need.
- `agent-governance` and `agent-supply-chain` are complementary: governance controls runtime behavior; supply chain controls artifact integrity. Both often apply to the same agent project.
- `go-cli-development` pairs with `goreleaser-release-pipeline` when the release pipeline itself needs debugging; prefer `go-cli-development` for CLI authoring and `goreleaser-release-pipeline` for release-pipeline-specific failures.
- `go-docker-builds` pairs with `go-build-and-test` when a Docker build fails; check toolchain state with `go-build-and-test` before debugging the Dockerfile.
- `neovim-plugin-development` pairs with `neovim-config` when a plugin's user-facing configuration layer needs updating alongside the plugin itself.
