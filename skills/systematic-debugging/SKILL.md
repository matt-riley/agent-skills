---
name: systematic-debugging
description: "Use when encountering any bug, test failure, unexpected behavior, or persistent error before proposing fixes — especially under time pressure, after multiple failed attempts, or when the root cause is unclear."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
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

## Iron Law

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**
>
> Violating this process is failure, not pragmatism.

Systematic debugging is faster than guess-and-check, not slower. The cost of a wrong fix is always higher than the cost of understanding the problem first.

## Routing boundary

| Signals | Route to skill | Route elsewhere |
|---------|---|---|
| Error or test output visible; no clear fix yet | Stay here. Start Root Cause Investigation. | |
| Root cause validated; fix strategy known | Move to test-driven-development | |
| Fix committed and verified; tests passing | Move to verification-before-completion | |
| User says "here's the fix, apply it" | Clarify whether user wants validation first. If not, document the external instruction. | |
| Incident requires immediate rollback or workaround | Propose minimal immediate action, then schedule root-cause investigation. | |

## Inputs to gather

Before starting investigation, collect:

- **Full error message or test failure output** (not a summary; the actual error text)
- **Reproduction steps** (exact commands or user actions that trigger the issue)
- **Environment context** (OS, tool versions, configuration, recent changes)
- **Timeline** (when did it start? what changed recently?)
- **Scope** (does it happen in all environments or specific ones?)

If reproduction is unclear, make reproduction your first step.

## First move

1. **Capture the full error or failure output.** Do not summarize; save the exact text.
2. **Reproduce consistently.** Run the failing command/test at least twice. Confirm the issue is not intermittent.
3. **Check recent changes.** Use `git log --oneline -10` or similar to list recent commits. Identify which change might have introduced the issue.
4. **Read the error message carefully.** Most error messages explain the problem directly; do not skip this step.

If you cannot reproduce the issue within two attempts, it may be environment-dependent. Document that and investigate environment differences.

## Workflow

### Phase 1: Root Cause Investigation

**Goal:** Understand why the error is happening, not how to fix it yet.

- **Read the error message end-to-end.** Stack traces, line numbers, and assertion messages are your primary data.
- **Reproduce the issue consistently.** If it's intermittent, try to narrow the trigger (specific input, timing, environment).
- **Trace data flow.** Follow the data from input through the code path to the point of failure. Use logs, prints, or a debugger.
- **Check component boundaries.** Is the issue in your code, a dependency, configuration, or environment?
- **Review recent changes.** Compare the code at the failure point to the previous known-good version. Use `git diff` or `git show`.
- **Collect working examples.** If similar code works elsewhere, copy that example and compare line-by-line.

**Red flags if investigation is incomplete:**
- You have not reproduced the issue yourself
- You have not read the error message fully
- You skipped checking recent changes
- You do not understand what the error is saying

### Phase 2: Pattern Analysis

**Goal:** Find what's different between the failing case and a working case.

- **Locate a working example.** Is there similar code that works? A passing test with related logic? A previous version of the same file?
- **Side-by-side comparison.** Compare the working and failing code line-by-line. Note every difference.
- **Hypothesis from differences.** For each difference, ask: "Could this difference cause the observed error?"
- **Narrow the variables.** If multiple differences exist, change one at a time to isolate which causes the failure.
- **Check assumptions.** Reread the code assuming your mental model is wrong. Is there a precondition you missed? A side effect you overlooked?

### Phase 3: Hypothesis and Testing

**Goal:** Form a single hypothesis and verify it with a minimal test.

- **State your hypothesis clearly.** "The bug is caused by [specific thing] because [evidence]."
- **Make the smallest possible change** to test the hypothesis. One line, one config value, or one test case.
- **Run the test.** Does the issue disappear? Does it reproduce?
- **Document the result.** Whether the hypothesis was right or wrong, record what you learned.

**If the hypothesis is wrong:**
- Do not accumulate random changes. Revert to a clean state.
- Return to Phase 2 and look for the next difference.
- Repeat Phase 3 with a new hypothesis.

### Phase 4: Implementation

**Goal:** Fix the root cause and verify it doesn't break anything else.

- **Write a failing test first.** The test should reproduce the bug and fail before your fix. (Route to test-driven-development if needed.)
- **Implement the fix** based on your validated hypothesis.
- **Run the failing test again.** It should pass now.
- **Run the full test suite.** Ensure no regressions.
- **Review the fix.** Does it fix only the root cause, or does it paper over a symptom? Is the code change minimal and clear?

**After 3+ consecutive fix attempts fail:**
- Stop making incremental changes.
- Question the design, not just the implementation.
- Is there a deeper architectural problem? Should the component be refactored?
- Escalate to the user or team lead for guidance.

## Common rationalisations

| Rationalisation | Reality |
|---|---|
| "Issue seems simple, skip the process" | Simple bugs have root causes too. Process is fast. A wrong fix on a "simple" bug breaks more than it fixes. |
| "Emergency, no time for investigation" | Systematic debugging is faster than guess-and-check. Guessing costs rework and creates new bugs. |
| "I see the problem, let me fix it" | Seeing a symptom ≠ understanding root cause. A symptom can have multiple causes. Fixing the symptom leaves the cause. |
| "Just try this first, then investigate" | First fix sets pattern. Random fixes create new bugs, distract from root cause, and slow handoff to others. |
| "3 fixes failed, let me try one more" | 3+ failures = architectural problem, not implementation detail. Further guessing is waste. Escalate. |

## Guardrails

- **Never propose a fix without stating the root cause.** If you cannot explain why the bug exists, you do not understand it yet.
- **Never make more than one change per hypothesis test.** Multiple changes hide which one actually works.
- **Never skip test reproduction.** If you cannot make the issue happen consistently, you cannot verify the fix.
- **After 3 failed fixes, stop and escalate.** Do not keep trying random changes.
- **Always document assumptions.** If you assume the issue is in component A, state it and verify it. Wrong assumptions waste time.

## Validation

Debugging is complete when:

1. **Root cause is documented.** You can explain the bug in one sentence: "The bug is caused by [specific thing]."
2. **The cause is verified.** You have evidence: a test that reproduces it, a diff that shows the change, a log trace that confirms it.
3. **The fix is minimal.** The code change addresses only the root cause, not symptoms.
4. **Tests pass.** The failing test now passes, and no new tests fail.
5. **Fix is reviewed.** Another person or the user has confirmed the fix makes sense.

- Smoke test:
  - should trigger: "This test still flakes; find the root cause before we change code."
  - should not trigger: "Rerun the failing test to confirm the fix worked." (→ `verification-before-completion`)

## Examples

Select the investigation pattern that best matches the current failure mode:

### Example 1: Test failure with stack trace

**Symptom:** Unit test fails with `AssertionError: expected 42 but got 0`

**Investigation:**
1. Read the test and the code it tests. The test calls `calculateTotal(items)` and expects 42.
2. Add a log inside `calculateTotal()` to see what's happening. Output shows `items` is an empty array.
3. Trace back: who calls `calculateTotal()`? The test does. How are `items` created? The test setup creates them.
4. Compare the test setup to a passing test in the same file. The passing test uses `beforeEach()` to set up items; this test does not.

**Root cause:** The test's setup function is not running.

**Fix:** Add `beforeEach()` to set up items. Verify the test passes.

### Example 2: Intermittent test failure

**Symptom:** A test fails once every 5-10 runs. Sometimes it passes.

**Investigation:**
1. Run the test 20 times in a loop. Note which inputs or states correlate with failures.
2. The test uses a timestamp or random value. Check whether the test clears state between runs.
3. Compare the test to other tests in the same file. Do they clean up after themselves?

**Root cause:** Test does not reset state between runs. When test B runs after test A, leftover state causes test B to fail.

**Fix:** Add a `teardown()` or reset at the end of each test. Verify the test passes consistently.

### Example 3: Regression after a commit

**Symptom:** Feature that worked yesterday is broken today.

**Investigation:**
1. Run `git log --oneline -5` to see recent changes.
2. Identify the commit that touched the feature code.
3. Check what that commit changed: `git show <commit-hash>`.
4. Compare the before and after. What is different?
5. Try reverting the commit locally. Does the feature work again?

**Root cause:** The commit removed a line by accident or changed a config value that the feature depends on.

**Fix:** Restore the line or config value. Verify the feature works.

## Reference files

- [Root Cause Tracing Techniques](references/root-cause-tracing.md) — Deep dive into error analysis, reproduction, and data flow tracing
- [Defense-in-Depth Debugging Strategies](references/defense-in-depth.md) — Layered observability and systematic elimination
