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

## High-visibility operational guardrail

- `configuration-env` — keep this easy to find for startup failures, env drift, and deployment/config debugging, but do not force it into every task by default

## Families

### Governance and process

- `rpi-workflow` — full Research -> Plan -> Implement -> Validate discipline for non-trivial work
- `plan-review` — plan drafting, hardening, approval gates, and optional structured reviewer personas
- `reverse-prompt` — sharpen a rough ask into a repository-grounded execution brief or contract-shaped brief before work starts
- `implementation-review` — post-implementation review and approval

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

### CI and delivery workflows

- `github-actions-failure-triage` — diagnose existing failing GitHub Actions runs with evidence-first minimal fixes
- `ci-images` — local CI parity and image-publishing workflows

### Testing, APIs, and delivery checks

- `testing-workflows` — default testing and debugging entry point
- `integration-testing-http` — specialist overlay for endpoint, auth, request/response, and HTTP contract testing
- `http-api-openapi` — keep handler and spec changes in sync

### Schema and persistence

- `database-migrations` — general database migration workflow
- `cloudflare-d1-migrations` — Cloudflare D1 migration workflow for Wrangler, local/preview/remote promotion, and recovery
- `cloudflare-d1-query-tuning` — Cloudflare D1 runtime query and repository-path tuning when schema or migration changes are out of scope
- `repository-adapters` — repository-layer adapter changes and DB error mapping
- `code-generation` — shared prerequisite when schema/query/template inputs feed generators

### Operations and runtime environment

- `configuration-env` — env loading, `.env`, and config-drift troubleshooting
- `docker-compose-dev` — local multi-service stack setup for prod-like development
- `observability-metrics` — `/health`, `/metrics`, and logging behavior validation

### Frontend and site quality

- `astro-seo` — Astro-specific SEO implementation and audit work
- `make-interfaces-feel-better` — UI polish for existing interfaces
- `templ-templates` — server-side templ template authoring and regeneration workflows

### Review follow-through and branch isolation

- `review-comment-resolution` — apply PR feedback, push the fix branch, and wait for resulting checks
- `git-worktrees` — set up isolated worktrees for parallel tasks, agents, or safer branch isolation

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

## Boundary reminders

Keep these boundaries crisp instead of broadening nearby skills:

- `git-worktrees` should own worktree setup and isolation for parallel or multi-branch work; do not bury worktree mechanics inside `rpi-workflow`, `plan-review`, or implementation skills.
- `review-comment-resolution` should own "apply review feedback and update the code/tests" work; keep it separate from `implementation-review`, which evaluates existing code rather than carrying feedback through to completion.
- `reverse-prompt` should own prompt and execution-brief sharpening; keep it separate from `plan-review`, which owns plan artifacts and approval gates.
- `writing-and-editing` should own reader-facing writing work; keep it separate from `github-presence`, which owns broader profile and repository-surface audits.
- `session-store-history` should own cross-session recall and session-to-ref/file tracing; keep it separate from current-workspace repo exploration, which should stay with repo-local search tools.
- `cloudflare-d1-query-tuning` should own runtime D1 query-shape and access-path tuning without schema changes; keep it separate from `cloudflare-d1-migrations` and from generic `repository-adapters` work when Cloudflare D1 runtime behavior is the main risk.

## Layering notes

- `plan-review` beats `rpi-workflow` when the user only wants a plan or plan approval.
- `reverse-prompt` can produce a contract-shaped execution brief, but it should not replace `plan-review` when the user wants a phased implementation plan.
- `integration-testing-http` is an overlay on `testing-workflows`, not a replacement for it.
- `http-api-openapi` is for contract synchronization, not generic HTTP testing.
- `cloudflare-d1-migrations` is the sharper match than `database-migrations` when Wrangler, `d1_databases`, or local/preview/remote D1 state is central to the task.
- `cloudflare-d1-query-tuning` is the sharper match than `repository-adapters` when the main risk is Cloudflare D1 runtime query performance without schema or migration changes.
- `code-generation` often pairs with schema, template, and API work, but usually should not be the only selected skill unless regeneration itself is the task.
- `configuration-env` and `docker-compose-dev` are situational operational helpers, not default entry points.
