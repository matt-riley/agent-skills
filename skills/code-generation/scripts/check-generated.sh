#!/usr/bin/env bash
set -euo pipefail

generate_cmd='make generate'
expected_clean=0

usage() {
  cat <<'EOF'
Usage: scripts/check-generated.sh [options]

Run code generation and report whether generated artifacts changed.

Options:
  --generate CMD     Generator command to run (default: make generate)
  --expect-clean     Exit non-zero if git diff changes after generation
  -h, --help         Show this help text
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --generate) generate_cmd="$2"; shift 2 ;;
    --expect-clean) expected_clean=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

bash -lc "$generate_cmd"
after=$(git diff --stat || true)
changed=0
if [[ -n "$after" ]]; then
  changed=1
fi

echo "{"command":"$generate_cmd","changed":$changed}"

if [[ $expected_clean -eq 1 && $changed -eq 1 ]]; then
  echo 'Error: generation changed tracked files' >&2
  exit 10
fi
