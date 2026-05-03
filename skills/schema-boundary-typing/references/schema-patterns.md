# Schema patterns

Use these patterns to keep runtime validation and static typing aligned.

## Validate at the first edge

Good boundaries include:

- HTTP request parsing
- webhook ingestion
- `JSON.parse(...)`
- storage reads
- message queue payloads

Validate there, then pass a typed value inward.

## Prefer derivation over duplication

When the validator library supports type inference, prefer deriving the TypeScript type from the schema instead of maintaining two parallel definitions.

Typical examples include repositories using libraries such as:

- Zod
- Valibot
- io-ts
- runtypes

If the repository already standardizes one of these, follow that pattern.

## Decide between a local guard and a schema library

Prefer a simple local guard when:

- the boundary is tiny
- the shape is unlikely to be reused
- the repository does not already standardize a schema library

Prefer an existing schema library when:

- the same shape or validation style appears in multiple places
- the boundary returns field-level validation information
- the repository already derives types from runtime schemas elsewhere

## Keep transport and domain separate when needed

Sometimes the validated input shape is not the final domain model.

In that case:

1. validate the transport shape
2. map it explicitly into the domain model
3. keep the mapping code obvious and testable

## Avoid double validation

Once data has been validated at the boundary, downstream code should depend on the validated type rather than re-parsing or re-asserting the same shape repeatedly.

## Failure behavior matters

Decide up front whether validation should:

- throw
- return a result object
- surface field errors
- map to an HTTP or domain-specific error

Match the repository's existing error-handling pattern instead of inventing a new one.
