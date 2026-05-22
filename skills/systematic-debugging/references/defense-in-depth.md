# Defense-in-Depth Debugging Strategies

Systematic debugging works best with layered observability and elimination strategies. This reference covers defensive techniques to surface bugs faster and narrow problems at each layer of the system.

## Observable Systems

The easier a system is to inspect, the faster you can debug it. Build observability in before you need it.

### Logging strategy

**Levels:**

- **ERROR:** Something failed. Always log errors with context (what were you trying to do, what input, what state).
- **WARN:** Something unexpected but recoverable happened. Document why it's acceptable.
- **INFO:** Major operations. "Starting process X," "Database connected," "User created."
- **DEBUG:** Detailed flow. Variable values, function entry/exit, decision branches.

**For debugging a specific bug:**

Add DEBUG logs at the boundaries you are investigating:

```javascript
function calculateTotal(items) {
  console.debug("calculateTotal called with:", items);  // Input
  let sum = 0;
  for (const item of items) {
    console.debug("Adding item:", item, "sum so far:", sum);  // Progress
    sum += item;
  }
  console.debug("calculateTotal returning:", sum);  // Output
  return sum;
}
```

Then run the failing case and read the log. You will see exactly where the data diverges.

### Log placement

Place logs at:

1. **Function entry:** What arguments were passed?
2. **Decision branches:** Which path was taken?
3. **Loop bodies:** Is the loop executing? How many times?
4. **Component boundaries:** What data is crossing the boundary?
5. **Error conditions:** What state led to the error?

### Structured logging

Instead of:

```
Calculation failed
```

Log:

```
Calculation failed for user_id=123, items=[1,2,3], expected=6, actual=0
```

Include context so you do not have to run the code again to understand what happened.

## Trace Logging for Data Flow

Follow a single piece of data through the system:

```javascript
const traceId = generateId();  // Unique ID for this request

function processRequest(data) {
  console.log(`[${traceId}] Input:`, data);
  const validated = validate(data);
  console.log(`[${traceId}] After validation:`, validated);
  const result = calculate(validated);
  console.log(`[${traceId}] After calculation:`, result);
  return result;
}
```

The `[traceId]` lets you follow one request through multiple functions. When logs are mixed (multiple requests running), you can filter by traceId and see one request's full journey.

## Boundary Testing

Test inputs and outputs at every major boundary:

### Input validation

```javascript
function processUser(user) {
  // BOUNDARY: Validate before processing
  if (!user || !user.id || !user.name) {
    throw new Error(`Invalid user: ${JSON.stringify(user)}`);
  }
  // Now you know user is safe
  return user.name.toUpperCase();
}
```

**Why:** If invalid data enters, you catch it at the boundary instead of debugging a cascade of failures downstream.

### Output validation

```javascript
function calculateTotal(items) {
  const sum = items.reduce((a, b) => a + b, 0);
  
  // BOUNDARY: Validate before returning
  if (typeof sum !== 'number' || isNaN(sum)) {
    throw new Error(`Invalid total: ${sum}`);
  }
  return sum;
}
```

**Why:** If output is wrong, you know the bug is in this function, not somewhere downstream.

## Working vs. Broken Comparison

Systematically compare working and broken code:

### Side-by-side diff

```javascript
// WORKS
function calculateTotal(items) {
  let sum = 0;
  for (let i = 0; i < items.length; i++) {
    sum += items[i];
  }
  return sum;
}

// BROKEN (from production)
function calculateTotal(items) {
  let sum;  // ← BUG: Should be 0, not undefined
  for (let i = 0; i < items.length; i++) {
    sum += items[i];  // ← Adds undefined to number = NaN
  }
  return sum;  // ← Returns NaN
}
```

The difference is small (initialized to 0 vs. undefined) but fatal.

### Test-driven comparison

Write a test for both:

```javascript
// Working version
test("calculateTotal([1,2,3]) returns 6", () => {
  expect(calculateTotal([1, 2, 3])).toBe(6);
});

// Run both implementations
// If one fails, compare line-by-line to find the difference
```

## Divide and Conquer

Narrow the problem by splitting the system in half repeatedly:

### Process breakdown

```
Input
  → Parsing
    → Validation
      → Transformation
        → Calculation
          → Output
```

Bug could be at any stage. Start in the middle:

1. Log the output of Transformation. Is it correct?
   - **Yes:** Bug is in Calculation
   - **No:** Bug is in Parsing, Validation, or Transformation
2. If bug is in Parsing/Validation/Transformation, repeat: log after the middle step (Validation). Is it correct?

By halving the search space each time, you locate the bug in log₂(N) steps, not N steps.

### Dependency isolation

Does the bug appear with a specific library version?

```bash
npm install lib@old-version  # Test with old version
npm test  # Does bug go away?
npm install lib@new-version  # Test with new version
npm test  # Does bug return?
```

If yes, the library is the problem. If no, the bug is in your code.

## State and Initialization Debugging

Many bugs are state-related: things not reset, initialized wrongly, or polluted.

### State snapshot

At critical points, log the full state:

```javascript
function processRequest(request) {
  console.log("STATE AT START:", {
    request,
    cache: globalCache,
    config: process.env,
  });
  
  // Do work
  
  console.log("STATE AT END:", {
    request,
    cache: globalCache,
    config: process.env,
  });
}
```

Compare start and end states. What changed unexpectedly?

### Cleanup and teardown

Intermittent bugs often signal state leakage. In tests:

```javascript
beforeEach(() => {
  // Reset state before each test
  globalCache = {};
  database.clear();
});

afterEach(() => {
  // Cleanup after each test
  globalCache = {};
  database.clear();
});
```

If tests start passing consistently, the bug was state leakage.

## Hypothesis Testing Protocol

Once you have a hypothesis, test it minimally:

### Single-variable testing

**Bad:** Change 5 things, run the test. Does it pass?

If yes, you do not know which change fixed it. If no, you do not know which change broke it.

**Good:** Change 1 thing, run the test. Document the result.

```
Hypothesis: Empty array causes calculateTotal to return 0 instead of null.

Test: 
  - Change calculateTotal to return null for empty array
  - Run test
  - Result: Test passes ✓
  
Next hypothesis: Now test with a filled array to ensure we didn't break it.
```

### Reverting for proof

```bash
# Current code has a fix. Does the bug return without it?
git stash            # Save current changes
npm test             # Run test
# If test fails, the stashed code fixed it
git stash pop        # Restore the fix
```

## Layered Debugging: From Symptoms to Root Cause

### Layer 1: Symptoms
- Identify what is broken (test failure, wrong output, crash)
- Capture the exact error message

### Layer 2: Reproduction
- Run the failure locally
- Make it consistent (same command, same result every time)

### Layer 3: Isolation
- Is it in your code or a dependency?
- Is it in one component or multiple?
- Does it depend on environment or input?

### Layer 4: Data flow
- Log inputs at function entry
- Log outputs at function exit
- Trace where the data diverges from expectations

### Layer 5: Root cause
- Compare working to broken code
- Form a hypothesis
- Test with minimal change
- Verify the fix does not break anything else

## Observability Checklist

Before declaring a bug "fixed," ensure the system is observable for next time:

- [ ] Error messages are descriptive (context, values, not just "error")
- [ ] Critical operations log at INFO level
- [ ] Data boundaries log input and output
- [ ] State is validated at entry and exit
- [ ] Logs are structured (traceable, filterable)
- [ ] Errors are caught and logged before crashing
- [ ] Tests clean up state after themselves

## When to escalate

If after systematic debugging you still have no root cause:

- [ ] You have reproduced the issue consistently
- [ ] You have traced data flow at every boundary
- [ ] You have compared working to broken code
- [ ] You have formed and tested 3+ hypotheses, all failed
- [ ] You have checked recent changes and environment differences

**Then escalate.** Do not keep guessing. A third pair of eyes, access to a different environment, or domain expertise may reveal what systematic local debugging missed.

## Checkpoint: Layered debugging complete

You have applied defense-in-depth when:

- [ ] You have logs at all critical boundaries
- [ ] You can trace one request/operation through the system
- [ ] You have isolated the bug to a specific component
- [ ] You have compared working to broken code at that component
- [ ] You have validated the fix does not break other tests
- [ ] You have added an observable log point so the next person can debug faster
