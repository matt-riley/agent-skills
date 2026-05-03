# Examples for Configuration Env

Use these as concrete patterns when the skill should activate.

## Example 1 - Bootstrap Env

User says: "I have a .env.example and a failing local startup. Walk me through the safest config validation path."

Expected behaviour:
- The response explains the config source order, recommends starting from .env.example, and validates with a build/start plus health-check style loop.
Key checks:
- Mentions .env.example as documentation/template rather than runtime source of truth.
- Mentions failing fast on missing required config.
- Mentions a health check or start command validation loop.

## Example 2 - Production Secrets

User says: "Can I just use a .env file in production for this service?"

Expected behaviour:
- The response says production should prefer real environment variables or a secrets manager and warns against committing or relying on .env files in production.
Key checks:
- Discourages .env files in production.
- Mentions environment variables or a secrets manager.
- Mentions not committing secrets.

## Example 3 - Worker Binding Drift

User says: "My Worker's D1 binding is missing from wrangler config, but there is no schema or migration change."

Expected behaviour:
- The response treats this as runtime configuration drift, not a D1 migration task.
- It tells the agent to inspect `wrangler.toml`, `wrangler.json`, or `wrangler.jsonc` for the `d1_databases` entry and repair the missing binding contract.
- It keeps migration advice out of scope unless investigation reveals actual schema-state drift.

Key checks:
- Redirects away from `cloudflare-d1-migrations`.
- Mentions the relevant Wrangler config file and `d1_databases` binding.
- Frames the fix as binding/config repair rather than schema work.
