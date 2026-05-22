# Agent Governance — Framework Integration Notes

This reference documents how to apply the governance patterns from `agent-governance` to specific agent frameworks.

## Supported frameworks

| Framework | Integration approach |
|-----------|---------------------|
| **PydanticAI** | `@agent.tool` + `@govern(policy)` decorators |
| **CrewAI** | Wrap `tool.func` on each crew agent before `crew.kickoff()` |
| **OpenAI Agents SDK** | `@function_tool` + `@govern(policy)` decorators |
| **LangChain** | Wrap tool callables with the governance decorator before passing to the agent |
| **AutoGen** | Apply at the tool-function level before registering with the assistant |

## Governance level selection

Match strictness to operational risk:

- **Internal/dev** — audit-only, no restrictions
- **Standard production** — allowlist + content filters + rate limiting
- **Compliance-critical** — all controls + human approval for sensitive operations
- **Locked** — allowlist only, no dynamic tools, full audit trail

See the governance patterns in `../SKILL.md` for full Python code examples including `GovernancePolicy`, `govern()` decorator, `TrustScore`, and `AuditTrail`.
