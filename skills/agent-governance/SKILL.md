---
name: agent-governance
description: "Use this skill when building AI agents that call external tools, implementing policy-based access controls, adding semantic intent classification, creating trust scoring systems, building audit trails, or enforcing rate limits and content filters on agents."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---
# Agent Governance Patterns

Patterns for adding safety, trust, and policy enforcement to AI agent systems.

## Use this skill when

- Building AI agents that call external tools (APIs, databases, file systems)
- Implementing policy-based access controls for agent tool usage
- Adding semantic intent classification to detect dangerous prompts
- Creating trust scoring systems for multi-agent workflows
- Building audit trails for agent actions and decisions
- Enforcing rate limits, content filters, or tool restrictions on agents
- Working with any agent framework (PydanticAI, CrewAI, OpenAI Agents, LangChain, AutoGen)

## Do not use this skill when

- The agent runs in a fully trusted environment with no external tool access and no compliance requirements.
- You only need static code analysis or security review of agent source code; this skill provides runtime governance patterns, not static audit tools.

## Inputs to gather

**Required before implementing**

- The agent framework in use (PydanticAI, CrewAI, OpenAI Agents SDK, etc.)
- The list of tools the agent calls.
- The risk level for the use case (internal dev, standard production, compliance-critical).

**Helpful if present**

- Existing policy config files or security review requirements.
- Whether human-in-the-loop approval is needed for any tool.

## First move

1. Determine the governance level (open, standard, strict, or locked) based on the use case risk.
2. Define the `GovernancePolicy` with allowed tools, blocked patterns, and rate limits.
3. Apply the `@govern` decorator to tool functions.
4. Wire up the `AuditTrail` for compliance logging.

## Governance patterns

Select the smallest control set that meets the risk level, then read [`references/policy-patterns.md`](references/policy-patterns.md) for the implementation details:

- Governance policy and YAML configuration
- Semantic intent classification
- Tool-level governance decorators
- Trust scoring
- Append-only audit trails
- PydanticAI, CrewAI, and OpenAI Agents SDK integration
- Governance-level selection and best practices

Load the reference when implementing or comparing controls. Keep audit-only, guardrail, and full-governance modes distinct, and layer policies from broad defaults to task-specific restrictions.

## Outputs

- Policy, allowlists, trust scoring, or audit trail changes implemented with clear boundaries and tests or validation steps.
- Runtime governance behavior documented or demonstrated.

## Workflow

See the sections above for trigger, inputs, first move, and detailed steps. The workflow is read the governance requirements, implement the policy/trust/audit controls with clear boundaries, and validate behavior (tests or manual).

## Guardrails

- **Must not** allow tool calls to proceed when a governance check errors; fail closed.
- **Must not** store or log secret values; only confirm whether expected policy names and scopes are present.
- **Should** compose policies with most-restrictive-wins semantics when layering org, team, and agent policies.
- **Should** keep governance enforcement independent of agent business logic.
- **Should** use append-only audit entries; never modify or delete them.

## Validation

Apply the implementation checklist after wiring governance into an agent:

- Blocked tools raise `PermissionError` with the correct policy name
- Content filters catch the blocked patterns before tool execution occurs
- Rate limit counts calls correctly and denies at the configured threshold
- Audit trail captures allowed, denied, and error events for every tool call
- Policy composition uses most-restrictive-wins semantics when layers are combined

```markdown
### Implementation checklist
- [ ] Define governance policy (allowed tools, blocked patterns, rate limits)
- [ ] Choose governance level (open/standard/strict/locked)
- [ ] Add @govern decorator to all tool functions
- [ ] Add intent classification to user input processing
- [ ] Implement trust scoring for multi-agent interactions
- [ ] Wire up audit trail export
- [ ] Test that blocked tools are properly denied
- [ ] Test that content filters catch sensitive patterns
- [ ] Test rate limiting behavior
- [ ] Verify audit trail captures all events
- [ ] Test policy composition (most-restrictive-wins)
```

- Smoke test:
  - should trigger: "Add tool allowlists and audit logs to this coding agent."
  - should not trigger: "Generate a SHA-256 manifest for this plugin bundle." (→ `agent-supply-chain`)

## Examples

Select the governance controls appropriate for the risk level of the agent:

- **Internal dev agent** — audit-only mode, no restrictions: create an `AuditTrail` and log events without blocking any calls.
- **Standard production agent** — allowlist + content filters + rate limiting: use `GovernancePolicy` with `allowed_tools`, `blocked_patterns`, and `max_calls_per_request`.
- **Compliance-critical agent** — all controls + human approval: add `require_human_approval` for sensitive tool operations such as `send_email` or `write_report`.

See [`references/policy-patterns.md`](references/policy-patterns.md) for full Python code for each governance component and framework-specific wiring.

## Reference files

- [`references/policy-patterns.md`](references/policy-patterns.md) — governance policy, classifier, decorator, trust, audit, and governance-level implementation patterns
- [`references/framework-integration.md`](references/framework-integration.md) — framework-specific integration notes for PydanticAI, CrewAI, OpenAI Agents SDK, LangChain, and AutoGen
