# Examples for HTTP API OpenAPI

Use these as concrete patterns when the skill should activate.

## Example 1 - New Endpoint Sync

User says: "I am adding a new authenticated HTTP endpoint. This repo might be code-first, so what actually needs to stay in sync?"

Expected behaviour:
- The response identifies whether the repo is spec-first, code-first, or hybrid, then explains how to keep the handler and contract aligned.
Key checks:
- Mentions both handler and OpenAPI/spec changes.
- Mentions detecting the repo's contract owner first.
- Mentions auth or error shape alignment.
- Mentions guardrails against editing generated contract artifacts by hand.

## Example 2 - Spec Drift Debug

User says: "The code and OpenAPI document are drifting apart after a recent endpoint change. How should I fix it?"

Expected behaviour:
- The response uses the repo's actual source-of-truth workflow and does not treat the code/spec as unrelated surfaces.
Key checks:
- Mentions contract owner or generation path.
- Mentions verifying both implementation and contract.
- Avoids hand-wavy advice that ignores one side of the contract.
