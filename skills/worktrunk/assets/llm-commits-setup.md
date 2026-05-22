# LLM commit message generation

## How it works

Worktrunk builds a templated prompt containing the diff, stat, branch name, and recent commits, then pipes it to an external command via `sh -c`. The command reads from stdin and writes the commit message to stdout. Any tool that follows this stdio contract works.

Config lives in `~/.config/worktrunk/config.toml` under `[commit.generation]`.

## Config blocks by tool

### Ollama — recommended for corporate/firewalled environments

Runs fully locally, no outbound API calls.

```toml
[commit.generation]
command = "ollama run llama3.2 --nowordwrap"
```

Or any other locally-pulled model: `ollama list` to see what's available.

### Codex

```toml
[commit.generation]
command = "codex exec -m gpt-5.1-codex-mini -c model_reasoning_effort='low' -c system_prompt='' --sandbox=read-only --json - | jq -sr '[.[] | select(.item.type? == \"agent_message\")] | last.item.text'"
```

### llm CLI

```toml
[commit.generation]
command = "llm -m claude-haiku-4.5"
```

### aichat

```toml
[commit.generation]
command = "aichat -m claude:claude-haiku-4.5"
```

### LLM CLI tools — example configurations

> **Note:** The examples below show common LLM CLI tools. Use the configuration that matches your installed agent CLI or LLM tool.

```toml
[commit.generation]
command = "CLAUDECODE= MAX_THINKING_TOKENS=0 claude -p --no-session-persistence --model=haiku --tools='' --disable-slash-commands --setting-sources='' --system-prompt=''"
```

- Unsets any nesting guard so the call works standalone
- `--no-session-persistence` prevents polluting `claude --continue` history

## Branch summary setup

Enable one-line LLM summaries per branch in `wt list --full` and the `wt switch` interactive picker (tab 5):

```toml
[list]
summary = true
```

Summaries are generated lazily and cached. They appear in `wt list --full` and as tooltip text in the picker.

## Template variables

These variables are available in `template` and `squash-template`:

| Variable | Description |
| --- | --- |
| `{{ git_diff }}` | Full diff of staged changes |
| `{{ git_diff_stat }}` | Diffstat summary |
| `{{ branch }}` | Branch name |
| `{{ repo }}` | Repository name |
| `{{ recent_commits }}` | Recent commit messages on the branch |
| `{{ commits }}` | All commits being squashed (squash only) |
| `{{ target_branch }}` | Target branch for the squash (squash only) |

## Custom template example

Override the default prompt with a short one-liner style:

```toml
[commit.generation]
command = "llm -m claude-haiku-4.5"
template = """
Write a single-line conventional commit message (max 72 chars) for this diff.
Output only the message, no explanation.

Branch: {{ branch }}
Diff stat:
{{ git_diff_stat }}

Diff:
{{ git_diff }}
"""
```

## Fallback when unconfigured

When `[commit.generation]` is not set, Worktrunk generates a deterministic commit message from the changed filenames. No LLM call is made. This is always safe but produces less descriptive messages.

**Do not run `wt merge` without `--no-squash` when `[commit.generation]` is unconfigured** — the squash step will hang waiting for stdin.

## Where LLM generation is used

| Operation | Uses LLM? |
| --- | --- |
| `wt step commit` | Yes — commit message |
| `wt step squash` | Yes — squash message |
| `wt merge` (default) | Yes — squash step |
| `wt merge --no-squash` | No |
| `wt list --full` with `summary = true` | Yes — branch summaries |
