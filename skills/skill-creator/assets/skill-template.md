# Skill template

Use this as the canonical starter when creating or revising a catalog skill. Keep the package minimal and move lookup-heavy detail into purpose-named references.

```md
---
name: my-skill-name
description: "Use when [specific request or trigger]. Not when [adjacent route] is more appropriate."
license: GNU GPL v3
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# My skill name

Use this skill when ...

## Use this skill when

- ...

## Do not use this skill when

- ...

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| ... | Yes | - |
| ... | No | [`a nearby skill`](../skill-creator/SKILL.md) |

## Inputs to gather

**Required before editing**

- ...

**Helpful if present**

- ...

**Only investigate if encountered**

- ...

## First move

1. ...

## Workflow

1. ...

## Outputs

- ...

## Guardrails

- **Must** ...
- **Must not** ...
- **Should** ...

## Validation

- ...

## Examples

- ...

## Reference files

- [references/REFERENCE.md](references/REFERENCE.md) — ...
```

Use `metadata.kind: task` for a multi-step playbook with explicit inputs, outputs, and validation. Use `metadata.kind: reference` for lookup-heavy guidance where navigation and examples are the main value. Every active skill must declare `category`, `audience`, `maturity`, and `kind`; `maturity` is `stable`, `draft`, or `experimental` (`beta` is legacy).

The frontmatter description should name the purpose and concrete activation conditions. Keep it tight, but do not enforce an arbitrary character range: purpose plus trigger situations and a useful scope boundary matter more than a fixed length. The description must state when to use the skill and, where overlap exists, when not to use it; it should not merely summarize the workflow.

The routing boundary is required when adjacent skills exist. Keep every local support link resolvable, and run the target-skill validator rather than pointing validation back at `skill-creator`.

## Eval file schemas

Add `evals/trigger-queries.json` when trigger boundaries need static coverage:

```json
[
  { "query": "A request that should activate the skill.", "should_trigger": true },
  { "query": "A near-miss that belongs to an adjacent skill.", "should_trigger": false }
]
```

Add `evals/evals.json` when workflow behavior needs assertions:

```json
{
  "skill_name": "my-skill-name",
  "evals": [
    {
      "id": "example-case",
      "prompt": "User task goes here.",
      "expected_behavior": "Human-readable success description.",
      "assertions": ["Mentions the correct workflow", "Uses the right validation step"],
      "files": []
    }
  ]
}
```

Keep evals only when they catch a real trigger or workflow regression; target the skill's own paths in validation commands.
