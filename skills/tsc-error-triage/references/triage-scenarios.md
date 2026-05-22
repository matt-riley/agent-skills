# Triage scenarios

Use these scenarios to check that compiler triage still starts at the first causal error and does not get trapped fixing noisy leaf failures.

| Scenario | What it usually means | First move | Maintenance note |
| --- | --- | --- | --- |
| One type change fans out into many assignment errors | A shared source type or helper regressed | Fix the shared export, helper, or generic before touching consumers | Update this row when a new high-fanout root cause appears |
| A new `TS2305`/missing export error appears before many downstream failures | The import surface or re-export chain broke | Inspect the defining module and the barrel/re-export path first | Keep this row aligned with the repo's current module layout |
| `TS7006` implicit `any` starts after a wrapper/refactor | A callback signature or generic context was lost | Restore the source function type instead of annotating every caller | Add the smallest new example that reproduces the lost inference |
| `cannot find module` or duplicate symbol errors follow a config change | `tsconfig`, paths, or declaration resolution changed | Check the active config boundary before editing imports broadly | Refresh this row when compiler mode or path aliasing changes |
| Leaf errors mention `string | undefined` vs `string` after a shared helper change | The helper is now too weakly typed | Tighten the helper return type, then rerun before fixing call sites | Keep the helper example short and truthful |

## Checklist

- Identify the earliest error that can explain the widest blast radius.
- Fix the source type, export, or config boundary first.
- Re-run typecheck before spending time on downstream leaf errors.
- Only edit leaf call sites after the shared cause is confirmed fixed.
