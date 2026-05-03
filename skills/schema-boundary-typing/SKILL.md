---
name: schema-boundary-typing
description: Introduce or refine runtime schema validation at untrusted boundaries so static TypeScript types stay truthful.
metadata:
  category: typescript
  audience: general-coding-agent
  maturity: stable
---

# Schema boundary typing

## Use this skill when

- The user wants runtime validation and static typing to agree at an API, storage, or parsing boundary.
- Untrusted input currently flows into application code with weak typing.
- The repository already uses a schema or validator library, or the boundary needs either a simple guard or a reusable schema pattern.

## Do not use this skill when

- The boundary is already validated elsewhere and the task is only to reuse an existing type.
- The task is mainly about internal domain modeling rather than input validation at the edge.

## Inputs to gather

**Required before editing**

- The untrusted boundary, such as request input, JSON parsing, or persisted records.
- Any existing schema or validator library already used by the repository.
- The expected validated shape and the code that consumes it.
- Error-handling expectations when validation fails.

**Helpful if present**

- Existing parsers, decoders, or helper wrappers around the same boundary.
- Tests for invalid payloads.
- Whether the validated type should be derived from the schema or mapped into a separate domain type.

## First move

1. Find the boundary where untrusted data first enters typed code.
2. Reuse the repository's existing schema or validator approach before adding anything new.
3. If no shared schema tool exists, decide whether a simple guard is enough or whether the boundary is important enough to justify a reusable schema pattern.
4. Define the validation close to the boundary, not deep inside consumers.

## Workflow

1. Model the external shape with the repository's existing schema or validator tool.
2. Parse or validate at the first boundary that can reject bad input cleanly.
3. When a simple guard is enough, keep the solution local and do not introduce a full schema dependency.
4. When a reusable schema exists or is justified, derive or expose the validated TypeScript type from it when the library supports that pattern.
5. Keep unvalidated data as `unknown` until it passes validation.
6. Map into a separate domain type only when the repository already distinguishes transport and domain models.
7. Update downstream consumers to rely on the validated type instead of re-checking ad hoc.

## Guardrails

- **Must not** claim a precise type for untrusted input without a matching runtime check.
- **Must not** introduce a new schema library when the repository already has a standard one or when a simple local guard is sufficient.
- **Should** validate once at the edge and pass the validated type inward.
- **Should** preserve existing error mapping and boundary behavior.
- **Should** prefer a simple local guard when the boundary is small, one-off, and unlikely to be shared.
- **May** keep a separate domain model when transport shapes and internal models differ materially.

## Validation

- Run targeted tests for valid and invalid boundary inputs.
- Re-run typecheck after deriving or re-exporting the validated type.
- Confirm consumers no longer rely on unvalidated `unknown` or ad hoc casts.

## Examples

- "Add runtime validation to this API payload and derive the TypeScript type from it."
- "This JSON parsing helper returns weakly typed data. Introduce a schema at the boundary."
- "Use the existing validator library to make this webhook payload type-safe."

## Reference files

- [`references/schema-patterns.md`](references/schema-patterns.md) - patterns for schema-first validation, derivation, and transport-to-domain boundaries.
