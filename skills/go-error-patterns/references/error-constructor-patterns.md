# Go Error Constructor Patterns

## Concrete-vs-interface decision table

| Situation | Use concrete type | Use `error` interface |
|-----------|------------------|----------------------|
| Caller needs to inspect fields (`err.Code`, `err.ID`) | ✅ | ❌ |
| Caller only needs to check `err != nil` | ❌ | ✅ |
| Error crosses a package boundary | Prefer interface | — |
| Error is used in a `switch err.(type)` | ✅ | ❌ |
| Lambda handler or HTTP handler writing to `error` return | ❌ | ✅ |

## Closure wrapping pattern

When a function needs to capture context without a new type:

```go
// Instead of:
type ValidationError struct{ Field string; Msg string }
func (e *ValidationError) Error() string { return fmt.Sprintf("%s: %s", e.Field, e.Msg) }

// Use fmt.Errorf with %w when the caller only needs to unwrap:
func validateAge(age int) error {
    if age < 0 {
        return fmt.Errorf("validateAge: %w", ErrNegativeAge)
    }
    return nil
}
```

## Alias removal pattern

Package-local type aliases for `error` create implicit coupling. Remove them:

```go
// Before (alias adds no value):
type AppError = error

func process() AppError { ... }

// After:
func process() error { ... }
```

If a concrete type was behind the alias and callers inspect it, make the concrete type explicit:

```go
type ProcessError struct { Code int }
func (e *ProcessError) Error() string { return fmt.Sprintf("process error %d", e.Code) }

func process() *ProcessError { ... }  // concrete return lets callers access Code
```

## `func(string) error` vs concrete constructors

Avoid passing `func(string) error` as a constructor argument across package boundaries:

```go
// Fragile: caller has to know the string format and reconstruct the type:
func NewHandler(makeErr func(string) error) *Handler { ... }

// Prefer a named factory or error type the caller can import:
type HandlerError struct{ Reason string }
func (e *HandlerError) Error() string { return e.Reason }

func NewHandler(makeErr func(string) *HandlerError) *Handler { ... }
```

This makes the error type inspectable, testable, and avoids the stringly-typed construction anti-pattern.

## Shared-type ownership

When two packages both return the same logical error type:

- Define the type in the lower-dependency package (or a shared `errors` sub-package).
- Never define the same error type in both packages — the compiler will treat them as distinct types even if they have identical fields.
- If the type is only used by one caller, define it in that caller's package.
