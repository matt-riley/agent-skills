# Examples for Stochastic multi-agent consensus

Use these as concrete patterns when the skill should activate.

## Example 1 - Option ranking

User says: "Poll 5 agents on these database options and tell me the consensus ranking, the biggest disagreement, and any outlier idea worth considering."

Expected behaviour:
- The response frames the task as independent polling, defines an aggregatable schema, and returns consensus, divergence, and outlier information.

Key checks:
- Uses independent polling rather than debate.
- Mentions a structured aggregation method.
- Reports consensus and divergence separately.
- Surfaces an outlier or high-variance idea.

## Example 2 - Binary decision

User says: "What do 7 agents think about shipping this behind a feature flag? Give me the vote split and the strongest case on each side."

Expected behaviour:
- The response chooses an odd sample size, treats each agent as an independent sample, and aggregates the yes/no split with reasons.

Key checks:
- Preserves the independent-sample framing.
- Returns a clear vote split.
- Summarizes the strongest arguments from each side.
