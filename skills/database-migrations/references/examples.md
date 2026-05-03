# Examples for Database Migrations

Use these as concrete patterns when the skill should activate.

## Example 1 - New Migration

User says: "This repo uses forward-only migrations. I need to add a unique index and want the safe apply/recovery workflow."

Expected behaviour:
- The response identifies the migration tool, determines the repo's migration contract, and outlines the correct create/apply/recovery steps.
Key checks:
- Mentions locating the repo migration tool.
- Mentions forward-only vs reversible behavior instead of assuming rollback support.
- Mentions follow-on schema checks such as generation or tests when relevant.

## Example 2 - Migration State Debug

User says: "A migration is in a weird state in development. What should I inspect first?"

Expected behaviour:
- The response focuses on migration state, tool-specific history/status, and safe recovery rather than ad hoc schema edits.
Key checks:
- Mentions migration state/history.
- Mentions safe recovery, including forward-only corrective paths when rollback is not part of the repo contract.
- Does not recommend manual schema drift as the first fix.
