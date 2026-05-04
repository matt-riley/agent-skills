# Catalog Standard

Reference this file when you need authoring principles, frontmatter spec, directory conventions, or shared tooling details for this personal skill catalog.

## About Skills

Skills are modular, self-contained packages that extend an AI agent's capabilities with specialised workflows, references, scripts, and output patterns. The goal is not to restate generic model knowledge; it is to package the conventions, edge cases, and repeatable procedures that matter in this environment.

## Directory standard

```text
skill-name/
├── SKILL.md
├── references/                # optional; use purpose-specific filenames when they help
│   ├── examples.md
│   ├── decision-rules.md
│   └── failure-modes.md
├── evals/                     # optional; add when they prevent real regressions
│   ├── trigger-queries.json
│   └── evals.json
├── scripts/                   # only when deterministic validation or transforms help
└── assets/                    # only when templates/resources materially help
```

`references/examples.md` and `references/edge-cases.md` are common patterns, not mandatory filenames. Use support-file names that describe what the agent should learn there.

**No-script-by-default rule:** prefer `references/` first. Add `scripts/` only when the agent is repeatedly reconstructing fragile logic or when a deterministic validation step is valuable.

## Core principles

### Concise is key

Keep `SKILL.md` focused on the workflow, selection guidance, and explicit references to support files. Assume the agent already knows the basics of programming, HTTP, SQL, and testing.

### Put triggering in frontmatter

The `description` field is the primary trigger mechanism. It must describe both what the skill does and when to use it from the user's point of view.

### Teach the same format you expect to see

A well-authored skill normally includes:

- `Use this skill when`
- `Do not use this skill when`
- `Inputs to gather`
- `First move`
- `Workflow`
- `Guardrails`
- `Validation`
- `Examples` and `Reference files` when those sections add signal

Do not cargo-cult every heading into every skill. Omit empty or redundant sections rather than leaving dead scaffolding behind.

### Use progressive disclosure

Put the main workflow in `SKILL.md`, move concrete examples and failure modes into `references/`, and only use `scripts/` for deterministic or repeated logic.

## Frontmatter

Required fields:

- `name`
- `description`

Local standard optional fields:

- `license: Proprietary`
- `compatibility` when environment assumptions matter
- `metadata.version` when the skill is release-managed
- `metadata.maturity`
- additional metadata only when it is genuinely useful and used consistently in this personal catalog

If a skill is release-managed in this repo, keep `metadata.version` as the human-visible mirror of the version tracked in `.release-please-manifest.json`.

Use `metadata.maturity` deliberately:

- `stable` — proven, reused, and unlikely to change shape soon
- `draft` — still being shaped or missing confidence
- `experimental` — intentionally risky, provisional, or likely to change quickly

Do not copy another repo's metadata scheme blindly. This personal catalog should keep metadata lean and maintenance-friendly.

## Shared tooling

This skill library standard expects shared tooling under the catalog root `_shared/` directory:

- `validate-skills.py` for structural validation
- `run-trigger-evals.py` for trigger checks
- `run-functional-evals.py` for with-skill vs baseline runs and grading scaffolds

Prefer those tools over ad hoc one-off eval formats.

## New skill starter minimum

When helping create a brand-new skill, the default starter package should usually include:

- `SKILL.md`
- `references/examples.md`
- `references/edge-cases.md`
- `references/validation-checklist.md`
- `evals/trigger-queries.json`
- `evals/evals.json`

Treat that as a starting point, not a requirement to keep dead scaffolding. Remove files that do not add signal.

When writing validation guidance for the new skill, separate:

- catalog-wide validation: `python _shared/validate-skills.py skills`
- target-skill trigger evals: `python _shared/run-trigger-evals.py skills/<new-skill-name>/evals/trigger-queries.json`
- target-skill functional evals: `python _shared/run-functional-evals.py skills/<new-skill-name>/evals/evals.json`

Do not substitute `skill-creator` paths when the task is to hand back validation guidance for another skill.
