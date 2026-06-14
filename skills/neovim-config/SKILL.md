---
name: neovim-config
description: "Use when editing, debugging, or validating a Neovim Lua configuration — including plugin management (vim.pack, lazy.nvim), LSP/completion wiring, treesitter, statusline, or startup behavior."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Neovim config

Use this skill when the task targets a Neovim Lua configuration and the work depends on loading the right checkout, applying plugin-specific wiring truthfully, and validating behavior with the right startup mode.

## Use this skill when

- The change touches a Neovim Lua config under `init.lua`, `lua/`, `plugin/`, `after/`, or `ftplugin/`.
- You are editing or validating plugin management with `vim.pack`, `lazy.nvim`, lockfiles, pinned refs, or plugin bootstrap behavior.
- The task involves keymaps, LSP/completion wiring, Blink, Copilot, treesitter, statusline, dashboard, or startup-time behavior.
- A repo checkout or worktree is loading the wrong config, the wrong lockfile, or the wrong plugin state.
- You need Neovim-specific validation rules such as real-TTY startup checks or isolated `XDG_*` repros.

## Do not use this skill when

- The bug is not specific to a Neovim Lua configuration and needs generic root-cause investigation first. Use [`systematic-debugging`](../systematic-debugging/SKILL.md).
- The task is general Lua application code outside a Neovim config surface. Use the repo's normal language workflow or [`systematic-debugging`](../systematic-debugging/SKILL.md).
- The main goal is writing or restructuring documentation about the config rather than changing or validating behavior. Use [`doc-coauthoring`](../doc-coauthoring/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Update plugin specs, keymaps, LSP/completion setup, treesitter, statusline, or startup wiring in a Neovim Lua config | Yes | - |
| Validate a worktree checkout, `vim.pack` migration, or startup regression that depends on loading the right Neovim config | Yes | - |
| Generic debugging for an app or runtime bug where Neovim config is only incidental | No | [`systematic-debugging`](../systematic-debugging/SKILL.md) |
| Documentation, onboarding, or explanation work for the config | No | [`doc-coauthoring`](../doc-coauthoring/SKILL.md) |

## Inputs to gather

**Required before editing**

- The real config root and app name (`init.lua`, namespace path, `NVIM_APPNAME`, lockfile location).
- The plugin manager in play (`vim.pack`, `lazy.nvim`, or another existing loader) and the exact plugin or runtime seam being changed.
- The validation path that matches the symptom: real TTY startup, headless repro, repo formatter/linter, or targeted runtime check.

**Helpful if present**

- The current pinned repo, branch, tag, or version range for affected plugins.
- The exact startup error, `:messages` output, pack review result, or statusline/treesitter symptom.
- Whether the repo contains nested `.worktrees/` that need to be excluded from repo-wide validators.

**Only investigate if encountered**

- Blink provider registration state, Copilot client lookup behavior, or `LspAttach` reload paths.
- `vim.NIL` payloads from decoded JSON.
- Extmark index math or Neovim 0.12 capture-list behavior in treesitter queries.

## First move

1. Identify the config surface, plugin manager, and exact runtime seam the task touches.
2. Point `nvim` at the target checkout with `XDG_CONFIG_HOME` and `NVIM_APPNAME` before trusting any repro or smoke test.
3. Choose the smallest truthful validation mode for the symptom: real TTY for UI-sensitive startup, isolated headless repro for scriptable checks, then repo validators only after path scoping is correct.

## Workflow

1. Confirm the real config root before editing.
   - Do not rely on `cd` alone; the command must target the intended checkout.
   - When validating a live `~/.config/<app>` checkout, set `XDG_CONFIG_HOME` to the parent `.config` directory, not the repo root itself.
   - Keep the smallest truthful implementation scope; once the wiring is clear, stop extra probing and ship.
2. Isolate runtime state before reproducing pack or startup behavior.
   - For isolated headless repros, isolate `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME` together so synthetic plugins or lockfile entries do not leak into the live config.
   - When running repo-wide validators, make them ignore nested `.worktrees/**` so duplicate checkouts do not poison `selene .` or `stylua --check .`.
3. Reproduce with the right validation mode for the symptom.
   - Use a real TTY for UI-sensitive startup issues such as dashboards, colorschemes, statusline rendering, or first-screen behavior; `nvim --headless` can miss those states.
   - For `vim.pack` migrations, verify config side effects directly; an installed package or exposed command is not enough to prove the plugin `config` callback ran.
4. Implement plugin wiring where the plugin lives, not in a central override maze.
   - Prefer plugin-local `main = ...` annotations or explicit `config` functions over a shared loader override table.
   - If a plugin keeps causing cascading churn and the user says it is not worth it, remove it cleanly instead of stacking shims.
   - Preserve explicit `false` values in Lua merges by checking `~= nil`; do not use `and/or` ternaries for booleans.
5. Apply plugin-specific rules before assuming the runtime is wrong.
   - `vim.pack`: use real upstream repos and verified branches, tags, refs, or version ranges rather than lazy.nvim shorthands; verify the reviewed target ref before trusting pack output.
   - `blink.cmp`: pin to `branch = "v1"` or `version = vim.version.range("^1")`, and confirm review or update output is actually comparing against that ref.
   - Blink + Copilot: reacquire the current attached Copilot client per request; do not cache the client reference.
   - Blink provider reloads from `LspAttach`: check `blink.cmp.config.sources.providers` first because `blink.reload()` asserts on unknown providers.
   - JSON payloads: normalize `vim.NIL` after `vim.json.decode()` before list operations.
   - Shutdown-time LSP behavior: preload runtime helpers on the LSP setup path instead of assuming `LspAttach` will run at teardown.
6. Handle Neovim API edge cases with the runtime's actual index and capture semantics.
   - On Neovim 0.12+, `iter_matches()` capture slots are lists; unwrap the capture before calling node methods like `:range()`.
   - `vim.ui.progress_status()` is already statusline-formatted text; do not double-escape its `%` markers.
   - Extmark columns are 0-based and end-exclusive while `string.find()` positions are 1-based and inclusive; adjust bracketed status or progress segment ranges accordingly.
7. Re-run the smallest meaningful validation for the touched surface.
   - Startup or UI change: open the target checkout in a real TTY and confirm the visual or interactive behavior.
   - Headless or scripted change: rerun the repo's existing formatter, linter, or startup smoke checks against the targeted config path.
   - `vim.pack`, Blink, or Copilot change: confirm the pinned ref, config callback side effect, and runtime attach or reload behavior that actually motivated the edit.

## Outputs

- A Neovim config change or validation plan that targets the correct checkout and runtime paths.
- A plugin-specific fix or diagnosis that respects `vim.pack`, Blink, Copilot, treesitter, statusline, or shutdown-time LSP constraints.
- A validation result that proves the touched behavior on the right startup mode instead of only on a misleading headless or wrong-checkout path.

## Guardrails

- **Must not** override user keybindings or plugin settings without noting the change.
- **Should** prefer lazy-loaded plugins when startup performance matters.
- **Should** verify plugin manager bootstrap before assuming plugin APIs are available.
- **Should** use the existing plugin manager (lazy.nvim, packer, etc.) rather than introducing a second one.
- **May** suggest alternative patterns but defer to the user's existing config conventions.

## Validation

- Checklist:
  - confirm `nvim` is loading the intended checkout via `XDG_CONFIG_HOME` and `NVIM_APPNAME`
  - use a real TTY for UI-sensitive startup or statusline or dashboard validation
  - ignore nested `.worktrees/**` before trusting repo-wide `stylua` or `selene` results
  - for `vim.pack`, verify the config callback side effect or pinned ref behavior, not just package presence
  - for Blink, Copilot, or LSP changes, verify provider registration, client lookup, or shutdown-time behavior on the real code path you changed
  - for treesitter or statusline changes, check capture unwrapping or index conversions against the rendered behavior
- Smoke test:
  - should trigger: "Fix this Neovim worktree so `vim.pack` loads `blink.cmp` v1 and Copilot completions work again."
  - should not trigger: "Find the root cause of this failing Lua service test." (→ `systematic-debugging`)

## Examples

- "Validate why this Neovim checkout still opens the live config instead of the worktree when I launch `nvim`."
- "Update my statusline Lua so `vim.ui.progress_status()` renders correctly and the extmark highlight range stops clipping the brackets."
- "Migrate this plugin spec from `lazy.nvim` to `vim.pack`, pin the right upstream ref, and prove the config callback actually runs."

## Reference files

- [`references/runtime-checks.md`](references/runtime-checks.md) - compact lookup table for config-targeting, `vim.pack`, Blink, Copilot, treesitter, and statusline validation checks.
