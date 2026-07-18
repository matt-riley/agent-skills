---
name: finishing-a-development-branch
description: "Use when implementation work is complete and you need to decide how to integrate the branch — merging locally, creating a PR, keeping the branch, or discarding the work."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# finishing-a-development-branch

## Use this skill when

- Implementation work on a feature or fix is complete (all code changes made)
- All local tests pass consistently
- You need to decide the final integration path: merge, PR, keep, or discard
- A worktree or isolated branch exists and needs lifecycle resolution
- The agent needs a structured, repeatable decision boundary before handing off

## Do not use this skill when

- Tests are still failing or not yet run
- Implementation is incomplete or blocked
- The task is mid-flight and still under active development
- No tests exist and you have not established pass/fail status (fix or establish tests first)
- The user has already decided the integration method; skip directly to executing it

## Inputs to gather

**Required before editing**
- Branch and base, test status, worktree context, delivery preference, and audience (who will review).

**Helpful if present**
- Known CI expectations or org PR vs. merge conventions.

**Only investigate if encountered**
- Stale worktree metadata or dirty state.

See `references/routing-boundaries.md` for the full Iron Law, detailed routing table, and inputs.

## First move

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

1. Verify worktree is clean.
2. Run relevant tests and confirm they pass.
3. If tests fail, fix/report and stop (Option 4/Discard remains available).
4. If green, present the four options.

## Workflow

### Verify tests pass first (the gate)

Before any of Options 1–3, confirm all applicable tests for the changed files have run and pass consistently. Do not present merge/PR/keep options on red or un-run tests.

### Four Integration Options

1. **Merge locally** — checkout base, pull, merge, re-verify, delete branch, cleanup worktree.
2. **Push and create PR** — push, `gh pr create` with summary + test evidence, keep the worktree active.
3. **Keep as-is** — report branch + worktree location; no cleanup.
4. **Discard** — require explicit typed "discard" confirmation, force-delete, cleanup.

See `references/decision-rules.md` for cleanup rules, validation steps per option, and guardrails in practice.

## Outputs

- Chosen integration action executed and verified (branch state, PR link, or explicit discard + cleanup).
- Clean worktree (or intentionally retained for follow-up).
- Clear next-step communication to the user or subsequent workflow.

## Guardrails

- **Tests are the gate** — never present Options 1–3 unless tests are green. Announce blockers.
- **No false progress** — do not claim done until the chosen integration action has executed and been verified.
- **Dirty worktree / branch safety** — verify clean state and branch existence before acting.
- **Confirmation for destruction** — Option 4 requires the word "discard".
- **Idempotent cleanup** — use safe removal commands that succeed even if partially cleaned.

Full guardrails and "in practice" notes: `references/decision-rules.md`.

## Validation

After action:
- Confirm the chosen option's post-conditions (base updated + branch gone for merge; PR exists for option 2; location reported for keep; confirmation + deletion for discard).
- Smoke test cases are documented in `references/decision-rules.md`.

## Examples

See `references/examples.md` for the four complete worked examples (merge, PR, keep, discard) with commands and verification.

## Reference files

- `references/examples.md` — full multi-example transcripts with commands and outcomes.
- `references/routing-boundaries.md` — Iron Law, routing table, inputs, first-move summary.
- `references/decision-rules.md` — options details, cleanup rules, guardrails-in-practice, validation, integration notes.
- [`git-worktrees`](../git-worktrees/SKILL.md) — worktree lifecycle and `mr_worktree_remove`.
- [`worktrunk`](../worktrunk/SKILL.md) — prefer `wt` commands when available.
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — Option 2 PR + checks handoff.
- [`review-comment-resolution`](../review-comment-resolution/SKILL.md) — post-PR review feedback loops.
