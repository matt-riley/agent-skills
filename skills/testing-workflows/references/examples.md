# Examples for Testing Workflows

Use these as concrete patterns when the skill should activate.

## Example 1 - Debug Test Failure

User says: "My Go tests are failing after a generated-code change. What is the right debugging sequence?"

Expected behaviour:
- The response starts with generation freshness, then isolates the failing test path, then checks integration/database concerns as needed.
Key checks:
- Mentions generation before deeper debugging when relevant.
- Mentions isolating a specific test or package.
- Mentions DB or integration setup for integration failures.

## Example 2 - New Feature Test Expectations

User says: "I added a new feature in domain, repository, and HTTP layers. What test coverage should I expect?"

Expected behaviour:
- The response maps expectations across domain/service, repository, and HTTP layers with order-independent test discipline.
Key checks:
- Mentions multiple test layers.
- Mentions order-independent or isolated tests.
- Mentions new features require tests before merge.
