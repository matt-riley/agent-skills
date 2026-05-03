---
name: observability-metrics
description: Validate and operate application observability endpoints (/health, /metrics)
  and logging behavior. Use when adding metrics, changing observability auth, debugging
  production-like issues, or verifying a deployment is healthy.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes bash, curl, and local access to health/metrics
  endpoints or logs.
metadata:
  owner: mattriley
  version: 1.0.0
  maturity: draft
---

# Observability metrics

## Use this skill when

- Adding a metric, a health probe, or touching `/metrics`/`/health` behaviour.
- Changing auth posture for observability endpoints.
- Verifying that a deployment is reachable and reporting sane telemetry.
- Debugging production-like issues where the question is whether telemetry itself is healthy.

## Do not use this skill when

- The core risk is secret handling or request-handling safety (use `security-basics`).
- The work is wiring new deployment infrastructure rather than validating telemetry endpoints.

## Inputs to gather

- The service port and any token needed to reach `/metrics` in the current environment.
- Whether metrics auth is enabled in this tier.
- The specific metric name or endpoint response being validated.

## First move

- `curl` the `/health` and `/metrics` endpoints directly and read the status/body before assuming application-level issues.

## Standard endpoints

| Endpoint       | Purpose                               | Default auth                     |
| -------------- | ------------------------------------- | -------------------------------- |
| `GET /health`  | Liveness/readiness check              | Public                           |
| `GET /metrics` | Prometheus-format operational metrics | Optional — protect in production |

## Validate locally (server must be running)

```bash
curl -i http://localhost:<PORT>/health
curl -i http://localhost:<PORT>/metrics

# If metrics auth is enabled:
curl -i -H "Authorization: Bearer $AUTH_TOKEN" http://localhost:<PORT>/metrics
```

- `/health` → expect `200 OK`
- `/metrics` → expect `200 OK` with Prometheus text format (`# HELP`, `# TYPE` lines)

## Security

`/metrics` exposes error rates, latency, queue depths, and operational state — treat it as sensitive.

- Enable auth protection for `/metrics` in production (env var or reverse proxy ACL).
- `/health` can remain public — it must be reachable by load balancer health checks.
- Structured logs must not contain secrets, auth tokens, full URLs with credentials, or PII.

## Adding a metric

1. Define the metric using your metrics library (e.g. `prometheus.NewCounter`, `prometheus.NewHistogram`).
2. Register it during app initialisation — not per-request.
3. Instrument the code path where the metric is recorded.
4. Start the server and verify the metric appears in `GET /metrics` output.

## Troubleshooting

| Symptom                       | Fix                                                                               |
| ----------------------------- | --------------------------------------------------------------------------------- |
| `/health` returns non-200     | Check DB connectivity and app startup logs                                        |
| `/metrics` returns 401        | Pass `Authorization: Bearer <token>` or check `METRICS_AUTH_ENABLED` setting      |
| Expected metric not in output | Confirm it was registered at startup; confirm the instrumented code path executed |

## Guardrails

- Protect `/metrics` in production; treat it as sensitive operational data.
- Keep `/health` reachable by load balancers and free of internal-state leakage.
- Register metrics at startup, not per request, to avoid duplicate-registration panics.
- Never let structured logs carry secrets, tokens, full credential URLs, or PII.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
