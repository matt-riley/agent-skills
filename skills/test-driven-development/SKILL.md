---
name: test-driven-development
description: "Use when implementing a new feature, fixing a bug, or refactoring existing behavior — proven correct by executable tests written before production code."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Test-Driven Development

Use this skill when implementing any feature, bugfix, or behavior change that requires confidence that the code works as intended. TDD is the practice of writing a failing test first, then writing minimal production code to pass it, then refactoring.

## Use this skill when

- Implementing any new feature or functionality.
- Fixing a bug or addressing a regression.
- Refactoring or improving existing code.
- Adding edge-case handling or boundary-condition logic.
- You need to ensure code behavior is correct and documented through executable tests.

## Do not use this skill when

- The task is documentation-only or configuration-only with no executable logic.
- The request is exploratory research or one-off investigation without production code output.
- The repository explicitly prohibits or does not support automated testing (rare; ask first).

## Iron Law

> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**
>
> Write the test. Watch it fail. Write minimal code to pass. Never write production code without a failing test first.
>
> Tests are specifications. They answer "what should this code do?" Tests written after are archaeology; they can only answer "what does this code do?"

## Routing boundary

| Scenario | Use TDD Skill | Route Away |
|---|---|---|
| **New feature request** | Yes — write test for the desired behavior first | N/A |
| **Bug report** | Yes — write test that reproduces the bug, then fix | Consider [github-actions-failure-triage](/skills/github-actions-failure-triage) if it's a CI failure |
| **Refactor request** | Yes — write test for current behavior, refactor while keeping tests green | Consider [typescript-any-eliminator](/skills/typescript-any-eliminator) or other targeted hardening skills for narrower improvements |
| **Code review feedback** | Yes if feedback requests behavior change or new handling | Use [review-comment-resolution](/skills/review-comment-resolution) for process; route back to TDD for code changes |
| **Performance optimization** | Yes — write benchmark test first, then optimize, keep tests green | N/A |
| **Configuration or docs only** | No | Document without this skill |

## Inputs to gather

Before starting, clarify:

1. **What is the expected behavior?** (What should the code do?)
2. **What test framework is in use?** (Jest, Mocha, Vitest, Go testing, etc. — check repo defaults)
3. **What is the scope?** (One function? A whole module? Incremental delivery?)
4. **Are there existing tests** that establish patterns or conventions?
5. **What are the acceptance criteria?** (Happy path? Edge cases? Error handling?)

## First move

1. **Do not write production code yet.**
2. Write one minimal failing test that asserts the desired behavior.
3. Run the test and confirm it fails **for the right reason** (e.g., "function does not exist" or "returned undefined", not a syntax error).
4. Only then move to the RED-GREEN-REFACTOR cycle.

The test failure is your proof that the feature does not exist yet. This is the RED phase.

## Workflow

1. **RED:** Write one minimal failing test for the specific behavior. Confirm it fails for the right reason (feature missing, not syntax error).
   - One assertion or one logical outcome per test when possible.
   - Use a test name that says what you expect: `should return 42 when input is valid` not `should work`.
   
2. **GREEN:** Write the simplest code that makes the test pass. No extra features, no YAGNI (You Aren't Gonna Need It).
   - Minimal. If the test wants a function that returns 42, return 42 (not dynamic logic yet).
   - Ignore performance, elegance, generality. Just pass the test.
   
3. **REFACTOR:** Clean up only after green. Remove duplication, improve names, extract helpers. Keep tests green.
   - Refactor code, not tests (unless the test itself was poorly written).
   - Run tests after every refactor step to catch mistakes early.
   
4. **Repeat** for the next behavior.

## Delete Rule

If production code was written before a test, **delete it**. Do not "adapt" it while writing tests afterward. Delete means delete.

Unverified code is not a time-saving shortcut; it is technical debt. Keeping it forces you to reverse-engineer what it was supposed to do, which takes longer than rewriting it test-first.

## Outputs

- Failing test written first (red).
- Minimal implementation that makes it pass (green).
- Refactor that improves the code while keeping tests green.
- Evidence of the TDD cycle (test output before/after).

## Guardrails

- **One test at a time.** Write one test, watch it fail, make it pass. Do not write all tests upfront.
- **Test one thing per test.** If a test asserts multiple behaviors, split it. Multiple assertions on the same object or outcome are OK; multiple independent behaviors are not.
- **Delete unverified code.** If you wrote production code before a test, delete it. Rewrite it test-first.
- **Watch every failure.** Confirm each test fails before you write code. A test that passes on the first run is not testing anything.
- **Minimal code.** Write only enough production code to pass the test. Save elegance and performance for the REFACTOR phase.
- **Keep tests green.** Refactor code, but never leave tests failing. A refactor that breaks tests is not done.

## Common rationalisations and reality

| Rationalisation | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. A test takes 30 seconds to write. |
| "I'll write tests after" | Tests-after answer "what does this do?" Tests-first answer "what should this do?" — Different questions, different results. |
| "Already manually tested" | Manual testing is ad-hoc and unmemoried. No record, can't re-run. Automated tests are proof and documentation. |
| "Deleting X hours of work is wasteful" | Sunk cost. Keeping unverified code is debt that compounds. Rewriting it test-first clears the debt. |
| "TDD will slow me down" | TDD is faster than debugging. A failing test is a precise bug report; `console.log` is archaeology. |
| "Mocking everything makes tests too complex" | Mock only external dependencies (databases, APIs, files). Test logic with real data structures. |
| "This code is too coupled to test" | That is the signal to refactor. Testability is a design metric. Hard-to-test code is brittle. |

## Verification Checklist

Before marking work complete:

- [ ] Every new function, method, or behavior has a test.
- [ ] Watched each test fail before implementing the code.
- [ ] Each test failed for the expected reason (not a syntax error or import issue).
- [ ] Wrote minimal code to pass each test; no extra features.
- [ ] All tests pass; no skipped or pending tests.
- [ ] No errors or warnings in test output.
- [ ] Refactored only after all tests passed.
- [ ] Tests are clear and maintainable (good names, obvious assertions).

## Validation

1. Run the full test suite for the modified module or package.
2. Confirm all tests pass and cover the new behavior.
3. Check test coverage (if the repo tracks it) to confirm the new code is exercised.
4. Review the test names to ensure they document the expected behavior.

- Smoke test:
  - should trigger: "Fix this parser bug by writing a failing test first."
  - should not trigger: "Rerun the parser tests before claiming the bug is fixed." (→ `verification-before-completion`)

## Examples

- **Adding a new validator:**
  Write a failing test: `expect(validateEmail('')).toBe(false)` → implement `validateEmail()` until it passes → add edge-case tests for malformed inputs.

- **Reproducing a bug before fixing it:**
  Write `expect(parseAmount('£1,000.00')).toBe(1000)` → confirm it fails → fix `parseAmount()` → confirm it passes.

- **Pinning behavior before refactoring:**
  Capture current return values in a test suite → refactor the implementation → verify all tests still pass.

See [`references/tdd-scenarios.md`](references/tdd-scenarios.md) for full TypeScript-focused walkthroughs.

## Reference files

- [`references/tdd-scenarios.md`](references/tdd-scenarios.md) — Scenario walkthroughs with TypeScript code examples (500–800 words).
