# Neovim config runtime checks

Use this reference during implementation or validation when you need the concrete runtime seam to inspect first.

## Startup targeting and isolation

| Situation | Preferred check | Why |
| --- | --- | --- |
| Repo checkout or worktree loads the wrong config | Set `XDG_CONFIG_HOME` and `NVIM_APPNAME` explicitly before launching `nvim` | Changing directories alone does not switch configs |
| Validating a live `~/.config/<app>` checkout | Point `XDG_CONFIG_HOME` at the parent `.config` directory | Pointing it at the repo root can create a nested config path and stray lockfile |
| Headless repro for startup, pack, or lockfile behavior | Isolate `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME` together | Partial isolation can still leak synthetic entries into the live lockfile or state |
| Repo-wide `stylua` or `selene` validation in a repo with nested `.worktrees/` | Ignore `.worktrees/**` first | Duplicate checkouts make validator output untrustworthy |

## Plugin-manager and completion checks

| Surface | Check first | Pitfall to avoid |
| --- | --- | --- |
| `vim.pack` migration | Verify the plugin's config side effect, not just package presence | Active packages or commands can exist even when `config` never ran |
| `vim.pack` repo or ref pinning | Use real upstream repos plus a verified branch, tag, ref, or version range | Lazy.nvim shorthands and wildcard versions can install the wrong target |
| `blink.cmp` major pin | Keep `branch = "v1"` or `version = vim.version.range("^1")` and confirm review output matches it | Pack review output can compare against the wrong ref |
| Blink + Copilot completion | Reacquire the active Copilot client for each request | Cached client references can be nil or stale at startup |
| Blink reload from `LspAttach` | Check `blink.cmp.config.sources.providers` before `blink.reload()` | Reloading an unknown provider asserts |
| Decoded JSON inputs | Normalize `vim.NIL` before list operations | `vim.json.decode("null")` does not return plain Lua `nil` |
| Shutdown-time LSP helpers | Preload on the LSP setup path | `LspAttach` is not a reliable teardown hook |

## UI and Neovim API edge cases

| Surface | Check first | Pitfall to avoid |
| --- | --- | --- |
| Dashboard, colorscheme, statusline, or first-screen behavior | Validate in a real TTY session | Headless probes can miss UI state |
| Treesitter query captures on Neovim 0.12+ | Unwrap the capture list before calling node methods | `iter_matches()` capture slots are lists now |
| `vim.ui.progress_status()` in a statusline | Render the returned text directly | Escaping `%` again corrupts the segment |
| Extmark ranges built from `string.find()` | Convert 1-based inclusive positions to 0-based end-exclusive columns | Off-by-one highlights clip brackets or payload edges |
