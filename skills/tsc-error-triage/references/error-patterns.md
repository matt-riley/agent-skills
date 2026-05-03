# Error patterns

Use this guide to recognize common TypeScript compiler error families and pick the right first investigation step.

## Implicit `any` and missing annotations

Typical signals:

- parameters implicitly have `any`
- callback values lose inference after a refactor

Check first:

- whether the defining function lost a generic or contextual type
- whether a wrapper changed the callback signature
- whether a new overload or helper broke inference

Prefer:

- restoring the original source type or generic constraint
- reusing an existing shared function type

## Nullability and optional-property mismatches

Typical signals:

- `undefined` or `null` is no longer assignable
- exact optional property changes trigger assignments to fail

Check first:

- whether the producer or consumer has the truthful shape
- whether a strict flag changed the contract
- whether a union should be modeled explicitly

Prefer:

- narrowing before use
- updating the shared contract instead of sprinkling non-null assertions

## Generic constraint and inference failures

Typical signals:

- `Type X does not satisfy constraint Y`
- an inferred return type widens unexpectedly

Check first:

- the defining generic, not just the usage site
- whether `keyof`, indexed access, or conditional types are missing
- whether a helper should preserve `T` instead of returning a broad fallback

Prefer:

- tightening the generic contract at the source
- adding the smallest useful constraint

## Module resolution and declaration mismatches

Typical signals:

- cannot find module
- duplicate identifier
- import shape changed after config or dependency work

Check first:

- the active `tsconfig` and its `moduleResolution`, `paths`, and `types`
- whether ESM/CJS interop changed the expected import form
- whether generated declarations are stale

Prefer:

- fixing the config or export surface before rewriting imports everywhere

## Literal widening and discriminant loss

Typical signals:

- discriminated unions stop narrowing
- string literals widen to `string`

Check first:

- whether `as const`, `satisfies`, or explicit return types were removed
- whether helper wrappers preserve literal information

Prefer:

- restoring literal-preserving patterns at the source
