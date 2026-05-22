---
name: tsconfig-hardening
description: "Tighten and rationalize TypeScript configuration safely, especially when enabling stricter compiler checks incrementally."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
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
2. Capture the current typecheck/build command and baseline compiler error count before changing flags.
3. Separate configuration cleanup from code fixes so the diff explains itself.
4. Pick one strictness or resolution problem to address first instead of flipping every flag at once.

## Concrete config diffs

Base config before:

```json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": false
  }
}
```

Base config after:

```json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": true
  }
}
```

Use a single-flag step like this before considering `strict: true`; the umbrella switch is only safe when the blast radius is already understood.

Package override before:

```json
{
  "extends": "../../tsconfig.base.json"
}
```

Package override after:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "noImplicitOverride": false
  }
}
```

Use a per-package override like this only to defer a base flag temporarily when one package is not ready yet.

## Workflow

1. Capture the current config shape and the commands it affects.
2. Normalize duplicated or conflicting settings across the `extends` chain.
3. Tighten flags in a deliberate order using the reference path below.
4. Keep module, path, include, exclude, and emit settings aligned with the actual build setup.
5. When a config change creates a burst of compiler errors, stop changing config further and switch to `skills/tsc-error-triage/SKILL.md` to work the failures in root-cause order.
6. Re-run typecheck, build, and targeted tests after each meaningful config change.
7. Stop widening the config change once the next flag would mix strictness work with emit, module, or package-layout churn.

## Guardrails

- **Must not** enable many strictness flags at once without first measuring the failure surface.
- **Must not** change emit, module, or resolution settings casually when the task is only about strictness.
- **Should** preserve existing build outputs unless the user asked for a packaging change.
- **Should** prefer explicit per-package overrides over hidden config drift.
- **May** defer especially noisy flags with a clear note when the repository is not ready yet.
- **Should** stop the config sweep when failures spread beyond one or two localized areas; at that point the work has become compiler triage, not hardening.

## Flag interaction notes

- `strict` is the umbrella switch; do not expect it to be a no-op if package configs were already overriding pieces of it.
- `noUncheckedIndexedAccess` often exposes index-signature and collection usage at once, so land it separately from optional-property changes.
- `exactOptionalPropertyTypes` tends to ripple through object defaults and partial-update helpers, so keep the diff small enough to explain the actual API impact.
- `noImplicitOverride` usually stays local to inheritance hierarchies and is a good follow-up batch after the broader nullability work.
- If a stricter flag would require `module`, `moduleResolution`, or `outDir` changes to stay buildable, pause and re-evaluate the root cause before widening the config patch.

## When to stop widening

Stop broadening the config work when any of these happen:

- the next change would touch both strictness and package-layout concerns
- the remaining failures are spread across unrelated packages
- the config diff no longer fits the current diagnosis in one review pass
- the only remaining fixes are code changes, not config changes

## Routing boundary

- Use this skill when the primary work is TypeScript configuration cleanup or strictness sequencing.
- Route to [`project-references-migration`](../project-references-migration/SKILL.md) when the main goal is incremental `tsc -b` project-references adoption across a layered workspace.
- Route to [`tsc-error-triage`](../tsc-error-triage/SKILL.md) once config changes have landed and the task becomes source-level compiler error remediation.

## Validation

- Run the repository's typecheck command after each config batch.
- Run the build if `tsconfig` affects emit or declaration generation.
- Confirm the final config still matches the intended runtime and package layout.
- Use [`references/hardening-scenarios.md`](references/hardening-scenarios.md) to keep strictness sequencing, stop thresholds, and do-not-widen cases aligned with the maintenance loop.

- Smoke test:
  - should trigger: "Enable noImplicitAny and clean up this repo's tsconfig chain safely."
  - should not trigger: "Fix the source errors from the last typecheck run." (→ `tsc-error-triage`)

## Examples

- "Turn on stricter TypeScript settings without breaking the whole repo at once."
- "Clean up this messy `tsconfig` hierarchy and make module resolution predictable."
- "Help me enable `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` safely."

## Reference files

- [`references/strictness-path.md`](references/strictness-path.md) - a safe order for tightening common TypeScript compiler settings and related checks.
- [`references/hardening-scenarios.md`](references/hardening-scenarios.md) - scenario checklist for sequencing strictness work without widening scope.
