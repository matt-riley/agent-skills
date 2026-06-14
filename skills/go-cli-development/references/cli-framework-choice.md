# CLI framework choice

## Decision table

| Command count | Config complexity | Recommendation | Rationale |
|---|---|---|---|
| 1-3 commands, simple flags | Low (env vars only) | `flag` (stdlib) | No dependency needed; `flag` handles `--help` and basic parsing |
| 1-3 commands, config files | Medium (YAML/JSON config) | `flag` + viper | Viper handles config; `flag` handles CLI args. Keep them separate. |
| 4+ commands, nested subcommands | Any | cobra | Cobra's command tree, `PreRunE` hooks, and help generation pay off at this scale |
| TUI required | Any | bubbletea | Bubble Tea is the standard Go TUI framework; use it for interactive terminal UIs |
| Existing repo uses cobra | Any | cobra | Follow the existing convention; do not mix frameworks in one CLI |

## stdlib `flag` pattern

```go
// cmd/cli/root.go
package cli

import (
    "flag"
    "fmt"
    "os"
)

func Execute() {
    port := flag.Int("port", 8080, "port to listen on")
    config := flag.String("config", "", "path to config file")
    flag.Parse()

    if *config != "" {
        // load config
    }

    fmt.Printf("Starting on port %d\n", *port)
    os.Exit(0)
}
```

**When to use:** Simple CLIs, proof-of-concept tools, single-purpose commands.

**When not to use:** CLIs with hierarchical subcommands (`app serve`, `app migrate`, `app config set`). Cobra's command tree is worth the dependency at that scale.

## cobra pattern

```go
// cmd/cli/root.go
package cli

import (
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "app",
    Short: "A CLI tool for something useful",
    RunE: func(cmd *cobra.Command, args []string) error {
        return cmd.Help()
    },
}

func Execute() error {
    return rootCmd.Execute()
}

// cmd/cli/serve.go
var serveCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the server",
    RunE: func(cmd *cobra.Command, args []string) error {
        port, _ := cmd.Flags().GetInt("port")
        fmt.Printf("Serving on port %d\n", port)
        return nil
    },
}

func init() {
    serveCmd.Flags().IntP("port", "p", 8080, "port to listen on")
    rootCmd.AddCommand(serveCmd)
}
```

**When to use:** Hierarchical command trees, subcommands with `PreRunE` hooks, CLIs expected to grow in complexity.

## Bubble Tea (TUI) pattern

```go
// cmd/cli/root.go
package cli

import (
    "fmt"
    "os"

    tea "github.com/charmbracelet/bubbletea"
)

type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 {
                m.cursor--
            }
        case "down", "j":
            if m.cursor < len(m.choices)-1 {
                m.cursor++
            }
        case "enter", " ":
            _, ok := m.selected[m.cursor]
            if ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    s := "Select items:\n\n"
    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i {
            cursor = ">"
        }
        checked := " "
        if _, ok := m.selected[i]; ok {
            checked = "x"
        }
        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }
    s += "\nPress q to quit.\n"
    return s
}

func Execute() error {
    p := tea.NewProgram(model{
        choices:  []string{"Option A", "Option B", "Option C"},
        selected: make(map[int]struct{}),
    })
    if _, err := p.Run(); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        return err
    }
    return nil
}
```

**When to use:** Interactive terminal UIs, selection menus, dashboards, live-updating displays.

## Mixing cobra + Bubble Tea

A common pattern: cobra for the command tree, Bubble Tea for interactive subcommands:

```go
var tuiCmd = &cobra.Command{
    Use:   "tui",
    Short: "Launch the interactive TUI",
    RunE: func(cmd *cobra.Command, args []string) error {
        p := tea.NewProgram(initialModel())
        if _, err := p.Run(); err != nil {
            return err
        }
        return nil
    },
}
```

## Project structure conventions

```
cli/
├── main.go              # import cmd/cli, call cli.Execute()
├── cmd/
│   └── cli/
│       ├── root.go      # root command, persistent flags, version
│       ├── serve.go     # 'serve' subcommand
│       ├── config.go    # 'config' subcommand
│       └── tui.go       # 'tui' subcommand (bubbletea)
├── internal/
│   ├── config/
│   │   └── config.go    # viper wiring
│   └── service/
│       └── service.go   # domain logic
└── .goreleaser.yaml
```

Keep `main.go` thin. `cmd/cli/` contains only cobra/flag wiring. `internal/` contains domain logic and config. This separation makes the CLI testable (capture stdout/stderr) and the domain reusable (library, API, other CLIs).
