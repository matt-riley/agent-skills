# Go Toolchain Environment Checklist

## `go env` key matrix

Run `go env` and verify these key values before diagnosing build or test failures:

| Variable | What to check | Common problem |
|----------|---------------|----------------|
| `GOROOT` | Matches the active `go` binary path | Stale override from a previous toolchain install |
| `GOPATH` | Points to a writable directory | Permissions issue or wrong user home |
| `GOMODCACHE` | Present and writable | Cache corruption — run `go clean -modcache` to reset |
| `GOPROXY` | Expected proxy or `direct` for private modules | Corporate firewall blocking module downloads |
| `GONOSUMCHECK` / `GONOSUMDB` | Set correctly for private module hosts | Checksum failures on internal packages |
| `CGO_ENABLED` | `0` for Lambda/static binaries, `1` if CGo is required | Cross-compile failures when CGo is unexpectedly enabled |
| `GOOS` / `GOARCH` | Match the target platform | Wrong architecture binary silently passes local tests |

## Stale-override reset commands

```sh
# Remove a stale GOROOT override
go env -w GOROOT=""           # or unset GOROOT in shell profile

# Reset module cache
go clean -modcache

# Reset build cache
go clean -cache

# Force re-download of all dependencies
go mod download

# Verify module consistency
go mod verify
```

## `govulncheck` stdlib-finding triage steps

When `govulncheck` reports a finding in the stdlib (`golang.org/x/...` or `std`):

1. Check if the finding is in a package your code actually calls: `govulncheck -show=traces ./...`
2. If the call trace does not include your code paths, the finding is advisory only.
3. If patching is required, update the Go toolchain version: `go get go@<version>` or update the `toolchain` directive in `go.mod`.
4. For Lambda/container deployments, the runtime Go version may differ from the build toolchain — check both.

## CI fixture-file audit

When tests pass locally but fail in CI:

1. Confirm `GOROOT` and `GOPATH` in the CI environment match expected values.
2. Check that `go.sum` is committed and up to date: `go mod tidy && git diff --exit-code go.sum`.
3. Verify test fixtures or embedded files are committed (not in `.gitignore`).
4. Check for `t.TempDir()` races: background goroutines writing after cleanup cause flakes on Linux but not macOS.
5. Check `CGO_ENABLED` — CI often sets `CGO_ENABLED=0` for cross-compile, which can silently break tests that depend on CGo.
