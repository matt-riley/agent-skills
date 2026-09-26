#!/usr/bin/env bash
# Deterministic check for the neovim-plugin-ci fixture.
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

WF=$(ls .github/workflows/*.y*ml 2>/dev/null | head -1)
[ -n "$WF" ] || { echo "FAIL: no workflow added under .github/workflows/"; exit 1; }
actionlint "$WF" >/dev/null 2>&1 || { echo "FAIL: actionlint rejects $WF"; actionlint "$WF" 2>&1 | head -3; exit 1; }

grep -q "nightly" "$WF" || { echo "FAIL: workflow does not run on nightly Neovim"; exit 1; }
grep -q "stable" "$WF" || { echo "FAIL: workflow does not run on stable Neovim"; exit 1; }
grep -q "stylua" "$WF" || { echo "FAIL: workflow does not lint with stylua"; exit 1; }

# Plenary must be a sibling checkout, not vendored inside the repo.
if grep -Eq "path:[[:space:]]*\.?/?plenary\.nvim[[:space:]]*$" "$WF"; then
  echo "FAIL: plenary.nvim is checked out inside the repository"
  exit 1
fi
grep -Eq "path:[[:space:]]*\.\./plenary\.nvim[[:space:]]*$" "$WF" \
  || { echo "FAIL: plenary.nvim is not checked out as a sibling (../plenary.nvim)"; exit 1; }

[ -f tests/minimal_init.lua ] || { echo "FAIL: tests/minimal_init.lua is missing"; exit 1; }
grep -q "\.\./plenary\.nvim" tests/minimal_init.lua \
  || { echo "FAIL: minimal_init.lua does not put ../plenary.nvim on runtimepath"; exit 1; }

if grep -Eq "command!|vim\.cmd\(\"command" tests/minimal_init.lua 2>/dev/null; then
  echo "FAIL: bootstrap uses vim.cmd command strings"
  exit 1
fi

if ! nvim --headless -u tests/minimal_init.lua -c "qa" >/dev/null 2>&1; then
  echo "FAIL: the test bootstrap does not load under nvim --headless"
  exit 1
fi

ACTUAL=$(shasum -a 256 tests/glimpse_spec.lua | cut -d' ' -f1)
[ "$ACTUAL" = "8e8c6bc634a789561df4c41cbbe9b36ca0dfbc4fc106e1b64f348ee2b8fb3a49" ] || { echo "FAIL: the existing spec was modified"; exit 1; }

grep -Eq "make test|plenary.test_harness" "$WF" \
  || { echo "FAIL: workflow never runs the plenary test suite"; exit 1; }

echo "PASS"
