---
name: project-references-migration
description: "Use when a layered TypeScript workspace needs an incremental project-references migration without breaking package boundaries or editor resolution."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: typescript
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Project references migration

## Use this skill when

- The repository has multiple TypeScript packages or layers and needs faster, more reliable builds.
- The user wants to adopt `tsc -b` project references incrementally.
- Declaration output, package boundaries, or editor performance are suffering in a growing TypeScript workspace.
- You need to make the graph coherent enough for `tsc -b`, fresh declarations, and editor go-to-definition to agree.

## Do not use this skill when

- The repository is a small single-project TypeScript setup.
- The task is only to fix one package's local `tsconfig`.
- The workspace already has healthy project references and only needs routine maintenance.
- The main goal is strictness hardening or general `tsconfig` cleanup rather than adopting `composite`, `references`, or `tsc -b`.

## Inputs to gather

**Required before editing**

- The package or layer graph and their current `tsconfig` files.
- The existing build and typecheck commands.
- Whether each package emits declarations, JavaScript, or types only.
- Output directories, package exports, and path alias usage.

**Helpful if present**

- Existing workspace tooling such as Nx, Turborepo, pnpm workspaces, or custom scripts.
- Known circular dependencies.
- Editor or CI pain points that motivate the migration.

## First move

1. Inventory the package graph, current `tsconfig` chain, and any obvious cycles.
2. Pick one leaf or low-risk package as the pilot migration surface.
3. Confirm how declarations, outputs, and package boundaries work today before adding references.
4. Stop and split the boundary if a proposed reference would create a cycle.

## Common shapes

Solution config:

```json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" }
  ]
}
```

Pilot package config:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "rootDir": "src",
    "outDir": "dist"
  },
  "references": [{ "path": "../core" }]
}
```

## Workflow

1. Create or normalize a shared base config only for settings that truly belong across referenced packages.
2. Enable `composite` and the required declaration settings on the pilot package.
3. Add explicit `references` only where the dependency graph is already real.
4. Align output directories, package exports, and path aliases with the referenced build layout.
5. Migrate packages incrementally from leaves upward.
6. Switch scripts to `tsc -b` or the repository's equivalent only after the referenced graph is coherent.
7. If a cycle appears, stop widening and split the dependency before adding more references.

## Outputs

- tsconfig and import changes that enable project references without breaking editor or build resolution for the workspace.
- Evidence (build, type-check, or test) that the migration is safe.

## Guardrails

- **Must not** migrate the whole workspace in one leap without a proven pilot.
- **Must not** introduce circular references to mirror accidental runtime coupling.
- **Should** keep runtime resolution, package exports, and declaration output aligned.
- **Should** prefer real package boundaries over giant shared path-alias surfaces.
- **May** leave exceptional packages on local configs temporarily when the graph is not ready.
- **Should** treat a repeated cycle or stale output mismatch as a sign to pause migration, not to add another config layer.

## Troubleshooting

- If the build succeeds but the editor opens stale declarations, restart the TypeScript server or reopen the workspace after confirming the package graph changed.
- If go-to-definition lands in the wrong emitted folder, verify `rootDir`, `outDir`, `declaration`, and package exports point at the same build layout.
- If outputs land beside source or in an unexpected subdirectory, inspect the package's `tsconfig` inheritance before widening the reference graph.

## Routing boundary

- Use this skill when a multi-package TypeScript workspace needs a deliberate `composite` / `references` migration path.
- Route to [`tsconfig-hardening`](../tsconfig-hardening/SKILL.md) when the task is mainly single-package compiler-option cleanup or strictness tuning.
- Route to [`tsc-error-triage`](../tsc-error-triage/SKILL.md) when the references migration has already landed and remaining work is source-level compiler failure triage.

## Validation

- Run the repository's referenced build or the nearest equivalent after each migration batch.
- Confirm declarations and outputs land in the expected locations.
- Run the typecheck workflow that consumes cross-package imports, not just the referenced build.
- Open a consuming file in the editor when possible, trigger go-to-definition on an imported symbol, and confirm it resolves to the expected referenced package source or fresh declarations rather than stale outputs.

- Smoke test:
  - should trigger: "Add tsconfig references across our TS packages so tsc -b works."
  - should not trigger: "Enable noUncheckedIndexedAccess in one package safely." (→ `tsconfig-hardening`)

## Examples

- `Before`
  ```jsonc
  {
    "compilerOptions": {
      "composite": false
    }
  }
  ```
  `After`
  ```jsonc
  {
    "compilerOptions": {
      "composite": true,
      "declaration": true,
      "declarationMap": true
    },
    "references": [{ "path": "../core" }]
  }
  ```
- Pilot one leaf package first, then validate that `tsc -b` and editor go-to-definition resolve against the fresh declarations instead of stale outputs.

## Reference files

- [`references/migration-checklist.md`](references/migration-checklist.md) - staged checklist for introducing project references without destabilizing the workspace.
