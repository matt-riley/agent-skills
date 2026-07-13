---
name: configuration-env
description: "Configure applications safely through environment variables, .env files, and repo-owned runtime config such as Wrangler bindings. Use for startup failures, environment drift, or deployment bootstrap."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

# Configuration and environment

## Use this skill when

- The server will not start because of missing or invalid configuration.
- Bootstrapping a new deployment environment and wiring real env vars or secrets.
- Behaviour differs between environments and the question is whether env loading is the cause.
- The main problem is repo-owned runtime config drift, such as a missing Cloudflare Worker binding in `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc`, without schema or migration work.

## Do not use this skill when

- The deeper concern is auth or sensitive-data exposure (use `security-basics`).
- The blocker is standing up a multi-service stack rather than env loading itself (use `docker-compose-dev`).

## Inputs to gather

- The authoritative list of required and optional variables (usually `.env.example` or README).
- The runtime platform (shell, CI, container) supplying env vars and whether `.env` is used.
- Any repo-owned runtime config that supplies bindings or non-secret settings, such as `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc`.
- The health-check endpoint or equivalent runtime check used to confirm a good startup.

## First move

- Compare real env vars and any `.env` against `.env.example` or the repo's config loader, then inspect runtime config files like `wrangler.*` for missing bindings or drift before starting the service and hitting `/health` or the closest existing startup check.

## Outputs

- A concrete config-drift diagnosis across real environment variables, `.env`, `.env.example`, and runtime binding files such as `wrangler.*`.
- The required variable, binding, or loader changes needed for the service to start with the expected configuration contract.
- Startup or `/health` verification showing the configuration was accepted, or an explicit blocker listing the missing required config.


## Catalog position

Keep this easy to reach for startup failures, env drift, and deployment/config debugging.

- Prefer `security-basics` when the question is primarily about auth, sensitive exposure, or request-handling safety.
- Prefer `docker-compose-dev` when the blocker is bringing up a multi-service stack rather than validating env loading itself.
- Prefer `cloudflare-d1-migrations` when the task changes D1 schema, migration files, or schema state rather than only fixing the Worker binding/config contract.
- Pair this with `rpi-workflow` only when configuration work is part of a larger multi-phase change.

## Loading priority (highest to lowest)

1. Real environment variables (shell, CI secrets, runtime platform)
2. `.env` file (local developer override)
3. `.env.example` (documentation only — never loaded at runtime)

## Setup

```bash
cp .env.example .env     # start from the documented template
# edit .env with real values for your environment
```

Never commit `.env`. Add it to `.gitignore`.

## Variable categories

Check `.env.example` or project README for authoritative var names. Common categories:

| Category      | Examples                                 |
| ------------- | ---------------------------------------- |
| Database      | `DATABASE_URL` — connection string       |
| Auth          | Secret key / bearer token                |
| Origins/CORS  | `ALLOWED_ORIGINS` — comma-separated list |
| TLS/Cookies   | `SECURE_COOKIES`, `COOKIE_DOMAIN`        |
| Feature flags | Enable/disable optional subsystems       |

Required variables cause startup failure. Optional variables activate features.

## Security constraints

- Production **must** use real env vars or a secrets manager — not `.env` files.
- Never set `ALLOWED_ORIGINS=*` when credentials or cookies are involved — use explicit origins.
- Enable secure cookies when behind HTTPS.
- Protect sensitive endpoints (metrics, admin) behind auth — do not leave them open by default.
- **Never hardcode secrets in source code.**

## Verification commands

```bash
make build && ./bin/server   # or equivalent start command
curl http://localhost:<PORT>/health
```

A healthy response confirms the configuration was accepted.

## Anti-patterns

- Hardcoding secrets in source code or test fixtures
- Using `.env` in production or CI
- `ALLOWED_ORIGINS=*` with cookie/credential-based auth
- Silently ignoring missing required config — always fail fast at startup

## Workflow

See the body and references for env/config drift and startup debugging steps.

## Guardrails

- Production must use real env vars or a secrets manager — never `.env` files.
- Required variables must fail the server at startup, not silently at request time.
- Never commit `.env`; only `.env.example` belongs in source.
- Never hardcode secrets in source code or test fixtures.

## Validation

Run the verification commands above and confirm the service starts successfully, the health endpoint responds, and missing required variables still fail fast.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
- [`scripts/check-config.sh`](scripts/check-config.sh) — run with `--help` for a repeatable environment/configuration check.
