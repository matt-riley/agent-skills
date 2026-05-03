---
name: plan-review-loop
description: Use after `/plan` to run explicit plan review loops with customizable Jason and Freddy reviewers; replace the old ambient extension-based review with an explicit skill-driven workflow.
metadata:
  category: workflow
  audience: planning-agent
  maturity: beta
  kind: reference
---

# Plan review loop

Use this skill to run structured plan reviews after `/plan` completes, with customizable reviewer personas and explicit approval gates.

## Use this skill when

- A `/plan` is complete and you want reviewers (Jason and Freddy by default) to analyze it
- You need to customize the default reviewers or add new personas for specialized feedback
- You want explicit control over the review loop timing and termination (after approval or 3 rounds, whichever comes first)
- You want to iterate on a plan based on reviewer feedback

## Do not use this skill when

- You do not yet have a completed `/plan` to review (use `/plan` first)
- You need ad-hoc human review outside the structured skill workflow (do that separately)
- The decision is already made and the plan is final (no review needed)

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
- This SKILL.md passes the skill-authoring validator: `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/plan-review-loop/SKILL.md`

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
- [`references/personas/jason.md`](references/personas/jason.md) — Jason persona (implementation/execution focus)
- [`references/personas/freddy.md`](references/personas/freddy.md) — Freddy persona (architecture/risk focus)
- [`assets/smoke-test-prompts.md`](assets/smoke-test-prompts.md) — manual validation scenarios (5 test cases: approve, revise, mixed, max-rounds, persona-swap)
