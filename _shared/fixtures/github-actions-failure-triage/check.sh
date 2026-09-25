#!/usr/bin/env bash
# Deterministic check for the github-actions-failure-triage fixture.
# Usage: check.sh [workspace]
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }
WF=".github/workflows/ci.yml"

[ -f "$WF" ] || { echo "FAIL: $WF is missing"; exit 1; }
for job in "test:" "lint:"; do
  grep -q "^  $job" "$WF" || { echo "FAIL: job '$job' was removed"; exit 1; }
done

if ! actionlint "$WF" >/dev/null 2>&1; then
  echo "FAIL: actionlint still reports problems"
  actionlint "$WF" 2>&1 | head -5
  exit 1
fi

while IFS= read -r dir; do
  dir=$(echo "$dir" | sed -E 's/^[[:space:]]*working-directory:[[:space:]]*//; s/["'"'"']//g')
  [ -d "$dir" ] || { echo "FAIL: working-directory '$dir' does not exist"; exit 1; }
done < <(grep -E "working-directory:" "$WF")

echo "PASS"
