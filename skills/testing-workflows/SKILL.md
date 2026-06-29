---
name: testing-workflows
description: "Write, run, and debug Go tests — unit and integration — including generator refresh when stale generated code causes failures. Use when adding test coverage or debugging test failures in domain logic, repositories, or handlers. For build failures, toolchain issues, or CI-parity problems, use go-build-and-test instead."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

# Testing workflows

## Use this skill when

- Running, extending, or debugging Go unit or integration tests for this project.
- Tests are failing unexpectedly and the cause is not obvious.
- A feature change needs appropriate coverage across domain, repository, or handler layers.

## Do not use this skill when

- The main risk is specifically HTTP endpoint behaviour (use `integration-testing-http`).
- Failures clearly stem from stale generated code (use `code-generation` first).
- The work is database schema change rather than test authoring (use `database-migrations`).

## Inputs to gather

- The failing test name or the module whose coverage is changing.
- The entrypoint used by this repository (`make test`, `go test`, or a CI target).
- Whether integration tests need a live DB and whether its credentials are available.

## First move

- Run the narrowest relevant test target first and read the actual failure output.
- If compile errors reference generated packages, run `make generate` before re-running.

## Outputs

- A narrow failing-test reproduction and diagnosis, including generator refresh when stale generated inputs are the real cause.
- New or updated tests for the touched domain, repository, or handler behavior at the correct scope.
- Broader test-run evidence showing the fix or feature is ready beyond the isolated case.


## Workflow

Use the most specific path for the task; fall through to the debugging sequence when tests fail for unclear reasons. Layer in `integration-testing-http` when the problem is specifically endpoint contracts, auth behaviour, or request/response assertions over HTTP.

### Fast paths

```bash
make test                           # all tests (may run generation first)
make test-unit                      # unit tests only
make test-integration               # integration tests only
go test -v -run TestName ./pkg/...  # single test, verbose
```

### Debugging failures

Follow this sequence:

1. **Compile errors in generated packages** → `make generate`, then retry.
2. **Specific test failure** → `go test -v -run TestName ./path/to/pkg` to isolate.
3. **DB-related failure in integration tests** → verify `DATABASE_URL` is set and migrations are applied.
4. **Flaky / order-dependent tests** → check for shared mutable state; each test must be isolated.

### Coverage expectations when adding features

| Layer            | What to test                                                    |
| ---------------- | --------------------------------------------------------------- |
| Domain / service | Validation rules and business logic (prefer table-driven tests) |
| Repository       | Persistence behaviour against a real or in-memory DB            |
| HTTP handlers    | Status codes, auth enforcement, request/response shapes         |

## Guardrails

- Run `make generate` before `make test` whenever schema, query, or template files changed.
- Repository tests must work with at least one DB (e.g. SQLite or in-memory). Optional DBs should **skip**, not fail, when unavailable.
- New features require tests before merging.
- Tests must be order-independent with no shared mutable state between test cases.
- Reach for `code-generation` first when failures smell like stale generated inputs rather than test logic.

## Validation

- Re-run the narrow failing test after each suspected fix before broadening.
- Run the repository's broader test target before claiming the change is ready.
- When adding features, confirm new or updated tests cover the touched domain, repository, or handler behavior.

## Examples

- `The domain validation test is failing after I renamed a field — isolate it and show me the fix.`
- `Add integration tests for the new repository method so it works against both SQLite and Postgres.`
- `The CI test run is red but I can't reproduce it locally — step me through the debugging sequence.`

## Reference files

- [`references/examples.md`](references/examples.md) — concrete user utterances, expected behaviour, and model answer shapes
- [`references/edge-cases.md`](references/edge-cases.md) — near-miss requests, partial matches, and first-attempt failure patterns
