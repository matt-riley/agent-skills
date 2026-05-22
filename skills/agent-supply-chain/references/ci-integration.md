# Agent Supply Chain — CI Integration Notes

This reference documents CI integration patterns for the `agent-supply-chain` skill.

## GitHub Actions

Add manifest verification as a pre-deploy step. The check re-hashes all plugin files and compares against `INTEGRITY.json`:

```yaml
- name: Verify plugin integrity
  run: |
    PLUGIN_DIR="${{ matrix.plugin || '.' }}"
    cd "$PLUGIN_DIR"
    python -c "
    from pathlib import Path
    import json, hashlib, sys

    def hash_file(p):
        h = hashlib.sha256()
        with open(p, 'rb') as f:
            for c in iter(lambda: f.read(8192), b''):
                h.update(c)
        return h.hexdigest()

    manifest = json.loads(Path('INTEGRITY.json').read_text())
    errors = []
    for rel, expected in manifest['files'].items():
        p = Path(rel)
        if not p.exists():
            errors.append(f'MISSING: {rel}')
        elif hash_file(p) != expected:
            errors.append(f'MODIFIED: {rel}')
    if errors:
        for e in errors:
            print(f'::error::{e}')
        sys.exit(1)
    print(f'Verified {len(manifest[\"files\"])} files')
    "
```

## Promotion gate

Use `promotion_check()` from `../SKILL.md` to block any deployment where integrity, required files, or dependency pinning checks fail:

```python
result = promotion_check("my-plugin/")
if not result["ready"]:
    for name, check in result["checks"].items():
        if not check["passed"]:
            raise SystemExit(f"FAILED: {name}")
```

## When to run verification

- After every code review merge to lock in the reviewed state
- As a required CI check before any staging or production promotion
- On a schedule to detect untracked changes in deployed plugin directories
