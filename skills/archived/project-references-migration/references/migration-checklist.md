# Migration checklist

Use this checklist when introducing project references incrementally.

## 1. Inventory the graph

Capture:

- packages and layers
- current `tsconfig` locations
- emit expectations
- output directories
- path aliases
- known cycles

## 2. Pick a pilot package

Good pilot candidates are:

- leaf packages
- low-churn utility packages
- packages with clear declaration boundaries

Avoid high-fanout entry packages first.

## 3. Prepare the pilot config

For the pilot package, verify:

- `composite` is enabled
- declaration-related settings match package needs
- `rootDir` and `outDir` are explicit when needed
- references only point to real dependencies

## 4. Align scripts and outputs

Before widening the migration:

- confirm local builds still work
- confirm output paths and package exports still match
- confirm downstream packages import the built surface correctly

## 5. Expand from leaves upward

Migrate packages in dependency order. After each batch:

- run referenced builds
- verify declarations
- run the cross-package typecheck flow that consumers actually use
- verify editor navigation or go-to-definition resolves to the expected referenced package source or fresh declarations
- stop if a cycle or config split emerges

## 6. Troubleshoot output and editor cache

When the graph is correct but the experience still looks stale:

- compare the emitted path with the package's `outDir` and declaration expectations
- check whether the editor is still reading an old `tsconfig` project cache
- reopen the affected file after restarting the TypeScript server
- confirm the import resolves to a fresh declaration or source file, not a deleted build artifact

When the build output looks wrong:

- verify `rootDir` is not forcing source files into an unexpected nested folder
- confirm package exports and path aliases point at the same built surface
- inspect the referenced package before changing consumer configs
