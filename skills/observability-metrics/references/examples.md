# Examples for Observability Metrics

Use these as concrete patterns when the skill should activate.

## Example 1 - Metrics Validation

User says: "I added a metric and changed observability auth. What should I validate locally?"

Expected behaviour:
- The response checks health/metrics behavior, security exposure, and metric-specific validation steps.
Key checks:
- Mentions health or metrics endpoint validation.
- Mentions security or sensitive endpoint protection.
- Mentions verifying the new metric itself.

## Example 2 - Observability Debug

User says: "The service is up but my observability output looks wrong. What should I inspect first?"

Expected behaviour:
- The response uses endpoint checks, logs, and troubleshooting steps specific to observability rather than generic debugging only.
Key checks:
- Mentions troubleshooting health/metrics/logging.
- Mentions local validation commands such as curl.
- Keeps focus on observability surfaces.
