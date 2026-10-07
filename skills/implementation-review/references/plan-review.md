<!-- Merged from the former `plan-review` skill. -->

# Plan review

## Use this skill when

- The user asks for an implementation plan, rollout plan, migration plan, or a hardened revision of an existing plan
- The user is already planning or wants review-gated planning before implementation begins
- The user wants named reviewer models or agents to approve the plan
- The user explicitly asks for reviewer-gated or multi-round approval, Jason/Freddy-style review, or `[PLAN-APPROVED]` / `[PLAN-REVISE-NEEDED]` verdict tokens on an existing plan
- The user wants stronger plan quality checks around repo fit, feasibility, validation, rollout safety, or scope control

## Do not use this skill when

- The main task is reviewing finished code, a diff, or merge readiness; use `implementation-review` instead
- The user only wants a contract-shaped brief or definition of done with no plan artifact; use `reverse-prompt` if explicit success and failure framing is the main output
- The user explicitly wants immediate implementation with no planning artifact or review gate
- The user wants the larger Research → Plan → Implement → Validate operating model; use `rpi-workflow` instead

## Inputs to gather

**Required before drafting or reviewing**

- The target repo or workspace and the exact user goal
- Scope boundaries, constraints, and any explicit non-goals
- The governing docs for that repo or workspace, such as `README.md`, stack manifests, `.github/copilot-instructions.md`, `AGENTS.md`, and nearby task-specific instructions
- Any existing plan artifact, research artifact, issue, or ticket that already defines the work

**Helpful if present**

- The requested reviewer panel, model list, or approval rule
- Known rollout risks, migration constraints, or coordination points with other repos or teams
- Expected validation commands, success criteria, or release checks
- Whether the plan should live in a workspace `plan.md` or in a repo-local artifact

**Only investigate if encountered**

- Whether the repo already has a current plan revision that should be updated instead of replaced
- Whether ambiguous requirements need clarification before the plan can be considered executable
- Whether there are prior rejected approaches or reviewer comments that must carry forward into the next revision

## First move

1. Identify the target repo or workspace and find the current plan artifact, if one exists.
2. Read the governing instructions and nearby context before rewriting the plan.
3. Clarify the review rule: advisory review, named reviewers, or unanimous approval gate.
4. Draft or update the plan itself before asking anyone to approve it.

## Workflow

1. **Read governing instructions and existing context.**
   - If you are not already operating in the target repo or workspace, switch context first.
   - Review existing plan artifacts, research, or issue context before drafting.

2. **Draft or update an executable plan.**
   - Capture the problem, intended approach, phased tasks, validation commands, risks, and explicit scope boundaries.
   - Prefer saving the plan to a workspace `plan.md` unless the user explicitly wants the plan stored inside the repo.
   - Revise the actual plan artifact, not just a chat summary.

3. **Choose the review mode deliberately.**
   - If the user names reviewer models, agents, or personas, use exactly that reviewer set.
   - If the user explicitly requests reviewer-gated or multi-round approval, use the Jason and Freddy personas under `references/plan-review-personas/` unless the user names another reviewer set.
   - If the user requires an approval gate, the plan is not final until every required reviewer approves.
   - If the user only asked for a plan, still pressure-test for feasibility, testing, rollout, and scope discipline.

4. **Run review rounds on a single shared revision.**
   - Every reviewer must see the same current plan revision.
   - Each reviewer should return exactly one verdict token: `[PLAN-APPROVED]` or `[PLAN-REVISE-NEEDED]`, followed by required changes or approval rationale.
   - When using the structured persona path, load `references/plan-review-review-verdicts.md` so token parsing, unanimous same-round approval, and the three-round limit stay consistent.
   - Load `references/plan-review-reviewer-prompt.md` when preparing reviewer prompts.

5. **Consolidate and iterate on the plan itself.**
   - Merge duplicate comments; prioritize blockers over polish.
   - If any reviewer requests changes, update the plan artifact and re-run the full reviewer set on the new revision.
   - Do not drop, swap, or skip reviewers mid-process unless the user explicitly changes the review panel.

6. **Finalize when the plan is executable.**
   - All required reviewers have returned `[PLAN-APPROVED]` in the same round when reviewer-gated mode is active.
   - Remaining assumptions or open questions are explicit in the plan.
   - The next implementation step is clear.
   - Stop at the planning handoff unless the user asks to implement or a broader approved workflow says to continue.

## Outputs

- A revised executable plan artifact covering phased work, validation commands, scope boundaries, assumptions, and notable risks.
- Reviewer-by-reviewer verdicts on the current plan revision, with required changes separated from optional suggestions.
- A final planning status of approved, blocked for revision, or advisory-only, plus the next implementation step.


## Guardrails

- **Must** keep planning and research read-only unless the user explicitly asks for implementation.
- **Must** ground the plan in the actual target repo structure, tooling, and constraints.
- **Must** keep scope boundaries, non-goals, and validation strategy explicit in the plan.
- **Must not** turn this into finished-code review or merge-readiness review.
- **Must** keep reviewer-gated mode explicit: do not invent a multi-round approval loop unless the user asks for reviewer-gated or multi-round approval.
- **Must not** mark a structured review approved unless every configured reviewer returns `[PLAN-APPROVED]` in the same round.
- **Must** stop structured reviewer rounds after three complete rounds and report not approved if unanimity is not reached.
- **Should** call out risky migrations, coordination dependencies, or rollout hazards directly in the plan.
- **Before finishing:** confirm reviewer status matches the latest round, the plan is approved or explicitly blocked, and the next step is stated.

## Validation

- Confirm the plan artifact reflects the latest reviewed revision.
- Confirm required reviewer status is current: approved, blocked by requested changes, or advisory-only.
- Confirm validation commands, success criteria, open assumptions, and the next implementation step are explicit.
- If named reviewers or model-based approval is unavailable in the current harness, state that limitation instead of fabricating approval.
- For structured mode, confirm each reviewer emitted exactly one recognized verdict token and that the round stayed within the three-round limit.

## Output checklist

- problem statement
- phased plan
- validation strategy
- reviewer status by round
- open assumptions or blockers
- next step

## Reference files

- Read `references/plan-review-examples.md` when you need concrete trigger examples or a response shape to mirror.
- Read `references/plan-review-edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
- Read `references/plan-review-reviewer-prompt.md` when preparing reviewer prompts or consolidating a review round.
- Read `references/plan-review-review-verdicts.md` when you want structured Jason/Freddy-style verdict tokens and same-round approval rules.
- Read `references/plan-review-personas/README.md` when you want to use or customize the Jason and Freddy reviewer personas.
- [`references/plan-review-personas/jason.md`](references/plan-review-personas/jason.md) — Jason persona (implementation/execution risk focus)
- [`references/plan-review-personas/freddy.md`](references/plan-review-personas/freddy.md) — Freddy persona (architecture/structural risk focus)
