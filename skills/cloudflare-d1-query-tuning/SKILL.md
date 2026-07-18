---
name: cloudflare-d1-query-tuning
description: "Tune slow Cloudflare D1 queries and D1-backed repository access without schema or migration changes. Use for N+1 access, over-fetching, pagination, or runtime D1 query-shape issues."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  category: data
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Cloudflare D1 query tuning

## Use this skill when

- A Cloudflare Workers repo has a slow D1 query and the task is to tune query shape or repository logic without touching schema or migration files.
- A D1-backed adapter or repository is over-fetching, doing N+1 lookups, or filtering/paginating in application code when SQL should do the work.
- You need D1-specific inspection such as `wrangler d1 execute`, `EXPLAIN QUERY PLAN`, or environment-aware repro steps before rewriting the query path.

## Do not use this skill when

- The task changes schema, indexes, constraints, or migration files; use `cloudflare-d1-migrations`.
- The repository does not use Cloudflare D1 and the main work is a generic adapter/query change; use `repository-adapters`.
- The problem is D1 binding setup, `preview_database_id`, or Wrangler environment drift rather than runtime query behavior; use `configuration-env`.
- The main request is caching, HTTP contract changes, or higher-level service behavior rather than the D1 query path itself.

## Inputs to gather

**Required before editing**

- The Wrangler config file and exact `d1_databases` binding in scope.
- The slow query path: repository/adapter method, raw SQL or query builder call, representative parameters, and expected result shape.
- Current evidence of slowness, such as logs, a reproducible request path, or direct `wrangler d1 execute` timing / `EXPLAIN QUERY PLAN` output.
- The repo's existing wrappers for D1 execution, tests, and local-vs-preview-vs-remote workflows.

**Helpful if present**

- Whether the problem reproduces in `--local`, `--preview`, `--remote`, or all three.
- The surrounding access pattern, such as per-row follow-up queries, repeated existence checks, or offset-heavy pagination.
- Whether the repo already uses prepared statements, batches, or transactions for nearby D1 work.

**Only investigate if encountered**

- Whether D1/SQLite feature limits like FTS, JSON functions, or virtual tables constrain the rewrite.
- Whether the only viable fix is actually an index or schema change; if so, stop and redirect rather than widening scope.
- Whether the query is generated and needs a code-generation step after edits.

## First move

First confirm the problem is runtime query shape or D1 access behavior, not a missing index, migration, or binding issue. Then inspect the exact D1 binding and reproduce the query with representative parameters in the right environment before proposing a rewrite.

## Workflow

1. Confirm the D1 runtime contract.
   - Read `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc` and note the exact `d1_databases` entry in scope.
   - Record the binding name, `database_name`, and any preview-vs-remote distinction before measuring anything.
   - Prefer repo wrappers over raw Wrangler once you understand how they map to D1 execution.

2. Capture the real slow path before rewriting.
   - Find the exact repository method, adapter call, or query source used by the slow request.
   - Reproduce it with representative parameters and inspect `EXPLAIN QUERY PLAN` in the same environment when feasible.
   - Check whether the issue is over-fetching, post-filtering in application code, N+1 follow-up queries, redundant existence checks, or offset-heavy pagination.

3. Tune the query path without changing schema.
   - Push filtering, ordering, limiting, aggregation, and existence checks into SQL when that preserves the contract.
   - Prefer narrower projections, `EXISTS`, set-based fetches, and query consolidation over `SELECT *`, row-by-row follow-ups, or post-processing large result sets.
   - Reuse the repo's prepared statement, batch, or transaction patterns when they reduce repeated round trips without changing semantics.
   - If the only meaningful improvement would require a new index or schema change, stop and hand off to `cloudflare-d1-migrations` instead of smuggling schema advice into this workflow.

4. Validate behavior and performance deltas together.
   - Re-run the same representative query path after the rewrite.
   - Compare the work done, such as plan shape, rows touched, or round trips, not just the final latency text.
   - Run the repo's normal tests or affected checks for the changed adapter/query path.

## Outputs

- The exact D1 binding, repository method, and query path identified for the slow request, with before/after plan evidence where available.
- A query or adapter rewrite that reduces scans, over-fetching, or round trips without changing schema or result semantics.
- Validation showing the tuned path preserves behavior and passes the repo's affected tests or checks.


## Guardrails

- **Must** inspect the exact D1 binding and environment before measuring or rewriting the query.
- **Must** preserve the query contract and result semantics while tuning.
- **Must not** recommend schema, index, or migration-file changes inside this workflow.
- **Must not** treat local D1 behavior as proof that preview or remote has the same runtime characteristics.
- **Should** keep rewrites at the query / adapter boundary instead of leaking D1-specific behavior upward.
- **Should** call out plainly when the no-schema constraint blocks the real fix.
- **May** pair with `repository-adapters` when the repo uses a strong domain-interface boundary and the adapter contract also needs care.

## Validation

- The same D1 query path was inspected before and after with comparable parameters.
- The tuned version reduces unnecessary work, such as wider scans, over-fetching, redundant round trips, or post-filtering outside SQL.
- The repo's relevant tests or validation commands still pass for the touched query or adapter path.

## Examples

- "Tune a slow D1 query without changing schema or migration files."
- "This Worker does N+1 D1 lookups in a loop. Collapse it into a better query path without touching migrations."
- "Rewrite this D1 pagination query so it stops over-fetching, but keep the same result contract."

## Reference files

- Read `references/inspection-and-rewrite.md` when you need D1-specific repro commands, `EXPLAIN QUERY PLAN` usage, or a checklist of no-schema rewrite wins.
