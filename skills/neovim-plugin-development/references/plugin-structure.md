# Neovim plugin structure, tests, CI, and docs

Lookup detail for `neovim-plugin-development`. Keep the main skill focused on activation and workflow; use this file when scaffolding or hardening layout, plenary tests, CI, vimdoc, or releases.

## Plugin structure

Canonical Neovim plugin layout:

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

### Entry point (`lua/<plugin>/init.lua`)

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

### Autoload and registration

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

## Configuration defaults

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

## Testing with plenary.nvim

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

## CI with GitHub Actions

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

## Documentation

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

## Release automation

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
