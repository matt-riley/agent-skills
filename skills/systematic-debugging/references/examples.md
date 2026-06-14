# Examples

Select the investigation pattern that best matches the current failure mode.

## Example 1: Test failure with stack trace

**Symptom:** Unit test fails with `AssertionError: expected 42 but got 0`

**Investigation:**
1. Read the test and the code it tests. The test calls `calculateTotal(items)` and expects 42.
2. Add a log inside `calculateTotal()` to see what's happening. Output shows `items` is an empty array.
3. Trace back: who calls `calculateTotal()`? The test does. How are `items` created? The test setup creates them.
4. Compare the test setup to a passing test in the same file. The passing test uses `beforeEach()` to set up items; this test does not.

**Root cause:** The test's setup function is not running.

**Fix:** Add `beforeEach()` to set up items. Verify the test passes.

## Example 2: Intermittent test failure

**Symptom:** A test fails once every 5-10 runs. Sometimes it passes.

**Investigation:**
1. Run the test 20 times in a loop. Note which inputs or states correlate with failures.
2. The test uses a timestamp or random value. Check whether the test clears state between runs.
3. Compare the test to other tests in the same file. Do they clean up after themselves?

**Root cause:** Test does not reset state between runs. When test B runs after test A, leftover state causes test B to fail.

**Fix:** Add a `teardown()` or reset at the end of each test. Verify the test passes consistently.

## Example 3: Regression after a commit

**Symptom:** Feature that worked yesterday is broken today.

**Investigation:**
1. Run `git log --oneline -5` to see recent changes.
2. Identify the commit that touched the feature code.
3. Check what that commit changed: `git show <commit-hash>`.
4. Compare the before and after. What is different?
5. Try reverting the commit locally. Does the feature work again?

**Root cause:** The commit removed a line by accident or changed a config value that the feature depends on.

**Fix:** Restore the line or config value. Verify the feature works.