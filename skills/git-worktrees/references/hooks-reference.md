# Worktrunk hooks reference

## Hook types

| Hook | Timing | Blocks operation? | Purpose |
| --- | --- | --- | --- |
| `pre-switch` | Before switching worktrees | Yes | Gate or prepare before switching |
| `post-switch` | After switching worktrees | No (background) | Notify, update tooling |
| `pre-start` | Before worktree is created | Yes | Validate before creation |
| `post-start` | After worktree is created | No (background) | Install deps, start dev server |
| `pre-commit` | Before commit is created | Yes | Lint, format, test gate |
| `post-commit` | After commit is created | No (background) | Notify, trigger CI |
| `pre-merge` | Before merge executes | Yes | CI gate (tests, lint) |
| `post-merge` | After merge completes | No (background) | Notify, deploy |
| `pre-remove` | Before worktree is removed | Yes | Stop processes, clean up resources |
| `post-remove` | After worktree is removed | No (background) | Notify, release cloud resources |

`pre-*` hooks block the operation and can abort it by exiting non-zero. `post-*` hooks run in the background and their exit code is ignored.

## Configuration forms

### String — single command

```toml
[post-start]
install = "npm ci"
```

### Table — concurrent named commands

All commands in a table block run concurrently.

```toml
[pre-merge]
test = "npm test"
lint = "npm run lint"
typecheck = "tsc --noEmit"
```

### `[[hook]]` pipeline blocks — sequential with concurrency within each block

Use double-bracket `[[hook]]` to chain sequential stages. Within each stage, named keys run concurrently.

```toml
# Stage 1: install deps (must complete before stage 2)
[[post-start]]
deps = "npm ci"

# Stage 2: start dev server (runs after deps)
[[post-start]]
server = "npm run dev -- --port {{ branch | hash_port }}"
```

## Template variables

### Worktree context

| Variable | Description |
| --- | --- |
| `{{ branch }}` | Current branch name |
| `{{ worktree_path }}` | Absolute path to the worktree |
| `{{ worktree_name }}` | Short name of the worktree (last path segment) |
| `{{ commit }}` | Full commit SHA |
| `{{ short_commit }}` | Short commit SHA |
| `{{ upstream }}` | Upstream tracking branch |

### Merge context (available in `pre-merge`, `post-merge`)

| Variable | Description |
| --- | --- |
| `{{ base }}` | Base branch name |
| `{{ base_worktree_path }}` | Absolute path to base branch worktree |
| `{{ target }}` | Target branch being merged into |
| `{{ target_worktree_path }}` | Absolute path to target branch worktree |
| `{{ pr_number }}` | PR number if available |
| `{{ pr_url }}` | PR URL if available |

### Repository context

| Variable | Description |
| --- | --- |
| `{{ repo }}` | Repository name |
| `{{ repo_path }}` | Absolute path to the primary (main) worktree |
| `{{ owner }}` | Repository owner/org |
| `{{ primary_worktree_path }}` | Absolute path to the primary worktree |
| `{{ default_branch }}` | Default branch name (e.g. `main`) |
| `{{ remote }}` | Remote name (e.g. `origin`) |
| `{{ remote_url }}` | Remote URL |

### Hook meta

| Variable | Description |
| --- | --- |
| `{{ cwd }}` | Working directory when hook runs |
| `{{ hook_type }}` | Hook type (e.g. `post-start`) |
| `{{ hook_name }}` | Named key of the command within the hook block |
| `{{ args }}` | Extra args passed to the hook invocation |

### State variables

| Variable | Description |
| --- | --- |
| `{{ vars.<key> }}` | Per-worktree state variable set via `wt config state vars set` |

## Filters

| Filter | Description | Example |
| --- | --- | --- |
| `sanitize` | Replaces non-alphanumeric chars with `-`; safe for directory names | `{{ branch \| sanitize }}` → `feature-auth` |
| `sanitize_db` | Like `sanitize` but lowercased and truncated for DB identifiers | `{{ branch \| sanitize_db }}` → `featureauth` |
| `sanitize_hash` | SHA-256 of the value, hex-encoded | `{{ branch \| sanitize_hash }}` |
| `hash_port` | Stable port in 10000–19999 derived from value | `{{ branch \| hash_port }}` → `14523` |

Filters compose with Tera syntax: `{{ ("db-" ~ branch) | hash_port }}` hashes the concatenated string.

## Pipeline syntax example

```toml
# .config/wt.toml

# Stage 1: install (blocking — stage 2 waits)
[[post-start]]
deps = "npm ci"

# Stage 2: start server (after install)
[[post-start]]
server = "npm run dev -- --port {{ branch | hash_port }}"

# Concurrent CI gate before merge
[[pre-merge]]
test = "npm test"
lint = "npm run lint"

# Clean up on removal
[pre-remove]
stop = "lsof -ti :{{ branch | hash_port }} -sTCP:LISTEN | xargs kill 2>/dev/null || true"
```

## Annotated complete example

```toml
# .config/wt.toml

# Install deps (must complete before dev server)
[[post-start]]
deps = "npm ci"

[[post-start]]
server = "npm run dev -- --port {{ branch | hash_port }}"

# Gate merge on tests
[[pre-merge]]
test = "npm test"
lint = "npm run lint"

# Clean up dev server on worktree removal
[pre-remove]
stop = "lsof -ti :{{ branch | hash_port }} -sTCP:LISTEN | xargs kill 2>/dev/null || true"
```

## Important: `--no-cd` invocations

When Worktrunk creates a worktree via a subprocess — for example, when an agent harness worktree-manager extension calls `wt switch --create --no-cd` — `post-start` hooks run from the **caller's cwd**, not the new worktree directory.

Hooks that do directory-relative work (e.g. `npm ci`) must use `{{ worktree_path }}` explicitly:

```toml
[[post-start]]
deps = "cd {{ worktree_path }} && npm ci"
```

Only omit the explicit `cd` if the hook is already parameterised by template variables that do not rely on cwd, or if you control the invocation and know `--no-cd` is not used.
