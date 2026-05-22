# Worktrunk configuration reference

Complete reference for Worktrunk configuration. See `wt config show` for active values and file
locations.

## Configuration files

| File | Location | Scope | Committed? |
|------|----------|-------|------------|
| User config | `~/.config/worktrunk/config.toml` (or `$XDG_CONFIG_HOME`) | All repos | No |
| Project config | `.config/wt.toml` | Single repo | Yes (shared with team) |

Create them with:
```sh
wt config create           # user config with documented examples
wt config create --project # project config
wt config show             # inspect active values and file paths
```

---

## User config (`~/.config/worktrunk/config.toml`)

### Worktree path template

Controls where new worktrees are created. Default: sibling directory.

```toml
# Default — sibling dir (e.g., ~/code/repo.feature-auth):
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"

# Inside repo — recommended for agent harness worktree-manager compatibility:
worktree-path = "{{ repo_path }}/.worktrees/{{ branch | sanitize }}"

# Centralised (e.g., ~/worktrees/myproject/feature-auth):
worktree-path = "~/worktrees/{{ repo }}/{{ branch | sanitize }}"
```

Available template variables: `{{ repo_path }}`, `{{ repo }}`, `{{ owner }}`, `{{ branch }}`,
`{{ branch | sanitize }}`, `{{ branch | sanitize_db }}`.

### LLM commit generation

```toml
[commit.generation]
# Required: external command that reads a prompt from stdin and writes a commit message to stdout
command = "CLAUDECODE= MAX_THINKING_TOKENS=0 claude -p --no-session-persistence --model=haiku --tools='' --disable-slash-commands --setting-sources='' --system-prompt=''"

# Optional: override the default commit prompt template
# template = "..."

# Optional: override the squash prompt template
# squash-template = "..."
```

See [`assets/llm-commits-setup.md`](../assets/llm-commits-setup.md) for config blocks for other
LLM tools.

### List command defaults

```toml
[list]
summary = false    # Enable LLM branch summaries in wt list --full and wt switch picker
full = false       # Always show CI, line diffs, summaries (equivalent to --full)
branches = false   # Include branches without worktrees
remotes = false    # Include remote-only branches
task-timeout-ms = 0  # Kill individual git commands after N ms; 0 = disabled
timeout-ms = 0       # Wall-clock budget for entire collect phase; 0 = disabled
```

### Merge defaults

```toml
[merge]
squash = true   # Squash commits (requires [commit.generation]; use --no-squash if unconfigured)
commit = true   # Commit uncommitted changes before merging
rebase = true   # Rebase onto target before merge
remove = true   # Remove worktree after merge
verify = true   # Run project hooks (pre-merge etc.)
ff = true       # Fast-forward merge (false = create merge commit)
```

### Switch defaults

```toml
[switch]
cd = true   # Change directory after switching

[switch.picker]
# Override git's pager for the interactive picker diff preview:
# pager = "delta --paging=never --width=$COLUMNS"
```

### Step defaults

```toml
[step.copy-ignored]
exclude = []   # Additional gitignored paths to skip when copying between worktrees
               # Built-in excludes: .bzr/, .git/, .hg/, .worktrees/, node_modules/.cache/ etc.
```

### Aliases

User-wide command templates available as `wt <name>`:

```toml
[aliases]
url   = "open http://localhost:{{ branch | hash_port }}"
open  = "code {{ worktree_path }}"
```

### Per-project overrides

User config can override settings per project. Scalar values replace global defaults; hooks and
aliases append to them.

```toml
[projects."github.com/user/repo"]
worktree-path = "{{ repo_path }}/.worktrees/{{ branch | sanitize }}"
list.full = true
merge.squash = false

[projects."github.com/user/repo".aliases]
deploy = "make deploy BRANCH={{ branch }}"
```

---

## Project config (`.config/wt.toml`)

Committed to the repository and shared with the team. Requires approval on first run.

### Hooks

All 8 hook types available. See [`assets/hooks-reference.md`](../assets/hooks-reference.md) for
full syntax and template variables.

```toml
# Common pattern: install deps, start server, gate merge on tests
[[post-start]]
deps = "npm ci"

[[post-start]]
server = "npm run dev -- --port {{ branch | hash_port }}"

[[pre-merge]]
test = "npm test"
lint = "npm run lint"

[pre-remove]
stop = "lsof -ti :{{ branch | hash_port }} -sTCP:LISTEN | xargs kill 2>/dev/null || true"
```

### List URL column

```toml
[list]
url = "http://localhost:{{ branch | hash_port }}"
```

### Project aliases

```toml
[aliases]
test = "cargo test --features {{ vars.features | default('default') }}"
open = "open http://localhost:{{ branch | hash_port }}"
```

---

## Minimal recommended config for agent harness users

```toml
# ~/.config/worktrunk/config.toml

# Keep worktrees inside the repo (matches agent harness worktree-manager convention)
worktree-path = "{{ repo_path }}/.worktrees/{{ branch | sanitize }}"

# LLM commit messages — fast, no session pollution
[commit.generation]
command = "CLAUDECODE= MAX_THINKING_TOKENS=0 claude -p --no-session-persistence --model=haiku --tools='' --disable-slash-commands --setting-sources='' --system-prompt=''"

[list]
summary = true
```
