---
name: skill-authoring
description: "Use when creating or revising a reusable agent skill under skills/<name>/SKILL.md — deciding activation, layering, examples, or validation, or choosing between a skill vs. instructions vs. a specialized agent."
metadata:
  category: authoring
  audience: general-coding-agent
  maturity: beta
---

# Skill authoring

Use this skill when creating or revising a reusable agent skill under `skills/<name>/SKILL.md`, especially when you need to decide activation, layering, examples, and validation.

Treat this as the benchmark shape other skills should copy: concise activation, shallow support files, and an obvious first validation step.

## Use this skill when

- You are creating or revising a reusable agent skill under `skills/<name>/SKILL.md`.
- You need a reusable authoring standard for a local skill package with shallow support files.

## Minimum acceptance gate

A skill is ready to hand off when it:

- says exactly when to use it and when not to
- description includes specific trigger phrases (not just a domain label)
- keeps `SKILL.md` concise by pushing lookup-heavy detail into shallow support files
- includes at least one concrete example and one validation step
- makes the next action obvious without asking the reader to infer the workflow

## Frontmatter specification

Every skill requires a YAML frontmatter block at the start of `SKILL.md`. This block tells the skill authoring system and agents how to discover, validate, and invoke your skill.

### Required fields

**name** (string, required)
- Alphanumeric characters, hyphens, and underscores only
- No spaces, uppercase, special characters, or punctuation
- Must match the skill directory name exactly (e.g., `skills/reverse-prompt/SKILL.md` → name: `reverse-prompt`)
- Lowercase recommended for consistency
- Examples: ✓ `reverse-prompt`, ✓ `skill-authoring`, ✓ `test-driven-development`

**description** (string, required)
- Minimum 20 characters; aim for 50–120 characters
- Clear, one-line summary of when to use this skill
- Must include concrete trigger phrases like "when", "use when", or "use this" — never just a domain label
- Examples of good descriptions:
  - ✓ "Use when a request is under-specified, ambiguous, or needs sharpening before research, planning, or implementation"
  - ✓ "Migrate JavaScript or TypeScript test suites from Mocha, Chai, or Sinon to Jest in small verified batches"
  - ✓ "Use when TypeScript source contains explicit any outside test files"
- Examples of poor descriptions:
  - ✗ "skill" (too short, vague, no trigger phrase)
  - ✗ "Testing" (domain label only, no trigger phrase)
  - ✗ "Migrate code" (too vague, no specific context)

### Optional fields

**metadata** (object, recommended)
- **category** (string): One of `authoring`, `ci`, `migrations`, `typescript`, `version-control`, `workflow`, etc.
- **audience** (string): `general-coding-agent` or a specialized audience
- **maturity** (string): `stable`, `draft`, or other lifecycle stage
- **kind** (string, **required for draft skills**): `task` for multi-step playbooks; `reference` for lookup-heavy guidance. Must be set before a skill can be promoted from `draft` to `stable`.
- **reader_testing** (string, documented extension): `required` when reader-testing is a mandatory stage. See `references/metadata-contract.md` for the full list of allowed optional extensions.

**Do not add** `license`, `compatibility`, `author`, `inspired-by`, `argument-hint`, or any other top-level keys beyond `name`, `description`, and `metadata`. Do not add upstream provenance keys (`github-path`, `github-ref`, `github-repo`, `github-tree-sha`, `version`, `enhancements`) inside the `metadata` block. See `references/metadata-contract.md` for the full contract, rationale, and exception policy.

### Frontmatter example

```yaml
---
name: reverse-prompt
description: Use when a request is under-specified, ambiguous, or needs sharpening before research, planning, or implementation begins — or when the user explicitly asks to improve, rewrite, or reverse-prompt their ask.
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
---
```

### Validation checklist

The validator script (`scripts/validate-skill-library.mjs`) checks that:

- [ ] `name` matches the directory name (e.g., `skills/my-skill/SKILL.md` → `name: my-skill`)
- [ ] `name` contains only alphanumeric, hyphens, underscores (no spaces or special characters)
- [ ] `description` exists and is at least 20 characters long
- [ ] `description` includes a trigger phrase ("when", "use this", or "use when")
- [ ] No forbidden top-level keys (`argument-hint`, `compatibility`, `license`, `author`, `inspired-by`)
- [ ] No forbidden provenance keys in `metadata` (`github-path`, `github-ref`, `github-repo`, `github-tree-sha`, `author`, `inspired-by`, `version`, `enhancements`)
- [ ] `metadata.kind` is set to `task` or `reference` for all `draft` skills
- [ ] Frontmatter is properly delimited with `---` markers
- [ ] No syntax errors in YAML parsing

### Troubleshooting frontmatter issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "frontmatter name does not match directory" | Name in `---` block doesn't match folder | Rename the `name:` field to match the skill directory name |
| "name contains invalid characters" | Spaces, uppercase, or special characters in name | Use lowercase alphanumeric, hyphens, underscores only (e.g., `my-skill-v2`) |
| "description is too short" | Description under 20 characters | Expand description to at least 20 chars and include concrete trigger phrases |
| "missing frontmatter key name" or "description" | Frontmatter block incomplete | Add both `name:` and `description:` keys between `---` delimiters |
| "missing frontmatter block" | No `---` delimiters in SKILL.md | Add `---` at the top of the file and close the frontmatter with another `---` |
| "unterminated frontmatter block" | Only one `---` marker or no closing `---` | Ensure frontmatter is wrapped: `---` on first line and `---` after the last field |
| "forbidden top-level frontmatter key" | Extra keys like `license`, `argument-hint` at top level | Move content to `metadata`, `## Inputs to gather`, or `references/`; see `metadata-contract.md` |
| "forbidden provenance key metadata.*" | Upstream `github-*` or attribution fields inside `metadata` | Remove provenance fields; preserve attribution in a commit message or `PROVENANCE.md` |
| "metadata.kind is required for draft skills" | New skill missing `kind` field | Add `kind: task` or `kind: reference` under `metadata` |

### Running the validator

To validate a skill's frontmatter and structure:

```bash
node skills/skill-authoring/scripts/validate-skill-library.mjs [SKILL.md paths...]
```

Validate all skills:
```bash
node skills/skill-authoring/scripts/validate-skill-library.mjs
```

The validator will report specific issues and how to fix them.

## Do not use this skill when

- The guidance belongs in global instructions or a repository-wide policy file instead of a reusable skill.
- The workflow is so narrow or stateful that it belongs in a specialized agent instead of a reusable skill.
- The request is a one-off task description with no reuse value.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Create or revise a reusable skill package | Yes | - |
| Create or update agent instruction files (copilot-instructions.md, AGENTS.md) | No | [`agent-instructions`](../agent-instructions/SKILL.md) |
| Author collaborative documentation such as READMEs or runbooks | No | [`doc-coauthoring`](../doc-coauthoring/SKILL.md) |

## Inputs to gather

- The problem the skill should solve and the kinds of requests that should activate it.
- The intended audience, such as a general coding agent or a narrow specialist workflow.
- Whether the skill is primarily a `reference skill` or a `task skill`.
- Required inputs, constraints, examples, and common failure modes.
- The outputs, artifacts, or decisions the skill should leave behind.
- Nearby instructions, skills, or agents that may overlap.
- Any environment assumptions that truly matter, such as required tools or network access.
- Whether the skill should follow an existing local package shape or frontmatter convention.

## First move

1. Check whether the guidance belongs in a skill at all instead of a broader instruction file or a specialized agent.
2. Choose a concise kebab-case skill name that matches the directory name.
3. Start from `assets/skill-template.md` and keep the main `SKILL.md` focused on activation, first actions, and validation.

## Workflow

1. Define what should activate the skill and what should not. As you define activation,
   draft a description that enumerates the same trigger situations as explicit phrases.
   Lean toward over-triggering rather than under — but pair it with at least one
   disambiguator (a scope boundary or a route-away condition) so adjacent skills are
   not crowded out.
2. Decide whether the package is primarily a `reference skill` or a `task skill`:
   - `reference skill` = lookup-heavy guidance, conventions, and examples
   - `task skill` = multi-step workflow with explicit inputs, outputs, and validation
3. Use a predictable package shape so the skill is easy to scaffold, inspect, and validate later:
   - stable frontmatter
   - clear section headings
   - shallow support-file layout
   - direct links to every support file
4. Draft the top-level `SKILL.md` so the next action is obvious within a few seconds of reading it.
5. Keep the main skill file concise and move lookup-heavy detail into reference files.
6. For task skills, make outputs or handoff artifacts explicit. For reference skills, make discovery and support-file navigation explicit.
7. Add assets for reusable templates or examples when they make the workflow easier to apply.
8. Add scripts only when they remove repeated work and can stay generic, self-contained, and optional.
9. Link every support file from `SKILL.md` so an agent can discover it without guessing.
10. Validate the final package for naming, structure, layering, and discoverability.

## Guardrails

- Keep the skill focused on a reusable workflow, not a one-off task.
- Make the smallest reasonable generic assumptions; only stop for clarification when ambiguity would materially change the design.
- Do not duplicate instructions that belong in broader config or in a specialized agent.
- Do not force a task-skill output shape onto a reference skill, but do not leave a task skill without explicit outputs or validation.
- Keep support files shallow under the skill root and reference them directly from `SKILL.md`.
- Prefer `references/` before `scripts/` unless automation clearly reduces repeated work.
- Prefer standard section names when they fit so future authoring or validation tools can reason about the skill without guessing.
- A description that only names the skill's domain without listing concrete trigger phrases is likely to undertrigger — the skill will be skipped when it would help.
- **Red flag:** if the draft starts embedding repo policy, one-off orchestration, or environment-specific branching, move that content out of the skill.
- **Handoff trigger:** if the shape needs a dedicated operator persona, split orchestration, or long-lived state, promote it to a specialized agent instead of widening the skill.
- **Critical:** A description that summarises the skill's workflow causes agents to follow the description as a shortcut instead of reading the full skill body. Descriptions must only contain triggering conditions — what signals mean "read this skill now?" — never process summaries. (This was empirically documented by Jesse Lactin's obra/superpowers collection.)
- **Red flag:** A description that starts with a verb like "Migrate...", "Diagnose...", "Replace...", "Rewrite..." is almost certainly a workflow summary. Start with "Use when..." or a symptom/scenario.

## Anti-patterns

- Wrong layering: putting lookup tables, full templates, or repo-specific exceptions directly in `SKILL.md` when a shallow reference file would keep the package clearer.
- Over-specialized shape: baking in a single repository's path conventions, CI roles, or internal team process so the skill stops being reusable.
- Hidden workflow: making the skill feel like a note to the author instead of a playbook with activation, workflow, and validation.

## Validation

- Read the completed skill once as if you were the target agent and confirm the next action is obvious.
- Check the layering against `references/layering-guide.md`.
- Run the checklist in `references/checklist.md`.
- Run `scripts/validate-skill-library.mjs` after changing `SKILL.md`, `assets/`, or `references/`.
- Check that the package shape is predictable enough for future tool-assisted authoring:
  - frontmatter is present and matches the directory name
  - section headings are stable and easy to scan
  - support files are shallow and linked directly from `SKILL.md`
- Check that the skill's structure matches its kind:
  - task skills declare outputs or handoff artifacts plus validation
  - reference skills make the lookup value and support-file paths obvious
- Smoke-test the description: in a fresh session with only the skill loaded, send one
  realistic request that should trigger it and one near-miss that should not. The
  description alone (not the SKILL.md body) should be sufficient to distinguish them.
  If neither triggers reliably, the description needs more explicit trigger phrases.
- Description test: Cover the SKILL.md body and read only the description. Does it tell you *when* to use the skill, or *what the skill does*? If the latter — rewrite it. The description alone should distinguish "should I read this?" without revealing the workflow.
- If the target client supports skill reload or listing, verify the skill remains discoverable there.

## Examples

- "Turn this conventions-heavy note into a reference skill with a one-paragraph activation block, direct links to support files, and a concrete example."
- "Rewrite `skills/reverse-prompt/SKILL.md` so the decision logic stays obvious at the top level and the detailed branching moves into references."
- "Create a `terraform-module-upgrade` skill that stays generic, uses shallow references, and makes the first validation step obvious."

## Reference files

- `assets/skill-template.md` - starter template for a new `SKILL.md`
- `references/layering-guide.md` - where guidance belongs across instructions, skills, and agents
- `references/checklist.md` - final authoring and validation checklist
- `references/metadata-contract.md` - canonical frontmatter contract: required fields, allowed optional extensions, forbidden keys, and exception policy
- `references/import-rewrite-contract.md` - shared target shape for rewriting upstream skills into this local library
- `references/quality-scenarios.md` - skill quality review scenarios and maintenance loop
- `scripts/validate-skill-library.mjs` - local validator for skill library metadata, examples, and support-file references
