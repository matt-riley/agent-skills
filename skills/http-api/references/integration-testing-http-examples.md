# Examples for Integration Testing HTTP

Use these as concrete patterns when the skill should activate.

## Example 1 - Extend Http Tests

User says: "I changed an endpoint and need to update the end-to-end HTTP integration tests. What should those tests assert?"

Expected behaviour:
- The response focuses on status codes, auth, request/response shapes, and the changed contract rather than only unit-level details.
Key checks:
- Mentions request/response contract assertions.
- Mentions auth or middleware if relevant.
- Mentions running the existing integration suite.

## Example 2 - Debug Http Failure

User says: "The integration test for my HTTP route is failing after a middleware change. How should I debug it?"

Expected behaviour:
- The response suggests isolating the failing route/test, checking middleware interactions, and preserving integration-level expectations.
Key checks:
- Mentions isolating the failing integration test.
- Mentions middleware or auth interactions.
- Keeps focus on end-to-end HTTP behavior.
