---
name: integration-testing-http
description: "Write and run end-to-end HTTP integration tests for server behavior. Use when you need to add or fix integration test coverage for handlers, middleware, auth enforcement, or endpoint contracts — not for keeping OpenAPI specs in sync."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  category: testing
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Integration testing (HTTP)

## Use this skill when

- Adding or changing HTTP handlers, middleware, auth enforcement, or request/response shapes.
- Adding end-to-end test coverage for an endpoint contract (status codes, validation, side effects).
- Debugging integration-test failures specific to HTTP behaviour rather than domain logic.

## Do not use this skill when

- The failure is clearly at the unit-test layer (use `testing-workflows`).
- The change is to the OpenAPI spec only with no handler work (use `http-api-openapi`).
- Compile errors come from stale generated code (run `code-generation` first).

## Inputs to gather

- The endpoint(s) being asserted and their documented status codes.
- Whether auth is required and the shape of the token/cookie under test.
- The integration-test runner entrypoint for this repository and its DB bootstrap.

## First move

- Run the targeted integration test with `-v` and read the real request/response output before proposing fixes.

## Outputs

- Targeted HTTP integration tests or assertions covering the touched endpoint's status codes, auth behavior, request validation, response shape, and side effects.
- New or updated integration cases for changed endpoints, including OpenAPI-aligned expectations when the contract also changed.
- Narrow test rerun results plus broader suite status when shared handlers or middleware were affected.


## Catalog position

- Start with `testing-workflows` for the default test/debug loop.
- Use this when the main risk is HTTP behaviour: endpoint contracts, auth enforcement, validation, or response shapes.
- Pair with `http-api-openapi` when handler changes and spec changes must stay in sync.

## Run

```bash
make test-integration
# or targeted:
go test -v -run TestE2E ./path/to/server/pkg/
```

## What integration tests must assert

For every endpoint touched, verify:

| Concern            | What to assert                                       |
| ------------------ | ---------------------------------------------------- |
| Status codes       | Happy path + all documented error cases              |
| Auth               | Unauthenticated → 401; invalid token → 401 or 403    |
| Request validation | Missing/invalid fields → 400 with error body         |
| Response schema    | Required fields present, correct types               |
| Side effects       | DB state, events, or derived data match expectations |

## Adding tests for a new or changed endpoint

1. Update the OpenAPI spec and validate it.
2. Add integration tests covering:
   - Successful request (happy path)
   - Auth failure (missing token + invalid token, if the endpoint requires auth)
   - Input validation failure (malformed or missing required fields)
   - Edge cases specific to the endpoint's logic
3. Run `make test-integration` — all must pass before merging.

## Workflow

1. Identify the endpoints, auth modes, and request/response contracts under change.
2. Prefer the repo's existing HTTP integration harness; extend rather than invent a parallel stack.
3. Write or update tests for status codes, auth enforcement, validation errors, response shape, and side effects.
4. Keep tests order-independent with clean DB/state per case; do not mock the DB in integration tests.
5. Align assertions with OpenAPI or handler contracts when both change.
6. Run the targeted integration test with verbose request/response output first.
7. Widen to the suite when shared middleware or handlers moved; fix root cause, not flakes.

## Guardrails

- Integration tests use a real or in-memory DB — do not mock the DB layer in integration tests.
- Each test or suite must start from a clean, isolated state — never share mutable state between tests.
- Tests must be order-independent; never rely on execution order.
- Assert auth enforcement explicitly for every endpoint that requires it.

## Debugging failures

1. If compile errors appear in generated packages → `make generate`, then retry.
2. Run with `-v` to see full request/response output for the failing test.
3. If DB-related failures occur → verify the test DB is initialised and migrations are applied.

## Validation

- Run the narrow HTTP integration test or suite that covers the changed endpoint first.
- Confirm status codes, auth behavior, request validation, response shape, and error body assertions are explicit.
- Re-run the repository's broader test target when handler or middleware changes affect shared paths.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
