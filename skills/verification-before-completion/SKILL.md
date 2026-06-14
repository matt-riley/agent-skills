---
name: verification-before-completion
description: "Use when about to claim work is complete, tests pass, a bug is fixed, or a build succeeds."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Verification Before Completion

## Iron Law

> **NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**
>
> A claim like "tests pass," "build succeeds," or "bug is fixed" requires you to have actually run the relevant command, read the full output, and confirmed the claim matches that evidence. Assumptions, previous runs, or code inspection alone do not count.

## Use this skill when

- You are about to claim a test suite passes, a specific test passes, or a test fails
- You are about to claim a build succeeded, lint check passed, or formatting succeeded
- You are about to claim a bug is fixed, a regression is gone, or a feature works as intended
- You are about to claim a command, script, or agent operation completed successfully
- You are about to mark a task `done` or report progress to the user
- You are about to commit or push code with a claim of readiness
- You are about to create a pull request or declare work "complete"
- You have made code changes and are unsure whether they work

## Do not use this skill when

- You are asking a user what test command to run (use this after they tell you)
- You are planning or designing a feature (verification comes after implementation)
- You are debugging failures and tracing root cause (this skill is for **confirming** fixes, not finding them)
- You are reading documentation, exploring code, or gathering context

See `references/common-failures.md` for the full Routing Boundary table and inputs.

## Inputs to gather

1. **Claim**: What are you about to claim?
2. **Command**: The single command that proves or disproves it.
3. **Success Criteria**: What "good" looks like in the output.
4. **Scope**: Full suite vs. specific target.

## First move

Before proceeding:
1. State the claim clearly.
2. Identify the proof command.
3. Describe success criteria.
4. Check readiness, then run fresh.

## Gate (mandatory)

**BEFORE claiming any status:**
- IDENTIFY the command
- RUN the exact command fresh (capture full stdout/stderr + exit code)
- READ the output (counts, warnings, exact messages)
- VERIFY the output matches (or contradicts) the claim with direct quotes
- ONLY THEN state the claim with evidence

## Workflow

1. Pause before claiming success.
2. Run the verification command.
3. Read and interpret the full output.
4. If verification fails, report actual status and debug.
5. If verification passes, claim with direct evidence from this run and proceed.

Common failure modes and the full "not sufficient" table live in `references/common-failures.md`.

## Outputs

- Claim stated with direct evidence quoted from a fresh run of the exact verification command.
- Pass/fail status, exit code, counts, and warnings captured.
- Next action (proceed / investigate further / report actual status) clear.

## Guardrails

- **Always run fresh**: Do not trust cached output, prior runs, or assumptions.
- **Read all output**: Exit codes, counts, and warnings matter. Do not skim.
- **No shortcuts**: Code inspection or "it should work" do not replace running the command.
- **Exact command**: Run what users will run.
- **Full scope**: If claiming "all tests," run all tests.
- **Capture context**: Note env, command, and timestamp.
- **Be honest about uncertainty**.

## Validation

After verification:
- [ ] I have run the relevant command fresh
- [ ] I have read the complete output (exit code, stdout, stderr)
- [ ] The output matches (or contradicts) my claim with direct evidence
- [ ] I am ready to state the claim with evidence
- Smoke tests and negative cases are in `references/common-failures.md`.

## Examples

See `references/examples.md` for the full set of claim examples (Tests Pass, Build Succeeds, Linter Clean, Bug Fixed, and the FALSE claim anti-pattern).

## Reference files

- `references/examples.md` — detailed claim walkthroughs with exact commands and output verification.
- `references/common-failures.md` — Iron Law, routing table, inputs, Gate steps, and the "Requires vs. Not sufficient" table.
- [`systematic-debugging`](../systematic-debugging/SKILL.md) — use when root cause investigation is needed before verifying a fix.
- [`test-driven-development`](../test-driven-development/SKILL.md) — use when writing tests to prove behavior before claiming correctness.
