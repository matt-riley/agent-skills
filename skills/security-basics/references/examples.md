# Examples for Security Basics

Use these as concrete patterns when the skill should activate.

## Example 1 - Auth And Logging Review

User says: "I changed auth handling and structured logs. What security checks should I apply before merging?"

Expected behaviour:
- The response checks secrets handling, logging hygiene, endpoint exposure, input trust, and cookies/CORS where relevant.
Key checks:
- Mentions secrets or auth token handling.
- Mentions log or PII or credential scrubbing.
- Mentions endpoint exposure or CORS/cookie safety.

## Example 2 - Sensitive Endpoint

User says: "I added a metrics endpoint and changed proxy headers. What should I be careful about?"

Expected behaviour:
- The response warns about trust boundaries, spoofable headers, and protecting sensitive endpoints.
Key checks:
- Mentions trust of forwarded headers or proxy boundary.
- Mentions protection of metrics/admin/debug endpoints.
- Includes a concrete security checklist-style response.
