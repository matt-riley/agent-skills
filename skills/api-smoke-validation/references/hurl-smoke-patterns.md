# hurl smoke patterns

Keep smoke checks fast, deterministic, and focused on changed behavior.

## Request selection

- Always include one health/basic reachability request.
- Include one changed-path request (the endpoint touched by the code change).
- Add one auth-protected request when auth logic changed.

## Assertion style

- Assert status first, then one or two high-value headers/body fields.
- Prefer stable shape checks over brittle full-body equality.
- Keep fixtures deterministic and idempotent when possible.

## Repeatability

- Parameterize base URL and auth inputs through variables/env files.
- Preserve a single command that teammates and CI can rerun unchanged.
