---
name: stochastic-multi-agent-consensus
description: Poll multiple agents independently, aggregate the results, and report consensus, divergence, and outliers. Use when the user wants many independent takes, a ranking, a vote, or a confidence-weighted comparison rather than an interactive debate.
license: Proprietary
compatibility: github-copilot-cli; assumes parallel task agents and optional session-workspace artifacts.
metadata:
  owner: mattriley
  version: 1.1.0
  maturity: draft
---

# Stochastic multi-agent consensus

Use this when the user wants independent polling with aggregation. If the agents need to challenge each other across rounds, use `agent-chatrooms` instead.

## Use this skill when

- The user wants many independent takes, a ranking, a vote, or a confidence-weighted comparison.
- Aggregating variance across samples is more informative than a single confident answer.
- The question has a structured answer shape (ranked list, binary, scorecard, shortlist).

## Do not use this skill when

- The user wants interactive debate or rounds of challenge (use `agent-chatrooms`).
- The question is fuzzy — tighten it before spending multiple agent calls.
- The expected answer has no natural structure to aggregate over.

## Inputs to gather

- The polling question, any option list, and the desired aggregation output.
- Sample size N (and whether odd N is needed for binary decisions).
- The fixed response schema each agent must produce.

## First move

- Lock the response schema, decide N, then launch the sample agents in parallel with the same core prompt plus small framing variations.

## Workflow

1. **Frame the polling question.**
   - Capture the exact problem, any option list, and what the user wants back: ranking, binary decision, scorecard, shortlist, or recommendations.
   - If the prompt is fuzzy, tighten it before spending multiple agent calls.

2. **Define a structured response schema before spawning.**
   - Every agent should return the same shape so the outputs can be compared mechanically.
   - Good schemas include ranked lists, yes/no plus reasons, scored options, or top-three recommendations with confidence.

3. **Choose the sample size deliberately.**
   - Good defaults: 5 agents for binary or ranking tasks, 7 for open recommendation tasks.
   - Use a larger N only when the user asks for it or the problem is unusually noisy.
   - Prefer odd N for binary decisions.

4. **Launch independent agents in parallel.**
   - Use one `task` agent per sample with the same core prompt and small framing variations.
   - Use `agent_type: "general-purpose"` for open reasoning and `explore` for codebase lookup or fact-finding.
   - Keep the task identical across samples; only the framing should vary slightly.

5. **Aggregate mechanically.**
   - Rankings: assign points and total them.
   - Binary choices: report the split and strongest reasons from each side.
   - Scores: report central tendency plus variance.
   - Open recommendations: cluster similar ideas into consensus, divergence, and outliers.

6. **Write a compact artifact and deliver the synthesis.**
   - Prefer session-local paths such as `files/consensus/<slug>/responses.json` and `files/consensus/<slug>/report.md`.
   - Report the top consensus item, the main disagreement, the most interesting outlier, and the effective N if any sample failed.

## Output checklist

- polling question and aggregation target
- sample size and any framing strategy
- consensus result
- main divergence
- most interesting outlier
- effective N and any exclusions
- artifact paths when created

## Guardrails

- Do not use this for interactive debate; this skill is for independent sampling.
- Keep the schema fixed before launching agents or the aggregation becomes meaningless.
- Be honest when the result is split; a lack of consensus is itself useful output.
- Keep N small by default so the signal is worth the cost.

## Support files

- Read `references/examples.md` when you need concrete trigger examples or an aggregation shape to mirror.
- Read `references/edge-cases.md` when the request is ambiguous, a near miss, or the first pass produces noisy outputs.
