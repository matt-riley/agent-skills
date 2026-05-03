---
name: tsc-error-triage
description: Diagnose and resolve TypeScript compiler errors by finding the smallest root-cause fix before editing call sites.
metadata:
  category: typescript
  audience: general-coding-agent
  maturity: stable
---

# TSC error triage

## Use this skill when

- The user asks you to fix TypeScript compiler errors or strict-mode regressions.
- A refactor, dependency upgrade, or config change causes a burst of `tsc` failures.
- `tsconfig` hardening or module-resolution changes have already been made and the next task is fixing the resulting compiler errors in root-cause order.
- You need to identify the root cause instead of patching each leaf error one by one.

## Do not use this skill when

- The task is primarily about runtime bugs with no TypeScript compiler signal.
- The repository is not using TypeScript or does not have a meaningful typecheck command.
- The request is to redesign the type model broadly rather than to triage concrete compiler failures.

## Inputs to gather

**Required before editing**

- The repository's typecheck command.
- The current compiler output or the files showing the failing errors.
- The recent change that likely introduced the failures, if known.
- The relevant `tsconfig` chain for the failing files.

**Helpful if present**

- Existing type suppression patterns such as `@ts-expect-error` or wrapper helpers.
- Adjacent tests covering the affected module.
- Whether the failures are isolated to one package or shared across a workspace.

## First move

1. Find the repository's typecheck command by checking the existing scripts, workspace commands, or TypeScript build setup.
2. If the command is still ambiguous, use `tsc --noEmit` for a single-project setup or `tsc -b` for a project-references setup as the safest fallback.
3. Run that command and capture the full compiler output.
4. Group the errors by root symbol, module, or config boundary instead of treating every error as independent.
5. Start with the earliest high-fanout error before fixing downstream call sites.

## Workflow

1. Reproduce the failures with the same command the repository already uses.
2. Find the first causal error in the chain, such as a bad export, a broken generic constraint, or a config mismatch.
3. Inspect the defining type, imports, and nearby helpers before editing consumers.
4. Apply the smallest truthful fix at the source of the error.
5. Re-run the typecheck to see which follow-on errors disappear.
6. Only then fix any remaining leaf errors that still reflect real type problems.

## Guardrails

- **Must not** silence compiler errors with `any`, `@ts-ignore`, or unsafe assertions unless the repository already documents that escape hatch.
- **Must not** patch leaf errors first when a shared root cause is still unresolved.
- **Should** prefer fixing exported types, generic constraints, and config boundaries before editing many call sites.
- **Should** preserve runtime behavior while improving type correctness.

## Validation

- Re-run the same typecheck command and confirm the targeted errors are gone.
- Check that no new class of compiler error was introduced nearby.
- Run targeted tests for the touched surface when the repository has them.

## Examples

- "TypeScript exploded after this refactor. Find the root cause instead of patching every call site."
- "Fix the `tsc --noEmit` errors after upgrading this dependency."
- "I enabled a stricter TS flag and now there are 80 errors. Triage them in the right order."

## Reference files

- [`references/error-patterns.md`](references/error-patterns.md) - common compiler error families, likely root causes, and preferred first checks.
