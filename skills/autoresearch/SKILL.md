---
name: autoresearch
description: "Use when running autonomous iterative experiments to optimize a measurable metric on an existing codebase — not for writing tests or diagnosing a specific failure."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Autoresearch

Use this skill when the goal is to improve a specific, measurable outcome through repeated automated experiments — write a change, measure it, keep it or revert it, repeat. You define the metric; the agent runs the loop autonomously until interrupted or the budget is exhausted.

This is distinct from test-driven development (writing tests for behavior) and systematic debugging (diagnosing a known failure). Use this skill when optimization through iteration is the work.

## Use this skill when

- You want to iteratively improve a measurable outcome: execution time, bundle size, test pass rate, build time, latency, coverage, complexity, or a custom benchmark score.
- You have a metric command that produces a numeric result and you want the agent to run experiments autonomously until interrupted or a budget is reached.
- The right solution is not obvious upfront and you want to explore the space empirically.
- You want to hill-climb: keep changes that help, discard changes that do not, and log everything.

## Do not use this skill when

- The task is writing tests for a new feature or behavior (use `test-driven-development`).
- The goal is diagnosing why something is broken (use `systematic-debugging`).
- There is no measurable metric — the outcome is purely qualitative or subjective.
- The codebase does not have a git repository or the user has not confirmed a dedicated experiment branch is acceptable.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Writing failing tests before implementing a feature | No | `test-driven-development` |
| Diagnosing why a test or build is failing | No | `systematic-debugging` |
| Iteratively optimizing a benchmark or metric | Yes | — |
| Improving code quality with no numeric signal | No | `systematic-debugging` or `verification-before-completion` |
| Running a single targeted experiment to validate a hypothesis | No | Implement directly; this skill is for multi-experiment autonomous loops |

## Inputs to gather

**Required before editing**

- **Goal**: what you are trying to improve (e.g., execution time, pass rate, bundle size).
- **Metric command**: the exact shell command that produces the metric (e.g., `npm run benchmark`, `go test -bench=. ./...`, `hyperfine './build.sh'`).
- **Metric extraction**: how to pull the numeric value from the output (regex, JSON field, specific line).
- **Direction**: `lower_is_better` or `higher_is_better`.
- **In-scope files/directories**: what the agent is allowed to edit.
- **Out-of-scope files/directories**: what must not be touched.

**Helpful if present**

- **Max experiments**: a count or `unlimited` (default: unlimited, stop only on interrupt).
- **Constraints**: time budget per run, dependency policy, test-passing requirement, API compatibility, memory limits.
- **Simplicity policy**: default is "simpler is better — weigh complexity cost against improvement magnitude."

**Only investigate if encountered**

- Existing benchmark history or prior result logs.
- CI-enforced test gates that must stay green throughout the loop.

## First move

1. Confirm all required inputs are known. If the metric command or extraction method is unclear, ask before creating the branch.
2. Create a dedicated experiment branch: `git checkout -b autoresearch/<tag>` (use today's date as the tag, e.g., `autoresearch/2025-07-09`).
3. Run the metric command on the unmodified code and record the baseline value before any experiments begin.

## Workflow

### Phase 1: Setup confirmation

Summarize all parameters in a table before proceeding:

| Parameter | Value |
| --- | --- |
| Goal | … |
| Metric command | … |
| Metric extraction | … |
| Direction | lower is better / higher is better |
| In-scope files | … |
| Out-of-scope files | … |
| Constraints | … |
| Max experiments | … |
| Simplicity policy | … |

Do not start the loop until confirmed.

### Phase 2: Branch and baseline

1. Create branch: `git checkout -b autoresearch/<tag>`.
2. Read all in-scope files to build full context of the current state.
3. Initialize `results.tsv` in the repo root with the header row (see `references/experiment-guide.md` for the TSV format). Add `results.tsv` and `run.log` to `.git/info/exclude` so they stay untracked without modifying any tracked file.
4. Run the metric command on unmodified code. Record as experiment `0` with status `baseline`.
5. Report baseline to the user before starting the loop.

### Phase 3: Experiment loop

Run until `MAX_EXPERIMENTS` is reached or the user interrupts. Do not stop to ask permission between iterations.

For each experiment:

1. **Think** — analyze previous results and current code. Generate a hypothesis. Consult `references/experiment-guide.md` for strategy ordering (low-hanging fruit first, diversify after plateaus, combine winners, etc.).
2. **Edit** — modify only in-scope files. Keep changes focused and minimal per experiment.
3. **Commit** — `git add <changed files> && git commit -m "experiment: <short description>"`.
4. **Run** — execute the metric command. Redirect to `run.log` (`<command> > run.log 2>&1`).
5. **Measure** — extract the metric from `run.log`. If extraction fails, read the last 50 lines for the error.
6. **Decide**:
   - **Improved**: keep the commit. Update the running best.
   - **Same or worse**: revert with a revert commit — `git revert HEAD --no-edit`. Log status `discard`.
   - **Crash/error**: if a quick single-line fix is obvious, apply it in a new commit and re-run once. If still broken after one fix attempt, revert with `git revert HEAD --no-edit` (or revert both commits if two were made) and log status `crash`. Do not use `--amend` or `reset --hard`.
7. **Log** — append one row to `results.tsv`: `experiment_number  commit_hash  metric_value  status  description`.
8. **Continue** — go to step 1.

### Phase 4: Report

When the loop ends:

1. Print the full `results.tsv` as a formatted table.
2. Summarize: total experiments, kept / discarded / crashed counts, baseline vs. final metric, improvement percentage, top 3 most impactful changes.
3. Show the kept-commit log: `git log --oneline <start_commit>..HEAD`.
4. Recommend next steps: ideas that were too risky or complex for the automated loop.

## Outputs

- `autoresearch/<tag>` branch containing only kept (improving) experiment commits.
- `results.tsv` (untracked) — full experiment journal.
- `run.log` (untracked) — output from the most recent metric run.
- A written Phase 4 summary report in the chat.

## Guardrails

- Never modify out-of-scope files, even to make a failing metric run succeed.
- Never skip the measurement step. Every experiment must be measured before the keep/discard decision.
- Never use `git reset --hard` as a revert strategy. Always revert with a new commit (`git revert HEAD --no-edit`) to preserve history and avoid data loss.
- Never use `git commit --amend` in the loop. Amended history makes the results log unreliable.
- Never install new dependencies or change environment configuration without explicit user approval.
- Keep changes per experiment small. Large batched changes hide which modification drove the metric.
- Do not keep a change that improves the metric but regresses another metric the user named as a constraint.

## Validation

Mechanical:

```bash
node skills/skill-authoring/scripts/validate-skill-library.mjs skills/autoresearch/SKILL.md
```

Smoke tests:

- should trigger: "I want you to keep running experiments on my Go benchmark until you find a 10% speedup"
- should not trigger: "Write a failing test for the `parseUser` function before I implement it" (→ `test-driven-development`)
- should not trigger: "My CI pipeline is failing and I don't know why" (→ `systematic-debugging`)

Before each reporting step, apply `verification-before-completion`: confirm the `results.tsv` row count matches the experiment count and the final metric was measured from the last run.

## Examples

- "Run experiments on `src/compute.ts` to reduce the `npm run benchmark` p95 latency. Keep going until I stop you."
- "I want to minimize `go test -bench=. ./...` ns/op for the `BenchmarkSort` function. File a result log and tell me what you tried."
- "Hill-climb my Rust build time. The metric is `time cargo build --release`, lower is better. Only touch `Cargo.toml` and `src/`."

## Reference files

- `references/experiment-guide.md` — experiment strategy order, TSV format spec, git safety patterns, and constraint handling
- `assets/setup-template.md` — fillable setup table to confirm inputs before the loop starts
