---
name: implementation-review
description: "Review completed code changes, diffs, and implementation revisions for merge readiness. Use for code review, named reviewer approval, validation gaps, regressions, security risk, or scope drift."
license: GNU GPL v3
metadata:
  version: 1.4.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

# Implementation review

## Use this skill when

- The user asks for code review, implementation review, diff review, PR review, or merge-readiness review
- The user wants named reviewer models or agents to approve a completed implementation
- The user wants a review focused on correctness, regressions, validation gaps, security issues, rollout safety, or scope drift
- The user wants to compare completed work against an approved plan, issue, PR description, or stated requirements

## Do not use this skill when

- The main task is drafting or hardening a plan; use `plan-review` instead
- The main task is applying reviewer feedback or writing new code rather than assessing the current implementation
- The implementation is still fluid and no stable revision, diff, or review target has been identified yet
- Review is one phase inside a larger multi-step execution; use `rpi-workflow` instead

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

4. **Run review rounds on a single shared revision.**
   - Every reviewer must see the same revision, diff, and validation summary.
   - Each reviewer should return: `APPROVE` or `REQUEST_CHANGES`, required changes, optional suggestions, and approval rationale.
   - Load `references/reviewer-prompt.md` when preparing reviewer prompts.

5. **Consolidate findings without blurring review and implementation.**
   - Merge duplicate findings; prioritize blockers over optional polish.
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
- A clear review verdict for the requested mode: advisory, blocked by requested changes, or approved under the required reviewer rule.


## Workflow

See the body and references for review rounds and consolidation steps.

## Guardrails

- **Must** focus on materially important issues: correctness, regression risk, validation gaps, rollout safety, security issues, and unintended scope changes.
- **Must not** substitute style nitpicks for substantive review findings.
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
