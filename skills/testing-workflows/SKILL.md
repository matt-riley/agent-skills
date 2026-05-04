---
name: testing-workflows
description: Run, debug, and extend tests for a Go project (unit + integration), including
  code generation prerequisites. Use when changing domain logic, repositories, HTTP
  handlers, or migrations, or when tests are failing unexpectedly.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes bash, make, go, and repository test entrypoints.
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: draft
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

## Fast paths

```bash
make test                           # all tests (may run generation first)
make test-unit                      # unit tests only
make test-integration               # integration tests only
go test -v -run TestName ./pkg/...  # single test, verbose
```

## Catalog position

Use this as the default testing entry point for Go work. If the problem is specifically about endpoint contracts, auth behaviour, or request/response assertions over HTTP, layer in `integration-testing-http` rather than replacing this skill entirely.

## Debugging failures

Follow this sequence:

1. **Compile errors in generated packages** → `make generate`, then retry.
2. **Specific test failure** → `go test -v -run TestName ./path/to/pkg` to isolate.
3. **DB-related failure in integration tests** → verify `DATABASE_URL` is set and migrations are applied.
4. **Flaky / order-dependent tests** → check for shared mutable state; each test must be isolated.

## Coverage expectations when adding features

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

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
