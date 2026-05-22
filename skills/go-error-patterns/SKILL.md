---
name: go-error-patterns
description: "Use when Go error-handling design or function-type mismatches surface — including `func(string) error` vs concrete constructors, package-local type aliases, or concrete-vs-interface error choices, but not when the immediate task is a build or test failure."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# Go error patterns

Use this skill when a Go task is really about error-type design, shared helper signatures, or architecture boundaries around Go services and lambdas, and the next step is to normalize types instead of treating the problem as a generic build failure.

## Use this skill when

- A shared helper expects `func(string) error`, but the available constructor returns a concrete error pointer type.
- Someone assumes Go function types are covariant and expects `func(string) *DomainError` to satisfy `func(string) error`.
- The design uses package-local type aliases for shared helper or DTO types and needs to be normalized.
- A Go signature needs a decision between returning `error` and returning a concrete pointer type.
- A Go architecture question touches lambda or binary granularity for separate product areas or categories.

## Do not use this skill when

- The immediate problem is a failing `go build`, `go test`, `govulncheck`, or CI parity issue.
- The real need is runtime input validation or schema typing at an API boundary.
- The cause is still completely unknown and needs language-agnostic debugging before any design choice is made.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| A helper accepts `func(string) error`, but the package constructor returns `*DomainError` | Yes | - |
| A local alias like `type OptionalString = optional.String` is being proposed as the finished design | Yes | Stay here and use the shared owning type directly |
| The question is whether to keep one lambda per area/category or merge binaries | Yes | Stay here and keep one lambda per area unless a merge is explicitly requested |
| `go test ./...` is failing and the root cause may be toolchain or CI isolation | No | [`go-build-and-test`](../go-build-and-test/SKILL.md) |
| The real problem is request validation or typing untrusted API input | No | [`schema-boundary-typing`](../schema-boundary-typing/SKILL.md) |
| No one yet understands the cause of the error or bug | No | [`systematic-debugging`](../systematic-debugging/SKILL.md) |

## Inputs to gather

**Required before editing**

- The exact helper signature, interface contract, or compiler error.
- The concrete error constructor or type currently being passed around.
- The owning package for any shared type or error definition.
- Whether callers truly need a concrete error type or only the `error` interface.

**Helpful if present**

- Existing patterns for error constructors and wrappers in nearby packages.
- A working example of a shared helper that already accepts `func(string) error`.
- Architecture context about how lambdas or binaries are split across product areas.

**Only investigate if encountered**

- Whether a local type alias exists only as a compatibility shim during a staged migration.
- Whether richer typed methods are genuinely consumed by callers and justify exposing a concrete error type.
- Whether the task should instead route to schema validation because the main concern is boundary typing, not domain-error construction.

## First move

1. Read the exact expected function signature or interface type instead of reasoning from memory.
2. Identify the owning package for the shared type or error so you can remove aliases rather than multiply them.
3. Decide whether the task is a design question here or an immediate build/test failure that belongs in [`go-build-and-test`](../go-build-and-test/SKILL.md).

## Workflow

1. Start from the contract: inspect the helper signature, interface, or shared package API that callers must satisfy.
2. If a helper expects `func(string) error` and the available constructor returns a concrete pointer, wrap the constructor in a local closure that returns `error` so the function type matches exactly.
3. Remove package-local type aliases from the finished design when the shared owning package type can be used directly. Keep aliases only as explicit temporary compatibility shims.
4. Prefer `error` in function signatures when callers only need the interface contract; keep concrete pointer types internal unless consumers truly need concrete-only behavior.
5. For architecture questions about Go deployment units, keep one lambda or binary per area or category unless the user explicitly asks to merge them.
6. After the design change, rerun the relevant Go build or test command for the touched package to confirm the signature and type choices compile cleanly.

## Outputs

- A concrete decision on constructor wrapping, alias removal, interface return types, or lambda granularity.
- The smallest code change needed to make the chosen Go contract truthful and compilable.
- A routing note when the work should move to [`go-build-and-test`](../go-build-and-test/SKILL.md), [`schema-boundary-typing`](../schema-boundary-typing/SKILL.md), or [`systematic-debugging`](../systematic-debugging/SKILL.md).

## Guardrails

- Do not assume Go function types are covariant; match the exact function type the helper expects.
- Do not leave package-local aliases as the final design when a shared type already has an owning package.
- Do not expose concrete pointer error types in signatures unless callers demonstrably need the concrete methods.
- Do not merge separate area lambdas or binaries unless the user explicitly asks for that architecture change.

## Validation

- Re-run the relevant `go build` or `go test` command for the touched package if the design change is implemented in code.
- Confirm the final signature returns the interface type the callers actually need.
- Check that any alias removal now imports the owning package type directly.
- Smoke test:
  - should trigger: "My Go helper takes `func(string) error`, but my constructor returns `*DomainError`; what is the right pattern?"
  - should not trigger: "`go test ./...` only fails in CI after a Go version bump." (→ `go-build-and-test`)

## Examples

- "Why doesn't `func(string) *ValidationError` satisfy `func(string) error` in Go, and what should I pass instead?"
- "We introduced `type OptionalString = optional.String` in a package; should that stay, or should we import the shared type directly?"
- "For this Go rewrite, should investment and protection stay as separate lambdas or be merged into one binary?"

## Reference files

- [`references/error-constructor-patterns.md`](references/error-constructor-patterns.md) — Go code examples for closure wrapping, alias removal, and the concrete-vs-interface decision table
- [`../../instructions/go.instructions.md`](../../instructions/go.instructions.md) — source rules for Go error-pattern decisions, shared-type ownership, and lambda granularity
- [`../go-build-and-test/SKILL.md`](../go-build-and-test/SKILL.md) — adjacent Go skill for build, test, toolchain, and CI parity failures
- [`../schema-boundary-typing/SKILL.md`](../schema-boundary-typing/SKILL.md) — route here when the real task is boundary validation rather than Go error design
- [`../systematic-debugging/SKILL.md`](../systematic-debugging/SKILL.md) — route here when the root cause is still unknown
