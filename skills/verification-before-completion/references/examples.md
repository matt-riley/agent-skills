# Examples

Each example shows the full Gate in practice — state the claim, identify the command, run it fresh, and verify the output.

## Example 1: "Tests Pass" Claim

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

## Example 2: "Build Succeeds" Claim

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

## Example 3: "Linter Clean" Claim

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

## Example 4: "Bug Fixed" Claim

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

## Example 5: FALSE Claim (Do Not Do This)

❌ **Bad**: "I fixed the linting errors. I removed the unused variable and the import that wasn't needed."

❌ **Why**: You inspected the code but didn't run the linter.

✅ **Better**: "I fixed the linting errors. I removed the unused variable and ran `oxlint .` — output: `Linted 3 files, no issues found.`"
