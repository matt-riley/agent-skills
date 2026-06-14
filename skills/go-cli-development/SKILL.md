---
name: go-cli-development
description: "Develop, structure, and release Go CLI tools. Use when building a new Go CLI, adding subcommands or flags, wiring config, formatting output, setting up goreleaser + Homebrew distribution, or debugging CLI-specific behavior — not for build failures or test debugging."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: go
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Go CLI development

Use this skill when building, extending, or releasing a Go command-line tool. It covers the full lifecycle: project structure, subcommand and flag patterns, config wiring, output presentation, release packaging, and Homebrew distribution.

## Use this skill when

- Creating a new Go CLI tool from scratch.
- Adding subcommands, flags, or argument handling to an existing Go CLI.
- Wiring configuration (viper, env vars, config files) into a CLI.
- Formatting CLI output: tables, colors, progress bars, or structured text.
- Building a TUI with Bubble Tea or similar Charmbracelet libraries.
- Setting up or debugging a goreleaser configuration for multi-platform release.
- Adding Homebrew formula distribution to a Go CLI release pipeline.
- Injecting version info at build time with `-ldflags`.
- Handling signals, graceful shutdown, or terminal state cleanup in a CLI.

## Do not use this skill when

- The Go CLI fails to build or test and the root cause is toolchain, GOROOT, or CI-parity — use [`go-build-and-test`](../go-build-and-test/SKILL.md).
- Individual tests in the CLI package are failing on logic or coverage — use [`testing-workflows`](../testing-workflows/SKILL.md).
- The task is only about error-handling design or `func(string) error` covariance — use [`go-error-patterns`](../go-error-patterns/SKILL.md).
- The CLI does not exist yet and the user only wants a discovery pass — use [`context-map`](../context-map/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| New Go CLI tool, starting from scratch | Yes | — |
| Adding a `serve` subcommand with flags to an existing Go CLI | Yes | — |
| Wiring viper config + env vars into a CLI's command tree | Yes | — |
| Setting up goreleaser with Homebrew tap for a Go CLI | Yes | — |
| `go build` fails on this CLI and the error is a toolchain mismatch | No | [`go-build-and-test`](../go-build-and-test/SKILL.md) |
| A test in `cmd/` is failing on wrong output, not on build | No | [`testing-workflows`](../testing-workflows/SKILL.md) |
| Designing Go error types for CLI error messages | No | [`go-error-patterns`](../go-error-patterns/SKILL.md) |

## Inputs to gather

**Required before editing**

- The CLI name, module path, and intended command tree (or a request that implies them).
- Whether the repo already has a CLI framework (cobra) or uses stdlib `flag`.
- Whether goreleaser and Homebrew tap distribution are expected.

**Helpful if present**

- The existing `main.go`, `cmd/` layout, and any `.goreleaser.yaml`.
- The target platforms (darwin, linux, windows) for release.
- Any existing Homebrew tap repo or formula pattern.

**Only investigate if encountered**

- Whether cobra adds value over stdlib `flag` for the command tree size.
- Whether Bubble Tea or other Charmbracelet libraries should be introduced for TUI needs.
- Whether `ldflags` version injection is already wired or needs to be added.

## First move

1. If the CLI does not exist yet, scaffold the canonical structure: `main.go` → `cmd/<name>/root.go` with cobra or stdlib `flag`.
2. If the CLI exists, identify the command tree and the specific subcommand, flag, or config surface being changed.
3. Check whether goreleaser or Homebrew config already exists before adding release plumbing.

## Workflow

### 1. Project structure

Use the canonical Go CLI layout:

```
<cli-name>/
├── main.go              # entrypoint: calls cmd.Execute()
├── cmd/
│   └── <name>/
│       ├── root.go      # root command, persistent flags, version
│       └── <subcmd>.go  # one file per subcommand
├── internal/
│   ├── config/          # viper + env wiring
│   └── <domain>/        # domain logic, kept separate from cmd
└── .goreleaser.yaml     # release config (when ready)
```

`main.go` should be thin — import `cmd`, call `Execute()`:

```go
package main

import "github.com/owner/repo/cmd/cli"

func main() {
    cli.Execute()
}
```

Prefer stdlib `flag` for CLIs with 1-3 commands and simple flags. Introduce cobra only when the command tree is deep, subcommands need `PreRunE` hooks, or the existing repo convention already uses it. Read [`references/cli-framework-choice.md`](references/cli-framework-choice.md) for the decision table.

### 2. Version injection

Inject version, commit, and date at build time with `-ldflags`:

```go
// cmd/cli/root.go
var (
    version = "dev"
    commit  = "none"
    date    = "unknown"
)

func init() {
    rootCmd.Version = fmt.Sprintf("%s (commit %s, built %s)", version, commit, date)
}
```

In `.goreleaser.yaml`, wire the ldflags:

```yaml
builds:
  - ldflags:
      - -s -w
      - -X github.com/owner/repo/cmd/cli.version={{.Version}}
      - -X github.com/owner/repo/cmd/cli.commit={{.Commit}}
      - -X github.com/owner/repo/cmd/cli.date={{.Date}}
```

For local builds without goreleaser, use a `Makefile` target or `go build -ldflags "-X ..."`.

### 3. Config wiring

Wire config with viper when the CLI reads config files, env vars, or both:

```go
// internal/config/config.go
func Init() (*Config, error) {
    v := viper.New()
    v.SetConfigName("config")
    v.SetConfigType("yaml")
    v.AddConfigPath("$HOME/.config/<cli>/")
    v.AddConfigPath(".")
    v.AutomaticEnv()
    v.SetEnvPrefix("CLI")
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    if err := v.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return nil, err
        }
    }

    var cfg Config
    if err := v.Unmarshal(&cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

Prefer the `~/.config/<cli>/` convention for config files and `<CLI>_` prefix for env vars. Do not hard-code paths to the user's home directory; use `os.UserHomeDir()` or viper's `$HOME` expansion.

### 4. Output formatting

Keep output formatting library choices minimal and consistent:

- **Tables**: `github.com/jedib0t/go-pretty/v6/table` or `github.com/olekukoneko/tablewriter`
- **Colors**: `github.com/fatih/color` for simple colored output; avoid color when stdout is not a terminal (check `os.Stdout` with `term.IsTerminal`)
- **Progress bars**: `github.com/schollz/progressbar/v3` for file downloads or long operations
- **Structured output**: add a `--json` / `--output json` flag for machine-readable output; use `encoding/json` with a dedicated output struct

Do not import a large framework just for color. Prefer the smallest dependency that solves the immediate formatting need.

### 5. Signal handling and graceful shutdown

Wire OS signal handling for any CLI that runs a long-lived process:

```go
func run(ctx context.Context) error {
    ctx, cancel := signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)
    defer cancel()
    // ... long-running work, checking ctx.Err()
    return nil
}
```

For Bubble Tea TUIs, the framework handles signals; do not add a second signal handler.

### 6. Goreleaser and Homebrew distribution

The canonical goreleaser config for a Go CLI distributed via Homebrew:

```yaml
before:
  hooks:
    - go mod tidy
builds:
  - env:
      - CGO_ENABLED=0
    goos: [linux, darwin]
    goarch: [amd64, arm64]
    ldflags:
      - -s -w
      - -X github.com/owner/repo/cmd/cli.version={{.Version}}
      - -X github.com/owner/repo/cmd/cli.commit={{.Commit}}
      - -X github.com/owner/repo/cmd/cli.date={{.Date}}
brews:
  - tap:
      owner: matt-riley
      name: homebrew-tools
      token: "{{ .Env.HOMEBREW_TAP_GITHUB_TOKEN }}"
    commit_author:
      name: Matt Riley
      email: matt@mattriley.me
    homepage: https://github.com/<owner>/<repo>
    description: "<short description>"
archives:
  - format: tar.gz
    name_template: >-
      {{ .ProjectName }}_{{ title .Os }}_{{ if eq .Arch "amd64" }}x86_64{{ else }}{{ .Arch }}{{ end }}
    format_overrides:
      - goos: windows
        format: zip
checksum:
  name_template: "checksums.txt"
changelog:
  sort: asc
  filters:
    exclude: ["^docs:", "^test:"]
```

Key rules:
- Set `CGO_ENABLED=0` for static binaries that run on scratch containers and minimal Linux.
- The Homebrew tap token must be available as `HOMEBREW_TAP_GITHUB_TOKEN` in CI.
- Include at least `darwin` and `linux` in `goos`; add `windows` only when explicitly requested.
- The `archives.name_template` should produce clean filenames without Go's arch convention.
- Read [`references/goreleaser-homebrew.md`](references/goreleaser-homebrew.md) for full goreleaser + Homebrew integration details.

### 7. Testing CLI behavior

Test CLI commands as integration tests, not unit tests of cobra setup:

```go
func TestRootCmd_HelpFlag(t *testing.T) {
    cmd := NewRootCmd()
    cmd.SetArgs([]string{"--help"})
    var buf bytes.Buffer
    cmd.SetOut(&buf)
    err := cmd.Execute()
    require.NoError(t, err)
    assert.Contains(t, buf.String(), "Usage:")
}
```

Capture stdout/stderr with `cmd.SetOut` and `cmd.SetErr`. Test one behavior per case: help output, flag parsing, error messages on invalid input. Do not test cobra wiring itself; test the observable CLI behavior.

## Outputs

- A Go CLI project with the canonical `main.go` → `cmd/` → `internal/` structure.
- Subcommand and flag wiring that follows the repo's chosen framework convention.
- Version injection via ldflags and a working goreleaser configuration.
- Homebrew formula distribution wired when the CLI is release-ready.
- CLI-specific tests that assert observable behavior, not framework wiring.

## Guardrails

- **Must** start with stdlib `flag` and ask before introducing cobra.
- **Must** use `CGO_ENABLED=0` for static binaries intended for distribution.
- **Must not** hard-code `$HOME` paths; use `os.UserHomeDir()` or viper path expansion.
- **Must not** import a large framework just for color output.
- **Should** provide `--json` output for scripting when the CLI produces structured data.
- **Should** wire signal handling for any long-running process.
- **Should** keep `main.go` thin — import `cmd`, call `Execute()`, return.
- **May** introduce Bubble Tea or Charmbracelet libraries when a TUI is explicitly requested.

## Validation

- Run `go build ./...` from the repo root and confirm the CLI binary builds without errors.
- Run `go test ./...` and confirm CLI integration tests pass.
- If goreleaser is wired, run `goreleaser check` to validate the config (skip `goreleaser release --snapshot` unless asked).
- Confirm version injection works: `<binary> --version` prints the expected version, commit, and date.
- Smoke test:
  - should trigger: "Create a new Go CLI called `tunnel` that takes a `--port` flag and prints a connection message."
  - should trigger: "Add a `list` subcommand to my existing Go CLI with table output and a `--format json` flag."
  - should trigger: "Wire goreleaser and Homebrew distribution for this Go CLI tool."
  - should not trigger: "`go build` fails on this CLI with a GOROOT error." (→ `go-build-and-test`)
  - should not trigger: "The table output test in `cmd/list_test.go` is failing." (→ `testing-workflows`)

## Examples

- "Scaffold a new Go CLI called `gh-myrepo` with cobra, a `list` subcommand that prints a table, and version injection."
- "Add a `--config` flag that reads a YAML file from `~/.config/<cli>/` using viper."
- "Set up goreleaser for my Go CLI to release darwin/amd64, darwin/arm64, and linux/amd64 binaries with a Homebrew formula."

## Reference files

- [`references/cli-framework-choice.md`](references/cli-framework-choice.md) — Decision table for stdlib `flag` vs cobra, plus project structure conventions.
- [`references/goreleaser-homebrew.md`](references/goreleaser-homebrew.md) — Full goreleaser config reference, Homebrew tap setup, CI token wiring, and release checklist.
- [`../goreleaser-release-pipeline/SKILL.md`](../goreleaser-release-pipeline/SKILL.md) — Adjacent skill for goreleaser-specific debugging when the release pipeline itself fails.
- [`../go-build-and-test/SKILL.md`](../go-build-and-test/SKILL.md) — Route here when the CLI fails to build due to toolchain or CI-parity issues.
