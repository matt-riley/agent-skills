# Experiment guide

Reference material for the `autoresearch` skill. Consult this during the experiment loop when choosing the next hypothesis or reviewing the log format.

## Experiment strategy

When generating the next experiment hypothesis, work through this priority order. Move down the list only after the current approach is exhausted or plateaued.

1. **Low-hanging fruit first** — simple parameter tweaks, obvious inefficiencies, redundant allocations, trivial algorithmic switches.
2. **Informed by results** — if a direction showed consistent improvement, explore further variations in that direction before diversifying.
3. **Diversify after plateaus** — if the last 3–5 experiments all resulted in `discard`, switch to a completely different approach or codebase area.
4. **Combine winners** — if experiment A and experiment B each improved the metric independently, try applying both together.
5. **Simplification passes** — periodically try removing code or reducing complexity to confirm the metric holds without the removed piece.
6. **Radical changes** — after exhausting incremental and diversified ideas, consider larger architectural changes. Flag these to the user before attempting if they touch public APIs or invariants.

## Results TSV format

The `results.tsv` file is the experiment journal. Keep it tab-separated and untracked.

**Header row:**

```
experiment	commit	metric	status	description
```

**Status values:**

| Value | Meaning |
| --- | --- |
| `baseline` | Measurement of unmodified code before any experiments (experiment 0) |
| `keep` | Experiment improved the metric; commit is retained on the branch |
| `discard` | Experiment did not improve; reverted with a revert commit |
| `crash` | Metric command failed or errored; reverted with a revert commit |

**Example rows:**

```
0	a1b2c3d	0.9979	baseline	unmodified code
1	b2c3d4e	0.9932	keep	increase cache size to 512
2	c3d4e5f	1.0050	discard	switch to eager evaluation
3	d4e5f6g	0.0000	crash	parallel write (segfault)
4	e5f6g7h	0.9901	keep	remove redundant lock acquisition
```

## Git safety patterns

These patterns replace the upstream `git reset --hard` and `git commit --amend` patterns, which are unsafe in automated loops.

### Reverting a bad experiment

Do not use `git reset --hard`. Use a revert commit instead:

```bash
git revert HEAD --no-edit
```

This adds a new commit that undoes the experiment. The branch history remains intact and the `results.tsv` log stays accurate.

### Reverting a crash with a failed fix attempt

If a crash experiment produced two commits (the experiment commit and an attempted fix commit):

```bash
git revert HEAD --no-edit    # reverts the fix attempt
git revert HEAD --no-edit    # reverts the original experiment
```

Never use `--amend` to alter commits in the loop. Amended commits make the results log unreliable because the recorded commit hash no longer exists.

### Branch hygiene

- All experiments happen on the `autoresearch/<tag>` branch.
- The `autoresearch/<tag>` branch is never merged into `main` or `develop` automatically — the user decides what to keep.
- `results.tsv` and `run.log` are added to `.git/info/exclude` and stay untracked throughout the session.

## Constraint handling

| Constraint type | Behavior |
| --- | --- |
| Time budget per run | If a run exceeds 2× the expected duration, interrupt it and treat as a crash. |
| Tests must stay green | Run the test suite after each `keep` decision. If tests regress, treat the experiment as `discard` regardless of metric improvement. |
| Memory or resource limit | Monitor resource usage; if usage exceeds the stated limit, treat as a crash. |
| No new dependencies | If a hypothetical change requires a new package, skip it and log as `skipped — requires dependency`. |
| API compatibility | Do not change exported signatures or public contracts unless the user explicitly approved. |
