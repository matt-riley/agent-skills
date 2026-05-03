#!/usr/bin/env bash
set -euo pipefail

start_cmd=''
health_url=''
declare -a required_vars=()

usage() {
  cat <<'EOF'
Usage: scripts/check-config.sh [options]

Validate required environment variables and optionally run a health check.

Options:
  --require VAR       Required environment variable (repeatable)
  --start CMD         Optional command that starts the service
  --health-url URL    Optional health endpoint to curl after startup
  -h, --help          Show this help text
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require) required_vars+=("$2"); shift 2 ;;
    --start) start_cmd="$2"; shift 2 ;;
    --health-url) health_url="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

missing=()
for var in "${required_vars[@]}"; do
  if [[ -z "$(printenv "$var")" ]]; then
    missing+=("$var")
  fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
  printf 'Error: missing required variables: %s
' "${missing[*]}" >&2
  exit 10
fi

if [[ -n "$start_cmd" ]]; then
  bash -lc "$start_cmd" &
  pid=$!
  trap 'kill $pid >/dev/null 2>&1 || true' EXIT
  sleep 2
fi

if [[ -n "$health_url" ]]; then
  curl --fail --silent --show-error "$health_url" >/dev/null
fi

echo '{"status":"ok","message":"configuration checks completed"}'
