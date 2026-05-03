#!/usr/bin/env bash
set -euo pipefail

generate_cmd=""
fmt_cmd=""
test_cmd=""
validate_cmd=""
require_clean_tree=0

usage() {
  cat <<'EOF'
Usage: scripts/release-readiness.sh [options]

Run a repeatable release-readiness checklist for CI/image workflows.

Options:
  --generate CMD     Command that refreshes generated artifacts
  --fmt CMD          Formatting command
  --test CMD         Test command
  --validate CMD     Optional schema/spec validation command
  --require-clean    Fail if git status is not clean before checks
  -h, --help         Show this help text
EOF
}

run_step() {
  local label="$1"
  local cmd="$2"
  if [[ -z "$cmd" ]]; then
    return 0
  fi
  echo "$label: $cmd"
  bash -lc "$cmd"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --generate) generate_cmd="$2"; shift 2 ;;
    --fmt) fmt_cmd="$2"; shift 2 ;;
    --test) test_cmd="$2"; shift 2 ;;
    --validate) validate_cmd="$2"; shift 2 ;;
    --require-clean) require_clean_tree=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ $require_clean_tree -eq 1 ]]; then
  if git status --short | grep -q '^'; then
    echo 'Error: working tree is dirty before release checks' >&2
    exit 10
  fi
fi

run_step generate "$generate_cmd"
run_step fmt "$fmt_cmd"
run_step test "$test_cmd"
run_step validate "$validate_cmd"

echo '{"status":"ok","message":"release readiness checks completed"}'
