---
name: worktrunk
description: "Use when a user needs to configure or operate Worktrunk (wt) for worktree lifecycle management, hooks, LLM commits, or parallel agent workflows."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: version-control
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# Worktrunk

Use this skill when a user needs to configure `wt`, set up LLM commit messages, author project hooks, or run multiple parallel agent lanes with isolated worktrees.

## Use this skill when

- User asks how to configure Worktrunk (`wt config`, `~/.config/worktrunk/config.toml`, `.config/wt.toml`)
- User wants to set up LLM-generated commit messages or branch summaries
- User needs to author or debug hooks (`post-start`, `pre-merge`, etc.)
- User is setting up parallel agent workflows with `wt switch --create --execute=…`
- User asks about `wt merge`, `wt step`, or the merge pipeline
- User is debugging shell integration or worktree path layout

## Do not use this skill when

- `wt --version` fails — Worktrunk is not installed; suggest `brew install worktrunk`
- A disposable clone is preferred over a worktree
- The task only needs raw `git worktree` commands — route to the `git-worktrees` skill instead
- The task is primarily about creating a PR, watching checks, or post-push review flow — route to [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md)

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| `wt` installed; user wants hooks or config | Yes | — |
| User wants raw `git worktree add/remove` only | No | `git-worktrees` skill |
| User needs PR/check workflow after pushing branch | No | `github-cli-pr-workflow` skill |
| `wt --version` fails | No | Suggest `brew install worktrunk` |
| Disposable clone, not a worktree | No | `git clone` directly |
| Implementation complete; deciding how to integrate branch | No | [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) |

## Inputs to gather

**Required before editing**

- Is this config setup, hook authoring, or a parallel agent workflow?
- Does `~/.config/worktrunk/config.toml` already exist? (`wt config show`)

**Helpful if present**

- Project type (Node, Rust, Python, etc.) for hook examples
- Whether LLM commit generation is desired and which LLM tool is available

## First move

1. `wt --version` — confirm install (a current version is required; install via `brew install worktrunk` if missing)
2. `wt config show` — inspect active config and file locations
3. `wt config create` — scaffold user config if missing; `wt config create --project` for project config

## Workflow

1. **Configure worktree path** — set `worktree-path` in user config (inside-repo `.worktrees/` is recommended for agent harness worktree-manager compatibility)
2. **Set up LLM commits** — add `[commit.generation]` block; see [`assets/llm-commits-setup.md`](assets/llm-commits-setup.md)
3. **Add project hooks** — author `.config/wt.toml` hooks for install, dev server, DB, CI gates; see [`assets/hooks-reference.md`](assets/hooks-reference.md)
4. **Enable branch summaries** (optional) — `[list] summary = true` in user config
5. **Run parallel agents** (optional) — use `wt switch --create --execute=<agent>`; see [`assets/parallel-agents-recipes.md`](assets/parallel-agents-recipes.md)

## Guardrails

- **Must** check `wt --version` before using any `wt` commands; fall back to raw git if Worktrunk is not installed.
- **Must not** bypass project hooks (post-start, pre-merge) without explicit justification.
- **Should** use `wt merge` for squash+rebase+cleanup in preference to manual git steps.
- **Should** configure `[commit.generation]` before relying on `wt step commit` for LLM messages.
- **May** use `--no-squash` when commit granularity matters for the PR.

## Outputs

- A configured `wt` setup: user and/or project config files (`~/.config/worktrunk/config.toml`, `.config/wt.toml`), authored hooks, and optionally LLM commit generation enabled
- Working worktrees or parallel agent lanes as requested, verified with `wt list` and `wt config show`

## Validation

```sh
wt config show                              # confirms settings loaded
wt switch --create test-wt-check           # creates worktree, fires hooks
wt list                                    # confirms branch with status markers
wt remove test-wt-check                   # cleans up
```

- Smoke test:
  - should trigger: "Configure wt hooks and parallel lanes for this repo."
  - should not trigger: "Create a raw git worktree for a one-off fix." (→ `git-worktrees`)

## Examples

- **Set up LLM commit messages for this repo:**
  ```sh
  wt config show              # inspect current config location
  # add [commit.generation] block — see assets/llm-commits-setup.md for provider options
  wt switch --create test-llm-check
  # make a small change, then `wt merge` to confirm LLM message is generated
  ```

- **Add a post-start hook that runs `npm ci` and starts the dev server:**
  ```toml
  # .config/wt.toml
  [[hooks.post-start]]
  command = "npm ci && npm run dev -- --port {{.Port}}"
  ```

- **Configure parallel agent lanes with unique ports per worktree:**
  ```sh
  wt switch --create agent-lane-1 --execute="copilot agent start"
  wt switch --create agent-lane-2 --execute="copilot agent start"
  wt list   # shows both lanes with status markers
  ```

## Reference files

- [`assets/hooks-reference.md`](assets/hooks-reference.md) — all hook types, template variables, filters, pipeline syntax
- [`assets/merge-pipeline.md`](assets/merge-pipeline.md) — `wt merge` pipeline, flags, and `wt step` sub-commands
- [`assets/llm-commits-setup.md`](assets/llm-commits-setup.md) — LLM commit generation config for Claude Code, Codex, llm CLI, aichat
- [`assets/parallel-agents-recipes.md`](assets/parallel-agents-recipes.md) — one-shot alias pattern, dev server per worktree, DB per worktree, cold-start elimination
- [`references/config-reference.md`](references/config-reference.md) — complete config key reference with defaults
