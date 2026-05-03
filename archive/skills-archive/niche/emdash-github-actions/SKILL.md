---
name: emdash-github-actions
description: Set up GitHub Actions CI/CD for EmDash plugin repositories, including type-checking, linting, tests, dependency auditing, and npm publishing when the plugin actually needs them.
metadata:
  maturity: draft
---

# EmDash plugin GitHub Actions

## Use this skill when

- The repository is an EmDash plugin and needs initial GitHub Actions workflows.
- The user wants CI for an EmDash plugin, such as type-checking, linting, tests, security checks, or npm publishing.
- The task is to add or standardize GitHub Actions automation for a new or existing EmDash plugin repo.
- The user asks for best-practice workflow setup for an EmDash plugin rather than generic CI advice.

## Do not use this skill when

- The main task is diagnosing a failing workflow run in a repo that already has GitHub Actions. Use [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md).
- The repository is not an EmDash plugin, even if it uses Astro or TypeScript.
- The main task is package publishing outside GitHub Actions workflow setup.
- The user only wants repository polish such as README or health files rather than CI workflow design.

## Inputs to gather

**Required before editing**

- `package.json`, especially scripts, `peerDependencies`, `dependencies`, `publishConfig`, and package name.
- Whether the plugin has React admin UI code such as `.tsx` files or `admin.tsx`.
- Whether tests already exist and, if so, which runner and config files are present.
- The default branch and any existing `.github/workflows/` files.

**Helpful if present**

- Existing `tsconfig.*`, lint config, or test config files.
- Whether the package is public, scoped, and actually intended for npm publication.
- CI or release conventions already used by sibling EmDash plugin repos.
- Whether the repo has a lockfile, which affects `npm ci` versus `npm install`.

**Only investigate if encountered**

- Whether the plugin needs a build step before publishing.
- Whether unusual peer dependencies or runtime assumptions require adapting the stock workflow templates.
- Whether supporting config files should be created because the repo lacks a stable local contract.

## First move

1. Inspect the plugin shape before drafting workflows: scripts, peer dependencies, source layout, tests, and existing CI files.
2. Decide which workflow set is actually warranted; most plugins need type-check, lint, and security, while test and publish flows are conditional.
3. Read [`references/workflows.md`](references/workflows.md) before editing so workflow choices stay aligned with the documented EmDash plugin contract.

## Workflow

1. Classify the plugin:
   - basic TypeScript plugin
   - plugin with React admin UI
   - plugin with existing tests
   - plugin intended for npm publication
2. Choose the smallest useful workflow set instead of forcing every possible workflow into every repository.
3. Create separate workflow files so GitHub checks stay independently visible and easy to disable or evolve.
4. Add or adapt supporting config files only when the repository does not already define the needed contract.
5. If publish automation is added, verify the package and release process are real, then remind the user that the repository needs an `NPM_TOKEN` secret.

## Guardrails

- **Must not** assume every EmDash plugin needs every workflow; match the workflow set to the actual repository.
- **Must not** overwrite an existing local TypeScript, lint, test, or release contract without checking whether it already works.
- **Must not** add npm publishing automation unless the package is actually meant to be published.
- **Must not** hard-code the branch trigger without verifying the repo's real default branch.
- **Should** prefer Node.js 22 with `actions/checkout@v5` and `actions/setup-node@v5` unless the repo already has a stronger supported contract.
- **Should** install the peer dependencies needed for CI type-checking, including `emdash` and React types when `.tsx` files are present.
- **Should** use `--skipLibCheck` for plugin CI type-checks so the check stays focused on the plugin's own code.
- **Should** prefer the documented `find`-based file discovery pattern over brittle shell globs in CI commands.

## Validation

- Confirm the workflow files, triggers, and commands match the plugin's actual scripts and package metadata.
- Check that chosen install commands fit the repo's lockfile situation and dependency shape.
- Verify that any supporting config files are consistent with the workflow commands rather than duplicating conflicting settings.
- Run `python skills/_shared/validate-skills.py /home/mattriley/.copilot/skills` after editing the skill package.

## Examples

- "Set up GitHub Actions for my EmDash plugin."
- "Add CI to this EmDash plugin repo."
- "I want automated type-checking and linting on PRs for this plugin."
- "Set up npm publishing for this EmDash plugin."

## Reference files

- [`references/workflows.md`](references/workflows.md) - load this when you need ready-to-adapt workflow templates, support-file examples, or the EmDash-specific rationale behind each workflow choice
