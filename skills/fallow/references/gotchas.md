# Fallow gotchas

These are the traps most likely to break an agent workflow or create unsafe cleanup advice.

## Machine-readable output needs clean stdout

- Use `--format json --quiet` whenever an agent will parse the output.
- Redirect stderr to `/dev/null` if you need to guarantee clean stdout.
- Do not use `2>&1`; progress lines and warnings can corrupt the JSON stream.

## Exit code 1 means "findings", not "tool failed"

Fallow uses three important exit paths:

| Code | Meaning | Agent response |
| --- | --- | --- |
| `0` | No error-severity findings | Normal success |
| `1` | Findings were reported | Keep the output; this is usually the expected analysis result |
| `2` | Runtime or config error | Treat as the real failure path |

For non-interactive one-shot analysis commands, append `|| true` so findings do not abort the surrounding workflow.

## `fix` needs explicit non-interactive confirmation

- `fallow fix --dry-run` previews the cleanup.
- `fallow fix --yes` applies it in a non-TTY environment.
- Running `fix` without `--yes` in an agent context can fail with exit code 2.

## `--changed-since` is incremental, not full-repo

`--changed-since <ref>` only reports findings in files changed since that ref. That is good for PR gates and bad for full audits.

## `--workspace` scopes output, not dependency analysis

Fallow still builds the full module graph across workspaces. The flag narrows which findings are reported, not which imports are resolved.

## `--production` changes what counts

Production mode excludes test/dev files and changes dependency expectations. Do not use it when you want a full-repo hygiene pass.

## Fallow is syntactic, not the TypeScript compiler

- Dynamic import patterns can produce findings that need manual review or suppression.
- Type-level narrowing and runtime-only behavior are outside Fallow's model.
- If the question is "why does tsc fail?" or "why did this runtime break?", route away from this skill.

## `watch` is interactive

Never run `fallow watch` in an agent workflow. Use one-shot commands instead.

## Trace before deleting

If an export, file, or dependency looks unused but the reachability story is surprising, use a trace command before suggesting deletion. This is especially important around barrel files, dynamic imports, scripts, and monorepo package edges.
