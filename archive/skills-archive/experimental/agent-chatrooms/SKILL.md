---
name: agent-chatrooms
description: Conduct a multi-agent debate in a shared transcript and synthesize the result. Use when the user explicitly wants agents to discuss, debate, argue, or pressure-test a decision, design, review, or trade-off from multiple perspectives.
license: Proprietary
compatibility: github-copilot-cli; assumes task, read_agent, write_agent, and session-workspace artifacts.
metadata:
  owner: mattriley
  version: 1.1.0
  maturity: draft
---

# Agent chatrooms

Use this when the user wants interacting agents that can challenge each other over multiple rounds. If the user wants many independent takes with aggregation, use `stochastic-multi-agent-consensus` instead.

## Use this skill when

- The user explicitly asks for a debate, discussion, argument, or multi-perspective pressure test.
- A decision, design, review, or trade-off benefits from productive tension between roles.
- Round-by-round challenge is more valuable than independent polling.

## Do not use this skill when

- The user wants independent samples aggregated (use `stochastic-multi-agent-consensus`).
- The question is still fuzzy — sharpen it before spawning agents.
- A single agent or the main conversation can answer correctly on its own.

## Inputs to gather

- The exact debate question and the decision the user needs out of the room.
- Any explicit panel size, round count, roles, or model pins.
- Where the shared transcript should live (session workspace path is usually fine).

## First move

- Frame the debate question and roster in one artifact, then launch one persistent background agent per participant so state survives across rounds.

## Workflow

1. **Frame the debate.**
   - Capture the exact question, constraints, and what decision the user needs out of the room.
   - Honor explicit panel size, round count, roles, or model requests.
   - Good defaults: 3 agents, 2 rounds.

2. **Choose complementary roles.**
   - If the user names roles, use them exactly.
   - Otherwise choose roles that create productive tension, such as architect / pragmatist / critic or user advocate / engineer / skeptic.
   - Avoid redundant roles that will produce the same answer.

3. **Create a shared transcript artifact.**
   - Prefer a session-local path such as `files/agent-chatrooms/<slug>/chat.json`.
   - Store the problem statement, constraints, agent roster, round entries, and final synthesis.
   - Keep the transcript structured enough that each round can be replayed or summarized cleanly.

4. **Run the room with persistent agents.**
   - Launch one background `task` agent per participant so each agent keeps its role and conversation state.
   - Use `agent_type: "general-purpose"` unless the problem is simple enough for `explore`.
   - After each round, collect responses with `read_agent`, append the shared transcript, and send the next round prompt with `write_agent`.
   - Stop early if the room has clearly converged.

5. **Synthesize yourself.**
   - Do the final synthesis in the main conversation rather than asking another agent to summarize the debate.
   - Call out agreements, the sharpest remaining disagreement, the recommended action, and unresolved risks.
   - Keep the raw transcript path available for inspection.

## Output checklist

- debate question and decision target
- participants and roles
- strongest agreement
- sharpest disagreement
- recommended action
- unresolved risks
- transcript/report artifact paths

## Guardrails

- Use this only when the user explicitly wants debate, discussion, argument, or multi-perspective pressure testing.
- If the question is still fuzzy, sharpen it before spawning agents.
- Keep the panel small unless the user explicitly wants a larger room.
- Do not collapse this into independent polling; the value comes from interaction between rounds.

## Support files

- Read `references/examples.md` when you need concrete trigger examples or a response shape to mirror.
- Read `references/edge-cases.md` when the request is ambiguous, a near miss, or the first pass goes sideways.
