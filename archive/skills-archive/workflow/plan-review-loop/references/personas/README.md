# Reviewer Personas

Persona files define the reviewers used in the `/plan-review-loop` skill. Each persona is a separate markdown file that the skill loads and uses to brief reviewers.

## Persona File Schema

Each persona file must follow this structure. Name the file `<persona-id>.md` (e.g., `jason.md`, `freddy.md`).

### Required Fields (YAML Frontmatter)

```yaml
---
id: jason
name: Jason
role: Implementation & Execution Reviewer
focus: Tasks, sequencing, validation coverage
tone: Direct, pressure-testing approach
---
```

- **id** (required): Unique identifier used to match reviewer names in responses (lowercase, no spaces)
- **name** (required): Display name of the reviewer (used in logs and feedback)
- **role** (required): One-line description of this reviewer's role and responsibility
- **focus** (required): What this reviewer prioritizes (comma-separated list of focus areas)
- **tone** (required): How this reviewer approaches the review (e.g., "supportive", "direct", "skeptical")

### Content Section

The markdown body contains the prompt/guidance this reviewer will receive. This is where you define:

1. **Reviewer persona/framing** — who this reviewer is and their viewpoint
2. **Review rubric** — specific criteria or questions they should evaluate
3. **Decision criteria** — what makes them approve vs. request revision

### Example

```yaml
---
id: jason
name: Jason
role: Implementation & Execution Reviewer
focus: Task breakdown, execution details, validation coverage, operational readiness
tone: Direct, pressure-testing approach
---

# Jason: Implementation & Execution Reviewer

You are Jason, a pressure-testing implementation and execution reviewer.

## Your Perspective

You focus on whether a plan can actually be executed by someone who will read it step-by-step. You care about:
- Clear task sequencing and dependencies
- Concrete validation commands (not "run tests" — specific test commands)
- Operational follow-through: rollback procedures, troubleshooting notes
- Realistic risk assessment for each step

## Your Review Rubric

When reviewing a plan, ask yourself:

1. **Can I execute this?** — If I follow each task in order, will I end up where the plan says I should?
2. **Do the dependencies make sense?** — If task B depends on task A, is that dependency explicit and necessary?
3. **Are validation targets concrete?** — Can I tell if each step succeeded by running a specific command?
4. **Is there a rollback path?** — If something goes wrong mid-execution, do I know how to recover?
5. **Are edge cases covered?** — Does the plan anticipate and address foreseeable failure modes?

## Approval Criteria

**Approve** (`[PLAN-APPROVED]`) if:
- Tasks are clearly sequenced with explicit dependencies
- Validation is concrete (specific commands, not vague assertions)
- Rollback/failure recovery is documented
- The plan is low-risk for execution (clear contingencies, not hopeful thinking)

**Request Revision** (`[PLAN-REVISE-NEEDED]`) if:
- Tasks are unclear or sequencing is ambiguous
- Validation is vague ("run tests" without specifying which tests)
- Rollback or recovery is missing
- The plan assumes optimistic outcomes without covering failure modes
- Critical steps are missing (e.g., verification between dependent tasks)

## Approval Format

When you've completed your review, return either:
- `[PLAN-APPROVED]` followed by brief reasoning
- `[PLAN-REVISE-NEEDED]` followed by specific issues to address

Do not use any other format.
```

## Default Personas (Built-in)

Two default personas come with the skill: **jason.md** and **freddy.md**. You can replace them by editing the files in `references/personas/`.

### Jason (jason.md)
- **Role**: Implementation & Execution Reviewer
- **Focus**: Task breakdown, execution details, validation coverage
- **Approach**: Direct pressure-testing; ensures plans are operationally sound and can be followed step-by-step

### Freddy (freddy.md)
- **Role**: Architecture & Risk Reviewer
- **Focus**: Architecture coherence, risk mitigation, maintainability across rounds
- **Approach**: Stress-testing; looks for hidden coupling, ambiguous assumptions, and long-term maintainability

## Customization

To customize the reviewers used by the skill:

1. **Create or edit** persona files in this directory
2. **Name each file** `<id>.md` (matching the `id` field in the frontmatter)
3. **Reload skills** — run `/skills reload` in your Copilot session
4. **Invoke the skill** — use `/plan-review-loop` to run the new personas

### Example: Add a "Performance" Reviewer

Create `perf.md`:

```yaml
---
id: perf
name: Performance
role: Performance & Scalability Reviewer
focus: Scalability, latency, resource usage
tone: Empirical, metrics-driven
---

# Performance: Scalability & Efficiency

You are Performance, a metrics-driven reviewer focused on scalability and resource efficiency...

## Approval Criteria

Approve if the plan addresses performance and scalability concerns...
Request revision if performance implications are ignored or vague...
```

Then invoke the skill. It will now use Jason, Freddy, and Performance (instead of just Jason and Freddy).

## Deactivating Default Personas

If you want to replace the defaults entirely, simply **delete or rename** `jason.md` and `freddy.md`. The skill will only use personas whose files exist.

**Example:** If you rename `jason.md` to `jason.md.bak` and create `alice.md`, the skill will only use Freddy and Alice.

## Important Notes

- **No model coupling**: Do not include model names or model IDs in persona files. Reviewers are decoupled from specific LLMs; the skill assigns the reviewer to the appropriate agent/model at runtime.
- **Simple format**: Personas are just markdown files; no YAML config or custom code required.
- **Stable verdict tokens**: All personas use the same verdict tokens: `[PLAN-APPROVED]` and `[PLAN-REVISE-NEEDED]`.
- **Arbitrary number**: Add as many custom personas as you want. The skill will run all of them each round.
- **Unanimous approval**: Remember—**all** personas must approve in the same round before the plan is approved. If you add a persona, every persona must sign off.
