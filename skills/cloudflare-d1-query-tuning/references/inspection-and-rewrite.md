# D1 inspection and rewrite notes

## Reproduce against the right database first

- Read the repo's Wrangler config before running commands so you choose the right `d1_databases` binding and environment.
- Keep `--local`, `--preview`, and `--remote` separate. A local repro is useful, but it does not prove the same plan or data distribution remotely.
- Prefer repo-owned wrappers when they already encode `--persist-to`, environment names, or auth.

## Useful D1 inspection commands

- Inspect the current query plan:

  ```bash
  npx wrangler d1 execute <DB> --local --command "EXPLAIN QUERY PLAN <query with representative literals>"
  ```

- Run the exact query through Wrangler when you need a direct repro outside the app path:

  ```bash
  npx wrangler d1 execute <DB> --local --command "<query>"
  ```

- When local persistence matters, carry the same `--persist-to <dir>` path through each local command.

## Common no-schema wins

- Replace `SELECT *` with the exact columns the caller needs.
- Move filtering, sorting, limiting, grouping, and existence checks into SQL instead of doing them in JS/TS/Go after the fetch.
- Replace per-row follow-up lookups with a single set-based query, join, or batched `IN (...)` lookup when the contract allows it.
- Use `EXISTS` or `LIMIT 1` for boolean checks instead of loading full rows.
- Remove redundant wrapper queries like `COUNT(*)` plus a second full fetch unless the caller truly needs both results.

## D1-specific cautions

- If `EXPLAIN QUERY PLAN` still shows a broad scan and the only real fix is a new index, stop and redirect to schema work rather than pretending a query rewrite solved it.
- Keep rewrites compatible with the repo's current D1 access layer, whether that is raw SQL, a query builder, or a thin repository adapter.
- If the query source is generated, change the source input and run the repo's generation step instead of editing generated output.
