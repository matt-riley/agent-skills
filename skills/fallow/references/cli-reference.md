# Fallow CLI reference

Use this cheat sheet to choose the right command family before you run anything.

## Command selection

| Goal | Command | Use these flags first |
| --- | --- | --- |
| Find dead code and structural findings | `fallow dead-code` | `--format json --quiet`, then issue filters as needed |
| Find duplicate code | `fallow dupes` | `--format json --quiet`, `--mode`, `--threshold` |
| Review complexity and hotspots | `fallow health` | `--format json --quiet`, `--top`, `--sort`, `--score` |
| Run a changed-file quality gate | `fallow audit` | `--format json --quiet`, `--base`, `--gate`, `--fail-on-issues` |
| Preview or apply cleanup | `fallow fix` | `--dry-run` first, then `--yes` |
| Inspect project structure/plugins/boundaries | `fallow list` | `--files`, `--entry-points`, `--plugins`, `--boundaries` |
| Detect feature flag patterns | `fallow flags` | `--format json --quiet`, `--top` |
| Verify which config was loaded | `fallow config` | `--path` |
| Explain a single issue type | `fallow explain` | `<issue-type> --format json` |

## High-value issue filters

These flags scope `fallow dead-code` to the findings you actually want to inspect.

| Question | Flag |
| --- | --- |
| Which exports look unused? | `--unused-exports` |
| Which files are unreachable? | `--unused-files` |
| Which types are unused? | `--unused-types` |
| Which dependencies look unused? | `--unused-deps` |
| Which imports are missing from package metadata? | `--unlisted-deps` |
| Are there circular imports? | `--circular-deps` |
| Are there architecture boundary violations? | `--boundary-violations` |
| Which suppressions are stale? | `--stale-suppressions` |

Combine filters when you want the union of those finding types.

## Trace and explain workflows

Use these before deleting anything when the reachability story is not obvious.

| Need | Command |
| --- | --- |
| Why is this export used or unused? | `fallow dead-code --trace path/to/file.ts:exportName --format json --quiet` |
| How is this file connected to the graph? | `fallow dead-code --trace-file path/to/file.ts --format json --quiet` |
| Where is this dependency actually imported? | `fallow dead-code --trace-dependency package-name --format json --quiet` |
| Why did duplication fire here? | `fallow dupes --trace path/to/file.ts:42 --format json --quiet` |
| What does one issue type mean? | `fallow explain boundary-violations --format json` |

## Core scoping flags

| Scope | Flag | Note |
| --- | --- | --- |
| Changed files since a git ref | `--changed-since <ref>` | Reports only findings in changed files |
| Changed workspaces in a monorepo | `--changed-workspaces <ref>` | Auto-selects touched workspaces |
| One workspace/package | `--workspace <name-or-pattern>` | Scopes output, not graph construction |
| Production-only view | `--production` | Excludes test/dev files and changes dependency reporting |

## Duplication modes

| Mode | Best for |
| --- | --- |
| `strict` | Exact copy-paste matches |
| `mild` | Normalized syntax differences; safe default |
| `weak` | Similar logic with different literals |
| `semantic` | Similar logic with renamed identifiers |

## Exit-code reminder

| Code | Meaning |
| --- | --- |
| `0` | No error-severity issues |
| `1` | Findings were reported |
| `2` | Real runtime or config error |

In agent workflows, keep the analysis result and the process failure path separate: parse the JSON, then interpret exit code 2 as the actual tool failure condition.
