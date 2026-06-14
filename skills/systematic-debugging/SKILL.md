---
name: systematic-debugging
description: "Use when encountering any bug, test failure, unexpected behavior, or persistent error before proposing fixes — especially under time pressure, after multiple failed attempts, or when the root cause is unclear."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Systematic Debugging

## Use this skill when

- You encounter a failing test, error message, or unexpected behavior
- Multiple fix attempts have failed (2+)
- The symptom is clear but the root cause is unclear
- You feel time pressure to "just try something" or skip investigation
- Behavior changed after recent commits or configuration changes
- A production issue or blocking regression surfaces
- The bug appears intermittent or environment-dependent
- You are about to propose a fix without understanding why the problem exists

## Do not use this skill when

- The root cause is already known and validated (move to implementation)
- The fix has already been verified in a test environment (move to validation)
- You are responding to a user's explicit "apply this specific fix" request (acknowledge context first, then validate)
- The issue is documentation-only or labeling (use domain-specific conventions directly)

See `references/phases-and-rationalisations.md` for the full routing boundary table and red flags.

## Inputs to gather

Before starting investigation, collect:
- Full error message or test failure output (not a summary).
- Reproduction steps.
- Environment context, timeline, scope.

If reproduction is unclear, make reproduction your first step.

## First move

1. Capture the full error or failure output. Do not summarize.
2. Reproduce consistently (at least twice).
3. Check recent changes (`git log --oneline -10`).
4. Read the error message carefully.

If you cannot reproduce within two attempts, document that it may be environment-dependent.

## Workflow

### Phase 1: Root Cause Investigation
Goal: Understand *why*, not how to fix yet.
- Read error end-to-end.
- Reproduce consistently.
- Trace data flow / boundaries.
- Review recent changes (`git diff` / `git show`).
- Collect working examples for side-by-side comparison.

**Red flags if incomplete:** not reproduced yourself, not read full error, skipped recent changes, do not understand the message.

### Phase 2: Pattern Analysis
Find the difference between failing and working case. One variable at a time. Hypothesis from differences.

### Phase 3: Hypothesis and Testing
State one clear hypothesis. Smallest change to test it. Run, document. If wrong: revert cleanly and return to Phase 2. Never accumulate random changes.

### Phase 4: Implementation
Write failing test first (consider `test-driven-development`). Fix based on validated hypothesis. Re-run failing + full suite. Ensure the change is minimal and only addresses the root cause.

**After 3+ consecutive failures:** stop incremental changes, question the design, escalate.

Detailed phases, red flags, and the rationalisations table live in `references/phases-and-rationalisations.md`. Technique deep-dives are in the existing `root-cause-tracing.md` and `defense-in-depth.md`.

## Outputs

- One-sentence root cause with supporting evidence (error text, diff, reproduction, comparison).
- Verified hypothesis (minimal test or reproduction that demonstrates the cause).
- Minimal fix that addresses only the root cause.
- Passing tests (the original failure now passes + no new regressions).
- Explicit review or handoff note.

## Guardrails

- **Never propose a fix without stating the root cause.** If you cannot explain why, you do not understand it yet.
- **Never make more than one change per hypothesis test.**
- **Never skip test reproduction.**
- **After 3 failed fixes, stop and escalate.**
- **Always document assumptions.**

## Validation

Debugging is complete when:
1. Root cause is documented in one sentence with evidence.
2. The cause is verified (test, diff, trace).
3. The fix is minimal and addresses only the root cause.
4. Tests pass (failing one + no new regressions).
5. Fix is reviewed.

- Smoke test:
  - should trigger: "This test still flakes; find the root cause before we change code."
  - should not trigger: "Rerun the failing test to confirm the fix worked." (→ `verification-before-completion`)

## Examples

See `references/examples.md` for the three detailed investigation patterns (stack trace, intermittent, post-commit regression) with root cause statements and minimal fixes.

## Reference files

- `references/examples.md` — concrete investigation walkthroughs with symptoms, steps, root causes, and fixes.
- `references/phases-and-rationalisations.md` — full phases, red flags, and common rationalisations table.
- `references/root-cause-tracing.md` — error anatomy, tracing techniques.
- `references/defense-in-depth.md` — logging, observability, layered elimination strategies.
- [`verification-before-completion`](../verification-before-completion/SKILL.md) — use after root cause is fixed to confirm with fresh evidence.
- [`test-driven-development`](../test-driven-development/SKILL.md) — write the failing test in Phase 4.
