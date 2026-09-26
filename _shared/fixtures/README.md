# Fixture evals

Deterministic checks for skills. A fixture is a small repo in a known-broken
state plus a `check.sh` that exits 0 only when the work is done. There is no
model in the verdict — it is a program's exit code, so scoring has no variance
and costs nothing to repeat.

## Layout

```
_shared/fixtures/<skill-name>/
├── TASK.md      # the prompt handed to the agent
├── check.sh     # PASS/FAIL verdict; accepts the workspace as $1
└── ...          # the broken repo itself
```

## check.sh contract

- Prints `PASS` and exits 0 when the work is genuinely done, otherwise prints a
  `FAIL: <reason>` line and exits non-zero.
- Takes the workspace to check as `$1`, defaulting to its own directory, so the
  runner can check a scratch copy using a pristine checker.
- Runs the real signal first (`tsc --noEmit`, `go test`, `actionlint`,
  `knip`, `goreleaser check`), then anti-gaming guards.
- Guards must catch the cheap ways to pass without doing the work: silencing the
  tool, weakening a type, editing the test that is the spec, adding ignore
  lists, deleting the job being diagnosed.
- Must be self-contained: set up anything it needs (a git remote for
  `goreleaser check`) instead of assuming the caller's environment.

## Fixture rules

- **No answer-revealing comments.** `# BUG:` notes belong in the commit message,
  not the fixture — an agent that reads "the matrix key is wrong" has been told
  the answer.
- One or two root causes with cascading symptoms, not a list of unrelated typos.
- The broken state must fail, and a genuine fix must pass. Verify both by hand
  when adding a fixture; there is no automated fix-direction test yet.

## Agent harness traps

- **Copy the skill into the workspace, never symlink it.** The agent may only
  read inside its workspace, so a linked `references/*.md` fails with
  permission denied and the skill is silently reduced to its `SKILL.md`.
  That alone took the `neovim-plugin-ci` fixture from 0/3 to 2/3.
- **Isolate the agent config home.** This Copilot CLI carries a user-level
  skill index and extensions, so a staged skill leaked into a workspace with
  none and both arms looked identical. Use `--isolated-home` for comparisons.
- **Check the agent output, not just the exit code**, when a result is
  surprising: the run that "failed" may have been a permission error.

## Usage

```bash
# prove every fixture still fails in its pristine state
python _shared/run-fixture-evals.py --check-only

# run the agent on one fixture, then check it (no model judges the result)
python _shared/run-fixture-evals.py --only tsc-error-triage

# same with the skill disabled, for a with/without comparison
python _shared/run-fixture-evals.py --baseline
```

`GORELESER` overrides the GoReleaser binary (defaults to `go run ...@latest`).

## Why these exist

Judge-scored cases have a measured noise floor of ~±0.13 on 7-case splits, which
makes a validation gate unable to certify realistic edits. These checks have no
judge: the agent is nondeterministic, the scoring is not. That turns the problem
from statistics back into engineering — run the agent k times and read the pass
rate.
