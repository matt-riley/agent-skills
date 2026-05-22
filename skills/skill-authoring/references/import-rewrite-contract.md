# Import rewrite contract

Use this document when rewriting an upstream skill into this local library. All three wave 1 imports — `code-tour`, `autoresearch`, and `agentic-eval` — must satisfy this contract before their packages are considered complete.

## Preserve vs. discard

### Preserve from upstream

- The core capability: the skill's central workflow concept, technique, or pattern.
- Concrete examples, representative artifacts, and schema references that make the workflow easier to apply.
- Any support file that materially reduces repeated work and can be adapted to the local package shape.
- Upstream safety rules that are at least as strong as the local rules (keep the stricter set).

### Discard from upstream

- Non-local frontmatter keys: `license`, `compatibility`, `author`, `inspired-by`, and any provenance or attribution fields — these belong in a commit message or a separate PROVENANCE note if you need to preserve attribution, not in frontmatter.
- Description blocks that lead with domain labels or workflow summaries instead of trigger phrases.
- Headings that do not match the stable local section names (adapt, do not carry forward upstream heading variations).
- Hard-coded absolute paths to skill locations outside this repository.
- Git operations that are unsafe under local policy — specifically `git reset --hard` as a primary loop revert and `git commit --amend` in automated or repeated sequences. Rewrite these using local-safe patterns.
- Python or shell scripts that cannot be kept generic and self-contained, or that duplicate what the existing local validator already covers.
- Inline code examples promoted as the primary skill content when a reference file or `assets/` example would keep `SKILL.md` concise.

## Canonical top-level shape

### Task skill

Use `metadata.kind: task` for multi-step playbooks with explicit inputs, outputs, and validation steps.

```
---
name: <kebab-case, matches directory>
description: "Use when <trigger phrase 1>, <trigger phrase 2>, or <trigger phrase 3>. Prefer over-triggering to under — <scope boundary if adjacent skills exist>."
metadata:
  category: <authoring|ci|migrations|typescript|version-control|workflow|...>
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# <Skill name>

One-paragraph activation lead.

## Use this skill when
## Do not use this skill when
## Routing boundary
## Inputs to gather
## First move
## Workflow
## Outputs
## Guardrails
## Validation
## Examples
## Reference files
```

### Reference skill

Use `metadata.kind: reference` for lookup-heavy guidance where the main value is navigation, conventions, or examples rather than a step-by-step playbook.

Replace `## Inputs to gather`, `## First move`, `## Workflow`, and `## Outputs` with a concise navigation block that makes support-file discovery obvious. Keep `## Use this skill when`, `## Do not use this skill when`, `## Routing boundary`, `## Guardrails`, `## Validation`, `## Examples`, and `## Reference files`.

## Frontmatter expectations

| Field | Required | Valid values / rules |
| --- | --- | --- |
| `name` | Yes | Lowercase kebab-case. Must match the skill directory name exactly. No spaces, uppercase, or special characters. |
| `description` | Yes | 50–120 characters. Must start with a trigger phrase ("Use when", "Use this when", or equivalent). Never a domain label alone. Never a workflow summary. |
| `metadata.category` | Recommended | `authoring`, `ci`, `migrations`, `typescript`, `version-control`, `workflow`, or a concise domain label. |
| `metadata.audience` | Recommended | `general-coding-agent` unless the skill is narrowly specialized. |
| `metadata.maturity` | Recommended | `draft` for new imports; `stable` only after smoke-test validation and live use. |
| `metadata.kind` | Required for new skills | `task` or `reference`. |

**Do not add** `license`, `compatibility`, `author`, `inspired-by`, or any other top-level keys not listed above.

**Multiline description blocks with embedded bullet lists are not valid.** Keep the description as a single quoted string. If the trigger conditions are complex, put them in `## Use this skill when` instead.

## Section and heading expectations

Every imported skill must use these stable section names. Do not carry forward upstream heading variations.

| Section | Task skill | Reference skill | Notes |
| --- | --- | --- | --- |
| H1 title | Required | Required | Must match the `name` field in plain words. |
| One-paragraph activation lead | Required | Required | A single paragraph that says when to use the skill. |
| `## Use this skill when` | Required | Required | Bullet list of specific trigger conditions. |
| `## Do not use this skill when` | Required | Required | At least two route-away conditions when adjacent skills exist. |
| `## Routing boundary` | Required | Required | Markdown table: Situation / Use this skill? / Route instead. |
| `## Inputs to gather` | Required | Omit | Three sub-sections: Required / Helpful if present / Only investigate if encountered. |
| `## First move` | Required | Omit | Numbered list. Three steps maximum. |
| `## Workflow` | Required | Omit | Numbered list. Sequential and actionable. |
| `## Outputs` | Required | Omit | Bullet list of artifacts or end-state expectations. |
| `## Guardrails` | Required | Required | Bullet list including safety-critical constraints. |
| `## Validation` | Required | Required | At least one mechanical check and one smoke-test. |
| `## Examples` | Required | Required | Three realistic user-request examples. |
| `## Reference files` | Required | Required | One entry per support file, linked and annotated. |

## Support-file decision rules

| Condition | Put it in |
| --- | --- |
| Lookup-heavy detail, conventions, schemas, or patterns that would bloat `SKILL.md` | `references/` |
| Reusable templates, starter artifacts, or worked examples that agents copy | `assets/` |
| Automation that removes repeated work, can stay generic and self-contained, and cannot be replaced by a reference file | `scripts/` |
| Upstream script that duplicates what `validate-skill-library.mjs` already covers | Remove |
| Upstream script in a non-portable language or with hard-coded paths | Rewrite or remove |

Every support file must be linked directly from `## Reference files` in `SKILL.md`. Do not add support files that are not referenced there.

## Routing and activation expectations

The `description` field is the primary activation signal. It must:

- Lead with a trigger phrase, not a domain label or capability summary.
- Name the specific situations or request patterns that should fire the skill.
- Include at least one scope boundary ("not when X is more appropriate") when adjacent skills exist.
- Never summarize the workflow — an agent reading only the description must know whether to invoke the skill, not how to execute it.

The `## Routing boundary` table must include at least one row that routes away from this skill to a named adjacent skill, so activation between nearby skills stays unambiguous.

## Validation expectations

Each imported skill package must pass both mechanical and behavioral validation before it is considered done.

### Mechanical

```bash
node skills/skill-authoring/scripts/validate-skill-library.mjs skills/<name>/SKILL.md
```

This checks `name`/directory match, description length, trigger phrase presence, frontmatter syntax, and no missing required keys.

### Smoke test (behavioral)

Write two prompts for each imported skill: one that should trigger it and one near-miss that should not. Confirm the `description` field alone (not the SKILL.md body) distinguishes the two without ambiguity.

Example format (record these in `## Validation` inside the skill):

```
- should trigger: "<realistic request that clearly applies>"
- should not trigger: "<near-miss that should route elsewhere>"
```

### Consistency check

Read the completed `SKILL.md` as the target agent. The next action must be obvious within a few seconds of reading it. If it is not obvious, the workflow or first-move sections need tightening.

## Per-skill notes

### code-tour

- **Kind:** `task`
- **Category:** `workflow`
- **Preserve:** The `.tour` JSON format concept and file schema, persona-targeting approach, step types (file/line, selection, pattern, uri, commands, view), and the discover-then-write workflow phases.
- **Support file decision:** The upstream schema JSON (`codetour-schema.json`) is worth keeping in `references/` as a look-up artifact. The upstream `examples.md` is worth keeping in `references/` as real-world tour examples. The two Python scripts (`validate_tour.py`, `generate_from_docs.py`) need evaluation — keep them only if they stay generic, self-contained, and earn a clear callout in `SKILL.md`; otherwise summarize their checks in a `references/validation-notes.md` instead.
- **Remove from upstream:** The hardcoded `~/.agents/skills/code-tour/scripts/...` paths, the long inline table of production GitHub repo URLs (move to `references/examples.md` or an assets file), and the `CRITICAL: Only create .tour JSON files` warning styled as uppercase — convert to a guardrail bullet.
- **Routing:** Route against `acquire-codebase-knowledge` (exploration without a tour output) and `context-map` (pre-edit mapping rather than a narrative walkthrough).
- **Safety rule:** Do not modify any non-`.tour` file during skill execution. Keep this as a guardrail, not a CRITICAL all-caps warning.

### autoresearch

- **Kind:** `task`
- **Category:** `workflow`
- **Preserve:** The setup → branch → loop → report phase structure, the measurable metric contract (goal, command, extraction, direction, scope, constraints, budget), the results TSV format, the simplicity policy concept, and the experiment strategy priority order (low-hanging fruit first, diversify after plateaus, combine winners, etc.).
- **Support file decision:** The results TSV format and the experiment strategy priority order work well as a `references/experiment-guide.md`. The phase-by-phase setup questions can become an `assets/setup-template.md` that an agent fills in instead of prose.
- **Rewrite for local safety — required:** The upstream loop uses `git reset --hard HEAD~1` as the standard revert and `git commit --amend` in crash recovery. Both violate local repo safety policy for automated or repeated sequences. Replace with: use the dedicated experiment branch as the safety boundary; revert bad experiments by creating a new commit that reverts the previous one (`git revert HEAD --no-edit`) rather than a hard reset; omit `--amend` from the automated loop entirely.
- **Remove from upstream:** `license`, `compatibility`, `metadata.author`, `metadata.inspired-by` frontmatter keys; the interactive question-and-answer framing (the skill should state what to gather, not mimic a questionnaire); the `---` horizontal rule dividers between phases (not local style).
- **Routing:** Route against `test-driven-development` (when the task is writing tests, not optimizing a measurable metric) and `systematic-debugging` (when the goal is diagnosing a specific failure, not iterative optimization).

### agentic-eval

- **Kind:** `reference`
- **Category:** `workflow`
- **Rationale for reference vs. task:** The upstream content is pattern-and-rubric guidance rather than a single sequential playbook with fixed inputs and outputs. Agents adopt it selectively depending on whether they are building a reflection loop, an evaluator-optimizer, or a rubric check. This fits the reference skill shape better than task.
- **Preserve:** The generate→evaluate→critique→refine loop concept and diagram, the three evaluation strategies (outcome-based, LLM-as-judge, rubric-based), the best-practices table (clear criteria, iteration limits, convergence check, log history, structured output), and the implementation checklist.
- **Support file decision:** Move the Python code examples from `SKILL.md` to `assets/examples.md` or `references/patterns.md` to keep `SKILL.md` concise. Keep the implementation checklist as `assets/eval-checklist.md` if it is genuinely reused.
- **Remove from upstream:** The `## Overview` and `## When to Use` non-standard headings (map to local heading names), inline Python code blocks as primary skill content (move to `assets/`), missing routing table and route-away conditions, missing `metadata` block.
- **Routing:** Route against `verification-before-completion` (verifying that completed work meets acceptance criteria, not iterating on output quality), `systematic-debugging` (diagnosing a specific root cause, not evaluating output quality), and `javascript-testing-expert` (writing test coverage, not an evaluation loop).
- **Activation boundary:** This skill applies when an agent is _designing_ or _implementing_ an evaluation loop; it does not apply when the agent is _running_ an existing test suite or _reviewing_ a completed artifact without iteration.
