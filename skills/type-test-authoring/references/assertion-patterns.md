# Assertion patterns

Use the repository's existing tool first. These patterns describe what to assert, not which new library to introduce.

## Positive cases

Positive cases prove that:

- inference returns the expected type
- an exported helper accepts valid inputs
- a public type surface remains assignable in the intended direction

Common patterns include:

- `expectTypeOf(...)`
- `expectAssignable<...>(...)`
- helper aliases that compare types at compile time
- simple fixture files that should typecheck cleanly

## Negative cases

Negative cases prove that invalid uses stay invalid.

Common patterns include:

- `@ts-expect-error`
- non-assignability helpers when the repo has them
- fixture files that intentionally fail under a separate command

Prefer `@ts-expect-error` to `@ts-ignore` because it fails when the error disappears unexpectedly.

## Keep the tests focused

A good type test usually protects one of these:

- a generic inference contract
- a narrow assignability rule
- a public exported type alias or helper
- a regression for a previously broken edge case

Avoid giant kitchen-sink fixtures unless the repository already uses that style.
