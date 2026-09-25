#!/usr/bin/env bash
# Deterministic check for the knip fixture.
# Usage: check.sh [workspace]
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

# Anti-gaming: the report must not be silenced through configuration.
for key in '"ignore"' '"ignoreDependencies"' '"ignoreFiles"' '"ignoreExportsUsedInFile"'; do
  if grep -q -- "$key" knip.json 2>/dev/null; then
    echo "FAIL: knip.json configures $key instead of removing the unused code"
    exit 1
  fi
done
if grep -q '"knip"' package.json 2>/dev/null; then
  echo "FAIL: knip config moved into package.json"
  exit 1
fi

if ! npx -y knip >/dev/null 2>&1; then
  echo "FAIL: knip still reports unused exports or dependencies"
  npx -y knip 2>&1 | tail -6
  exit 1
fi
echo "PASS"
