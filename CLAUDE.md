# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repository is the source of truth for a portable Agent Skills catalog shared across GitHub Copilot, Pi, OpenAI Codex, and Gemini CLI. The product is the `skills/` tree — everything else exists to validate, link, or release it.

Each skill package under `skills/<name>/` is self-contained:

- `SKILL.md` — the portable workflow and boundaries (source of truth for that skill)
- `references/` — examples, edge cases, deeper guidance
- `evals/` — trigger and functional eval fixtures
- `agents/openai.yaml` — Codex-specific UI metadata (display name, short description, implicit-invocation policy)
- `scripts/` or `assets/` — only when they add real deterministic value; do not add empty scaffolding to match the pattern

Start with `README.md` for catalog-wide/release behavior, `skills/README.md` as the task-oriented skill chooser, and `skills/<name>/SKILL.md` for the skill being edited. If a subdirectory has its own `AGENTS.md`, follow the closest one.

## Commands

Run from the repo root.

```bash
npm run validate          # python _shared/validate-skills.py skills — primary repo-wide check
npm run link:user          # bash scripts/link-user-skills.sh — symlink skills/ into ~/.agents/skills and ~/.copilot/skills
```

Targeted evals for one skill (require the `copilot` CLI unless `--static` is passed):

```bash
python _shared/run-trigger-evals.py skills/<skill-name>/evals/trigger-queries.json [--max-queries 1] [--static]
python _shared/run-functional-evals.py skills/<skill-name>/evals/evals.json [--max-evals 1] [--static]
```

There is no separate build or lint script — `npm run validate` plus targeted evals are the health checks.

## The validation contract (`_shared/validate-skills.py`)

This is the thing that actually enforces catalog consistency. When editing a skill, keep these constraints in mind:

- Directory name must match frontmatter `name` (kebab-case, `^[a-z0-9]+(?:-[a-z0-9]+)*$`).
- Frontmatter `description` is trigger text and must match `agents/openai.yaml` `interface.short_description` exactly, if that file exists.
- `SKILL.md` should use these canonical headings when they add signal. Omit empty or redundant sections; headings that are present must retain this semantic order and appear outside code fences:
  - `## Use this skill when`
  - `## Do not use this skill when`
  - `## Inputs to gather`
  - `## First move`
  - `## Workflow`
  - `## Guardrails`
  - `## Validation`
  - `## Examples`
  - `## Reference files`
- Inter-skill links (`../<name>/SKILL.md`) must point at a skill that exists.
- Support files under `references/`, `scripts/`, `assets/` must be linked from `SKILL.md`.
- Every skill needs `license: GNU GPL v3` (Learned Rule 1). Release-managed skills additionally need `metadata.version` (with the x-release-please-version marker) and `metadata.maturity`; `metadata.version` must match `.release-please-manifest.json`.
- Draft skills should declare `metadata.kind: task` or `reference`.
- If a skill has `evals/`, both `trigger-queries.json` and `evals.json` are expected (paired contract).

## Release and versioning

This repo uses Release Please via the shared `matt-riley-ci` workflow.

- Root package `@matt-riley/agent-skills` is the only component that creates a GitHub Release.
- Each `skills/<name>` directory has its own independently versioned, tracked in `.release-please-manifest.json` and mirrored into `SKILL.md` frontmatter `metadata.version`.
- Conventional commits (`feat:`, `fix:`) on a skill's path drive that skill's next version bump. Changed skills get plain git tags (`<skill-name>-v<version>`), not GitHub Releases.
- When adding a new skill, add it to both `release-please-config.json` and `.release-please-manifest.json`, plus a `metadata.version` line in its `SKILL.md`.
- Do not make casual manual version bumps.

## Editing conventions

- Keep `SKILL.md` concise and workflow-oriented; put examples, edge cases, and decision rules in `references/` instead.
- Prefer `references/` before adding `scripts/`; scripts only for deterministic, repeated logic.
- Use portable wording (Agent Skills-compatible) over harness-specific instructions where possible. Keep harness-specific install/packaging details in repo docs (`README.md`) or `agents/openai.yaml`, not inside `SKILL.md`.
- Avoid hard-coded local install paths inside active skills.
- If a skill's identity, trigger, or behavior changes, update in this order: the skill's `SKILL.md`, then `skills/README.md` chooser entries, related eval fixtures, and `agents/openai.yaml`.
- When using `skill-creator` to add a new skill, use `skills/skill-creator/references/catalog-standard.md` as the repo standard.
- Keep `skills/README.md` de-duplicated: if a skill is already covered under core defaults or a guardrail section, don't repeat it elsewhere unless the second mention adds distinct routing guidance.
- After editing skill content or metadata, run `npm run validate` before finishing.

## Learned rules (from AGENTS.md)

1. Always use `license: GNU GPL v3` in skill frontmatter and skill-authoring templates, and direct license lookups to the repo-root `LICENSE` file — this catalog is GPL-licensed at the repository level.
2. When a skill is renamed, update inter-skill links and `skills/README.md` routing entries in the same pass — stale names break catalog validation and send agents to nonexistent packages.
