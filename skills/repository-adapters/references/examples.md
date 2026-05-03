# Examples for Repository Adapters

Use these as concrete patterns when the skill should activate.

## Example 1 - Adapter Method Change

User says: "I need to add a repository method and wire the DB adapter correctly. What should I preserve?"

Expected behaviour:
- The response focuses on consumer-side interface contracts, adapter query changes, error mapping, and verification.
Key checks:
- Mentions domain interface or adapter boundary.
- Mentions error mapping rules.
- Mentions verification after query changes.

## Example 2 - Db Error Handling

User says: "The DB now returns a duplicate-key error for this adapter path. How should the repository layer handle it?"

Expected behaviour:
- The response maps DB-specific failures into domain-appropriate errors instead of leaking raw DB details upward.
Key checks:
- Mentions domain-facing error mapping.
- Avoids leaking raw DB-specific behavior as the final interface.
- Keeps focus on the adapter layer.
