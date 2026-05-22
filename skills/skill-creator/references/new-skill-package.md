# New Skill Package Guide

Use this file when the task is to hand back a copy-ready starter bundle for a brand-new skill.

## Minimum package

Create the smallest package that still makes the workflow obvious:

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

Add `scripts/` or extra `assets/` only when they remove repeated fragile reconstruction or provide deterministic validation the agent cannot reproduce safely in prose.

## Frontmatter baseline

Use lean frontmatter that tells the agent what the skill does and when to use it:

```yaml
---
name: <new-skill-name>
description: <what the skill does and when to use it from the user's point of view>
license: GNU GPL v3
compatibility: Agent Skills-compatible coding agents
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: draft
---
```

Only keep `compatibility` if the environment assumption matters for the skill.
Use the repo-root `LICENSE` file as the canonical license text.
If the new skill should participate in release automation, keep the marker comment and add the skill to `release-please-config.json` plus `.release-please-manifest.json`.

## Recommended support files

- `references/examples.md` - concrete in-scope prompts and what good activation looks like.
- `references/edge-cases.md` - near misses, false-trigger risks, and overbuilding warnings.
- `references/validation-checklist.md` - the final pre-handoff checklist plus the commands to run against the new skill path.
- `evals/trigger-queries.json` - representative prompts that should and should not activate the skill.
- `evals/evals.json` - workflow-quality assertions for the skill's expected behavior.

Rename reference files when a more specific purpose is clearer than a generic label.

This is the progressive-disclosure split for the starter bundle:

- `SKILL.md` holds the main workflow, selection guidance, and validation summary.
- `references/` holds examples, edge cases, and checklists that add detail without bloating the main skill file.
- `evals/` holds the measurable trigger and workflow checks.
- `scripts/` are omitted by default; add them only when prose plus evals cannot reliably capture the workflow.

## Validation command bundle

When presenting a new skill to the user, include target-skill commands rather than `skill-creator` paths:

```bash
python _shared/validate-skills.py skills
python _shared/run-trigger-evals.py skills/<new-skill-name>/evals/trigger-queries.json
python _shared/run-functional-evals.py skills/<new-skill-name>/evals/evals.json
```

Use the shared catalog validator for the whole skills directory, then use the new skill's own eval paths for trigger and functional checks.

## Delivery checklist

- Replace every placeholder in the starter files before calling the skill ready.
- Keep the frontmatter description, `Use this skill when`, and `Do not use this skill when` aligned.
- Confirm the new skill stays distinct from nearby skills in `skills/README.md`.
- Ensure each support file is mentioned explicitly in `SKILL.md`.
- When you hand the starter bundle to the user, say explicitly that `scripts/` are opt-in rather than part of the default package.
