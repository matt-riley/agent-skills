---
name: templ-templates
description: "Edit and troubleshoot server-side HTML templates (.templ files for Go's templ framework), including regeneration and handler wiring. Use when changing UI components, layouts, or page templates."
metadata:
  owner: mattriley
  maturity: draft
  kind: task
---

# Templ templates

## Use this skill when

- Editing `.templ` files, regenerating `*_templ.go`, or wiring handlers to generated render functions.
- Debugging a compile error caused by stale template generation.
- Tightening the boundary between handlers (which compute data) and templates (which render it).

## Do not use this skill when

- The work is broader code generation across schema/queries (use `code-generation`).
- The change is pure CSS/asset work with no template edits.

## Inputs to gather

- The path of the `.templ` file being changed and its consumers.
- The repository's regeneration command (`templ generate`, `make templ-generate`, or `make generate`).
- Any typed data the handler currently passes and what needs to change.

## First move

- Locate the target `.templ` file, make the edit, regenerate, then `go build` before running tests.

## Locate templates

Find `.templ` files in your project:

```bash
find . -name "*.templ" -not -path "*/vendor/*"
```

Common locations: `internal/`, `templates/`, `web/`, or alongside handlers.

## Workflow

1. Edit the `.templ` file.
2. Regenerate (produces `*_templ.go`):

```bash
templ generate          # or: make templ-generate / make generate
```

3. Verify:

```bash
go build ./...
make test
```

## Outputs

- Edited `.templ` source files and regenerated `*_templ.go` artifacts produced through the repo's normal templ command.
- Template-to-handler wiring that passes typed data cleanly and preserves `Content-Type: text/html; charset=utf-8` for rendered responses.
- Build and test evidence showing the regenerated templates compile and behave as expected.


## Handler wiring

- Handlers call generated template render functions.
- Set response `Content-Type: text/html; charset=utf-8`.
- Pass data from handler/domain into templates via typed parameters — do not compute data inside templates.

## Guardrails

- Never edit `*_templ.go` files by hand — they are overwritten by `templ generate`.
- Business logic belongs in handlers or the domain layer, not in templates. Templates receive data; they do not compute it.
- Always set `Content-Type: text/html; charset=utf-8` on handler responses rendering templates.

## Common pitfalls

| Symptom                                                 | Fix                                                                   |
| ------------------------------------------------------- | --------------------------------------------------------------------- |
| Compile errors referencing missing `*_templ.go` symbols | Run `templ generate`                                                  |
| Template renders stale output                           | Rebuild — Go does not auto-detect `.templ` changes                    |
| Logic creep in templates                                | Move conditions/computations to the handler; pass pre-computed values |

## Validation

- Run the repository's templ regeneration command after editing `.templ` files.
- Confirm generated Go output changed only as expected and was not hand-edited.
- Run `go build` or the repo's narrow build target, then relevant tests for handlers or pages touched.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
