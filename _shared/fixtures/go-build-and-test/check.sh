#!/usr/bin/env bash
# Deterministic check for the go-build-and-test fixture.
# Usage: check.sh [workspace]   (defaults to this directory)
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

EXPECTED_TEST_SHA="5ba9ea47be987dfd5793b86c25811c6c66ec7332f5d1bd409eb9a1e6ffb6530f"
ACTUAL=$(shasum -a 256 greet/greet_test.go 2>/dev/null | cut -d' ' -f1)
if [ "$ACTUAL" != "$EXPECTED_TEST_SHA" ]; then
  echo "FAIL: greet/greet_test.go was modified (the test is the spec)"
  exit 1
fi
if grep -q "t.Skip" greet/greet_test.go; then
  echo "FAIL: t.Skip added to the test"
  exit 1
fi
if ! go build ./... >/dev/null 2>&1; then
  echo "FAIL: go build ./... still fails"
  exit 1
fi
if ! go test ./... >/dev/null 2>&1; then
  echo "FAIL: go test ./... still fails"
  exit 1
fi
echo "PASS"
