#!/usr/bin/env bash
# Deterministic check for the ts-generated-boundary fixture.
set -uo pipefail
WORKSPACE="${1:-$(cd "$(dirname "$0")" && pwd)}"
cd "$WORKSPACE" || { echo "FAIL: no workspace $WORKSPACE"; exit 1; }

if ! npx -y -p typescript@5 tsc --noEmit >/dev/null 2>&1; then
  echo "FAIL: tsc --noEmit still reports errors"
  exit 1
fi

GOT=$(shasum -a 256 src/generated/api-client.ts | cut -d' ' -f1)
[ "$GOT" = "a097600500e51375ccb0c3a3efc8a1afeaf1be1a2405f558d59ddfa221fadcc0" ] || { echo "FAIL: the generated client was hand-edited"; exit 1; }

for pattern in "as any" "as unknown as" "@ts-ignore" "@ts-nocheck"; do
  if grep -rq -- "$pattern" src/service.ts; then
    echo "FAIL: '$pattern' used instead of narrowing"
    exit 1
  fi
done
if grep -Eq " as [A-Z{]" src/service.ts; then
  echo "FAIL: a type assertion is used instead of narrowing"
  exit 1
fi

grep -q "getUser(" src/service.ts || { echo "FAIL: the generated client is no longer used"; exit 1; }
grep -Eq "user\.[a-zA-Z_]+|user\[" src/service.ts || { echo "FAIL: no narrowed property access on the result"; exit 1; }
grep -Eq "typeof|instanceof| in |Array\.isArray|function is[A-Z]|): [a-zA-Z]+ is " src/service.ts \
  || { echo "FAIL: no runtime narrowing or type guard in service.ts"; exit 1; }

echo "PASS"
