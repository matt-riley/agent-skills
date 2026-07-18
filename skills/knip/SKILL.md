---
name: knip
description: "Use when a JavaScript or TypeScript project needs Knip to find unused dependencies, exports, files, or unresolved imports; not for runtime failures or dormant-task recovery."
license: GNU GPL v3
metadata:
  category: code-quality
  audience: general-coding-agent
  maturity: stable
  kind: reference
  version: 1.0.0 # x-release-please-version
---

# Knip

Use this skill when the job is to inspect or clean up a JavaScript or TypeScript codebase with Knip, especially for unused dependencies, exports, files, or unresolved imports.

## Use this skill when

- The user asks to find unused dependencies, exports, files, or unresolved imports in a JS/TS repo.
- The user wants a codebase-health audit before deleting code, tightening package dependencies, or trimming project entry points.
- The user wants a PR-safe or CI-friendly Knip check for a repository, package, or workspace.
- The user wants to preview or apply Knip fixes after confirming the report is accurate.
- The user wants to understand why Knip flags a dependency, export, or file as unused.

## Do not use this skill when

- The main problem is a runtime failure, broken test, or unexpected behavior; route to `systematic-debugging`.
- The main problem is TypeScript compiler output or tsconfig fallout; route to `tsc-error-triage` or `tsconfig-hardening`.
- The task is resuming a dormant or blocked task from partial context; route to `resolve-open-loops`.
- The analysis involves dead code, duplication, circular dependencies, or complexity hotspots rather than Knip's unused-import and dependency model; route to `fallow`.
- The repository is not primarily JavaScript or TypeScript.
- The request is about generic linting, formatting, or bundle-size work rather than Knip-based unused-code analysis.

## Inputs to gather

**Required before starting**

- The repository root or package scope to analyze.
- Whether the user wants a report, a fix preview, or an applied cleanup.
- Whether the project is a single package or a workspace/monorepo.

**Helpful if present**

- The package manager and existing Knip config file name.
- Any directories, entry points, or generated files that should stay in scope.
- Prior false positives or ignore rules that should be respected.

## First move

1. Identify the Knip config and package scope before choosing a command.
2. Run a report before changing config or code, then inspect any unresolved-import or entry-point surprises.
3. Only apply fixes after the report matches the intended cleanup.

## Workflow

1. Start with the smallest useful Knip run for the package or workspace in question.
2. Read the issue categories carefully so unused exports, files, dependencies, and unresolved imports are handled separately.
3. Prefer config-driven exclusions and entry-point settings over ad hoc ignores.
4. If the result is noisy, narrow the scope or adjust config before deleting code.
5. Use fix mode only after the report is understood and the change is clearly safe.
6. Re-run Knip after any config or cleanup change to confirm the issue list moved in the expected direction.

## Guardrails

- Treat Knip as an unused-code and reachability tool, not as a substitute for `tsc`, a linter, a security scanner, or a debugger.
- Do not delete an export, file, or dependency just because Knip reported it; confirm the reachability story first.
- Prefer fixing the config or entry-point model when the report points at a false positive.
- Do not make every source file an entry point; broad `entry` patterns can hide unused exports and weaken unused-file detection.
- Treat exit code 1 as "issues found", not necessarily a tool failure; distinguish it from runtime or configuration errors before changing course.
- Use the narrowest scope that still answers the question the user asked.
- Do not apply fixes until a dry run or preview confirms the intended cleanup.

## Validation

- Run `python _shared/validate-skills.py skills` from the catalog root.
- If eval tooling is available, run `python _shared/run-trigger-evals.py skills/knip/evals/trigger-queries.json --static` and `python _shared/run-functional-evals.py skills/knip/evals/evals.json --static`.
- Smoke test the activation wording with one request that should trigger and one near-miss that should not:
  - should trigger: `Run Knip on this TypeScript monorepo and tell me which exports, files, or dependencies look unused.`
  - should not trigger: `The test suite started failing after yesterday's merge and I need the root cause.`

## Examples

- `Use Knip to audit this React workspace for unused dependencies and exports before the release branch cuts.`
- `Run Knip in preview mode and show me which files or imports are only false positives because of generated code.`

## Reference files

- [`references/cli-reference.md`](references/cli-reference.md) - command families, scope controls, and fix-preview workflow
- [`references/configuration-and-triage.md`](references/configuration-and-triage.md) - config location, workspace handling, and false-positive triage
