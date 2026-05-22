---
name: type-test-authoring
description: "Write compile-time type tests that protect public TypeScript APIs, inference behavior, and negative cases."
metadata:
  category: typescript
  audience: general-coding-agent
  maturity: stable
---

# Type test authoring

## Use this skill when

- The user wants to protect generic helpers, utility types, or public APIs with compile-time tests.
- A type inference bug or regression should be locked down with a dedicated test.
- The repository already uses a type-test approach such as `tsd`, `dtslint`, `expectTypeOf`, or `@ts-expect-error` fixtures.
- The type contract is important enough to justify introducing the repository's first small compile-time type-test pattern.

## Do not use this skill when

- The task is only about runtime behavior and not static type contracts.
- The repository has no meaningful type-test workflow and a normal unit test is more appropriate.
- The change only needs a quick local code sample instead of a maintained regression test.

## Inputs to gather

**Required before editing**

- The public type surface or helper that needs protection.
- The repository's existing type-test tool or convention, if any.
- The positive and negative cases that should stay stable.
- The command used to run the relevant type tests or typecheck fixtures.

**Helpful if present**

- Existing helper assertions such as `expectTypeOf`, `expectAssignable`, or `@ts-expect-error` fixtures.
- Prior bugs that should become regression cases.
- Runtime tests that already cover the same API behavior.

## First move

1. Read the nearest existing type test and match its tool and style.
2. If no type tests exist yet, inspect the repository for an already-installed type-test tool and otherwise start with the lightest existing TypeScript fixture pattern, such as `@ts-expect-error` in dedicated typecheck files.
3. Identify the exact inference or assignability contract that needs protection.
4. Add one positive and one negative case before broadening coverage.

## Bootstrap without an existing pattern

If the repository has no established type-test convention:

1. Prefer a lightweight TypeScript fixture that the existing toolchain already understands.
2. Use a dedicated `*.test-d.ts` or `*.type-test.ts` file when the contract needs to stay out of runtime code.
3. Use inline `@ts-expect-error` only when the regression is tiny and close to the API that owns it.
4. Keep the first pass small enough to validate with the repo's normal `tsc --noEmit` or equivalent.

## Inline vs fixture-file tradeoffs

- Inline assertions keep the example next to the code they protect and are best for one or two local cases.
- Fixture files scale better when you need multiple positive and negative cases or want to keep runtime sources clean.
- Fixture files are easier to expand later, but inline assertions are faster when the repo only needs a single regression lock.
- If the contract is part of a public surface, prefer the style that makes the expected call shape easiest to read at a glance.

## Workflow

1. Encode the expected inference or assignability behavior using the repository's current type-test tool, or the lightest new pattern justified by the repository's existing tooling.
2. Add negative cases that fail for the right reason, such as `@ts-expect-error` or explicit non-assignability checks.
3. Keep runtime logic minimal so the test stays about types, not behavior.
4. Prefer small focused assertions over giant fixture files.
5. Add a regression case for the bug or edge case that motivated the work.
6. Run the repository's type-test or fixture command and confirm both positive and negative cases behave as intended.

## Guardrails

- **Must not** use type tests as a substitute for runtime tests when runtime behavior changed.
- **Must not** add `@ts-ignore` where a negative assertion should use `@ts-expect-error` or an existing helper.
- **Should** match the repository's current type-test tool instead of introducing a new one casually.
- **Should** keep tests focused on exported or intentionally shared types.
- **May** use compact helper aliases when the repository already has them.
- **Should** stop at compile-time coverage when the bug is purely static; if the behavior depends on runtime data, use runtime tests instead.

## Routing boundary

- Use this skill after source typing work (for example via [`typescript-any-eliminator`](../typescript-any-eliminator/SKILL.md) or [`schema-boundary-typing`](../schema-boundary-typing/SKILL.md)) has made the target type surface truthful.
- Keep this skill focused on compile-time guarantees only; route runtime API behavior tests to a runtime test skill.

## Red flags

- The contract only fails when the code executes, not when the type system checks it.
- The first fixture would need a brand-new test harness instead of the existing TypeScript workflow.
- The type assertion depends on generated data, environment state, or file system layout.
- The test would be clearer as a small runtime example with a separate typecheck fixture for just the static boundary.

## Validation

- Run the existing type-test command or the nearest equivalent fixture-based typecheck.
- Confirm negative cases fail for the intended reason rather than from unrelated compiler noise.
- Re-run adjacent runtime tests when the same API surface also changed at runtime.
- Use [`references/type-test-scenarios.md`](references/type-test-scenarios.md) to choose inline assertions versus fixture/bootstrap patterns, and update it when the local type-test shape changes.

- Smoke test:
  - should trigger: "Add a compile-time test that locks parseUser inference."
  - should not trigger: "Add a runtime API test for parseUser invalid input." (→ `test-driven-development`)

## Examples

- `expectTypeOf`
  ```ts
  expectTypeOf(parseUser({ id: 1 })).toEqualTypeOf<User>();
  // @ts-expect-error wrong shape
  parseUser({ id: "1" });
  ```
- `@ts-expect-error` fixture
  ```ts
  acceptsString("ok");
  // @ts-expect-error numbers are rejected
  acceptsString(123);
  ```

## Reference files

- [`references/assertion-patterns.md`](references/assertion-patterns.md) - common positive and negative assertion patterns for compile-time type testing.
- [`references/type-test-scenarios.md`](references/type-test-scenarios.md) - scenario checklist for choosing the lightest durable type-test structure.
