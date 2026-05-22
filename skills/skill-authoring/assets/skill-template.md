# Skill template

Use this as a starting point for a new skill, then tailor the sections to the workflow.

Keep the package shape predictable when it fits the workflow so future authoring or validation tools can scaffold and inspect it without guessing.

```md
---
name: my-skill-name
description: "What this skill does. Use it when [trigger phrase 1], [trigger phrase 2], or [trigger phrase 3]. Prefer over-triggering to under — include a scope boundary if similar skills exist (e.g. but not when X is more appropriate)."
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
| ... | No | ... |

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

- ...

## Validation

- ...
- confirm the frontmatter, headings, and support-file links are easy to inspect mechanically

## Examples

- ...

## Reference files

- `references/REFERENCE.md` - ...
```

Use `metadata.kind: task` for multi-step playbooks with explicit outputs and validation.

Use `metadata.kind: reference` for lookup-heavy guidance where the main value is navigation, conventions, or examples.

`metadata.kind` is **required** for all `draft` skills and must be set before promotion to `stable`. See `skills/skill-authoring/references/metadata-contract.md` for the full frontmatter contract, including forbidden top-level keys and forbidden provenance fields.
