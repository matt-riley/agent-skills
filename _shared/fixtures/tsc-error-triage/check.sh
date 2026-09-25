#!/usr/bin/env bash
# Deterministic check for the tsc-error-triage fixture.
# Usage: check.sh [workspace]   (defaults to this directory)
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

# 1. Real signal: the typecheck must pass.
if ! npx -y -p typescript@5 tsc --noEmit >/dev/null 2>&1; then
  echo "FAIL: tsc --noEmit still reports errors"
  exit 1
fi

# 2. Anti-gaming guards: passing by weakening or silencing the types is not a fix.
for pattern in "@ts-nocheck" "@ts-ignore" "as any" "as unknown as"; do
  if grep -rq -- "$pattern" src; then
    echo "FAIL: '$pattern' used to silence the compiler"
    exit 1
  fi
done

python3 - "$WORKSPACE/src/types.ts" <<'PY'
import re
import sys

source = open(sys.argv[1], encoding="utf-8").read()
match = re.search(r"export type Priority\s*=\s*([^;]+);", source)
if not match:
    print("FAIL: no exported Priority type alias")
    raise SystemExit(1)
body = match.group(1)
missing = [
    value for value in ("urgent", "high", "low")
    if f"'{value}'" not in body and f'"{value}"' not in body
]
if missing:
    print("FAIL: Priority union is missing: " + ", ".join(missing))
    raise SystemExit(1)
PY
if [ $? -ne 0 ]; then
  exit 1
fi

echo "PASS"
