---
name: neovim-plugin-development
description: "Develop, test, and release Neovim Lua plugins. Use when building a new Neovim plugin, adding features to an existing plugin, setting up CI with GitHub Actions, writing plenary tests, generating documentation, or configuring release automation — not for editing user-level Neovim config."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: neovim
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Neovim plugin development

Use this skill when developing, testing, or releasing a Neovim Lua plugin. It covers plugin structure, Lua module conventions, testing with plenary.nvim, CI with GitHub Actions, documentation with doc/ files, and release automation.

## Use this skill when

- Creating a new Neovim plugin from scratch.
- Adding a feature, command, or keymap to an existing Neovim plugin.
- Writing or debugging tests for a Neovim plugin using plenary.nvim.
- Setting up CI for a Neovim plugin (linting with selene/stylua, testing with plenary, release automation).
- Generating or updating plugin documentation (`doc/<plugin>.txt`).
- Configuring release automation for a Neovim plugin (tags, changelogs, lazy.nvim compatibility).
- Debugging a runtime error in a Neovim plugin (Lua module loading, autocommands, user commands).

## Do not use this skill when

- Editing or debugging a user's Neovim configuration (`init.lua`, `lazy.nvim` plugin specs, LSP wiring) — use [`neovim-config`](../neovim-config/SKILL.md).
- The task is general Lua scripting outside the Neovim plugin API.
- The plugin fails to load but the issue is config-side (wrong checkout, lazy.nvim spec, XDG paths) — use [`neovim-config`](../neovim-config/SKILL.md).
- The main task is writing a README or documentation for a non-Neovim project — use [`doc-coauthoring`](../doc-coauthoring/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| New Neovim plugin, starting from scratch | Yes | — |
| Adding a `:MyCommand` user command to an existing plugin | Yes | — |
| Writing plenary tests for a plugin's Lua module | Yes | — |
| Setting up CI with selene, stylua, and plenary for a plugin repo | Yes | — |
| Fixing `init.lua` config — LSP, keymaps, colorscheme, lazy.nvim specs | No | [`neovim-config`](../neovim-config/SKILL.md) |
| Debugging why `lazy.nvim` loads the wrong plugin version | No | [`neovim-config`](../neovim-config/SKILL.md) |

## Inputs to gather

**Required before editing**

- The plugin name and repository path.
- Whether the plugin uses `lua/<plugin>/init.lua` or `lua/<plugin>.lua` entry point.
- The existing test framework (plenary.nvim) and CI configuration.

**Helpful if present**

- The existing `Makefile` targets for lint, test, and doc generation.
- The plugin's current release process (tags, changelogs, lazy.nvim compatibility).
- Any existing `doc/<plugin>.txt` file.

**Only investigate if encountered**

- Whether the plugin should use `vim.api.nvim_create_autocmd` vs `vim.cmd("autocmd ...")`.
- Whether the plugin needs `vim.treesitter` integration.
- Whether the plugin should register with `lazy.nvim`'s lazy-loading hints.

## First move

1. If the plugin does not exist yet, scaffold the canonical structure: `lua/<name>/init.lua`, `plugin/`, `doc/`, `Makefile`.
2. If the plugin exists, identify the entry point and the specific feature or fix being made.
3. Check whether tests exist and CI is configured before adding new infrastructure.

## Workflow

1. **Scaffold or locate structure** — Use `lua/<plugin>/init.lua` as the entry point, optional `plugin/` autoload, `doc/`, `tests/`, and CI under `.github/workflows/`. Read `references/plugin-structure.md` for the full tree, entry-point and registration patterns.
2. **Configuration defaults** — Merge user opts with `vim.tbl_deep_extend("force", ...)`, keep defaults on `M.config`, make `setup()` idempotent. Details and examples in `references/plugin-structure.md`.
3. **Tests (plenary.nvim)** — Add behavior-focused `*_spec.lua` under `tests/`, run via `make test` with a `minimal_init.lua` that does not load the user's full config. Spec and Makefile patterns in `references/plugin-structure.md`.
4. **CI** — Lint with selene + stylua; test on stable and nightly Neovim with plenary checked out as a sibling. Workflow shapes in `references/plugin-structure.md`.
5. **Documentation** — Maintain `doc/<plugin>.txt` vimdoc; optionally generate HTML or convert from markdown with panvimdoc/lemmy-help. Templates in `references/plugin-structure.md`.
6. **Release** — Tag `v*` releases via GitHub Actions; keep `lua/` and `doc/` at repo root for lazy.nvim compatibility. Release workflow in `references/plugin-structure.md`.

## Outputs

- A Neovim Lua plugin with the canonical `lua/`, `doc/`, and `tests/` structure.
- User commands and keymaps registered via the Neovim API.
- plenary.nvim tests covering each feature module.
- CI workflows for linting (selene + stylua) and testing (stable + nightly).
- Vimdoc help file in `doc/<plugin>.txt`.

## Guardrails

- **Must** use `vim.api.nvim_create_user_command` and `vim.keymap.set` over `vim.cmd` strings.
- **Must** provide sensible defaults for every configurable option.
- **Must** make `setup()` idempotent — safe to call multiple times.
- **Must not** load the user's full Neovim config during tests; use `minimal_init.lua`.
- **Should** keep each feature in its own `lua/<plugin>/<feature>.lua` module.
- **Should** test behavior, not internal implementation details.
- **Should** run CI on both `stable` and `nightly` Neovim.
- **May** use `vim.treesitter` APIs when the plugin works with syntax trees.

## Validation

- Run `make lint` (selene + stylua) and confirm no issues.
- Run `make test` and confirm all plenary tests pass.
- Open Neovim, run `:help <plugin>` and confirm the docs render correctly.
- Open Neovim, run `:lua require("<plugin>").setup()` and confirm no errors.
- Smoke test:
  - should trigger: "Create a new Neovim plugin called `trailblazer.nvim` that adds a `:Trail` command."
  - should trigger: "Add a `highlight` option and test to my Neovim plugin."
  - should trigger: "Set up CI with selene, stylua, and plenary for this Neovim plugin repo."
  - should not trigger: "Fix the LSP configuration in my `init.lua`." (→ `neovim-config`)
  - should not trigger: "Why does lazy.nvim load the wrong version of this plugin?" (→ `neovim-config`)

## Examples

- "Scaffold a new Neovim plugin called `glimpse.nvim` that previews file contents in a floating window."
- "Add a `:Glimpse` command and `<leader>gp` keymap with plenary tests."
- "Set up GitHub Actions CI with selene linting and plenary tests on stable and nightly Neovim."

## Reference files

- [`references/plugin-structure.md`](references/plugin-structure.md) — plugin layout, config defaults, plenary tests, CI workflows, vimdoc, and release automation
- [`../neovim-config/SKILL.md`](../neovim-config/SKILL.md) — Adjacent skill for editing user-level Neovim configuration (init.lua, lazy.nvim specs, LSP wiring).
