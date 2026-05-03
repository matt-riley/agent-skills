---
name: prompt-contracts
description: Define a task contract with GOAL, CONSTRAINTS, FORMAT, and FAILURE conditions before execution. Use when the user explicitly wants a prompt contract, success criteria, failure conditions, or a durable definition of done for non-trivial work.
license: Proprietary
compatibility: github-copilot-cli; pairs well with ask_user, plan mode, and validation-first execution.
metadata:
  owner: mattriley
  version: 1.1.0
  maturity: draft
---

# Prompt contracts

Use this when the user wants an explicit definition of done, not just a loose task description. The contract is an execution spec: it tells you what success means, what you cannot do, what shape the output must have, and what would count as failure.

## Use this skill when

- The user explicitly asks for a prompt contract, definition of done, success criteria, or failure conditions.
- A non-trivial task needs durable gating language before execution starts.
- You need to make fake-done outcomes impossible by naming concrete failure conditions up front.

## Do not use this skill when

- The user wants a full plan with tasks, milestones, or rollout phases rather than an execution spec (use `plan-review` instead).
- The task is a one-liner or obviously trivial.
- A normal plan or review workflow would already answer the request.

## Inputs to gather

- The user-visible outcome and any measurable success target.
- Hard constraints on scope, technology, compatibility, rollout, or dependencies.
- The expected output shape (files, tests, docs, APIs, review artefacts).
- Known failure conditions that would mean the task is not done even if something "works".

## First move

- Decide whether the deliverable is contract-only or contract-plus-execution, then draft the four sections (GOAL, CONSTRAINTS, FORMAT, FAILURE) using testable language.

## Catalog position

- Use this only when explicit success/failure framing is the main deliverable or gate.
- Pair with `plan-review` when the user wants both a plan and a contract.
- Pair with `rpi-workflow` when the contract should guide a larger multi-phase execution.

## Workflow

1. **Decide whether this is contract-only or contract-plus-execution.**
   - If the user only wants the spec, stop after drafting or refining the contract.
   - If the contract is meant to gate implementation, keep it concise and actionable so it can be used immediately.

2. **Draft or normalize the four sections.**
   - `GOAL`: the user-visible outcome and any measurable success target.
   - `CONSTRAINTS`: hard limits on scope, technology, compatibility, rollout, or dependencies.
   - `FORMAT`: exact output shape such as files, tests, docs, APIs, or review artifacts.
   - `FAILURE`: concrete conditions that mean the task is not done even if something appears to work.

3. **Resolve only material ambiguity.**
   - Use `ask_user` when the contract depends on a meaningful product or implementation decision.
   - If the remaining ambiguity is minor, draft the reasonable assumption explicitly and proceed.
   - If the task is trivial, say the full contract is overkill and use a minimal version.

4. **Treat the contract as binding during execution.**
   - Do not optimize for speed by drifting outside the constraints.
   - Re-check the FAILURE section during implementation; it is the fastest way to catch fake-done outcomes.

5. **Deliver with explicit contract status.**
   - Report whether GOAL, CONSTRAINTS, FORMAT, and FAILURE all pass.
   - If something cannot be verified, mark it `UNVERIFIABLE` and explain what evidence is missing.
   - If any failure condition triggered, do not present the task as complete.

## Minimal contract template

```markdown
GOAL: ...

CONSTRAINTS:
- ...

FORMAT:
- ...

FAILURE:
- ...
```

## Guardrails

- Use concrete, testable language; avoid vague words like "fast", "clean", or "robust" without criteria.
- Failure conditions should catch edge cases, missing validation, silent errors, regressions, and over-engineering.
- Do not force a contract onto one-line or obviously trivial tasks.

## Support files

- Read `references/examples.md` when you need concrete trigger examples or a contract shape to mirror.
- Read `references/edge-cases.md` when the request is ambiguous, a near miss, or the contract starts conflicting with itself.
