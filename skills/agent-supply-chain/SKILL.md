---
name: agent-supply-chain
description: "Use this skill when generating SHA-256 integrity manifests for agent plugins, verifying that installed plugins match their manifests, detecting tampered files, auditing dependency pinning, or building provenance chains for plugin promotion."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---
# Agent Supply Chain Integrity

Generate and verify integrity manifests for AI agent plugins and tools. Detect tampering, enforce version pinning, and establish supply chain provenance.

## Use this skill when

- Generating SHA-256 integrity manifests for agent plugins or tool packages before promotion
- Verifying that installed plugins match their published manifests
- Detecting tampered, modified, or untracked files in agent tool directories
- Auditing dependency pinning and version policies for agent components
- Building provenance chains for agent plugin promotion (dev → staging → production)
- Any request like "verify plugin integrity", "generate manifest", "check supply chain", or "sign this plugin"

## Do not use this skill when

- The plugin is a simple local script with no distributable files or production promotion path.
- You need runtime governance or policy controls for agent tool calls during execution; use `agent-governance` instead.

## Inputs to gather

**Required before implementing**

- The list of plugins, tools, or agent packages used by the agent.
- The promotion pipeline (dev → staging → production) if any.

**Helpful if present**

- Existing CI pipeline config for where integrity checks should run.

## First move

1. Inventory all plugins, tools, and agent packages used by the agent.
2. Generate an integrity manifest using Pattern 1.
3. Add Pattern 2 verification to the existing CI pipeline.

## Overview

Agent plugins and MCP servers have the same supply chain risks as npm packages or container images — except the ecosystem has no equivalent of npm provenance, Sigstore, or SLSA. This skill fills that gap.

```
Plugin Directory → Hash All Files (SHA-256) → Generate INTEGRITY.json
                                                    ↓
Later: Plugin Directory → Re-Hash Files → Compare Against INTEGRITY.json
                                                    ↓
                                          Match? VERIFIED : TAMPERED
```

---

## Pattern 1: Generate Integrity Manifest

Create a deterministic `INTEGRITY.json` with SHA-256 hashes of all plugin files.

```python
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "INTEGRITY.json"}

def hash_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest(plugin_dir: str) -> dict:
    """Generate an integrity manifest for a plugin directory."""
    root = Path(plugin_dir)
    files = {}

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name in EXCLUDE_FILES:
            continue
        if any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        files[rel] = hash_file(path)

    # Chain hash: SHA-256 of all file hashes concatenated in sorted order
    chain = hashlib.sha256()
    for key in sorted(files.keys()):
        chain.update(files[key].encode("ascii"))

    manifest = {
        "plugin_name": root.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "sha256",
        "file_count": len(files),
        "files": files,
        "manifest_hash": chain.hexdigest(),
    }
    return manifest

# Generate and save
manifest = generate_manifest("my-plugin/")
Path("my-plugin/INTEGRITY.json").write_text(
    json.dumps(manifest, indent=2) + "\n"
)
print(f"Generated manifest: {manifest['file_count']} files, "
      f"hash: {manifest['manifest_hash'][:16]}...")
```

**Output (`INTEGRITY.json`):**
```json
{
  "plugin_name": "my-plugin",
  "generated_at": "2026-04-01T03:00:00+00:00",
  "algorithm": "sha256",
  "file_count": 12,
  "files": {
    ".claude-plugin/plugin.json": "a1b2c3d4...",
    "README.md": "e5f6a7b8...",
    "skills/search/SKILL.md": "c9d0e1f2...",
    "agency.json": "3a4b5c6d..."
  },
  "manifest_hash": "7e8f9a0b1c2d3e4f..."
}
```

---

## Pattern 2: Verify Integrity

Check that current files match the manifest.

```python
# Requires: hash_file() and generate_manifest() from Pattern 1 above
import json
from pathlib import Path

def verify_manifest(plugin_dir: str) -> tuple[bool, list[str]]:
    """Verify plugin files against INTEGRITY.json."""
    root = Path(plugin_dir)
    manifest_path = root / "INTEGRITY.json"

    if not manifest_path.exists():
        return False, ["INTEGRITY.json not found"]

    manifest = json.loads(manifest_path.read_text())
    recorded = manifest.get("files", {})
    errors = []

    # Check recorded files
    for rel_path, expected_hash in recorded.items():
        full = root / rel_path
        if not full.exists():
            errors.append(f"MISSING: {rel_path}")
            continue
        actual = hash_file(full)
        if actual != expected_hash:
            errors.append(f"MODIFIED: {rel_path}")

    # Check for new untracked files
    current = generate_manifest(plugin_dir)
    for rel_path in current["files"]:
        if rel_path not in recorded:
            errors.append(f"UNTRACKED: {rel_path}")

    return len(errors) == 0, errors

# Verify
passed, errors = verify_manifest("my-plugin/")
if passed:
    print("VERIFIED: All files match manifest")
else:
    print(f"FAILED: {len(errors)} issue(s)")
    for e in errors:
        print(f"  {e}")
```

**Output on tampered plugin:**
```
FAILED: 3 issue(s)
  MODIFIED: skills/search/SKILL.md
  MISSING: agency.json
  UNTRACKED: backdoor.py
```

---

## Pattern 3: Dependency Version Audit

Check that agent dependencies use pinned versions.

```python
import re

def audit_versions(config_path: str) -> list[dict]:
    """Audit dependency version pinning in a config file."""
    findings = []
    path = Path(config_path)
    content = path.read_text()

    if path.name == "package.json":
        data = json.loads(content)
        for section in ("dependencies", "devDependencies"):
            for pkg, ver in data.get(section, {}).items():
                if ver.startswith("^") or ver.startswith("~") or ver == "*" or ver == "latest":
                    findings.append({
                        "package": pkg,
                        "version": ver,
                        "severity": "HIGH" if ver in ("*", "latest") else "MEDIUM",
                        "fix": f'Pin to exact: "{pkg}": "{ver.lstrip("^~")}"'
                    })

    elif path.name in ("requirements.txt", "pyproject.toml"):
        for line in content.splitlines():
            line = line.strip()
            if ">=" in line and "<" not in line:
                findings.append({
                    "package": line.split(">=")[0].strip(),
                    "version": line,
                    "severity": "MEDIUM",
                    "fix": f"Add upper bound: {line},<next_major"
                })

    return findings
```

---

## Pattern 4: Promotion Gate

Use integrity verification as a gate before promoting plugins.

```python
def promotion_check(plugin_dir: str) -> dict:
    """Check if a plugin is ready for production promotion."""
    checks = {}

    # 1. Integrity manifest exists and verifies
    passed, errors = verify_manifest(plugin_dir)
    checks["integrity"] = {
        "passed": passed,
        "errors": errors
    }

    # 2. Required files exist
    root = Path(plugin_dir)
    required = ["README.md"]
    missing = [f for f in required if not (root / f).exists()]

    # Require at least one plugin manifest (supports both layouts)
    manifest_paths = [
        root / ".github/plugin/plugin.json",
        root / ".claude-plugin/plugin.json",
    ]
    if not any(p.exists() for p in manifest_paths):
        missing.append(".github/plugin/plugin.json (or .claude-plugin/plugin.json)")

    checks["required_files"] = {
        "passed": len(missing) == 0,
        "missing": missing
    }

    # 3. No unpinned dependencies
    mcp_path = root / ".mcp.json"
    if mcp_path.exists():
        config = json.loads(mcp_path.read_text())
        unpinned = []
        for server in config.get("mcpServers", {}).values():
            if isinstance(server, dict):
                for arg in server.get("args", []):
                    if isinstance(arg, str) and "@latest" in arg:
                        unpinned.append(arg)
        checks["pinned_deps"] = {
            "passed": len(unpinned) == 0,
            "unpinned": unpinned
        }

    # Overall
    all_passed = all(c["passed"] for c in checks.values())
    return {"ready": all_passed, "checks": checks}

result = promotion_check("my-plugin/")
if result["ready"]:
    print("Plugin is ready for production promotion")
else:
    print("Plugin NOT ready:")
    for name, check in result["checks"].items():
        if not check["passed"]:
            print(f"  FAILED: {name}")
```

---

## CI Integration

Add to your GitHub Actions workflow:

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

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| **Generate manifest after code review** | Ensures reviewed code matches production code |
| **Include manifest in the PR** | Reviewers can verify what was hashed |
| **Verify in CI before deploy** | Catches post-review modifications |
| **Chain hash for tamper evidence** | Single hash represents entire plugin state |
| **Exclude build artifacts** | Only hash source files — .git, __pycache__, node_modules excluded |
| **Pin all dependency versions** | Unpinned deps = different code on every install |

---

## Outputs

- `INTEGRITY.json` manifest with SHA-256 file hashes and chain hash for a plugin directory.
- Verification report listing any MISSING, MODIFIED, or UNTRACKED files.
- Dependency version audit findings with severity and fix suggestions.
- Promotion gate check result with pass/fail for integrity, required files, and pinned dependencies.

## Workflow

1. Inventory plugins, tools, and agent packages the runtime loads.
2. Generate or refresh the integrity manifest (SHA-256 per file plus chain hash) for each packaged artifact.
3. Store manifests in source control next to the packages they protect.
4. Add CI verification that fails on MISSING, MODIFIED, or UNTRACKED files.
5. Run dependency version audits for unpinned or vulnerable packages.
6. Wire a promotion gate that requires integrity pass, required files present, and pinned dependencies before release.
7. On verification failure, fail closed — do not load or promote the artifact.
8. Document how operators regenerate manifests after intentional package changes.

## Guardrails

- **Must not** allow plugins with unverified checksums to load in production.
- **Must not** promote an artifact without verifying its manifest first.
- **Should** fail closed when a checksum verification error occurs.
- **Should** store manifests in source control so they can be audited.
- **Should** run dependency version audits on every dependency upgrade.

## Validation

After implementing supply chain controls, verify end-to-end integrity:

- Run `generate_manifest()` on a fresh plugin directory and confirm `INTEGRITY.json` is written with the correct file count.
- Modify a tracked file and re-run `verify_manifest()` — confirm the output includes `MODIFIED: <file>`.
- Add an untracked file and re-verify — confirm the output includes `UNTRACKED: <file>`.
- Run `promotion_check()` before any production promotion and confirm all checks (integrity, required files, pinned deps) pass.
- Run the CI verification step in `references/ci-integration.md` and confirm the workflow exits 0 on a clean plugin.

- Smoke test:
  - should trigger: "Generate a SHA-256 manifest for this plugin and verify it in CI."
  - should not trigger: "Add runtime tool allowlists to this agent." (→ `agent-governance`)

## Examples

- "Lock in the state of `my-agent-plugin/` after code review" → run `generate_manifest("my-agent-plugin/")`, commit `INTEGRITY.json` to the PR.
- "Verify that the deployed plugin hasn't been tampered with since the last review" → run `verify_manifest("my-agent-plugin/")` and check for MODIFIED or UNTRACKED entries.
- "Gate our plugin release pipeline on integrity" → use `promotion_check()` as a pre-deploy step; fail the pipeline if any check does not pass.

## Reference files

- [`references/ci-integration.md`](references/ci-integration.md) — GitHub Actions workflow template for manifest verification in CI
