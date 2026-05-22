# Parallel agent recipes

Practical recipes for running multiple agents in parallel with isolated worktrees.

## One-shot alias: create worktree + launch agent

```sh
# Add to ~/.zshrc or ~/.bashrc
alias wsc='wt switch --create --execute=claude'

# Create a worktree and launch Claude with a task prompt
wsc feature-auth -- 'Add JWT authentication'
wsc fix-pagination -- 'Fix the off-by-one in page cursor'
wsc write-api-tests -- 'Write tests for the REST API'
```

Monitor all agents with live status, CI, and activity markers:

```sh
wt list
# Branch         Status       HEAD±   main↕  CI   Message
# feature-auth   ↑ 🤖                 ↑2    ●    Add JWT auth
# fix-pagination ↑ 💬                 ↑1    ●    Fix cursor bug
# write-api-tests  🤖                 ↑3    ◌    Write API tests
```

`🤖` — agent working, `💬` — agent waiting for input.

## Dev server per worktree

Each worktree gets a stable, unique port derived from the branch name via `hash_port`.

```toml
# .config/wt.toml
[post-start]
server = "npm run dev -- --port {{ branch | hash_port }}"

[list]
url = "http://localhost:{{ branch | hash_port }}"

[pre-remove]
stop = "lsof -ti :{{ branch | hash_port }} -sTCP:LISTEN | xargs kill 2>/dev/null || true"
```

`hash_port` maps any string to a port in `10000–19999` deterministically — `feature-auth` always
gets the same port regardless of machine or time. `wt list` shows the URL column with each
worktree's server (dimmed if the port isn't listening).

## Database per worktree

Each worktree gets an isolated Docker Postgres container. A two-step pipeline sets up names and
ports as per-branch variables, then later hook steps reference them.

```toml
# .config/wt.toml

[[post-start]]
set-vars = """
wt config state vars set \
  container='{{ repo }}-{{ branch | sanitize }}-postgres' \
  port='{{ ("db-" ~ branch) | hash_port }}' \
  db_url='postgres://postgres:dev@localhost:{{ ("db-" ~ branch) | hash_port }}/{{ branch | sanitize_db }}'
"""

[[post-start]]
db = """
docker run -d --rm \
  --name {{ vars.container }} \
  -p {{ vars.port }}:5432 \
  -e POSTGRES_DB={{ branch | sanitize_db }} \
  -e POSTGRES_PASSWORD=dev \
  postgres:16
"""

[pre-remove]
db-stop = "docker stop {{ vars.container }} 2>/dev/null || true"
```

Notes:
- `("db-" ~ branch) | hash_port` gives a different port to the DB than the dev server.
- `sanitize_db` produces a lowercase, underscore-safe DB name with a short hash suffix to avoid collisions.
- The connection string is accessible from the shell too: `DATABASE_URL=$(wt config state vars get db_url) npm start`

## Cold-start elimination

Copy gitignored files (`node_modules/`, `target/`, `.env`) from the primary worktree to a new
one before installing, so the install reuses cached packages instead of downloading from scratch.

```toml
# .config/wt.toml
[[post-start]]
copy = "wt step copy-ignored"

[[post-start]]
install = "npm ci"
```

The `[[post-start]]` pipeline syntax ensures `copy` completes before `install` runs.

To limit what gets copied, add a `.worktreeinclude` file at the repo root with glob patterns
(files must be both gitignored AND listed in `.worktreeinclude` to be copied).

## Activity markers for custom workflows

Set status markers manually for any workflow — same markers that agent harnesses use automatically:

```sh
wt config state marker set "🚧"                     # current branch
wt config state marker set "✅" --branch feature     # specific branch
wt config state marker set "🤖"                      # agent working
wt config state marker set "💬"                      # agent waiting
```

Clear a marker:

```sh
wt config state marker set ""
```

## Monitoring all branches (including those without worktrees)

```sh
wt list --full --branches
```

Shows CI pipeline status (●/◌/✗), line diffs since merge-base, and LLM-generated branch
summaries for every branch — including branches that don't have a local worktree checked out.

CI indicators are clickable links to the PR or pipeline page.

## Per-branch variables

Store arbitrary state per branch, accessible from hook templates as `{{ vars.key }}`:

```sh
wt config state vars set env=staging
wt config state vars get env
```

Use cases:
- Stick a branch to a deployment environment (`{{ vars.env | default("dev") }}`)
- Parametrise aliases per branch
- Coordinate state across pipeline steps (see Database recipe above)
