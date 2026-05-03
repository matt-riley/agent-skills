---
name: tsconfig-hardening
description: Tighten and rationalize TypeScript configuration safely, especially when enabling stricter compiler checks incrementally.
metadata:
  category: typescript
  audience: general-coding-agent
  maturity: stable
---

# Tsconfig hardening

## Use this skill when

- The user wants to enable stricter TypeScript settings safely.
- A repository has a confusing `tsconfig` chain that needs cleanup or consolidation.
- Module resolution, emit behavior, or workspace config drift is causing recurring TypeScript issues.
- The user wants to change TypeScript configuration even if that work may produce compiler errors that will need follow-on triage.

## Do not use this skill when

- The task is to fix one local type error without changing project configuration.
- The build problem is mainly in Babel, bundler, or runtime tooling with no meaningful `tsconfig` change.
- The repository intentionally uses a loose config and the user did not ask to harden it.
- The main task is now triaging the compiler errors caused by an earlier config change rather than changing config further.

## Inputs to gather

**Required before editing**

- The active `tsconfig` files and their `extends` chain.
- The repository's typecheck, build, and test commands.
- The current strictness posture, such as `strict`, `noImplicitAny`, or `noUncheckedIndexedAccess`.
- Whether the project emits JavaScript, declarations, or typechecks only.

**Helpful if present**

- Baseline compiler error counts before changing flags.
- Whether the repository mixes ESM and CJS.
- Package-level overrides in a monorepo.

## First move

1. Inventory the `tsconfig` chain and run `tsc --showConfig` or the nearest equivalent when available.
2. Separate configuration cleanup from code fixes so the diff explains itself.
3. Pick one strictness or resolution problem to address first instead of flipping every flag at once.

## Workflow

1. Capture the current config shape and the commands it affects.
2. Normalize duplicated or conflicting settings across the `extends` chain.
3. Tighten flags in a deliberate order using the reference path below.
4. Keep module, path, include, exclude, and emit settings aligned with the actual build setup.
5. When a config change creates a burst of compiler errors, stop changing config further and switch to `skills/tsc-error-triage/SKILL.md` to work the failures in root-cause order.
6. Re-run typecheck, build, and targeted tests after each meaningful config change.

## Guardrails

- **Must not** enable many strictness flags at once without first measuring the failure surface.
- **Must not** change emit, module, or resolution settings casually when the task is only about strictness.
- **Should** preserve existing build outputs unless the user asked for a packaging change.
- **Should** prefer explicit per-package overrides over hidden config drift.
- **May** defer especially noisy flags with a clear note when the repository is not ready yet.

## Validation

- Run the repository's typecheck command after each config batch.
- Run the build if `tsconfig` affects emit or declaration generation.
- Confirm the final config still matches the intended runtime and package layout.

## Examples

- "Turn on stricter TypeScript settings without breaking the whole repo at once."
- "Clean up this messy `tsconfig` hierarchy and make module resolution predictable."
- "Help me enable `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` safely."

## Reference files

- [`references/strictness-path.md`](references/strictness-path.md) - a safe order for tightening common TypeScript compiler settings and related checks.
