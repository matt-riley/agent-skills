---
name: verification-before-completion
description: "Use when about to claim work is complete, tests pass, a bug is fixed, or a build succeeds."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
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

## Routing Boundary

| Your situation | Use this skill? | Routing |
|---|---|---|
| "I think I fixed the bug" (no command run yet) | ✅ Yes | Run the test that reproduces the bug, read output |
| "All tests pass" (from yesterday's run) | ✅ Yes | Rerun tests fresh, capture current output |
| "The linter should be happy" (no check run) | ✅ Yes | Run linter fresh, capture full output |
| "I've understood the codebase" | ❌ No | Continue exploration or code inspection |
| "The build failed; here's why" + no rebuild | ✅ Yes | Rebuild, read full error output |
| "This PR is ready" (untested) | ✅ Yes | Run tests, linting, build before claiming readiness |

## Inputs to gather

1. **Claim**: What are you about to claim? (e.g., "tests pass", "bug is fixed", "build works")
2. **Command**: What single command proves or disproves this claim?
3. **Success Criteria**: What does success look like in the output? (exit code 0, "0 failures", "All tests passed", etc.)
4. **Scope**: Which tests, files, or targets? (e.g., "all tests" vs. "one unit test" vs. "integration suite")

## First move

Before proceeding:

1. **State the claim clearly**: "I am about to claim: [specific claim]"
2. **Identify the proof command**: "The command that proves this is: `[command]`"
3. **Describe success**: "Success means: [specific output pattern or exit code]"
4. **Check if ready**: "Am I ready to run this now?" (Do I have all the prerequisites? Is the environment set up?)

## Gate

**BEFORE claiming any status or marking work complete:**

1. **IDENTIFY**: What command proves this claim? (e.g., `npm test`, `pytest`, `go test`, `cargo test`)
2. **RUN**: Execute the full command fresh — do not rely on cached output or prior runs
   - Capture complete output (exit code, all stdout, all stderr)
   - Run the exact same command users will run to verify
3. **READ**: Study the full output carefully
   - Check exit code (0 = success, non-zero = failure)
   - Count actual pass/fail counts, not assumed counts
   - Note any warnings, deprecations, or flakiness
4. **VERIFY**: Does the output confirm your claim?
   - **If NO**: State the actual status with evidence from the output
   - **If YES**: State the claim WITH direct evidence (quote the output)
5. **ONLY THEN**: Make the claim and proceed

## Workflow

1. Pause before claiming success
2. Run the verification command
3. Read and interpret the output
4. If verification fails, report the actual status and debug
5. If verification passes, claim with evidence and proceed

## Common Failures

| Claim | Requires | Not sufficient |
|---|---|---|
| **Tests pass** | Test command output: all pass, 0 failures, exit code 0 | "I think they pass," previous run, linter passing, code reviewed |
| **Linter clean** | Linter stdout: no errors, 0 errors total | Partial file checks, "should be clean," no syntax errors |
| **Build succeeds** | Build command: exit code 0, no build errors in output | Linter passing, code compiles locally, "should build" |
| **Bug fixed** | Reproduction test now passes; symptom gone in live run | Code changed, test file created but not run, review approved |
| **Agent completed** | VCS diff shows actual committed changes or agent output shows execution | Agent log says "success," agent says it ran the command |
| **Formatting applied** | Formatter command: exit code 0, or git diff shows changes applied | Formatter installed, "should work," no actual check run |
| **Dependency installed** | `npm list`/`pip list`/`cargo tree` shows version, or import succeeds | `npm install` ran, "should be installed," no verification |

## Guardrails

- **Always run fresh**: Do not trust cached output, prior runs, or assumptions. The command must be run in the current state.
- **Read all output**: Exit codes matter. Error counts matter. Warnings matter. Do not skim.
- **No shortcuts**: Code inspection, linter readiness, or "it should work" do not replace running the command.
- **Exact command**: Run the same command the user will use to verify (e.g., `npm test`, not `npm run test-fast`).
- **Full scope**: If claiming "all tests pass," run all tests. If claiming "critical tests pass," run only those and be explicit.
- **Capture context**: Note the environment (Node version, OS, branch), command run, and output date so you can reference it later.
- **Be honest about uncertainty**: If output is ambiguous, say so. Do not force-fit evidence to a desired conclusion.

## Validation

After verification:

- [ ] I have run the relevant command fresh
- [ ] I have read the complete output (exit code, stdout, stderr)
- [ ] The output matches (or contradicts) my claim
- [ ] I am ready to state the claim with evidence
- [ ] If verification failed, I understand why and what to fix next

- Smoke test:
  - should trigger: "Before I say it's fixed, rerun the failing test and read the output."
  - should not trigger: "Find out why this failing test breaks only on CI." (→ `systematic-debugging`)

## Examples

Each example below shows the full Gate in practice — state the claim, identify the command, run it fresh, and verify the output.

### Example 1: "Tests Pass" Claim

**Setup**: "I just fixed a failing unit test in `src/utils.ts`."

**Before claiming**:
- Claim: "The test suite passes."
- Command: `npm test`
- Success: "exit code 0, all tests pass"

**Run**:
```bash
$ npm test
PASS  src/utils.test.ts
  ✓ handles edge case (45 ms)
  ✓ validates input (12 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
```

**Verify**: Exit code 0, "2 passed, 2 total" ✅

**Claim**: "The test suite passes. Output: `Test Suites: 1 passed, 1 total`; `Tests: 2 passed, 2 total`."

---

### Example 2: "Build Succeeds" Claim

**Setup**: "I made changes to the Go service."

**Before claiming**:
- Claim: "The build succeeds."
- Command: `go build ./...`
- Success: "exit code 0, no build errors"

**Run**:
```bash
$ go build ./...
(no output)
$ echo $?
0
```

**Verify**: Exit code 0 ✅

**Claim**: "The build succeeds. `go build ./...` exited with code 0."

---

### Example 3: "Linter Clean" Claim

**Setup**: "I ran `oxfmt` on the TypeScript files."

**Before claiming**:
- Claim: "Linter finds no errors."
- Command: `oxlint --fix .` (or `oxlint .` to check only)
- Success: "no errors reported, exit code 0"

**Run**:
```bash
$ oxlint .
Linted 12 files, no issues found.
```

**Verify**: "no issues found," exit code 0 ✅

**Claim**: "Linter clean. `oxlint .` reports 'no issues found'."

---

### Example 4: "Bug Fixed" Claim

**Setup**: "A test was failing because of a logic error. I fixed it."

**Before claiming**:
- Claim: "The bug is fixed."
- Command: `npm test -- --testNamePattern="exact test name"`
- Success: "test passes (was failing before)"

**Run**:
```bash
$ npm test -- --testNamePattern="handles null input safely"
PASS  src/parser.test.ts
  ✓ handles null input safely (8 ms)
```

**Verify**: Test passes ✅

**Claim**: "The bug is fixed. The failing test now passes: `handles null input safely`."

---

### Example 5: FALSE Claim (Do Not Do This)

❌ **Bad**: "I fixed the linting errors. I removed the unused variable and the import that wasn't needed."

❌ **Why**: You inspected the code but didn't run the linter.

✅ **Better**: "I fixed the linting errors. I removed the unused variable and ran `oxlint .` — output: `Linted 3 files, no issues found.`"

---

## Notes

- This skill applies to all verification scenarios: test passes, build succeeds, lint clean, bug fixed, command execution, agent completion.
- Do not skip the Gate. The Gate is the entire point of this skill.
- If you are uncertain, state the uncertainty as part of your verification result.

## Reference files

- [`systematic-debugging`](../systematic-debugging/SKILL.md) — use when root cause investigation is needed before verifying a fix
- [`test-driven-development`](../test-driven-development/SKILL.md) — use when writing tests to prove behavior before claiming correctness
