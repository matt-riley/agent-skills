# Routing Boundaries and Decision Rules

## Iron Law

> **TESTS MUST PASS BEFORE OPTIONS 1–3 ARE PRESENTED**
>
> If tests are failing, do not present Options 1–3 (merge, PR, keep) — fix or report the failure first. The skill enforces this boundary: verify test status, present options only on green, handle blockers if red. **Exception:** Option 4 (Discard) is always available when the user explicitly wants to abandon the failing branch.

## Routing Boundary

| Signal | Route |
|--------|-------|
| Tests passing, ready to integrate | → Present Four Options |
| Tests failing or not run | → Fix or report; do not present options |
| User rejects all four options or requests custom flow | → Clarify intent; escalate if outside standard paths |
| Worktree is dirty (uncommitted changes) | → Commit/stage first, then proceed |

## Inputs to Gather (Summary)

- **Branch and base:** What feature/fix branch? What is the target base branch (main/develop)?
- **Test status:** Which tests are relevant? Have they all passed locally?
- **Worktree context:** Is this isolated in a git worktree or the main checkout?
- **Delivery preference:** Any organizational or project convention about PR vs. merge?
- **Audience:** Who reviews this? (PR needed if code review is required; otherwise merge is faster)

## First Move (Summary)

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

Then:
1. Verify worktree is clean (no uncommitted tracked changes; ignore untracked files)
2. Run all relevant tests locally and confirm they pass
3. If tests fail → fix and retest, report the failure, do not proceed to options
4. If tests pass → proceed to Four Integration Options section

See the main SKILL.md for the full high-level workflow and Guardrails. Detailed rules and long-form examples live in the other references files.