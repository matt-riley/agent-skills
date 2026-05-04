# AGENTS.md

## Project overview

This repository is the source of truth for a portable Agent Skills catalog used across Copilot, Pi, Codex, and Gemini CLI.

Most work happens under `skills/`. Each skill directory may include:

- `SKILL.md` — the portable workflow and boundaries
- `references/` — examples, edge cases, decision rules, or deeper guidance
- `evals/` — trigger and functional eval fixtures
- `agents/` — harness-specific metadata such as `agents/openai.yaml`
- `scripts/` or `assets/` — only when they add real value

Start with:

- `README.md` for repo-level context
- `skills/README.md` for the catalog chooser
- `skills/<name>/SKILL.md` for the skill you are editing

If a subdirectory has its own `AGENTS.md`, follow the closest file.

## Repository layout

```text
agent-skills/
├── _shared/   # validation and eval tooling
├── scripts/   # repo helper scripts
└── skills/    # portable skill packages
```

## Common commands

Run from the repo root.

### Validate the catalog

```bash
npm run validate
```

Equivalent direct command:

```bash
python _shared/validate-skills.py skills
```

### Link the catalog into user-level skill directories

```bash
npm run link:user
```

### Run targeted evals for one skill

```bash
python _shared/run-trigger-evals.py skills/<skill-name>/evals/trigger-queries.json
python _shared/run-functional-evals.py skills/<skill-name>/evals/evals.json
```

The eval runners shell out to the `copilot` CLI, so only run them when that dependency is available.

## Editing conventions

### Skill authoring

- Keep `SKILL.md` concise and workflow-oriented.
- Put detailed examples, edge cases, and decision rules in `references/` instead of bloating `SKILL.md`.
- Prefer `references/` before adding `scripts/`; add scripts only for deterministic, repeated logic.
- Use portable wording in `SKILL.md` rather than harness-specific instructions when possible.
- Keep harness-specific installation or packaging details in repo docs or harness-specific metadata files.

### Frontmatter

Every `SKILL.md` should have at least:

- `name`
- `description`

Common optional fields in this catalog:

- `license: Proprietary`
- `compatibility`
- `metadata.version`
- `metadata.maturity`

If a skill is release-managed, `metadata.version` in `SKILL.md` should stay aligned with `.release-please-manifest.json`.

### Directory conventions

Follow the existing skill package pattern:

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── evals/
├── agents/
├── scripts/
└── assets/
```

Not every directory is required. Do not add empty scaffolding just to match the pattern.

## When adding or changing skills

- Keep `skills/README.md` accurate if the catalog or chooser changes.
- If you change a skill's identity or trigger behavior, review any related `agents/openai.yaml` metadata and eval fixtures.
- When creating a new skill, use `skills/skill-creator/references/catalog-standard.md` as the repo standard.
- New release-managed skills must also be added to:
  - `release-please-config.json`
  - `.release-please-manifest.json`

## Release and versioning notes

This repo uses Release Please.

- The root package `@matt-riley/agent-skills` is the only component that creates a GitHub Release.
- Skills are versioned individually.
- Skill versions are mirrored into `SKILL.md` frontmatter at `metadata.version`.
- Conventional commits drive release automation.
- Do not make casual manual version bumps; only touch release metadata when the repo workflow requires it, such as adding a new skill.

## Practical guardrails

- Do not weaken portability with hard-coded local paths inside active skills.
- Do not move detailed guidance into `README.md` when it belongs in a specific skill package.
- Prefer the smallest accurate change that keeps the catalog internally consistent.
- After editing skill content or metadata, run `npm run validate` before finishing.
