# Unsafe shortcuts to avoid

These shortcuts often make the compiler quiet without making the code safer.

## 1. `as unknown as`

Avoid double assertions such as:

```ts
const user = payload as unknown as User;
```

This bypasses the real typing problem. Prefer a guard, assertion function, parser, or schema validator.

## 2. Unjustified widening

Avoid replacing `any` with another vague type just to make the diff look safer:

- `object`
- `Function`
- `Record<string, unknown>` when the shape is actually known
- broad unions that include impossible states

Choose the narrowest truthful type you can justify from the usage.

## 3. Moving `any` somewhere else

Do not fix one local error by pushing `any` into a shared helper, return type, or wrapper. That spreads the unsoundness instead of removing it.

## 4. Trusting unvalidated input

Do not change an external boundary from `any` directly to a precise interface without adding the runtime check that makes the type true.

## 5. Rebuilding types that already exist

If the repository already has a shared type, schema-derived type, or validator-backed type, reuse it. Creating a local near-duplicate usually causes drift.

## 6. Over-expanding the scope

This skill is about truthful `any` elimination, not a broad rewrite of the module's TypeScript design. If the best fix would become a large architectural refactor, make the smallest safe improvement first and explain the larger follow-up separately.
