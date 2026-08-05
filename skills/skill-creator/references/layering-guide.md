# Layering guide

Use this guide to decide where guidance belongs.

## Put guidance in global instructions when

- It applies across most tasks.
- It describes universal defaults, safety rules, or tool preferences.
- It should affect behavior even when no specific skill is active.

## Put guidance in a reference skill when

- It mainly helps an agent find conventions, patterns, examples, or lookup-heavy guidance quickly.
- The next step is mostly navigation or decision support rather than a long multi-step playbook.
- The guidance benefits from references or examples but does not need a strong output contract.

## Put guidance in a task skill when

- It describes a reusable workflow that should activate only for certain tasks.
- The workflow needs explicit inputs, outputs, guardrails, or validation.
- The workflow benefits from examples, guardrails, references, or optional helper scripts.
- The guidance should be portable across repositories or clients with only light adaptation.

## Put guidance in a specialized agent when

- The behavior is narrow, high-touch, or deeply stateful.
- The workflow needs a dedicated persona or unusually strong orchestration.
- The task requires a custom operating model that would be awkward inside a shared skill.

## Escalation rule

If a skill starts accumulating repository-specific policy, one-off playbook steps, or orchestration logic for a single environment, move that material out of the skill.
