---
name: tsc-error-triage
description: "Diagnose and resolve TypeScript compiler errors by finding the smallest root-cause fix before editing call sites."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
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

## Iron Law

> **Never patch leaf errors when a shared root cause is unresolved.**
>
> Fix the first causal error in the chain — broken export, generic constraint, config mismatch — before touching downstream call sites.
> One root-cause fix can collapse dozens of leaf errors.

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
6. Look for one shared compiler snippet that points at a broken export, generic constraint, or config boundary.

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

## Routing boundary

- Use this skill when causal failures are source-type issues and need root-cause-first triage.
- Route to [`tsconfig-hardening`](../tsconfig-hardening/SKILL.md) when first causal failures point to compiler configuration, project references, or module-resolution drift rather than source typings.
- Route to [`project-references-migration`](../archived/project-references-migration/SKILL.md) (archived) when the main issue is an incomplete or inconsistent `tsc -b` / `composite` workspace migration.
- Route to [`type-test-authoring`](../type-test-authoring/SKILL.md) only after compiler stability is restored and you need compile-time regression locks.

## Validation

- Re-run the same typecheck command and confirm the targeted errors are gone.
- Check that no new class of compiler error was introduced nearby.
- Run targeted tests for the touched surface when the repository has them.
- Keep [`references/triage-scenarios.md`](references/triage-scenarios.md) in sync when a new root-cause pattern or noisy downstream failure shape becomes common.

- Smoke test:
  - should trigger: "Fix the tsc errors that exploded after yesterday's refactor."
  - should not trigger: "Turn on noImplicitAny across the repo safely." (→ `tsconfig-hardening`)

## Examples

- `tsc --noEmit` reports:
  ```text
  src/use.ts(8,12): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
  src/index.ts(3,1): error TS2305: Module '"./api"' has no exported member 'makeId'.
  ```
  Fix the missing export or shared generic first; the argument errors are downstream noise.
- `High-fanout fix`
  ```ts
  export function parseId(value: string | undefined): string {
    if (!value) throw new Error('missing id');
    return value;
  }
  ```
  One shared helper like this can collapse dozens of leaf errors once its return type is truthful.
- `Before`
  ```ts
  export const toId = (value) => value.toString();
  ```
  `After`
  ```ts
  export const toId = (value: string | number) => value.toString();
  ```

## Reference files

- [`references/error-patterns.md`](references/error-patterns.md) - common compiler error families, likely root causes, and preferred first checks.
- [`references/triage-scenarios.md`](references/triage-scenarios.md) - compact scenario matrix for root-cause-first compiler triage.
