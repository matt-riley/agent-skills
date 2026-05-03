# D1 recovery and import notes

## Remote drift or partial-apply recovery

- Start by comparing three things, in order: migration files in git, the applied ledger table (`d1_migrations` unless config renamed it), and the live schema.
- Use `npx wrangler d1 migrations list <DB> --remote` to see what Wrangler still considers pending.
- Use `npx wrangler d1 execute <DB> --remote --command "<sql>"` to inspect schema details and ledger rows when console output is not enough.
- Before any destructive repair, capture a safety point with:
  - `npx wrangler d1 export <DB> --remote --output=./backup.sql`, or
  - `npx wrangler d1 time-travel info <DB> --timestamp <RFC3339>`
- Prefer a new corrective forward migration after inspection. Reach for `time-travel restore` only when the job is explicit disaster recovery and the restore trade-off is understood.

## SQLite dump import without future-migration breakage

- Best case: run the repo's existing D1 migrations first, then import data only.
- If the dump defines the schema and must become the new baseline, make that baseline explicit so later migrations start from the imported shape.
- Clean common dump hazards before import:
  - remove `BEGIN TRANSACTION` and `COMMIT`
  - remove `CREATE TABLE _cf_KV ...` if present; call this out explicitly because it is easy to miss and specific to D1 imports
  - split oversized multi-row `INSERT` statements when D1 reports `Statement too long`
- Use `npx wrangler d1 execute <DB> --remote --file=<dump.sql>` or the matching local command to ingest SQL.
- Watch for foreign-key ordering problems, virtual tables during export/import, and SQLite-only objects that do not belong in the ongoing migration history.
