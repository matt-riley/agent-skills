# Configuration and triage

Use this file when Knip reports something surprising and you need to decide whether to fix code, tune config, or suppress a known edge case.

## Configuration file locations

Knip looks for common config names such as `knip.json`, `knip.jsonc`, `.knip.json`, `.knip.jsonc`, `knip.ts`, `knip.js`, `knip.config.ts`, `knip.config.js`, and a `knip` entry in `package.json`.

## Core config ideas

- `entry` tells Knip where analysis should start.
- `project` tells Knip which files belong in the broader codebase scan.
- `workspaces` lets monorepos and workspace-style repos tune `entry`, `project`, and plugins per package.
- `includeEntryExports` makes Knip report unused exports from entry files when the repo is self-contained or private.
- `ignoreExportsUsedInFile` handles files where some exports are only used internally.
- `ignoreUnresolved` and `ignoreDependencies` are workspace-level escape hatches for known configuration edges.

## Triage order

1. Check whether the file is an entry point or configuration file that Knip intentionally treats differently.
2. Check whether the workspace or project patterns are too broad or too narrow.
3. Check whether a generated file, internal-only export, or conditional dependency is producing a known false positive.
4. Prefer config fixes over blanket ignores when the report is useful but incomplete.
5. Use a workspace ignore only when the package is intentionally out of scope and the config story is settled.
6. Use `ignoreFiles` or `ignoreIssues` for narrow false positives before reaching for broad `ignore` patterns.

## Common false-positive patterns

- Generated files that export a large surface area on purpose.
- Monorepos where a dependency is listed once but consumed from a descendant workspace.
- Projects with custom entry files that are not covered by the default patterns.
- Config files that statically mention a plugin or dependency but do not behave like normal application source.
