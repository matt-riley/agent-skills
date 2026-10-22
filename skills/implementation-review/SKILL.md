---
name: implementation-review
description: "Review completed code changes, diffs, and implementation revisions for merge readiness, or draft and harden an implementation plan before work starts (plan mode). Use for code review, plan review, named reviewer approval, validation gaps, regressions, security risk, or scope drift."
license: GNU GPL v3
metadata:
  version: 1.6.0 # x-release-please-version
  owner: mattriley
  category: governance
  audience: general-coding-agent
  maturity: stable
  kind: task
---

# Implementation review

## Use this skill when

- The user asks for code review, implementation review, diff review, PR review, or merge-readiness review
- The user wants named reviewer models or agents to approve a completed implementation
- The user wants a review focused on correctness, regressions, validation gaps, security issues, rollout safety, or scope drift
- The user wants to compare completed work against an approved plan, issue, PR description, or stated requirements
- The user wants an implementation, rollout, or migration plan drafted or hardened, or reviewer-gated plan approval before implementation (plan mode)

## Do not use this skill when

- The main task is applying reviewer feedback or writing new code rather than assessing the current implementation
- The implementation is still fluid with no stable revision to review; if an approach needs shaping, use plan mode instead
- Review is one phase inside a larger multi-step execution; use `rpi-workflow` instead

## Plan mode

When the deliverable is a plan rather than finished work, follow `references/plan-review.md`: draft or update the plan first, then review it for repo fit, feasibility, validation, rollout safety, and scope.

- Reviewer-gated, multi-round approval uses the personas in `references/plan-review-personas/` with the verdict tokens in `references/plan-review-review-verdicts.md`, unanimous per round, three rounds at most.
- Reviewer prompts: `references/plan-review-reviewer-prompt.md`. Worked cases: `references/plan-review-examples.md`. Near misses: `references/plan-review-edge-cases.md`.
- A plan is never "approved" by the same agent that wrote it; prefer a different model family, as for code review.

## Inputs to gather

**Required before reviewing**

- The target repo or workspace and the exact review target: working tree diff, branch, PR, commit range, or file set
- The stated scope boundaries, requirements, or user goal for the implementation
- Current validation evidence such as tests, builds, lint results, or manual checks
- The governing docs for that repo or workspace, such as `README.md`, stack manifests, `.github/copilot-instructions.md`, `AGENTS.md`, and nearby task-specific instructions

**Helpful if present**

- The approved plan, issue, PR description, or research artifact the implementation should satisfy
- The requested reviewer panel, model list, or approval rule
- Known risk areas, rollout constraints, or security-sensitive surfaces
- A short summary of what changed and why

**Only investigate if encountered**

- Whether the implementation changed after review started and the reviewed revision needs to be re-frozen
- Whether claimed validation is stale, missing, or mismatched with the actual diff
- Whether part of the change is intentionally deferred so it should be recorded as a follow-up instead of a blocker

## First move

1. Identify the exact review target and freeze the revision being reviewed.
2. Read the governing instructions plus the approved plan or requirements, if they exist.
3. Gather the diff, changed files, and validation evidence before asking for approvals.
4. Decide whether this is advisory review only or an approval-gated completion check.

## Workflow

1. **Confirm the review target and freeze the revision.**
   - Identify whether the review applies to a working tree diff, branch, PR, commit range, or specific file set.
   - If you are not already operating in the target repo or workspace, switch context before reviewing.
   - Read the repo-local instructions and any nearby plan, issue, PR, or research context.

2. **Gather review context before asking for approval.**
   - Collect the current diff, changed files, validation results, and any stated scope boundaries.
   - If there was an approved plan or explicit requirements, compare the implementation against them.
   - If the implementation is still moving, make the reviewed revision explicit before review starts.

3. **Choose the review mode deliberately.**
   - If the user names reviewer models or agents, use exactly that reviewer set.
   - If the user requires an approval gate, the implementation is not final until every required reviewer approves.
   - If the user only asked for review, still stress-test for correctness, regressions, validation gaps, security issues, rollout safety, and scope drift.
   - When invoked from a review command (`/review`, `/pr`), stay read-only and report every finding as `path:line`, tagged with its severity and verdict impact.
   - When you choose the reviewers yourself, prefer a different model family from the one that wrote the change; same-family reviewers tend to share its blind spots. Say which family reviewed if it matters.

4. **Review on two separate axes, against one shared revision.**
   - **Standards:** does the diff follow the repo's documented standards (`AGENTS.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, lint configs)? Cite the file and rule for each violation. Add the smell baseline in `references/reviewer-prompt.md` as labelled judgement calls ("possible Feature Envy"), never hard violations. A documented repo standard overrides the baseline, and anything tooling already enforces is skipped.
   - **Spec:** does the diff do what the issue, plan, or PR description asked? Report missing or partial requirements, behaviour nobody asked for (scope creep), and requirements that look implemented but wrong, quoting the spec line for each. With no spec, say so and skip this axis.
   - Run the two axes as separate reviewers (parallel subagents when the harness has them) so one does not mask the other. Report them under separate headings and do not re-rank findings across axes.
   - Every reviewer sees the same revision, diff, and validation summary and returns `APPROVE` or `REQUEST_CHANGES`, required changes, optional suggestions, and rationale. Load `references/reviewer-prompt.md` when preparing reviewer prompts.
   - **Blast radius:** name the one fact the change is safe because of (for example "this call only drops already-dead cache entries"), then look past the diff for what grep will not show: wire formats, persisted data, flags, other readers of the same bytes. Push that fact as far down this ladder as is cheap and say where it stopped: (1) asserted, (2) pointed at a real `file:line`, (3) walked the bad case and showed it cannot happen, (4) ran a script or test that calls the real code. Anything short of (4) is reported as **unproven**.

5. **Consolidate findings without blurring review and implementation.**
   - Merge duplicate findings within an axis; prioritize blockers over optional polish.
   - If any reviewer requests changes, surface those findings and stop — do not execute the fixes unless the user explicitly asked for both review and fixes in one pass.
   - When the user has addressed the requested changes, re-run the full reviewer set on the updated revision before considering the review complete.
   - Do not drop, swap, or skip reviewers mid-process unless the user explicitly changes the review panel.

6. **Finalize when the implementation is review-complete.**
   - All required reviewers have approved.
   - Validation status is current and explicit.
   - Remaining risks, follow-ups, or deferred work are called out.
   - Do not present reviewer feedback execution as done unless the implementation was actually updated and re-reviewed.

## Outputs

- A frozen review target (diff, branch, PR, commit range, or file set) paired with the current validation evidence for that revision.
- Consolidated blocker and optional findings tied to correctness, regression risk, security, rollout safety, and stated requirements.
- `## Standards` and `## Spec` findings reported separately, each as `path:line` with severity.
- The safety fact and how far it was proven (or **unproven**).
- A clear review verdict for the requested mode: advisory, blocked by requested changes, or approved under the required reviewer rule.

## Guardrails

- **Must** focus on materially important issues: correctness, regression risk, validation gaps, rollout safety, security issues, and unintended scope changes.
- **Must not** substitute style nitpicks for substantive review findings; smell-baseline hits stay labelled judgement calls, never blockers on their own.
- **Must not** merge or re-rank Standards and Spec findings into one list.
- **Must not** silently rewrite code as a substitute for producing a clear review outcome.
- **Must** preserve existing user changes and unrelated work while assessing the review target.
- **Should** compare the implementation against the approved plan or requirements when those exist.
- **Should** treat follow-up fixes as a separate implementation step unless the user explicitly asks for both review and fixes in one pass.
- **Before finishing:** confirm reviewer status matches the latest round, blockers and optional suggestions are clearly separated, validation is current, and the implementation-readiness verdict plus next step are stated explicitly.

## Validation

- Confirm the reviewed revision, diff, and validation evidence are current.
- State whether the review is advisory, blocked by requested changes, or approved under the requested rule.
- Keep blockers, optional suggestions, residual risks, and follow-up work clearly separated.
- If named reviewers or models are unavailable in the current harness, say so and provide the best available single-review result instead of pretending approvals occurred.

## Reference files

- Read `references/examples.md` when you need concrete trigger examples or a response shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
- Read `references/reviewer-prompt.md` when preparing or normalizing reviewer prompts for a round.
