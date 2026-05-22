# Boundary triage

Use this guide to decide which replacement strategy is honest for a given `any`.

## Start with these questions

1. Is the value shape already known elsewhere in the repository?
2. Is the value trusted because it was produced by typed code you control?
3. Is the value untrusted because it crosses an external boundary such as JSON, network I/O, storage, or user input?
4. Does the function need to preserve caller-provided structure?
5. Is the current `any` in generated code or third-party declarations?

## Choose the replacement

| Situation | Preferred replacement | Why |
| --- | --- | --- |
| Shared shape already exists | Existing domain type, DTO, schema-derived type, or helper type | Lowest churn and best consistency |
| Caller controls the structure | Generic with constraints | Preserves inference and avoids hard-coding a local copy |
| Small number of known states | Explicit union or discriminated union | Keeps state transitions readable and exhaustive |
| External or untrusted boundary | `unknown` plus a guard or validator | Truthful until runtime checks prove the shape |
| Truly open-ended map | `Record<string, unknown>` with downstream narrowing | Honest only when keys and values are genuinely unconstrained |
| Generated or vendor-owned file | Leave it alone or change the source generator instead | Hand edits are brittle and often out of scope |

## When `unknown` is the right answer

Use `unknown` when the value enters the system from a place you do not fully trust yet:

- `JSON.parse(...)`
- `response.json()`
- webhook payloads
- request bodies and query strings
- storage records whose shape is not enforced at compile time

Then narrow with one of:

- a type guard
- an assertion function
- a schema validator already used by the repository
- an explicit parser that returns a typed result

## When not to reach for `unknown`

Do not replace `any` with `unknown` merely to postpone thinking about the type. If the value is already typed elsewhere in the repository, reuse that type instead.

## When to stop and keep the boundary honest

Leave the boundary permissive when:

- the file is generated
- the declaration belongs to a third-party package
- the runtime data is intentionally unstructured and downstream code already narrows before use

In those cases, document the reason nearby and improve the first consumer boundary instead of forcing a fake precision at the source.
