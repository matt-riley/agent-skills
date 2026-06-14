---
name: neovim-plugin-development
description: "Develop, test, and release Neovim Lua plugins. Use when building a new Neovim plugin, adding features to an existing plugin, setting up CI with GitHub Actions, writing plenary tests, generating documentation, or configuring release automation — not for editing user-level Neovim config."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: neovim
  audience: general-coding-agent
  maturity: draft
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

### 1. Plugin structure

The canonical Neovim plugin layout:

```
<plugin>.nvim/
├── lua/
│   └── <plugin>/
│       ├── init.lua          # entry point: setup(), module table
│       ├── config.lua        # default configuration
│       └── <feature>.lua     # one module per feature
├── plugin/
│   └── <plugin>.lua          # autoload: calls require("<plugin>").setup()
├── doc/
│   ├── <plugin>.txt          # vimdoc help file
│   └── <plugin>.html         # rendered HTML (optional)
├── tests/
│   └── <plugin>/
│       └── <feature>_spec.lua
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── test.yml
├── .stylua.toml
├── selene.toml
├── Makefile
└── README.md
```

**Entry point (`lua/<plugin>/init.lua`):**

```lua
local M = {}

M.config = {
    option = true,
}

function M.setup(opts)
    M.config = vim.tbl_deep_extend("force", M.config, opts or {})
    -- Initialization logic here
end

return M
```

**Autoload (`plugin/<plugin>.lua`):**

In Neovim 0.11+ with `vim.pack`, `plugin/` files are not autoloaded. Instead, register user commands and keymaps inside the setup function or use a loader pattern. For `lazy.nvim` users, the plugin spec handles lazy-loading:

```lua
-- lua/<plugin>/init.lua
function M.setup(opts)
    M.config = vim.tbl_deep_extend("force", M.config, opts or {})

    vim.api.nvim_create_user_command("MyCommand", function()
        require("<plugin>.feature").run()
    end, {})

    vim.keymap.set("n", "<leader>mc", function()
        require("<plugin>.feature").run()
    end, { desc = "My command" })
end
```

Prefer `vim.api.nvim_create_user_command` and `vim.keymap.set` over `vim.cmd` strings. Keep each feature in its own module file.

### 2. Configuration defaults

Use `vim.tbl_deep_extend("force", ...)` for merging user config with defaults:

```lua
M.config = {
    enabled = true,
    keymaps = {
        toggle = "<leader>tt",
    },
    highlights = {
        header = "Comment",
    },
}

function M.setup(opts)
    M.config = vim.tbl_deep_extend("force", M.config, opts or {})

    if not M.config.enabled then
        return
    end

    vim.api.nvim_set_hl(0, "MyPluginHeader", M.config.highlights.header)
    -- Continue initialization
end
```

Key rules:
- Provide sensible defaults for every configurable option.
- Check `nil` vs `false` explicitly — `vim.tbl_deep_extend("force")` overwrites with `false` but not `nil`.
- Allow `setup()` to be called multiple times (idempotent initialization).
- Store config on the module table (`M.config`) so other modules can access it.

### 3. Testing with plenary.nvim

```lua
-- tests/<plugin>/feature_spec.lua
local feature = require("<plugin>.feature")

describe("feature", function()
    before_each(function()
        require("<plugin>").setup({ enabled = true })
    end)

    it("returns the expected value", function()
        local result = feature.do_something()
        assert.are.same("expected", result)
    end)

    it("handles nil input gracefully", function()
        local ok, err = pcall(feature.do_something, nil)
        assert.is_false(ok)
    end)
end)
```

Use `make test` to run:

```makefile
test:
	nvim --headless -c "lua require('plenary.test_harness').test_directory('tests/', { minimal_init = 'tests/minimal_init.lua' })"
```

The `minimal_init.lua` bootstraps plenary and the plugin without loading the user's full config:

```lua
-- tests/minimal_init.lua
vim.cmd([[set runtimepath+=.]])
vim.cmd([[set runtimepath+=../plenary.nvim]])
vim.cmd([[set runtimepath+=../nvim-treesitter]])
```

Key rules:
- Use `before_each` to reset plugin state between tests.
- Test behavior, not internal implementation details.
- One `describe` block per module, one `it` per behavior.
- Use `pcall` to test error paths without crashing the test runner.

### 4. CI with GitHub Actions

**Lint workflow (`.github/workflows/lint.yml`):**

```yaml
name: Lint
on: [push, pull_request]
jobs:
  selene:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: NTBBloodbath/selene-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
  stylua:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: JohnnyMorganz/stylua-action@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          version: latest
          args: --check .
```

**Test workflow (`.github/workflows/test.yml`):**

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest]
        nvim-version: [stable, nightly]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: rhysd/action-setup-vim@v1
        with:
          neovim: true
          version: ${{ matrix.nvim-version }}
      - uses: actions/checkout@v4
        with:
          repository: nvim-lua/plenary.nvim
          path: plenary.nvim
      - run: make test
      - uses: peaceiris/actions-gh-pages@v4
        if: github.ref == 'refs/heads/main' && matrix.nvim-version == 'stable'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./doc
```

Key rules:
- Run lint on every push; run tests on PRs and main.
- Test against both `stable` and `nightly` Neovim.
- Publish rendered docs to GitHub Pages on main push.
- Check out `plenary.nvim` as a sibling directory for test dependencies.

### 5. Documentation

Vimdoc files live in `doc/<plugin>.txt`:

```
*<plugin>.txt*   My Neovim Plugin

==============================================================================
CONTENTS                                            *<plugin>-contents*

  1. Introduction ....................... |<plugin>-intro|
  2. Commands ........................... |<plugin>-commands|
  3. Configuration ...................... |<plugin>-config|

==============================================================================
INTRODUCTION                                         *<plugin>-intro*

<plugin>.nvim does something useful.

==============================================================================
COMMANDS                                             *<plugin>-commands*

:MyCommand                                           *:MyCommand*
    Runs the main feature.

==============================================================================
CONFIGURATION                                        *<plugin>-config*

>lua
    require("<plugin>").setup({
        enabled = true,
        keymaps = {
            toggle = "<leader>tt",
        },
    })
<
```

Generate HTML from the vimdoc with a Makefile target:

```makefile
doc:
	nvim --headless -c "lua require('<plugin>.docgen').generate()" -c "qa!"
```

Or use `panvimdoc` or `lemmy-help` for markdown-to-vimdoc conversion.

### 6. Release automation

Use GitHub Releases with semantic version tags. The `nvim-plugin-template` pattern:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - "v*"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

For `lazy.nvim` compatibility, the plugin only needs a GitHub repo with the `lua/` and `doc/` directories at the root — no special packaging required.

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

- [`../neovim-config/SKILL.md`](../neovim-config/SKILL.md) — Adjacent skill for editing user-level Neovim configuration (init.lua, lazy.nvim specs, LSP wiring).
