# Knip CLI reference

Use this file to choose the lightest Knip command family for the job.

## Report first

- `knip` - run the default report from the project root.
- `pnpm knip --max-show-issues 5` or `npm run knip -- --max-show-issues 5` - prefer the repository's existing package-manager entry point when one exists.
- `knip --config path/to/knip.json` - use a nonstandard config file or location.
- `knip --debug` - inspect the resolved workspaces, plugins, and file selection when the report looks surprising.
- `knip --max-show-issues 5` - keep large reports readable while you are tuning config.

## Scope the output

- `knip --production` - narrow the scan when the user only cares about production code and not tests, stories, or other non-production surfaces.
- `knip --strict` - tighten dependency checks in production mode when the workspace should be isolated.
- `knip --workspace <name-or-path>` - focus on one workspace in a monorepo while still letting Knip reason about the surrounding graph.

## Fix after preview

- `knip --fix` - apply cleanup after the report has been reviewed and the changes look safe.
- Re-run the plain report after fixes to confirm the remaining issues are the ones you expect.

## Trace suspicious results

- `knip --trace` - show where exports or dependencies are used when a result looks wrong.
- `knip --trace-file <path>` - trace one file when a specific export or dependency is in question.
- `knip --trace-export <name>` - trace one export when the issue is centered on a symbol.
- `knip --trace-dependency <name>` - trace where a dependency is imported.

## When a flag changes behavior

- Prefer `--config` when the config file is nonstandard instead of renaming files to fit the default search order.
- Prefer `--debug` when Knip appears to be scanning the wrong workspace or missing an expected entry file.
- Treat exit code 1 as "lint issues found"; confirm stderr and command output before calling the run itself broken.
- Avoid widening `entry` just to quiet unused-file reports; that can suppress useful unused-export findings from entry files.
