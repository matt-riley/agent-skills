---
name: agent-supply-chain
description: "Use this skill when generating SHA-256 integrity manifests for agent plugins, verifying that installed plugins match their manifests, detecting tampered files, auditing dependency pinning, or building provenance chains for plugin promotion."
license: GNU GPL v3
metadata:
  version: 2.0.1 # x-release-please-version
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
2. Generate an integrity manifest using [Pattern 1](references/integrity-patterns.md#pattern-1-generate-integrity-manifest).
3. Add [Pattern 2](references/integrity-patterns.md#pattern-2-verify-integrity) verification to the existing CI pipeline.

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

## Integrity patterns

The complete Python examples for manifest generation, verification, dependency version audits, and promotion checks live in [`references/integrity-patterns.md`](references/integrity-patterns.md). Use them as examples and adapt paths, required files, and package metadata to the artifact under review.

## CI integration

Add the verification gate to the existing pipeline using [`references/ci-integration.md`](references/ci-integration.md), which contains the canonical GitHub Actions and promotion-gate examples.

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
- [`references/integrity-patterns.md`](references/integrity-patterns.md) — Python examples for manifest generation, verification, dependency audits, and promotion gates
