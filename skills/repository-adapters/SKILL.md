---
name: repository-adapters
description: "Implement or modify database repository adapters. Use when adding adapter methods, changing queries, or mapping database errors while preserving domain boundaries."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: draft
  kind: task
---

# Repository adapters

## Use this skill when

- Adding a repository method, changing a query, or touching an adapter between domain and DB.
- Mapping DB-specific errors to domain errors at the adapter boundary.
- Adding support for a new DB dialect to an existing repository interface.

## Do not use this skill when

- The work is the migration itself (use `database-migrations`).
- The main risk is Cloudflare D1 runtime query performance without schema changes; use `cloudflare-d1-query-tuning`.
- The change is above the adapter layer (services, handlers, or HTTP contracts).

## Inputs to gather

- The domain interface definition and every adapter that implements it.
- The generator in use (sqlc, gorm gen, etc.) and its regeneration command.
- Which DB dialects are mandatory vs optional in this repository.

## First move

- Update the query source for each dialect, regenerate, then adjust the adapter to call the new or changed query before touching tests.

## Outputs

- Updated repository-layer inputs such as query sources, regenerated artifacts, and adapter implementation changes at the domain boundary.
- DB-to-domain error mapping preserved or corrected for the touched operations so adapter callers keep the expected contract.
- Test evidence for the primary adapter path, with optional dialects skipping cleanly when unavailable.


## Architecture pattern

```
Domain interface (repository.go)      ← handlers depend on this
    ↓
Adapter implementation (sqlite.go, postgres.go, etc.)
    ↓
Generated query layer (if using sqlc, gorm gen, etc.) ← never edit by hand
```

- **Domain interface**: defines what persistence operations exist; lives with the domain, not with the DB.
- **Adapter**: implements the domain interface using DB-specific queries.
- **Generated layer**: produced by a code generator; editing it by hand is overwritten on next generation.

## Safe change workflow

1. Update the query source (SQL file, ORM definition) for each DB dialect.
2. Regenerate: `make generate`
3. Update the adapter implementation to call the new or changed query.
4. Add or update tests covering the changed behaviour.
5. Run: `make test`

## Error mapping rules

Map DB-level errors to domain errors **at the adapter boundary** — never let DB-specific errors leak to callers:

| DB error                        | Domain error                                                  |
| ------------------------------- | ------------------------------------------------------------- |
| Uniqueness/constraint violation | `ErrDuplicate` or equivalent                                  |
| No rows / not found             | `ErrNotFound` or equivalent                                   |
| Unknown DB error                | Wrap with context: `fmt.Errorf("operation context: %w", err)` |

**Never** include raw DB error strings in responses or logs — they expose implementation details and may contain sensitive data.

## Guardrails

- Never edit generated query files by hand.
- Each DB dialect's adapter must implement the same domain interface — no adapter-specific methods exposed to callers.
- Error wrapping must use `%w` to preserve the error chain for `errors.Is` / `errors.As`.
- Optional DB support (e.g. Postgres when only SQLite is required) must **skip** gracefully in tests, not fail.
- Never leak raw DB error strings in API responses or logs.

## Validation

```bash
make test     # SQLite (or primary DB) must pass; optional DBs skip when unavailable
```

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
