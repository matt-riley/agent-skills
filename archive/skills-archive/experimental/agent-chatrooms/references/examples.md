# Examples for Agent chatrooms

Use these as concrete patterns when the skill should activate.

## Example 1 - Architecture debate

User says: "Have three agents debate whether this service should stay monolithic or split into workers, then give me the final recommendation."

Expected behaviour:
- The response frames a debate, assigns distinct roles, runs a small number of rounds, and returns a synthesis rather than a raw pile of opinions.

Key checks:
- Uses a debate workflow rather than independent polling.
- Mentions distinct participant roles.
- Mentions a shared transcript or round-by-round exchange.
- Produces a final recommendation plus the key disagreement.

## Example 2 - Pressure test a review

User says: "Use an agent chatroom with an architect, security reviewer, and pragmatist to pressure-test whether our admin export should run inline in the API or as a background job."

Expected behaviour:
- The response preserves the requested roles, runs the room as an adversarial discussion, and surfaces the most important disagreement and recommended path.

Key checks:
- Uses the exact user-specified roles.
- Keeps the discussion multi-round or explicitly stops early on convergence.
- Ends with agreements, disagreement, and recommended action.
