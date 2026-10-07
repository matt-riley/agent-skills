# D1 contract and promotion notes

## Confirm the exact database contract first

- Read the repo's `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc` before suggesting file paths or commands.
- For the chosen `d1_databases` entry, record:
  - binding name
  - `database_name`
  - `preview_database_id` if present
  - any custom `migrations_dir`
  - any custom `migrations_table`
- If the repo wraps Wrangler in package scripts, Make targets, or task runners, prefer those wrappers once you understand how they map to D1 commands.

## Local validation should match the repo's persisted state

- `wrangler d1 migrations list <DB> --local` and `apply --local` are only meaningful against the right local database state.
- If the repo uses `--persist-to <dir>` or a custom local persistence location, carry that path through every local list/apply/execute command in the sequence.
- A green local apply only proves the migration works against that local database; it does not prove preview or remote state is aligned.

## Promote deliberately

- If the repo has a preview database, list and apply there before remote:
  - `npx wrangler d1 migrations list <DB> --preview`
  - `npx wrangler d1 migrations apply <DB> --preview`
- If the repo does **not** have `preview_database_id` configured, say that explicitly and move from local validation straight to remote inspection/apply instead of inventing a preview stage.
- Before remote apply, inspect pending remote migrations explicitly:
  - `npx wrangler d1 migrations list <DB> --remote`
- Apply remotely only after the intended earlier environments are aligned:
  - `npx wrangler d1 migrations apply <DB> --remote`

## Ledger inspection queries

- If the repo kept the default ledger name, inspect `d1_migrations`.
- If config sets a custom `migrations_table`, use that name in every query and recovery check.
- Typical inspection flow:
  - list pending migrations with Wrangler
  - inspect the ledger table with `wrangler d1 execute`
  - inspect the live schema with `.schema`-style SQL or targeted `sqlite_master` queries
