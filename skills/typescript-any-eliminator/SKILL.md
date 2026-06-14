---
name: typescript-any-eliminator
description: Use when TypeScript source contains explicit `any` in application code, shared helpers, DTOs, or API layers that should be narrowed without changing runtime behavior — or when a reviewer or lint rule flags unsafe `any` usage.
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: typescript
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# TypeScript any eliminator

## Use this skill when

- The user asks to remove, reduce, or replace `any` types in TypeScript code.
- You find explicit `any` in application code, shared helpers, DTOs, or API layers that should be narrowed safely.
- The task is to improve type safety without changing runtime behavior.

## Do not use this skill when

- The task is broad TypeScript type-system work that is not mainly about eliminating `any`.
- The `any` appears in generated code or third-party declarations that should not be hand-edited.
- The repository intentionally documents a permissive boundary and the task is not to tighten it.
- The work primarily requires behavior-changing refactors rather than truthful type replacement.

## Inputs to gather

**Required before editing**

- The targeted `any` sites and the surrounding API surface.
- The repository's typecheck command, such as `tsc --noEmit` or an equivalent project wrapper.
- Existing shared domain types, DTOs, schemas, validators, or helper types that may already model the value.
- Whether each boundary is trusted or untrusted.

**Helpful if present**

- Nearby tests or examples that show the intended shape.
- Whether the touched file is generated or backed by third-party typings.
- Existing lint rules or conventions around `unknown`, guards, and assertions.

## First move

1. Inventory the targeted `any` sites and read the adjacent types before editing.
2. Run the repository's typecheck command if available so you understand the current failure surface.
3. Start with the smallest self-contained `any` site and consult the reference files before inventing new patterns.

## Stop here if the boundary is honest

Do not force a fake precise type when the right answer is to keep the boundary permissive or move the fix closer to the real source.

- keep `unknown` plus a guard when the value is untrusted
- leave generated or vendor-owned files alone
- stop when the change would become a broader TypeScript redesign instead of a truthful `any` replacement
- report the boundary plainly instead of rationalizing a wider type as "good enough"

## Workflow

1. Trace inbound and outbound values so the replacement type matches real usage.
2. Reuse an existing domain type, DTO, schema, validator, or helper type before creating a new local type.
3. Choose the narrowest truthful replacement strategy:
   - an existing shared type
   - a generic with constraints
   - a discriminated union or other explicit union
   - `unknown` plus narrowing or validation at an untrusted boundary
4. If the honest boundary is still permissive, stop at `unknown` plus a guard instead of inventing a fake precise type.
5. Update adjacent call sites only when needed to keep the typed surface coherent.
6. Preserve runtime behavior while tightening the types.
7. Re-run the typecheck and targeted tests after the change.

## Outputs

- `any` usages replaced with precise types (inferred or explicit) in application code, helpers, DTOs, or API layers.
- No runtime behavior change; type errors or tests confirm safety.

## Guardrails

- **Must not** replace `any` with an equally vague type unless that is the honest boundary.
- **Must not** use unsafe casts such as `as unknown as` to silence the compiler.
- **Must not** move `any` elsewhere to make the local error disappear.
- **Should** prefer `unknown` only at untrusted boundaries, then narrow with guards or validators.
- **Should** keep edits small and local unless a larger refactor is required to keep types coherent.
- **May** leave a documented or generated `any` boundary in place when editing it would be unsafe or out of scope.
- **Red flag:** if the first safe fix is a schema, parser, or shared type already used elsewhere, reuse that instead of inventing a new local shape.
- **Handoff trigger:** if the change requires runtime validation work outside this file, route that boundary work to the relevant schema or validator owner.

## Routing boundary

- Route to [`schema-boundary-typing`](../schema-boundary-typing/SKILL.md) when truthful `any` removal depends on runtime validation at an untrusted input boundary.
- Route to [`type-test-authoring`](../type-test-authoring/SKILL.md) after the type surface is truthful and you need compile-time regression coverage for inference or assignability.
- If compiler failures remain after `any` cleanup, route causal error triage to [`tsc-error-triage`](../tsc-error-triage/SKILL.md).

## Validation

- Re-run the repository's typecheck command after the edit.
- Run targeted tests or the nearest equivalent validation command for the touched surface when available.
- Confirm the final type is more precise than `any`, `object`, `Function`, or another unjustified widening.

- Smoke test:
  - should trigger: "Replace any in this API helper with a truthful type."
  - should not trigger: "Add runtime validation for this untrusted JSON input." (→ `schema-boundary-typing`)

## Examples

- `Before`
  ```ts
  export function read(input: any) {
    return input.user.id;
  }
  ```
  `After`
  ```ts
  export function read(input: unknown) {
    if (!isUser(input)) throw new Error("invalid user");
    return input.user.id;
  }
  ```
- `Before`
  ```ts
  type Payload = Record<string, any>;
  ```
  `After`
  ```ts
  type Payload = Record<string, unknown>;
  ```

## Support-file examples

- Reuse and constrained-generic before/after patterns live in `references/replacement-patterns.md`.
- Honest stop cases for generated code, vendor declarations, and intentionally unstructured boundaries live in `references/boundary-triage.md`.

## Reference files

- [`references/replacement-patterns.md`](references/replacement-patterns.md) - before/after replacement patterns, including generic keyed access and `unknown` plus type-guard examples.
- [`references/boundary-triage.md`](references/boundary-triage.md) - how to choose between existing types, unions, `unknown`, guards, and validators.
- [`references/unsafe-shortcuts-to-avoid.md`](references/unsafe-shortcuts-to-avoid.md) - anti-patterns that hide type problems instead of fixing them.
