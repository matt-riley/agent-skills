# Examples for Ci Images

Use these as concrete patterns when the skill should activate.

## Example 1 - Release Readiness Check

User says: "I updated generated code and release automation. Validate the local CI equivalents and tell me if the image release is safe to publish."

Expected behaviour:
- The response identifies the local CI-equivalent commands to run, checks generated artifacts and tests, and states the release-readiness outcome with any blockers.
Key checks:
- Mentions generation freshness before release.
- Mentions tests or CI-equivalent checks.
- Calls out image tagging or release publish expectations.

## Example 2 - Stale Generated Output

User says: "CI says generated output is stale just before a container release. What should happen next?"

Expected behaviour:
- The response explains that generation must be rerun and committed before release, and does not recommend publishing from a stale or dirty state.
Key checks:
- Says stale generated output blocks release readiness.
- Says the working tree should be checked before publish.
- Does not recommend publishing immediately without fixes.
