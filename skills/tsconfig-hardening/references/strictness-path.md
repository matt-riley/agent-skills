# Strictness path

Use this path when a repository wants stricter TypeScript settings without taking an uncontrolled blast radius.

## 1. Understand the current baseline

Before changing flags:

- run the existing typecheck command
- inspect the `extends` chain
- note whether the repo emits JS, declarations, or typechecks only

## 2. Clean config structure first

Prefer to fix:

- duplicated settings across parent and child configs
- conflicting `include` and `exclude` rules
- stale `paths`, `baseUrl`, or `types`
- accidental divergence between packages that should share a base config

If the real goal is adopting `composite`, `references`, or `tsc -b` across packages, use `skills/project-references-migration/SKILL.md` instead of treating it as ordinary strictness cleanup.

## 3. Tighten flags in small batches

A common order is:

1. `noImplicitAny`
2. `strictNullChecks` if not already implied by `strict`
3. `noImplicitOverride`
4. `noUncheckedIndexedAccess`
5. `exactOptionalPropertyTypes`
6. `noPropertyAccessFromIndexSignature` when relevant

This order favors the most foundational truthfulness checks before the noisier ergonomics flags.

## 4. Keep emit and resolution separate

If the task is strictness hardening, avoid coupling it with unrelated changes to:

- `module`
- `moduleResolution`
- `outDir`
- declaration emit behavior

Change those only when they are part of the root cause.

## 5. Re-measure after each batch

After every meaningful config change:

- re-run typecheck
- record whether the remaining errors are localized or widespread
- stop broadening the change if the next batch would mix concerns
