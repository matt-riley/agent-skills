---
name: plan-review-loop
description: "Use when a completed /plan needs explicit multi-reviewer approval and refinement before implementation begins."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: planning-agent
  maturity: draft
  kind: task
---

# Plan review loop

Use this skill to run structured plan reviews after `/plan` completes, with customizable reviewer personas and explicit approval gates.

## Use this skill when

- A `/plan` is complete and you want reviewers (Jason and Freddy by default) to analyze it before implementation begins
- A plan was revised after reviewer feedback and needs another structured approval round
- You want documented approval gates with explicit verdict tokens before committing to an implementation
- You need feedback from implementation-risk and architectural-risk perspectives on the same plan

## Do not use this skill when

- You do not yet have a completed `/plan` to review (use `/plan` first)
- You need ad-hoc human review outside the structured skill workflow (do that separately)
- The decision is already made and the plan is final (no review needed)

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| A finished plan needs structured multi-reviewer approval before implementation | Yes | — |
| You want stress-testing of a design and CONTEXT.md updated | No | [`grill-with-docs`](../grill-with-docs/SKILL.md) |
| You want fast informal critique without a full review loop | No | [`grill-me`](../grill-me/SKILL.md) |
| The plan is already approved and implementation has started | No | proceed with implementation |

## Inputs to gather

**Required**

- A completed `/plan` output from the current session

**Optional**

- Custom reviewer personas (default: Jason and Freddy) defined in `references/personas/`
- Prior reviewer feedback to incorporate if re-invoking for another round

## First move

1. After `/plan` completes, invoke the skill explicitly: `Use the /plan-review-loop skill to review and refine the current plan`
2. Reviewers analyze the plan according to their personas and rubrics
3. Each reviewer returns a verdict token: `[PLAN-APPROVED]` or `[PLAN-REVISE-NEEDED]`
4. If all return `[PLAN-APPROVED]` in the same round → plan is ready
5. If any returns `[PLAN-REVISE-NEEDED]` → update your plan and invoke the skill again
6. If you reach 3 rounds without unanimous approval → the skill exits and you decide the next step

## Workflow

1. **Invoke:** After `/plan` finishes, explicitly request the review loop skill
2. **Review Round:** Each configured reviewer (Jason and Freddy by default) analyzes the plan
3. **Collect verdicts:** Reviewers return tokens; parse the explicit `[PLAN-APPROVED]` or `[PLAN-REVISE-NEEDED]`
4. **Decision:**
   - All reviewers return `[PLAN-APPROVED]` in the same round → ✅ plan is approved, proceed to implementation
   - At least one returns `[PLAN-REVISE-NEEDED]` → ❌ plan needs revision; update it and request another review
   - Round 3 completes without unanimous approval → ⏱️ max rounds reached; you decide next steps
5. **Customize (optional):** Edit or create `references/personas/*.md` to replace or add reviewers

## Outputs

- Approval verdict: unanimous `[PLAN-APPROVED]` in the same round (plan is ready to implement) or `[PLAN-REVISE-NEEDED]` with reviewer notes (plan needs revision)
- Round number when approval was reached or a statement that the 3-round maximum was hit without consensus

## Guardrails

- Do not modify the plan yourself between rounds; the skill parses reviewer tokens to determine completion status
- Do not exceed 3 review rounds without explicit decision outside this skill
- Verdict tokens are case-sensitive and exact: `[PLAN-APPROVED]` and `[PLAN-REVISE-NEEDED]` only
- Missing, malformed, or ambiguous tokens (multiple tokens in one response) block approval
- All configured reviewers must return a verdict in the same round for unanimous approval

## Validation

The skill validates successfully when:

- All persona files in `references/personas/` conform to the schema documented in `references/personas/README.md`
- Verdict tokens (`[PLAN-APPROVED]` / `[PLAN-REVISE-NEEDED]`) are preserved unchanged and exactly matched
- The round logic enforces a 3-round maximum and unanimous same-round approval requirement

- Smoke test:
  - should trigger: "Use Jason and Freddy to review this finished /plan before implementation."
  - should not trigger: "Stress-test this design and update CONTEXT.md as we go." (→ `grill-with-docs`)

## Examples

- **Approve path (happy path):**
  ```
  You: Use the /plan-review-loop skill to review and refine the current plan
  Jason: [PLAN-APPROVED] The tasks are well-structured and validation is solid.
  Freddy: [PLAN-APPROVED] Architecture is clear and risk mitigation is covered.
  Result: ✅ Plan approved! Ready to proceed.
  ```

- **Revise path (iteration):**
  ```
  You: Use the /plan-review-loop skill to review and refine the current plan
  Jason: [PLAN-REVISE-NEEDED] Missing rollback procedure in task 5.
  Freddy: [PLAN-APPROVED] Architecture looks good.
  Result: ❌ Not approved (Jason needs revision). Update the plan and request another round.
  ```

- **Customization:**
  ```
  Create or edit references/personas/alice.md to add a custom security reviewer.
  Then invoke: Use the /plan-review-loop skill with Alice, Jason, and Freddy as reviewers.
  ```

## Reference files

- [`references/personas/README.md`](references/personas/README.md) — persona schema, YAML frontmatter, and customization guide
- [`references/review-contract.md`](references/review-contract.md) — detailed verdict tokens, round rules, and approval criteria
- [`../plan-review/references/personas/jason.md`](../plan-review/references/personas/jason.md) — Jason persona (implementation/execution focus)
- [`../plan-review/references/personas/freddy.md`](../plan-review/references/personas/freddy.md) — Freddy persona (architecture/risk focus)
- [`assets/smoke-test-prompts.md`](assets/smoke-test-prompts.md) — manual validation scenarios (5 test cases: approve, revise, mixed, max-rounds, persona-swap)
