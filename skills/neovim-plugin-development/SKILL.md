---
name: neovim-plugin-development
description: "Develop, test, and release Neovim Lua plugins. Use when building a new Neovim plugin, adding features to an existing plugin, setting up CI with GitHub Actions, writing plenary tests, generating documentation, or configuring release automation — not for editing user-level Neovim config."
license: GNU GPL v3
metadata:
  version: 1.1.1 # x-release-please-version
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
- The main task is writing a README or documentation for a non-Neovim project — use [`writing-and-editing`](../writing-and-editing/SKILL.md).

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

0. Before making any edit, list every file you plan to touch and cross-check that list against the request's explicit exclusions ("do not touch docs", "do not restructure modules/workflow", "do not vendor dependencies", etc.). Drop any file from the plan that isn't strictly necessary for the literal request.

1. If the plugin does not exist yet, scaffold the canonical structure: `lua/<name>/init.lua`, `plugin/`, `doc/`, `Makefile`.
2. If the plugin exists, identify the entry point and the specific feature or fix being made.
3. Check whether tests exist and CI is configured before adding new infrastructure.

## Workflow

1. **Scaffold or locate structure** — Use `lua/<plugin>/init.lua` as the entry point, optional `plugin/` autoload, `doc/`, `tests/`, and CI under `.github/workflows/`. Read `references/plugin-structure.md` for the full tree, entry-point and registration patterns.
2. **Configuration defaults** — Merge user opts with `vim.tbl_deep_extend("force", ...)`, keep defaults on `M.config`, make `setup()` idempotent. Details and examples in `references/plugin-structure.md`.
3. **Tests (plenary.nvim)** — Add behavior-focused `*_spec.lua` under `tests/`, run via `make test` with a `minimal_init.lua` that does not load the user's full config. Spec and Makefile patterns in `references/plugin-structure.md`.
4. **CI** — Lint with selene + stylua; test on stable and nightly Neovim with plenary checked out via its own `actions/checkout` step to a `../plenary.nvim` path (`repository: nvim-lua/plenary.nvim`, `path: ../plenary.nvim`) — fetched at CI time, never committed. Point `minimal_init.lua`'s runtimepath at that exact path so the workflow's checkout location and the test bootstrap stay in sync. Workflow shapes in `references/plugin-structure.md`.
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
- **Must not** restructure, rewrite, or replace existing modules, CI workflows, or docs that the request did not ask about — add the requested feature and stop.
- **Must** treat any explicit user exclusion (e.g., "do not touch docs", "do not restructure the workflow", "do not vendor dependencies") as an absolute override of this skill's default workflow steps — even when a default step (like updating `doc/<plugin>.txt` after adding a command) would normally apply, skip it if the user excluded it.
- **Must** prefer the smallest possible diff for the literal request: add a new file/module where possible, and touch existing files only for the minimal registration point strictly required (e.g., one `require`/one command registration line) rather than editing unrelated existing modules.
- **Must not** modify plugin source under `lua/<plugin>/` when the request is scoped to CI, linting, or test-bootstrap only — CI-only work is limited to `.github/workflows/`, `Makefile` lint/test targets, and `tests/minimal_init.lua` (or an equivalent test bootstrap file). If the plugin truly lacks a hook needed to test it, surface that as a question instead of silently editing source.
- **Must** check `plenary.nvim` out as a sibling of the plugin repo (`../plenary.nvim`), and point the test bootstrap's runtimepath at the same path, so the checkout and the bootstrap cannot disagree.

- **Must** distinguish "vendoring" (committing a dependency's source into the plugin repo's git history, e.g. a checked-in `plenary.nvim/` directory or submodule) from "fetching at CI time" (an ephemeral `actions/checkout` or `git clone` step inside a workflow run, nothing written to the repo). A CI workflow that clones `plenary.nvim` as a job step is required for tests to run on a fresh runner and is **not** vendoring — do not skip this step when a request says "do not vendor test dependencies".
- **Must** make CI workflows self-sufficient for a fresh runner: explicitly install/checkout every tool the job needs (Neovim stable + nightly via an action like `rhysd/action-setup-vim`, `stylua` via a dedicated action or `cargo install stylua`, and `plenary.nvim` via a second `actions/checkout` step with `repository: nvim-lua/plenary.nvim` and an explicit sibling `path: ../plenary.nvim`). Do not assume any tool or dependency is already present on the runner.
- **Should** keep each feature in its own `lua/<plugin>/<feature>.lua` module.
- **Should** test behavior, not internal implementation details.
- **Should** run CI on both `stable` and `nightly` Neovim.
- **May** use `vim.treesitter` APIs when the plugin works with syntax trees.

## Validation

- Run `make lint` (selene + stylua) and confirm no issues.
- Run `make test` and confirm all plenary tests pass.

- For CI-only requests, verify the workflow itself installs/checks out every runtime dependency it needs (Neovim, stylua, plenary.nvim) as job steps rather than assuming any are pre-installed — a workflow that only passes because the dev machine already has these cached will fail on a fresh GitHub-hosted runner.
- Confirm no dependency (e.g. `plenary.nvim`) is committed into the repository's git history — checking it out as an ephemeral CI step is expected and is not vendoring.
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
