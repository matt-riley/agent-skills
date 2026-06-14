---
name: go-build-and-test
description: "Use when Go build, test, toolchain, or CI parity failures surface — including stale GOROOT overrides, govulncheck stdlib patch findings, or TempDir race flakes, but not when the real issue is Go error-pattern design."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# Go build and test

Use this skill when a Go repository is failing to build or test and the next move is to verify toolchain state, reproduce the failure across the affected packages, and separate code defects from environment or CI-parity problems.

## Use this skill when

- `go build`, `go test`, or the repository's Go validation command is failing.
- A Go CI job fails but local commands appear green.
- Toolchain mismatches, stale `GOROOT` or `GOTOOLDIR` overrides, or `GOPATH` confusion may be loading the wrong standard library or tools.
- `govulncheck` reports standard-library findings that may already be fixed in a newer Go patch release.
- Tests appear flaky because of platform assumptions, background writes, or `t.TempDir()` cleanup races.
- A Go test depends on repo fixture files and may be reading local-only or ignored files that CI does not have.

## Do not use this skill when

- The real question is about Go error-constructor signatures, covariance, or concrete-vs-interface error design.
- The cause is completely unknown across the system and you need language-agnostic root-cause investigation first.
- The task is mainly about API-boundary validation or schema typing rather than build, test, or toolchain behavior.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| `go build ./...` or `go test ./...` fails in one or more packages | Yes | - |
| `govulncheck` reports only standard-library findings fixed in a later Go patch | Yes | Stay here and update the pinned Go toolchain before changing workflow policy |
| Linux CI fails with a late `TempDir` cleanup or background-event race | Yes | Stay here and investigate test isolation |
| The problem is `func(string) *DomainError` vs `func(string) error` or error-type design | No | [`go-error-patterns`](../go-error-patterns/SKILL.md) |
| The failure signal is vague and no one knows whether the cause is Go code, config, or infrastructure | No | [`systematic-debugging`](../systematic-debugging/SKILL.md) |

## Inputs to gather

**Required before editing**

- The exact failing command and full output.
- The affected package path or CI job name.
- `go version` plus the active `go env GOROOT GOTOOLDIR GOPATH GOVERSION` output.
- Any exported shell overrides for `GOROOT`, `GOTOOLDIR`, or `GOPATH`.
- Whether the failure reproduces locally, in CI only, or on one operating system.

**Helpful if present**

- The pinned Go version from `go.mod`, CI config, or toolchain setup.
- Recent changes touching Go packages, test fixtures, or workflow pins.
- A list of repo files the failing test reads as samples or fixtures.

**Only investigate if encountered**

- Whether `govulncheck` findings are stdlib-only and already fixed upstream in a later patch release.
- Whether tests using `t.TempDir()` return before background goroutines or finished-event writes complete.
- Whether CLI plumbing really needs a framework; prefer stdlib first and ask before introducing Cobra or similar packages.

## First move

1. Reproduce the failure with the repository's existing Go command, or fall back to `go build ./...` and `go test ./...` scoped to the affected packages instead of a single file.
2. Capture `go version`, `go env GOROOT GOTOOLDIR GOPATH GOVERSION`, and any exported shell overrides before changing code.
3. Decide whether the first branch is toolchain mismatch, CI-parity/test-isolation, or a real package code failure.

## Workflow

1. Re-run the failing Go command at package scope so you are debugging the real build or test surface, not one edited file in isolation.
2. Verify the active toolchain before blaming code: compare `go version`, `go env`, and shell exports, and unset stale `GOROOT` or `GOTOOLDIR` overrides if they point at an older install than the active Go binary.
3. If the failure is from `govulncheck`, check whether every finding is in the standard library and already fixed in a later patch release; if so, update the repo's Go toolchain pin first instead of adding allowlists or changing workflow wiring.
4. If CI fails but local runs pass, compare OS assumptions, filesystem behavior, and event timing. For tests using `t.TempDir()` with invalid roots or background diagnostics, wait for late finished-event delivery before the test returns so Linux cleanup does not race pending writes.
5. Audit fixture and sample-file usage. Tests that read repository files must depend only on tracked files that exist in CI, never local-only dotfiles or ignored paths.
6. Once environment and parity issues are eliminated, apply the smallest code or test fix in the affected package and rerun the same build and test commands to confirm the failure is resolved.

## Outputs

- A confirmed diagnosis of whether the failure was caused by toolchain state, CI/test isolation, tracked-file assumptions, or package code.
- The smallest validated fix, such as an unset override, updated Go pin, isolated test change, or package code change.
- A note when the issue should be rerouted to [`go-error-patterns`](../go-error-patterns/SKILL.md) or [`systematic-debugging`](../systematic-debugging/SKILL.md) instead of continuing here.

## Guardrails

- Do not patch one file and declare success without rerunning the relevant package-level build and test commands.
- Do not add allowlists or workflow exceptions for stdlib-only `govulncheck` findings before checking whether a Go patch update fixes them.
- Do not trust stale `GOROOT` or `GOTOOLDIR` exports just because `go version` looks correct; verify the full environment.
- Do not let tests depend on ignored or untracked repository files.
- Do not edit generated files manually; run the repository's established generation commands instead.
- Prefer the standard library first, but ask before introducing a package like Cobra for CLI plumbing rather than rejecting it automatically.

## Validation

- Re-run the same failing Go command and confirm it now passes for the affected packages.
- Re-check `go version` and `go env` if the fix touched toolchain pins or environment overrides.
- Confirm any fixture files used by tests are tracked in git and present in CI.
- Smoke test:
  - should trigger: "GitHub Actions says `go test ./...` passes locally but fails on Linux with a TempDir cleanup error in our Go package."
  - should not trigger: "Why does `func(string) *ValidationError` not satisfy `func(string) error` in Go?" (→ `go-error-patterns`)

## Examples

- "Our Go CI job started failing after a toolchain update and I need to figure out whether `GOROOT` or `GOTOOLDIR` is stale."
- "`govulncheck` is red on a Dependabot PR, but the report only mentions standard-library packages."
- "This Go test passes on macOS and fails on Linux because a background event writes after `t.TempDir()` cleanup."

## Reference files

- [`references/toolchain-environment-checklist.md`](references/toolchain-environment-checklist.md) — `go env` key matrix, stale-override reset commands, `govulncheck` stdlib-finding triage steps, and CI fixture-file audit
- [`../go-error-patterns/SKILL.md`](../go-error-patterns/SKILL.md) — adjacent Go skill for covariance and error-design questions
- [`../systematic-debugging/SKILL.md`](../systematic-debugging/SKILL.md) — route here when the failure is too ambiguous for a Go-specific triage workflow
