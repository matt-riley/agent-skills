# TDD Scenarios with TypeScript Examples

This document walks through four common TDD scenarios with practical TypeScript code examples.

## 1. New Feature: Happy Path and Edge Cases

**Scenario:** You need to implement a function that validates and normalizes email addresses. Start with the happy path, then add edge cases.

**Test first (RED):**

```typescript
describe("normalizeEmail", () => {
  it("should return lowercase email with whitespace trimmed", () => {
    expect(normalizeEmail("  John@EXAMPLE.com  ")).toBe("john@example.com");
  });
});
```

Run the test — it fails because `normalizeEmail` does not exist.

**Minimal code (GREEN):**

```typescript
export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}
```

Test passes. Now add the next behavior.

**Next test (edge case — RED):**

```typescript
it("should throw on invalid email format", () => {
  expect(() => normalizeEmail("not-an-email")).toThrow("Invalid email format");
});
```

Run the test — it fails. Implement:

```typescript
export function normalizeEmail(email: string): string {
  const normalized = email.trim().toLowerCase();
  if (!normalized.includes("@") || !normalized.includes(".")) {
    throw new Error("Invalid email format");
  }
  return normalized;
}
```

Test passes. Repeat for additional edge cases: empty strings, multiple @-signs, etc. Each test drives one new behavior.

**REFACTOR (GREEN → CLEAN):** Once all tests pass, improve the regex or extract helper functions without breaking any test.

**Key insight:** Each test is a specification. The test suite becomes the living documentation of what the function does and does not accept.

---

## 2. Bug Fix: Write the Test That Reproduces the Bug First

**Scenario:** A bug report: "The cart total is wrong when a discount is applied before tax." You do not fix the code; you write the test first.

**Write the failing test (RED):**

```typescript
describe("calculateCartTotal", () => {
  it("should apply tax after discount", () => {
    const items = [{ price: 100, quantity: 1 }];
    const discountPercent = 10;
    const taxPercent = 10;
    
    const total = calculateCartTotal(items, discountPercent, taxPercent);
    // Subtotal: 100, Discount: 10, After discount: 90, Tax: 9, Total: 99
    expect(total).toBe(99);
  });
});
```

Run the test — it fails (returns 98 or 108 or something else). This failure is proof the bug exists.

**Now implement the fix (GREEN):**

```typescript
export function calculateCartTotal(
  items: Array<{ price: number; quantity: number }>,
  discountPercent: number,
  taxPercent: number
): number {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const afterDiscount = subtotal * (1 - discountPercent / 100);
  const total = afterDiscount * (1 + taxPercent / 100);
  return Math.round(total * 100) / 100;
}
```

Test passes. The bug is fixed and documented by the test.

**Key insight:** The test proves the fix works. Future developers can read the test and understand the correct behavior. If someone breaks this later, the test catches it immediately.

---

## 3. Refactor: Pin Current Behavior, Then Refactor

**Scenario:** You want to refactor a utility function to use a better algorithm, but you want to preserve correctness.

**Write a test for current behavior (RED → GREEN first):**

```typescript
describe("fibonacci", () => {
  it("should return correct fibonacci sequence", () => {
    expect(fibonacci(0)).toBe(0);
    expect(fibonacci(1)).toBe(1);
    expect(fibonacci(5)).toBe(5);
    expect(fibonacci(10)).toBe(55);
  });
});
```

Assume the current implementation already passes (GREEN — no changes needed yet).

**Refactor the code (keeping tests green):**

```typescript
// OLD: recursive (slow for large n)
export function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// NEW: iterative (fast)
export function fibonacci(n: number): number {
  if (n <= 1) return n;
  let [a, b] = [0, 1];
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b];
  }
  return b;
}
```

Run the test suite after the refactor. All tests pass. The behavior is identical, but the implementation is faster. The test is your safety net.

**Key insight:** Tests are the anchor. They free you to refactor fearlessly because you know immediately if you broke something.

---

## 4. Edge Case: Test Boundary Conditions Before Implementing

**Scenario:** You need to implement a `getElement` function that retrieves an item from an array by index. Think about what could go wrong: negative indices, out-of-bounds indices, null array, etc.

**Boundary condition tests (RED):**

```typescript
describe("getElement", () => {
  it("should return the element at the given index", () => {
    expect(getElement([1, 2, 3], 0)).toBe(1);
    expect(getElement([1, 2, 3], 2)).toBe(3);
  });

  it("should return undefined for out-of-bounds index", () => {
    expect(getElement([1, 2, 3], 10)).toBeUndefined();
  });

  it("should return undefined for negative index", () => {
    expect(getElement([1, 2, 3], -1)).toBeUndefined();
  });

  it("should handle empty array", () => {
    expect(getElement([], 0)).toBeUndefined();
  });

  it("should throw if array is null", () => {
    expect(() => getElement(null as any, 0)).toThrow();
  });
});
```

Run the tests — most fail because the function does not exist or does not handle these cases.

**Implementation (GREEN):**

```typescript
export function getElement<T>(array: T[] | null, index: number): T | undefined {
  if (!array || index < 0 || index >= array.length) {
    return undefined;
  }
  return array[index];
}
```

All tests pass. The function handles the happy path and all boundary conditions.

**REFACTOR:** Improve error messages, documentation, or type hints if needed. Tests stay green.

**Key insight:** Thinking about edge cases *before* coding leads to robust implementations. The test list becomes your requirements checklist.

---

## TypeScript-Specific Notes

- **Use types in tests to catch errors early:** `describe("myFunc", () => { const result: ReturnType = myFunc(...); })` helps catch signature mismatches.
- **Test generics separately:** If your function is generic, test with multiple types (strings, numbers, custom objects) to ensure type safety.
- **Mock external dependencies:** For database or API calls, use Jest mocks or test doubles. Test logic with real data; mock I/O.
- **Prefer `expect().toThrow()` for error cases:** Do not use `try/catch` in tests. Use `expect(() => myFunc()).toThrow(ErrorType)`.
- **Use `beforeEach` and `afterEach` sparingly:** Keep tests independent. Use setup only when truly shared.

---

## How to Apply

1. **New feature?** Start with the happy path, then add edge cases.
2. **Bug fix?** Write the test that reproduces the bug before fixing.
3. **Refactor?** Pin current behavior with tests, then refactor safely.
4. **Boundary cases?** Think through edge cases, write tests, then implement.

Every test is a specification. The test suite is executable documentation. Write tests first, keep them green, and refactor with confidence.
