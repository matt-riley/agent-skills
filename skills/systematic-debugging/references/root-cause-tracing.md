# Root Cause Tracing Techniques

When an error occurs, the error message tells you *what happened*. Root cause analysis tells you *why it happened*. This reference covers the core techniques for systematic root-cause tracing.

## Error Message Anatomy

Every error message contains:

1. **Error type** — The class or category (`AssertionError`, `TypeError`, `SyntaxError`, `FileNotFoundError`)
2. **Error message** — The explanation (`expected 42 but got 0`, `no such file`, `cannot read property 'foo' of undefined`)
3. **Stack trace** — The call chain leading to the error (file, line number, function name)
4. **Context** — Variables, state, or input that led to the error

**Technique:** Read the error message from top to bottom. Do not skip lines. The first line usually contains the most direct clue.

### Reading a stack trace

A stack trace shows the call chain *in reverse order* (most recent call first):

```
Error: no such column: 'user_id'
  at SQLite3 (query.js:142)
  at Query.run (db.js:89)
  at FetchUser (user.js:34)
  at main (index.js:12)
```

Start at the top: the error happened in `query.js:142` during a SQLite query. The query ran from `db.js:89`. That code was called from `user.js:34` in `FetchUser`. Trace backwards to find where the problem was introduced.

**Root cause is usually at the lowest level** (furthest down the trace), but the nearest application code is your entry point. Start at the first file in your own codebase, then work inward.

## Reproducing Consistently

A bug you cannot reproduce is a bug you cannot debug. Before investigating, make the failure repeatable.

### Reproduction steps

Document the exact steps:

```
1. Run: npm test -- --grep "user creation"
2. Observe: Test fails with "expected 42 but got 0"
3. Repeat: Run the same command 3 times. Failure happens every time.
```

### Intermittent bugs

If the bug is not consistent, narrow it:

- Run the failing command 10+ times. Does it fail every time or randomly?
- If random, try: different inputs, different environments (localhost vs. Docker), different order of operations.
- Intermittency often signals state leakage (one test polluting the next) or timing dependencies (race conditions, delays).

### Isolating the trigger

Use binary search:

1. Start with the simplest reproduction (one function call, one input value).
2. Add complexity one piece at a time until the bug surfaces.
3. Remove parts one at a time to find the minimal reproduction.

**Minimal reproduction example:**

```javascript
// Before: Complex test with many steps
// After: Single function call with one input that fails
const result = calculateTotal([]);  // Bug: returns 0 instead of null
```

## Component Boundary Tracing

Most bugs live at component boundaries — where data moves from one part of the system to another.

### The data flow chain

Ask: where does the input come from, and where does the output go?

```
User input → Validation → Processing → Database → Response → Client display
```

If the error happens at the database step, trace backwards: Did validation pass? Did processing modify the data? Did the input match expectations?

### Identifying the boundary

- **UI to API:** Does the client send what the API expects? Use network inspector or logs.
- **API to Database:** Does the database receive the right schema? Check query logs.
- **Library to Code:** Is the library returning what you expected? Check the library docs and return values.
- **Configuration to Runtime:** Is the config value actually being read? Log it at startup.

**Technique:** Add logging or a breakpoint at each boundary. Confirm data is what you expect at each stage.

## Data Flow Analysis

Trace a single piece of data from input to error:

1. **Where does it come from?** (user input, file, API response, database)
2. **What changes happen to it?** (parsing, validation, calculation, serialization)
3. **Where does it go?** (database, response, file, next function)
4. **Where does it diverge from expectations?** (This is usually the bug.)

### Example: Wrong calculation

```
Input: items = [5, 10, 15]
Expected: sum = 30
Actual: sum = 0

Trace:
1. items comes from database query
2. calculateTotal(items) sums them
3. Return value is passed to response

Where is sum = 0?
→ Check calculateTotal function. 
→ Log shows items is [] not [5, 10, 15].
→ Bug is not in calculateTotal. Bug is in the database query.
```

## Recent Changes Analysis

Bugs often appear after a commit. Use git to narrow the change:

### Find the commit

```bash
git log --oneline -20  # List last 20 commits
git show <commit-hash>  # See what changed in that commit
```

### Diff-based investigation

```bash
# See lines added/removed in the last commit
git diff HEAD~1 HEAD

# See lines changed in a specific file
git diff HEAD~1 HEAD -- src/myfile.js
```

Ask:
- Did a line get deleted that should not have been?
- Did a variable name change but not everywhere?
- Did a config value change?
- Did a function signature change but not all callers?

### Reverting for proof

If you suspect a specific commit caused the bug:

```bash
git revert <commit-hash>  # Undo that commit
# Test: does the bug go away?
git revert --abort  # Undo the revert if you were wrong
```

If the bug disappears after revert, the commit is the culprit. Now find what in that commit is wrong.

## Hypothesis Formation

After investigation, form a testable hypothesis:

**Bad hypothesis:** "The code is broken." (Too vague.)

**Good hypothesis:** "The code is broken because the `items` array is empty, not because `calculateTotal()` is wrong, because (1) I reproduced the bug with the same empty array, (2) a working test passes the same logic with a filled array, and (3) the database query logs show an empty result."

Your hypothesis should include:
- **What is wrong** (the specific thing that's different)
- **Why you think it's wrong** (evidence: logs, diffs, comparison to working code)
- **How to test it** (change one line and verify)

## Working Example Comparison

Find code that works and code that does not. Compare them side-by-side:

```javascript
// WORKS
const result = calculateTotal([5, 10, 15]);  // Returns 30

// BROKEN
const result = calculateTotal([]);  // Returns 0, expected null
```

Differences:
- One passes filled array, one passes empty array
- One returns number, one returns 0

The bug is likely in how `calculateTotal` handles an empty array. Check the function:

```javascript
function calculateTotal(items) {
  let sum = 0;
  for (const item of items) {
    sum += item;
  }
  return sum;  // BUG: Should return null for empty array, not 0
}
```

**Technique:** Copy the working code and compare character-by-character. Use a diff tool if available.

## Common Root Cause Patterns

### Off-by-one errors

```
Expected: index 0–2 (3 items)
Actual: index 0–1 (2 items)
→ Check loop condition: `for (let i = 0; i < array.length; i++)` vs. `i <= array.length`
```

### Missing null/undefined checks

```
Error: Cannot read property 'foo' of undefined
→ Object is null or undefined. Add a check before accessing properties.
```

### Stale or leftover state

```
Test A sets global state. Test B runs next without cleaning up.
→ Tests now fail in a different order or intermittently.
→ Check teardown/cleanup functions.
```

### Configuration mismatch

```
Local environment works. CI fails.
→ Environment variable is not set in CI. Check config at startup.
```

### Unhandled async errors

```
Promise rejection silently ignored.
→ Missing `.catch()` or `await`. Check error handling.
```

## Isolation and Elimination

Use elimination to narrow the problem:

1. **Comment out half the code.** Does the bug still happen? If not, it's in the commented-out half.
2. **Revert changes one-by-one.** Does the bug disappear after reverting commit X? Commit X is the problem.
3. **Run in a different environment.** Does it fail locally but not in Docker? The environment is the problem.
4. **Replace a dependency.** Does the bug persist if you use a different library? The dependency is the problem.

**Technique:** Each step should eliminate an entire category of possibilities, not just one line.

## Checkpoint: When investigation is complete

You are ready to test a hypothesis when you can answer:

- [ ] What is the error? (Exact message, not summary)
- [ ] How do you reproduce it consistently?
- [ ] What recent change might have caused it?
- [ ] Where in the code does it fail? (File, function, line)
- [ ] What data is different from the working case?
- [ ] What is your hypothesis for the root cause?

If you cannot answer all of these, keep investigating.
