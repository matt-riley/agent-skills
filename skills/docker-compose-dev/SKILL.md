---
name: docker-compose-dev
description: "Run a service stack locally using Docker Compose for prod-like development (e.g. PostgreSQL + app). Use when you need a real DB backend, multi-service integration, or want to reproduce production-like behavior locally."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

# Docker Compose dev stack

## Use this skill when

- A real DB backend or multi-service stack is needed for local or integration work.
- Reproducing production-like behaviour locally is the blocker.
- Debugging app/DB connectivity, startup order, or environment-variable wiring against the Compose stack.

## Do not use this skill when

- The task is purely configuration or env validation (use `configuration-env`).
- Unit tests can satisfy the change with in-memory or stub dependencies.

## Inputs to gather

- Whether an `.env.example` template exists and which credentials need real values.
- The app's health-check endpoint and port for post-start verification.
- Which services depend on which (for `depends_on` and healthcheck decisions).

## First move

- Copy `.env.example` to `.env`, bring the stack up, run migrations if not auto-applied, and verify the health endpoint.

## Outputs

- A compose-backed local stack started from the repo's `.env` template with required migrate or seed steps applied deliberately.
- Running service state confirmed via `docker compose ps`, logs, and/or the repo's health endpoint.
- An explicit teardown/reset outcome, including whether persistent volumes were preserved or intentionally destroyed.


## Quick start

```bash
cp .env.example .env              # copy env template; edit credentials as needed
make docker-compose-up            # or: docker compose up -d
```

Run any setup steps that do not run automatically (most setups require this):

```bash
make migrate-up                   # apply database migrations
```

Verify the app is healthy:

```bash
curl http://localhost:<PORT>/health
```

## Common operations

```bash
make docker-compose-logs          # or: docker compose logs -f
make docker-compose-ps            # or: docker compose ps
make docker-compose-down          # stop and remove containers
```

Full reset (wipes persistent volumes):

```bash
docker compose down -v            # removes containers AND volumes
```

Use `-v` only when you want to destroy all data (e.g. start fresh with a clean DB).

## Workflow

See the body and references for Docker Compose stack steps.

## Examples

See references and the skill body for docker-compose-dev examples.

## Reference files

See the references/ directory and linked files in the main content.

## Guardrails

- Migrations are **not** run automatically by `docker compose up` — run them explicitly after services start.
- If credentials in `.env` change, update any `DATABASE_URL` or connection strings that reference them.
- Use Compose for integration/E2E testing against real services; use in-memory or stub variants for unit tests.
- Never use `docker compose down -v` unless you intentionally want to destroy all persistent data.

## Troubleshooting

| Symptom                 | Fix                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------- |
| App crashes immediately | Check logs: `docker compose logs app`                                                   |
| DB connection refused   | Confirm DB service is healthy before the app starts; add `depends_on` with health check |
| Migrations fail         | Verify `DATABASE_URL` matches the credentials in `.env` and the DB is reachable         |

## Validation

- Confirm `docker compose ps` or the repo wrapper shows the expected services running.
- Run the service health check or smoke test against the compose-backed app.
- Confirm migrations and required seed/setup steps were applied deliberately, not assumed.
- Before teardown, decide whether volumes should be preserved or intentionally destroyed.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
