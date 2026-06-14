# Goreleaser + Homebrew integration

## Full goreleaser reference

The canonical goreleaser configuration for a Go CLI released via Homebrew:

```yaml
# .goreleaser.yaml
before:
  hooks:
    - go mod tidy

builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - darwin
    goarch:
      - amd64
      - arm64
    ldflags:
      - -s -w
      - -X github.com/owner/repo/cmd/cli.version={{.Version}}
      - -X github.com/owner/repo/cmd/cli.commit={{.Commit}}
      - -X github.com/owner/repo/cmd/cli.date={{.Date}}

brews:
  - repository:
      owner: matt-riley
      name: homebrew-tools
      token: "{{ .Env.HOMEBREW_TAP_GITHUB_TOKEN }}"
    commit_author:
      name: Matt Riley
      email: matt@mattriley.me
    homepage: "https://github.com/<owner>/<repo>"
    description: "<one-line description>"
    license: "GNU GPL v3"
    dependencies:
      - name: go
        type: build

archives:
  - format: tar.gz
    name_template: >-
      {{ .ProjectName }}_{{ title .Os }}_{{ if eq .Arch "amd64" }}x86_64{{ else }}{{ .Arch }}{{ end }}
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: "checksums.txt"

snapshot:
  name_template: "{{ incpatch .Version }}-next"

changelog:
  sort: asc
  filters:
    exclude:
      - "^docs:"
      - "^test:"
      - "^ci:"
      - "^chore:"
```

## Key fields explained

| Field | Purpose | Notes |
|---|---|---|
| `before.hooks` | Run before builds | `go mod tidy` ensures go.sum is consistent |
| `builds[].env.CGO_ENABLED=0` | Static binary | Required for scratch containers and musl-free Linux |
| `builds[].goos` | Target operating systems | Include at least `darwin` and `linux` |
| `builds[].goarch` | Target architectures | Include `amd64` and `arm64` for Apple Silicon |
| `builds[].ldflags` | Linker flags | `-s -w` strips debug info; version vars inject build metadata |
| `brews[].repository` | Homebrew tap | Must be a public GitHub repo |
| `brews[].token` | GitHub PAT | Must have `repo` scope; store as `HOMEBREW_TAP_GITHUB_TOKEN` in CI |
| `archives[].name_template` | Binary naming | Produces clean names like `mytool_Darwin_x86_64.tar.gz` |
| `checksum` | SHA256 checksums | Generated automatically; used by Homebrew formula |

## Homebrew tap setup

1. Create `homebrew-tools` repo on GitHub (public).
2. The first goreleaser run creates the formula at `Formula/<project>.rb`.
3. The formula auto-updates on each release — no manual formula editing needed.

## CI token setup

In `.github/workflows/release.yml`:

```yaml
name: Release
on:
  push:
    tags:
      - "v*"
permissions:
  contents: write
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-go@v5
        with:
          go-version: "1.26"
      - uses: goreleaser/goreleaser-action@v6
        with:
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          HOMEBREW_TAP_GITHUB_TOKEN: ${{ secrets.HOMEBREW_TAP_GITHUB_TOKEN }}
```

Key rules:
- `fetch-depth: 0` is required for goreleaser to compute changelogs.
- `contents: write` permission is needed to create the GitHub Release.
- `HOMEBREW_TAP_GITHUB_TOKEN` must be a classic PAT with `repo` scope (fine-grained tokens cannot push to other repos).

## Local testing

Before pushing a tag:

```bash
# Validate config
goreleaser check

# Build locally without publishing
goreleaser release --snapshot --clean

# Check that the binary builds and --version works
./dist/<name>_darwin_arm64/<name> --version
```

## Release checklist

- [ ] `.goreleaser.yaml` exists and `goreleaser check` passes.
- [ ] Version ldflags are wired in `cmd/cli/root.go`.
- [ ] `HOMEBREW_TAP_GITHUB_TOKEN` is set in repo secrets.
- [ ] CI workflow triggers on `v*` tags.
- [ ] `fetch-depth: 0` is set in the checkout step.
- [ ] Tested with `goreleaser release --snapshot --clean`.
- [ ] `homebrew-tools` repo exists and is public.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `goreleaser: command not found` | goreleaser not installed | `brew install goreleaser` |
| `403 Resource not accessible by integration` | Token lacks repo scope | Use a classic PAT, not a fine-grained token |
| `Formula already exists` | Manual formula conflict | Delete the formula file from homebrew-tools; goreleaser will recreate it |
| `--version prints "dev"` | Ldflags not wired | Check that `-X` paths match the actual package path in `cmd/cli/root.go` |
| `fatal: No names found, cannot describe anything` | No tags in shallow clone | Add `fetch-depth: 0` to the checkout action |
