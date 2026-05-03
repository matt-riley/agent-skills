# Examples for Templ Templates

Use these as concrete patterns when the skill should activate.

## Example 1 - Templ Edit Flow

User says: "I changed a .templ page component. What workflow should I follow to regenerate and verify the app?"

Expected behaviour:
- The response identifies the template location, regeneration step, handler wiring checks, and verification steps.
Key checks:
- Mentions locating `.templ` files.
- Mentions regeneration.
- Mentions handler wiring or verification.

## Example 2 - Templ Troubleshooting

User says: "The generated template code and the rendered page are out of sync after my change. What should I inspect?"

Expected behaviour:
- The response focuses on template source, generation, and Go wiring instead of generic frontend debugging alone.
Key checks:
- Mentions source template and generated output relationship.
- Mentions Go handler wiring or route integration.
- Mentions common pitfalls or invariants.
