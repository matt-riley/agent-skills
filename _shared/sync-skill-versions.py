#!/usr/bin/env python3
"""Mirror skill versions from .release-please-manifest.json into SKILL.md frontmatter.

Release Please is configured with `extra-files` (type: generic) so release PRs
should update the `metadata.version` line marked with `# x-release-please-version`
in every SKILL.md automatically. If that mirroring ever fails (e.g. the release
workflow skips extra-files), the manifest and frontmatter drift apart and
`npm run validate` fails.

Usage:
    python _shared/sync-skill-versions.py            # apply the mirror
    python _shared/sync-skill-versions.py --check    # exit 1 on any drift, write nothing
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / '.release-please-manifest.json'

# Matches the frontmatter version line, with or without the release-please marker.
VERSION_LINE_RE = re.compile(
    r'^(?P<indent>\s+version:\s*)(?P<version>\S+)(?P<marker>\s*#\s*x-release-please-version)?\s*$'
)
MARKER = ' # x-release-please-version'


def sync_file(skill_md: Path, version: str, check_only: bool) -> str:
    """Return 'ok', 'drift', 'missing-file', or 'no-version-line'."""
    if not skill_md.is_file():
        return 'missing-file'
    lines = skill_md.read_text(encoding='utf-8').splitlines(keepends=True)
    updated = False
    for idx, line in enumerate(lines):
        match = VERSION_LINE_RE.match(line.rstrip('\n'))
        if not match:
            continue
        rebuilt = f"{match.group('indent')}{version}{MARKER}"
        if line.rstrip('\n') != rebuilt:
            lines[idx] = rebuilt + '\n'
            updated = True
        break
    else:
        return 'no-version-line'
    if updated and not check_only:
        skill_md.write_text(''.join(lines), encoding='utf-8')
    return 'drift' if updated else 'ok'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='report drift and exit non-zero without writing')
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    drift: list[str] = []
    errors: list[str] = []
    synced = 0
    for key, version in sorted(manifest.items()):
        if not key.startswith('skills/'):
            continue
        status = sync_file(REPO_ROOT / key / 'SKILL.md', version, args.check)
        if status == 'ok':
            synced += 1
        elif status == 'drift':
            drift.append(f'{key}/SKILL.md -> {version}')
        else:
            errors.append(f'{key}: {status}')

    mode = 'check' if args.check else 'sync'
    print(json.dumps({
        'mode': mode,
        'skills_checked': synced + len(drift),
        'drifted': drift,
        'errors': errors,
    }, indent=2))
    if errors or (args.check and drift):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
