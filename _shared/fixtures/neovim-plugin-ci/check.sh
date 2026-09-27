#!/usr/bin/env bash
# Deterministic check for the neovim-plugin-ci fixture.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${1:-$SCRIPT_DIR}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

WF=$(ls .github/workflows/*.y*ml 2>/dev/null | head -1)
[ -n "$WF" ] || { echo "FAIL: no workflow added under .github/workflows/"; exit 1; }
actionlint "$WF" >/dev/null 2>&1 || { echo "FAIL: actionlint rejects $WF"; actionlint "$WF" 2>&1 | head -3; exit 1; }

grep -q "nightly" "$WF" || { echo "FAIL: workflow does not run on nightly Neovim"; exit 1; }
grep -q "stable" "$WF" || { echo "FAIL: workflow does not run on stable Neovim"; exit 1; }
grep -q "stylua" "$WF" || { echo "FAIL: workflow does not lint with stylua"; exit 1; }

# Plenary must be a sibling checkout, not vendored inside the repo.
# Plenary must be fetched at CI time (never committed) and the bootstrap must
# look for it where the workflow puts it. Either layout is fine; a mismatch is not.
python3 - "$WF" tests/minimal_init.lua <<'PY'
import re
import sys

workflow = open(sys.argv[1], encoding="utf-8").read()
bootstrap = open(sys.argv[2], encoding="utf-8").read()

step = re.search(r"repository:\s*nvim-lua/plenary\.nvim(.*?)(?:\n\s*-\s|\Z)", workflow, re.S)
if not step:
    print("FAIL: the workflow never checks out nvim-lua/plenary.nvim")
    raise SystemExit(1)

path_match = re.search(r"path:\s*([^\s#]+)", step.group(1))
workflow_path = path_match.group(1).strip() if path_match else "plenary.nvim"

boot_match = re.search(r"([\w./-]*plenary\.nvim)", bootstrap)
if not boot_match:
    print("FAIL: minimal_init.lua never references plenary.nvim")
    raise SystemExit(1)
boot_path = boot_match.group(1)

# Compare where each side expects to find plenary. Either location is valid,
# but both must agree: the bootstrap has to look where the workflow put it.
def prefix_of(path: str) -> str:
    """'plenary.nvim' and '/plenary.nvim' mean the workspace root; '../x' the parent."""
    # Bootstrap paths are captured from strings like getcwd() .. "/plenary.nvim",
    # so a leading slash is an artefact of concatenation, not an absolute path.
    path = path.lstrip("/")
    marker = "plenary.nvim"
    pre = path[: path.find(marker)].rstrip("/")
    return "" if pre in ("", "/") else pre

if prefix_of(workflow_path) != prefix_of(boot_path):
    print(f"FAIL: workflow checks out plenary at '{workflow_path}' but the "
          f"bootstrap expects '{boot_path}'")
    raise SystemExit(1)
PY
[ $? -eq 0 ] || exit 1

if [ -d plenary.nvim ]; then
  echo "FAIL: plenary.nvim is vendored into the repository"
  exit 1
fi

[ -f tests/minimal_init.lua ] || { echo "FAIL: tests/minimal_init.lua is missing"; exit 1; }
grep -q "plenary\.nvim" tests/minimal_init.lua \
  || { echo "FAIL: minimal_init.lua does not put plenary on runtimepath"; exit 1; }

if grep -Eq "command!|vim\.cmd\(\"command" tests/minimal_init.lua 2>/dev/null; then
  echo "FAIL: bootstrap uses vim.cmd command strings"
  exit 1
fi

if ! nvim --headless -u tests/minimal_init.lua -c "qa" >/dev/null 2>&1; then
  echo "FAIL: the test bootstrap does not load under nvim --headless"
  exit 1
fi

# A wired-up workflow that cannot actually run the tests is not done. Put
# plenary where the workflow says the runner fetches it, then run the suite.
PLENARY_CACHE="$(cd "$SCRIPT_DIR/../.deps" && pwd)/plenary.nvim"
[ -d "$PLENARY_CACHE" ] || { echo "FAIL: plenary cache missing at $PLENARY_CACHE"; exit 1; }
DEST=$(python3 - "$WF" <<'PY'
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
step = re.search(r"repository:\s*nvim-lua/plenary\.nvim(.*?)(?:\n\s*-\s|\Z)", text, re.S)
match = re.search(r"path:\s*([^\s#]+)", step.group(1)) if step else None
print(match.group(1) if match else "plenary.nvim")
PY
)
case "$DEST" in
  ../*) PLENARY_DEST="$(dirname "$WORKSPACE")/$(basename "$DEST")" ;;
  *)    PLENARY_DEST="$WORKSPACE/$(basename "$DEST")" ;;
esac
rm -rf "$PLENARY_DEST"
cp -R "$PLENARY_CACHE" "$PLENARY_DEST"

if ! grep -qE "^test:" Makefile 2>/dev/null; then
  echo "FAIL: no 'test' target to run the plenary suite"
  exit 1
fi
# Bounded: a test target that never quits nvim must fail, not hang the check.
python3 - "$WORKSPACE" <<'PY'
import subprocess
import sys

try:
    proc = subprocess.run(["make", "test"], cwd=sys.argv[1], capture_output=True,
                          text=True, timeout=180)
except subprocess.TimeoutExpired:
    print("FAIL: make test did not finish within 180s (the target never quits nvim)")
    raise SystemExit(1)
output = (proc.stdout or "") + (proc.stderr or "")
if proc.returncode != 0:
    tail = output.strip().splitlines()[-3:]
    print("FAIL: make test does not pass with plenary present")
    for line in tail:
        print("   ", line[:160])
    raise SystemExit(1)
# nvim exits 0 even when a -c command errors, so a Makefile that never ran the
# suite would otherwise pass. Require evidence that specs actually executed.
if "glimpse_spec" not in output and "Success" not in output:
    print("FAIL: make test exited 0 but no spec appears to have run")
    raise SystemExit(1)
PY
[ $? -eq 0 ] || exit 1

ACTUAL=$(shasum -a 256 tests/glimpse_spec.lua | cut -d' ' -f1)
[ "$ACTUAL" = "8e8c6bc634a789561df4c41cbbe9b36ca0dfbc4fc106e1b64f348ee2b8fb3a49" ] || { echo "FAIL: the existing spec was modified"; exit 1; }

grep -Eq "make test|plenary.test_harness" "$WF" \
  || { echo "FAIL: workflow never runs the plenary test suite"; exit 1; }

echo "PASS"
