#!/usr/bin/env bash
# Deterministic check for the goreleaser-release-pipeline fixture.
# Usage: check.sh [workspace]
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }
WF=".github/workflows/release.yml"
GORELESER="${GORELESER:-goreleaser}"

[ -f "$WF" ] || { echo "FAIL: $WF is missing"; exit 1; }
[ -f ".goreleaser.yaml" ] || { echo "FAIL: .goreleaser.yaml is missing"; exit 1; }

# goreleaser check inspects git refs, so the workspace needs a repo with a remote
# whether it is the fixture itself or a scratch copy.
if ! git rev-parse --git-dir >/dev/null 2>&1; then git init -q; fi
if ! git remote | grep -q .; then git remote add origin https://github.com/example/rel.git; fi
if ! git rev-parse HEAD >/dev/null 2>&1; then
  git add -A >/dev/null 2>&1
  git -c user.email=fixture@example.com -c user.name=fixture commit -qm fixture >/dev/null 2>&1
fi

# The publish job must survive and stay gated on the release output.
grep -q "goreleaser:" "$WF" || { echo "FAIL: the goreleaser job was removed"; exit 1; }
grep -q "release_created" "$WF" || { echo "FAIL: publish job is no longer gated on release_created"; exit 1; }

if ! actionlint "$WF" >/dev/null 2>&1; then
  echo "FAIL: actionlint reports problems in $WF"
  actionlint "$WF" 2>&1 | head -5
  exit 1
fi

# The tag reaching GoReleaser must be plain semver: either release-please stops
# prefixing the component, or the workflow strips the prefix before publishing.
python3 - <<'PY'
import json
import re
import sys

config = json.load(open("release-please-config.json", encoding="utf-8"))
prefixes = bool(config.get("include-component-in-tag", False))
workflow = open(".github/workflows/release.yml", encoding="utf-8").read()
strips = bool(re.search(r"tag_name.*(sed|cut|##\*|strip)", workflow)) or "component" in workflow.lower()
if prefixes and not strips:
    print("FAIL: release-please still emits component-prefixed tags (rel-v1.2.3) "
          "and nothing strips the prefix for GoReleaser")
    raise SystemExit(1)
PY
[ $? -eq 0 ] || exit 1

if ! $GORELESER check >/dev/null 2>&1; then
  echo "FAIL: goreleaser check rejects the configuration"
  $GORELESER check 2>&1 | tail -4
  exit 1
fi
echo "PASS"
