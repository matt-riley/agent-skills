# Edge cases for Templ Templates

Use this file when the request is ambiguous, risky, or only partially matches the skill.

## Near-miss prompts
- "Write React JSX for a client-side component."
- "Explain HTML templating in abstract terms."
- "Add an OpenAPI endpoint schema."

## Common edge cases
- If the UI change belongs in CSS/assets only, do not over-route into templ-specific regeneration work.
- If the template output is generated, avoid patching generated files directly.
- If the repo uses a wrapper script for templ generation, prefer that over raw CLI assumptions.

## Reminders
- If the request really matches this shape, the skill should activate: "I changed a .templ file; help me regenerate and verify the handler wiring."
- If the request really matches this shape, the skill should activate: "Troubleshoot this server-side templ component and keep the Go wiring in sync."
