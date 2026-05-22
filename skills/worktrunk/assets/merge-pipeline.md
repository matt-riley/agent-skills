# `wt merge` pipeline

## Pipeline steps (in order)

| Step | Description |
| --- | --- |
| 1. Commit | Commit any staged/unstaged changes in the worktree |
| 2. Squash | Squash all branch commits into a single commit with an LLM message |
| 3. Rebase | Rebase the branch onto the target branch |
| 4. Pre-merge hooks | Run `[[pre-merge]]` hooks (blocking CI gate) |
| 5. Merge | Merge the branch into the target |
| 6. Pre-remove hooks | Run `[[pre-remove]]` hooks (stop processes, clean resources) |
| 7. Cleanup | Remove the worktree from disk |
| 8. Post-remove + post-merge hooks | Background notifications and follow-up tasks |

## Important: squash requires `[commit.generation]`

The squash step calls the configured LLM command to generate a commit message. If `[commit.generation]` is not configured, `wt merge` will hang waiting for stdin.

**Safe default when LLM is not configured:**

```sh
wt merge --no-squash
```

See [`llm-commits-setup.md`](llm-commits-setup.md) for configuration.

## Flags

| Flag | Description |
| --- | --- |
| `--no-squash` | Skip the squash step; preserve individual commits |
| `--no-commit` | Skip the initial commit step |
| `--no-rebase` | Skip rebase onto target |
| `--no-remove` | Skip worktree removal after merge |
| `--no-ff` | Force a merge commit even when fast-forward is possible |
| `--stage <all\|tracked\|none>` | Control what is staged before commit (`all` = git add -A, `tracked` = git add -u, `none` = only already-staged) |
| `--format=json` | Output structured merge result to stdout (useful for automation) |
| `--yes` | Skip approval prompts (for non-interactive automation) |

## Local CI pattern

Gate merges on passing tests and lint:

```toml
# .config/wt.toml
[[pre-merge]]
test = "cargo test"
lint = "cargo clippy"
```

The pre-merge hooks run concurrently. A non-zero exit code from any command aborts the merge.

## Comparison: `wt merge` vs manual steps

| Capability | `wt merge` | Manual |
| --- | --- | --- |
| Commit uncommitted changes | ✅ `--stage` flag | `git add && git commit` |
| LLM squash commit message | ✅ squash step | `git rebase -i` + write message |
| Rebase onto target | ✅ automatic | `git rebase <target>` |
| Pre-merge CI gate (hooks) | ✅ `[[pre-merge]]` | Manual or CI only |
| Merge into target | ✅ | `git merge` |
| Remove worktree | ✅ | `git worktree remove` |
| JSON output for automation | ✅ `--format=json` | Not available |

## When to use `--no-squash`

- Preserving individual commit history in the target branch
- Reviewer wants to see per-commit diffs in a PR
- `[commit.generation]` is not configured (avoids stdin hang)
- Branch has carefully authored commits that should not be collapsed

## `wt step` sub-commands

`wt step` exposes the individual pipeline stages for fine-grained control:

| Sub-command | Description |
| --- | --- |
| `wt step commit` | Stage and commit changes using LLM commit message |
| `wt step squash` | Squash branch commits with LLM squash message |
| `wt step rebase` | Rebase branch onto target |
| `wt step push` | Push branch to remote |
| `wt step copy-ignored` | Copy gitignored files from primary worktree to current worktree |

Use `wt step` to build custom pipelines or to run individual steps interactively without triggering the full merge flow.
