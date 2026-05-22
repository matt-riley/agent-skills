# Tsconfig hardening scenarios

Use this reference when sequencing strictness or resolution changes without widening scope.

## Sequence to prefer

1. Capture the baseline with the current typecheck command and `tsc --showConfig` or the nearest equivalent.
2. Clean the config chain first:
   - duplicates
   - conflicting `include` / `exclude`
   - stale `paths`, `baseUrl`, or `types`
   - accidental divergence across packages that should share a base config
3. Tighten flags in small batches:
   - `noImplicitAny`
   - `strictNullChecks`
   - `noImplicitOverride`
   - `noUncheckedIndexedAccess`
   - `exactOptionalPropertyTypes`
   - `noPropertyAccessFromIndexSignature`
4. Re-run typecheck after each batch. If `tsconfig` affects emit or declaration generation, also run the build.
5. If errors spike or spread, stop adding flags and triage root causes first.

## Stop thresholds

- error count rises sharply instead of shrinking
- failures move from one area to many unrelated files
- a batch would mix strictness with emit, module, or resolution changes
- the next step requires project references, bundler config, or runtime tooling changes

## Do-not-widen cases

- Do not change `module`, `moduleResolution`, `outDir`, or declaration emit unless they are the root cause.
- Do not enable several noisy flags at once.
- Do not absorb compiler-error cleanup into the hardening diff; hand off to `tsc-error-triage` when needed.
- Do not widen into project references unless the real problem is package graph coordination.

## Common scenario checklist

| Scenario | Move first | Stop when |
| --- | --- | --- |
| Fresh strictness pass | baseline + duplicate cleanup | the first batch is understood |
| One noisy flag causes many errors | isolate the flag | fixes become cross-cutting |
| Config drift across packages | normalize the shared base config | package intent is clear |
| Resolution issue during hardening | verify paths and includes before flags | the root cause is no longer config shape |
| Emit-related churn appears | separate emit from strictness | the change has one purpose again |

## Maintenance loop

- Update this file when the preferred flag order or stop threshold changes.
- Keep `SKILL.md` pointing here so the maintenance path stays discoverable.
