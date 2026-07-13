---
name: database-migrations
description: "Create, apply, inspect, and recover database schema migrations after detecting the repository's migration contract. Use when changing persistent schema, adding indexes/constraints, or troubleshooting migration state."
license: GNU GPL v3
metadata:
  version: 1.3.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

## Use this skill when

- The task changes persistent schema, indexes, constraints, or migration files.
- A migration is stuck, partially applied, or out of sync across environments.
- The repo needs the safe create/apply/status/recovery workflow for schema changes.

## Do not use this skill when

- The request is to design a brand new schema from scratch with no migration workflow yet.
- The repository uses Cloudflare D1 and the main risk is Wrangler's local / preview / remote migration workflow; use `cloudflare-d1-migrations`.
- The change is query tuning, repository logic, or data access behavior without persistent schema changes.
- The task is only a data backfill or one-off repair with no migration artifact to create or inspect.

## Inputs to gather

- Migration tool and migration directory (`Makefile`, README, tool config, CI scripts).
- Repo contract:
  - forward-only vs reversible up/down migrations
  - hand-authored SQL/DSL vs generated/scaffolded migration artifacts
  - single-dialect vs multi-dialect/multi-environment expectations
- Commands for create/scaffold, apply, status/history, and recovery.
- Whether the schema feeds code generation or other follow-on steps.

## First move

Inspect the repo contract before suggesting commands or file edits. Determine whether this repo expects reversible migrations, forward-only corrective migrations, or generated migration artifacts.

## Workflow

1. Identify the real migration entrypoints.
   - Prefer repo wrappers such as `make migrate-*`, `task migrate:*`, or scripts.
   - If wrappers are absent, locate the direct tool command (`goose`, `flyway`, `liquibase`, `alembic`, etc.).

2. Branch on the repo's migration contract.
   - **Reversible / up-down repos:** scaffold the migration the repo's way and implement both forward and rollback sections when the tool or project expects them.
   - **Forward-only repos:** create a new forward migration and plan recovery as another forward fix, not as an assumed rollback.
   - **Generated / DSL-backed repos:** edit the declared migration source and run the repo's generator/scaffolder instead of hand-authoring output files blindly.

3. Apply or inspect state using the repo's status/history tooling.
   - Confirm what is applied, pending, failed, or partially applied before attempting recovery.
   - If environments differ, note the environment-specific risk before changing anything.

4. Complete the follow-on validation the repo expects.
   - Regenerate downstream artifacts if schema changes feed generators such as `sqlc`.
   - Run the smallest relevant tests/checks after the migration path is correct.

## Outputs

- The repo's migration contract and correct migration entrypoints identified before any schema changes are applied.
- New or corrected migration artifacts created through the repo's expected scaffolding or generation path.
- Migration status/history plus downstream code-generation or test evidence confirming the expected schema state.


## Workflow

See the body and references for migration create/apply/rollback steps.

## Guardrails

- Never assume every repo supports `down` migrations. Detect whether the contract is forward-only or reversible first.
- Never edit already-applied migration files to "fix" history; create a corrective migration instead.
- Never use ad hoc manual schema edits as the first recovery step when the repo has migration state/history tooling.
- Respect dialect and environment differences; SQLite-safe SQL is not automatically Postgres-safe, and local state is not automatically preview/prod state.
- If the repo packages or embeds migration files at build/runtime, make sure new files are included in that packaging flow.

## Validation

- Migration status/history shows the expected applied or pending state.
- Any required code generation or schema-dependent checks have been re-run.
- Relevant tests/checks pass for the touched schema surface.

## Support files

- Read `references/examples.md` when you need phrasing examples for new migrations or migration-state recovery.
- Read `references/edge-cases.md` when the repo uses generated migrations, forward-only history, or environment-specific recovery rules.
