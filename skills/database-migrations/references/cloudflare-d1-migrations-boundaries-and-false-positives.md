# D1 migration boundaries and false positives

## Use the migration workflow only when schema state is in play

- Reach for this skill when the task creates, inspects, applies, baselines, or repairs migration history or live schema state for a D1 database.
- If the request is only about wiring a binding, fixing `preview_database_id`, or repairing Wrangler env config so the Worker boots, that is config drift rather than migration work.
- If the request is about slow queries, prepared statements, N+1 lookups, or other runtime D1 behavior with unchanged schema and migration files, treat it as query/runtime work instead of migration work.

## Common routing redirects

- **Binding/env drift only:** use `configuration-env`.
- **Runtime D1 query behavior with no schema change:** use `cloudflare-d1-query-tuning`.
- **Non-D1 schema migrations:** use `database-migrations`.

## Preview is conditional, not automatic

- Do not prescribe `--preview` just because the repo uses D1.
- Only include preview inspection or apply steps when the selected D1 config or repo workflow actually uses a preview database, typically via `preview_database_id` or an equivalent documented repo wrapper.
- If no preview database is configured, the safe sequence is usually local inspection/apply and then remote inspection/apply.

## Multiple databases mean naming the target

- If the repo has more than one `d1_databases` entry, name the exact binding or `database_name` before listing or applying migrations.
- Avoid "run this against the D1 database" phrasing when the repo has multiple bindings; that ambiguity is a real migration risk.
