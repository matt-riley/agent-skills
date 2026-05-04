---
name: cloudflare-d1-migrations
description: Use when a repository uses Cloudflare D1 and the task is to create, inspect, apply, baseline, or recover schema migrations or schema state across local, preview, or remote databases; do not use for binding-only setup or config drift, or for runtime query tuning.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes Wrangler plus a Cloudflare Workers repository with D1 bindings.
metadata:
  owner: mattriley
  version: 1.1.0 # x-release-please-version
  maturity: stable
---

# Cloudflare D1 migrations

## Use this skill when

- The repository uses Cloudflare D1 and the task changes schema, indexes, constraints, or migration files.
- A D1 migration behaves differently across local, preview, and remote environments.
- You need the D1-specific workflow for safe migration creation, promotion, baseline import, or recovery with Wrangler.
- The repo may customize `migrations_dir`, `migrations_table`, or preview/remote database settings and those settings matter to the workflow.

## Do not use this skill when

- The repository does not use Cloudflare D1; use `database-migrations` for the general migration workflow instead.
- The task is only D1 binding, `preview_database_id`, or Wrangler env setup drift with no migration file, import baseline, or schema-state concern; use `configuration-env`.
- The task is query tuning, repository logic, or runtime D1 access without migration artifacts; use `cloudflare-d1-query-tuning`.
- The problem is a runtime prepared-statement or query bug and schema plus migration files are unchanged; say plainly that this is not a migration or schema-state task, then redirect to runtime or query debugging instead of treating the migration ledger as the main path.

## Inputs to gather

**Required before editing**

- The Wrangler config file and the specific `d1_databases` binding involved.
- The D1 contract from config: `database_name`, binding name, `preview_database_id`, and any custom `migrations_dir` or `migrations_table`.
- Repo wrappers for D1 work (`package.json` scripts, Makefile targets, CI commands) and whether they already wrap Wrangler.
- Which environment is in scope right now: `--local`, `--preview`, or `--remote`.

**Helpful if present**

- The local persistence path used for `wrangler dev` or `wrangler d1 ... --local --persist-to`.
- Whether the repo seeds, imports, or exports SQL as part of local setup or CI.
- Known downstream checks after schema changes, such as tests, `wrangler dev`, or build steps.

**Only investigate if encountered**

- Whether the repo renamed the applied-migrations ledger away from the default `d1_migrations`.
- Whether recovery may need D1 export or time-travel rather than another forward migration.
- Whether the import SQL includes foreign-key ordering issues, very large inserts, or virtual tables.

## First move

First confirm the request is actually about migration or schema state, not just a missing binding, env value, or runtime query bug. If schema and migration files are unchanged, say explicitly that this is not a migration or schema-state task and redirect before you inspect the D1 migration ledger. Otherwise inspect the Wrangler config and repo wrappers before suggesting commands so you identify the exact D1 binding, preview/remote targets, migration directory/table, and local persistence path without mixing local, preview, and remote state.

## Workflow

1. Confirm the D1 migration contract and environment mapping.
   - Read `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc` and note the chosen `d1_databases` entry.
   - Record `database_name`, binding name, `preview_database_id`, and any custom `migrations_dir` or `migrations_table`; do not assume defaults if config says otherwise.
   - Prefer repo wrappers over raw Wrangler, but expect D1 to map to `wrangler d1 migrations create`, `list`, and `apply`.
   - If the repo has multiple environments or databases, name the exact one in scope before proposing commands.

2. Create the migration the D1 way.
   - Scaffold with the repo wrapper or `npx wrangler d1 migrations create <DB> <message>`.
   - Author SQLite-compatible SQL in the generated file.
   - If the migration temporarily violates foreign keys, make that explicit with `PRAGMA defer_foreign_keys = true` at the right point in the SQL.
   - Treat D1 migrations as forward-only; do not invent `down` sections.
   - If the migration backfills data, keep the schema contract explicit so the new file still works from a clean database.

3. Validate locally before promotion.
   - Check pending local migrations with `npx wrangler d1 migrations list <DB> --local`.
   - If the repo persists local state outside the default location, include `--persist-to <dir>` in both list and apply commands.
   - Apply locally with `npx wrangler d1 migrations apply <DB> --local`.
   - Inspect schema or ledger state with `npx wrangler d1 execute <DB> --local --command "<sql>"` and then run the repo's tests or `wrangler dev` path.

4. Promote in environment order, not by assumption.
   - Say explicitly whether `preview_database_id` is configured. If it is, inspect and apply there with `--preview` before touching remote; if it is not, say that plainly and move from local validation to remote.
   - Before each promotion step, compare pending files with `npx wrangler d1 migrations list <DB> --preview` or `--remote`.
   - Apply remotely only after the intended pre-remote environment is aligned.
   - Apply remotely with `npx wrangler d1 migrations apply <DB> --remote`.
   - Remember that D1 captures a backup during apply and rolls back a failed migration, but that is not a license to skip inspection first.

5. Recover drift or import existing SQL safely.
   - For remote drift, compare repo migration files with the applied ledger table (`d1_migrations` or the configured `migrations_table`) and current schema before changing anything.
   - If you need a safety point before repair, prefer D1 export or time-travel metadata over ad hoc guesswork.
   - Repair state with a new corrective forward migration unless the task is explicit disaster recovery requiring time-travel restore.
   - For SQLite dump import, prefer existing migrations first and then a data-only import; otherwise create a deliberate baseline that matches the imported schema exactly before later migrations resume.
   - When cleaning import SQL, call out the D1-specific hazards explicitly: remove `BEGIN TRANSACTION` / `COMMIT`, remove any `CREATE TABLE _cf_KV ...` definition, split oversized inserts if D1 reports `Statement too long`, and watch foreign-key ordering or virtual-table issues.
   - Use `npx wrangler d1 execute <DB> --local|--remote --file=<dump.sql>` or the repo wrapper that maps to it for the actual import path.

## Guardrails

- **Must** inspect the D1 binding plus `migrations_dir` / `migrations_table` before suggesting file paths or ledger queries.
- **Must** keep local, preview, and remote states separate; a clean local apply does not prove preview or remote is aligned.
- **Must** name the exact target database/environment when the repo has multiple D1 bindings or environments.
- **Must** say explicitly when the prompt is not a migration or schema-state task, especially for runtime prepared-statement or query bugs with unchanged schema/migrations.
- **Must not** use this skill for binding-only D1 config drift or generic runtime tuning when no migration or schema-state artifact is in play.
- **Must not** recommend editing an already-applied migration file.
- **Must not** suggest rollback-oriented `down` migrations for D1; use corrective forward migrations or explicit D1 recovery tooling.
- **Must not** assume preview exists; only add `--preview` when config or repo workflow actually uses a preview database.
- **Must not** lead with migration-ledger inspection when the task is a runtime D1 bug and migration artifacts are unchanged.
- **Should** prefer repo-owned wrappers around Wrangler when they exist.
- **Should** validate the resulting schema with direct `wrangler d1 execute` inspection rather than only trusting console success text.

## Validation

- `wrangler d1 migrations list` shows the expected pending or clean state in the targeted environments.
- The schema or ledger was inspected with `wrangler d1 execute` or equivalent repo wrappers after applying.
- The repo's normal follow-on checks for D1 changes were run, such as tests, `wrangler dev`, or build/deploy validation.

## Examples

- "This Worker uses D1. I need to add a migration, test it locally, then promote it safely."
- "A D1 migration seems half-applied remotely. What should I inspect before repairing it?"
- "I have a SQLite dump to import into D1, but I do not want to break later migrations."

## Reference files

- Read `references/contract-and-promotion.md` when the main risk is choosing the right D1 binding, migration directory/table, persistence path, or preview/remote promotion order.
- Read `references/recovery-and-imports.md` when the task involves remote drift, D1 recovery, SQLite import/export, or dump cleanup.
- Read `references/boundaries-and-false-positives.md` when the request mentions D1 but may actually be binding/config drift, runtime query behavior, or a repo with no preview database.
