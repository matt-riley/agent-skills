# Edge cases for HTTP API OpenAPI

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write a generic REST API tutorial."
- "Generate a client SDK for this spec only."
- "Tune a database repository query."

## Common edge cases
- If the repo does not own an OpenAPI spec, do not fabricate one; document the missing contract instead.
- If the change is internal-only and not externally exposed, confirm whether the OpenAPI surface should change at all.
- If the repo is code-first, change the owned code inputs and regenerate the spec instead of hand-editing generated OpenAPI output.
- If generation is involved, coordinate with the code-generation workflow rather than editing generated artifacts directly.

## Reminders
- If the request really matches this shape, the skill should activate: "I changed an HTTP handler and need the OpenAPI contract updated or regenerated the way this repo expects."
- If the request really matches this shape, the skill should activate: "Please update or regenerate the endpoint contract, auth requirements, and response schema together."
