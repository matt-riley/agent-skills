# Phases, Red Flags, and Common Rationalisations

## Workflow Phases (Summary)

### Phase 1: Root Cause Investigation
**Goal:** Understand why the error is happening, not how to fix it yet.
- Read the error message end-to-end.
- Reproduce consistently.
- Trace data flow.
- Check component boundaries.
- Review recent changes (`git diff`, `git show`).
- Collect working examples for comparison.

**Red flags if investigation is incomplete:**
- You have not reproduced the issue yourself
- You have not read the error message fully
- You skipped checking recent changes
- You do not understand what the error is saying

### Phase 2: Pattern Analysis
**Goal:** Find what's different between the failing case and a working case.
- Locate a working example.
- Side-by-side comparison.
- Hypothesis from differences.
- Narrow the variables (one change at a time).
- Check assumptions.

### Phase 3: Hypothesis and Testing
**Goal:** Form a single hypothesis and verify it with a minimal test.
- State your hypothesis clearly.
- Make the smallest possible change to test it.
- Run the test. Document the result.
- If wrong: do not accumulate random changes; revert and return to Phase 2.

**If the hypothesis is wrong:** Do not accumulate random changes. Revert to a clean state. Return to Phase 2.

### Phase 4: Implementation
**Goal:** Fix the root cause and verify it doesn't break anything else.
- Write a failing test first (route to test-driven-development if needed).
- Implement the fix based on the validated hypothesis.
- Run the failing test again (should pass).
- Run the full test suite.
- Review the fix (minimal, addresses only the root cause).

**After 3+ consecutive fix attempts fail:**
- Stop making incremental changes.
- Question the design.
- Escalate to the user or team lead.

## Common Rationalisations

| Rationalisation | Reality |
|---|---|
| "Issue seems simple, skip the process" | Simple bugs have root causes too. Process is fast. A wrong fix on a "simple" bug breaks more than it fixes. |
| "Emergency, no time for investigation" | Systematic debugging is faster than guess-and-check. Guessing costs rework and creates new bugs. |
| "I see the problem, let me fix it" | Seeing a symptom ≠ understanding root cause. A symptom can have multiple causes. Fixing the symptom leaves the cause. |
| "Just try this first, then investigate" | First fix sets pattern. Random fixes create new bugs, distract from root cause, and slow handoff to others. |
| "3 fixes failed, let me try one more" | 3+ failures = architectural problem, not implementation detail. Further guessing is waste. Escalate. |

See the main SKILL.md for Guardrails and the high-level flow. Existing technique references (`root-cause-tracing.md`, `defense-in-depth.md`) provide deeper methods. Long examples are in `examples.md`.