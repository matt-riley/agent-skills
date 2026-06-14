# Skill Templates

Reference this file when drafting a new skill or reviewing canonical section structure and eval schemas.

## Canonical `SKILL.md` shape

Use this as the default outline, then trim sections that do not earn their place:

````markdown
---
name: example-skill
description: What the skill does and when to use it.
license: GNU GPL v3
metadata:
  maturity: stable
  kind: task
---

# Example Skill

## Use this skill when
- Positive trigger

## Do not use this skill when
- Anti-trigger

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

## Guardrails
- **Must** ...
- **Must not** ...
- **Should** ...
- **May** ...

## Validation
- ...

## Reference files
- Read the relevant file under `references/` when its topic matches the current task.
````

## Canonical eval file schemas

`evals/trigger-queries.json`:

```json
[
  { "query": "I changed sqlc files; regenerate before tests.", "should_trigger": true },
  { "query": "Explain what protobuf is.", "should_trigger": false }
]
```

`evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "example-case",
      "prompt": "User task goes here.",
      "expected_behavior": "Human-readable success description.",
      "assertions": [
        "Mentions the correct workflow",
        "Uses the right validation step"
      ],
      "files": []
    }
  ]
}
```

Use `files` only when the eval depends on specific local inputs.

`evals/` is optional. Add it when it will catch real trigger mistakes or workflow regressions, not just because the directory template allows it.

## Minimum starter bundle

When the task is to create a new skill from scratch, the default minimal package is:

```text
<new-skill-name>/
├── SKILL.md
├── references/
│   ├── examples.md
│   ├── edge-cases.md
│   └── validation-checklist.md
└── evals/
    ├── trigger-queries.json
    └── evals.json
```

Validation commands should target the new skill path, not the authoring skill:

```bash
python _shared/validate-skills.py skills
python _shared/run-trigger-evals.py skills/<new-skill-name>/evals/trigger-queries.json
python _shared/run-functional-evals.py skills/<new-skill-name>/evals/evals.json
```

## Copy-ready starter scaffold

If the user wants an actual starter package instead of a shape description, copy the files under `assets/new-skill-starter/` into the new skill directory and replace the placeholders there.
