# Examples for Research -> Plan -> Implement -> Validate (RPI-V)

Use these as concrete patterns when the skill should activate.

## Example 1 - Non Trivial Change

User says: "Use a research -> plan -> implement -> validate workflow for this non-trivial change and keep context disciplined."

Expected behaviour:
- The response sequences the work into phases, keeps research read-only, and requires validation before completion.
Key checks:
- Mentions the phased RPI-V flow explicitly.
- Keeps research read-only before implementation.
- Mentions validation before completion.

## Example 2 - Phase Boundaries

User says: "I want to work one phase at a time and preserve artifacts between phases. What is the workflow?"

Expected behaviour:
- The response explains workspace-artifact persistence, phase boundaries, and phase-specific verification instead of blurring the steps together.
Key checks:
- Mentions `plan.md`, `files/`, or equivalent durable workspace checkpoints.
- Mentions one phase at a time.
- Mentions verification per phase.
