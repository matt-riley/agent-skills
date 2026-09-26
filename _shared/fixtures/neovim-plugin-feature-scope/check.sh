#!/usr/bin/env bash
# Deterministic check for the neovim-plugin-feature-scope fixture.
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }
ASSERT=$(mktemp /tmp/glimpse-assert-XXXXXX.lua)
trap 'rm -f "$ASSERT"' EXIT
cat > "$ASSERT" <<'LUA'
local ok, err = pcall(function()
  local function fail(msg) error(msg, 0) end
  if vim.fn.exists(":Glimpse") ~= 2 then fail("the :Glimpse command is not defined") end
  local mapped = false
  for _, m in ipairs(vim.api.nvim_get_keymap("n")) do
    if m.lhs and m.lhs:sub(-2) == "gp" then mapped = true end
  end
  if not mapped then fail("no normal-mode mapping ending in gp") end
end)
if not ok then
  io.stderr:write("FAIL: " .. tostring(err) .. "\n")
  vim.cmd("cq")
end
LUA
nvim --headless -u tests/minimal_init.lua -c "lua dofile('$ASSERT')" -c "qa" >/dev/null 2>&1 \
  || { echo "FAIL: :Glimpse command or <leader>gp keymap missing"; nvim --headless -u tests/minimal_init.lua -c "lua dofile('$ASSERT')" -c "qa" 2>&1 | tail -2; exit 1; }

for pair in "lua/glimpse/preview.lua:3fb2a167aeee1486e51e609906fa33ceb50f0ae092c8fc5742e46042051f9fb8" "doc/glimpse.txt:4cac28c7c6e9aff81517823f81b4054f18629358e373c0ff8c687219689f2ceb" ".github/workflows/ci.yml:ba0291afb711860ae269d808d41dcc1b574816f2669204eb7ce1628dc6229540"; do
  file="${pair%%:*}"; want="${pair##*:}"
  got=$(shasum -a 256 "$file" | cut -d' ' -f1)
  [ "$got" = "$want" ] || { echo "FAIL: unrelated file was rewritten: $file"; exit 1; }
done

ls tests/*_spec.lua >/dev/null 2>&1 || { echo "FAIL: no plenary spec added"; exit 1; }
grep -rq "vim.api.nvim_create_user_command" lua/ || { echo "FAIL: command not registered through the Neovim API"; exit 1; }
grep -rq "vim.keymap.set" lua/ || { echo "FAIL: keymap not registered through vim.keymap.set"; exit 1; }
grep -rq "command!" lua/ tests/ 2>/dev/null && { echo "FAIL: vim.cmd command string used"; exit 1; }

if ! stylua --check lua tests >/dev/null 2>&1; then
  echo "FAIL: stylua --check reports formatting issues"
  exit 1
fi
echo "PASS"
