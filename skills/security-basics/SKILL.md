---
name: security-basics
description: "Apply security and privacy guardrails to application code. Use when touching authentication, request handling, sensitive endpoint exposure, logging, or anything that could leak data or allow unauthorised access."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: draft
  kind: task
---

# Security basics

## Use this skill when

- Code under review or being written touches authentication, session handling, secrets, or credential material.
- Request handling, input parsing, header trust, or CORS/cookie behaviour is changing.
- A sensitive endpoint (admin, metrics, debug) is being added, exposed, or reworked.
- Logging or telemetry may incidentally capture credentials, tokens, or PII.

## Do not use this skill when

- The task is writing a full threat model, pen-test plan, or formal compliance artefact.
- The change has no security-sensitive surface (pure UI copy, doc-only edits).
- A specialised skill already covers the narrower concern (for example, `configuration-env` for env/secret plumbing).

## Inputs to gather

- The concrete diff or file set touching auth, request handling, or sensitive endpoints.
- How the service sits behind proxies or load balancers (for header trust decisions).
- Whether the environment is production or a lower tier (for CORS and cookie posture).

## First move

- Identify every auth, secret, input-trust, endpoint-exposure, and logging touchpoint in the change.
- Run the review checklist below against each touchpoint before proposing fixes.

## Outputs

- A concrete security review or fix list covering auth, secrets, input validation, endpoint exposure, CORS/cookies, and logging touchpoints.
- Checklist-backed confirmation that no hardcoded secrets, unsafe trust boundaries, leaked internals, or unprotected sensitive endpoints remain.
- Targeted validation evidence for authorization failures, invalid input handling, and scrubbed logs or responses.


## Authentication & secrets

- Auth tokens, passwords, and API keys must come from environment variables or a secrets manager — never hardcode them.
- Do not log request headers containing auth, session cookies, or full URLs that may embed credentials.
- Fail fast at startup if required auth config is missing.

## Input trust

- Trust **nothing** from client input without validation (schema, type, length, format).
- If behind a reverse proxy, trust `X-Forwarded-For` / `X-Real-IP` **only** when the proxy is known and controlled.
- Strip or overwrite forwarding headers at the proxy before forwarding to the app to prevent IP spoofing.
- Rate-limit by the real client IP, not by spoofable headers.

## Sensitive endpoint exposure

- Admin, metrics, and debug endpoints must be protected: auth middleware, network ACL, or both.
- `/health` and public status endpoints can remain open but must **not** reveal internal state, versions, or stack traces.

## CORS & cookies

- Set `Allowed-Origins` to explicit origins in production — never `*` when cookies or `Authorization` headers are in use.
- Enable secure cookies (`SameSite=Strict` + `Secure` flag) when the app is behind HTTPS.

## Review checklist

Before merging code that touches auth, request handling, or data exposure:

- [ ] No hardcoded secrets in source code or test fixtures
- [ ] All inputs validated (shape, type, length, format)
- [ ] Error responses do not leak internals (stack traces, DB errors, file paths)
- [ ] CORS origins are explicitly restricted for production
- [ ] Sensitive endpoints are protected
- [ ] Structured logs are scrubbed of credentials and PII

## Guardrails

- Never hardcode secrets, tokens, or API keys in source or test fixtures.
- Never trust spoofable request headers without a known, controlled proxy boundary.
- Never let error responses leak stack traces, DB errors, or internal file paths.
- Never default production CORS to `*` when cookies or `Authorization` headers are in play.
- Never log raw credentials, tokens, or PII — scrub at the structured-logging boundary.

## Validation

- Run targeted tests or checks for the changed auth, request-handling, logging, or exposure surface.
- Confirm no secrets, tokens, credentials, private data, or sensitive endpoint outputs were added to logs or public responses.
- Confirm authorization failures, invalid input, and cross-origin/cookie behavior are covered where relevant.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
