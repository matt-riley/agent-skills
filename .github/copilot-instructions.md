# agent-skills repository instructions

## Start here

- Read `README.md` for catalog-wide behavior and release/versioning rules.
- Use `skills/README.md` as the skill chooser.
- Treat `skills/<name>/SKILL.md` as the source of truth for an individual skill; support files only extend it.

## Commands

- `npm run validate` — primary repo-wide validation (`python _shared/validate-skills.py skills`)
- `python _shared/run-trigger-evals.py skills/<skill-name>/evals/trigger-queries.json` — run trigger evals for one skill
- `python _shared/run-functional-evals.py skills/<skill-name>/evals/evals.json` — run functional evals for one skill
- `python _shared/run-trigger-evals.py skills/<skill-name>/evals/trigger-queries.json --max-queries 1` — quickest single trigger fixture pass
- `python _shared/run-functional-evals.py skills/<skill-name>/evals/evals.json --max-evals 1` — quickest single functional fixture pass
- Add `--static` to either eval runner when you want fixture validation without invoking the `copilot` CLI
- `npm run link:user` — symlink this repo's `skills/` into `~/.agents/skills` and `~/.copilot/skills`

This repo does not define a separate build or lint script in `package.json`; the main health checks are catalog validation plus targeted evals.

## High-level architecture

- This repository is the source of truth for a portable Agent Skills catalog shared across GitHub Copilot, Pi, OpenAI Codex, and Gemini CLI. The product is the `skills/` tree.
- Each skill package is self-contained: `SKILL.md` holds the portable workflow and boundaries, `references/` holds examples and deeper guidance, `evals/` holds trigger and functional fixtures, `agents/` holds harness-specific metadata, and `scripts/` or `assets/` are only added when they provide real deterministic value.
- `_shared/` is the catalog contract layer. `validate-skills.py` enforces frontmatter, canonical headings, release metadata alignment, support-file linking, OpenAI metadata sync, and shell syntax checks; the eval runners execute or statically validate skill fixtures.
- `scripts/link-user-skills.sh` is the local install bridge that links this checkout's `skills/` directory into the user-level skill locations expected by supported agents.
- Release automation is split between the root package and individual skills: Release Please manages the root release, while skill versions live in `.release-please-manifest.json`, mirror into `skills/*/SKILL.md`, and get plain git tags when they bump.

## Key conventions

- Keep `SKILL.md` concise and workflow-oriented. Move examples, edge cases, and decision rules into `references/` instead of bloating the main file.
- Do not add empty scaffold directories just to match the common package shape.
- If a skill's behavior, trigger, or identity changes, update the skill's `SKILL.md` first, then any related `skills/README.md`, eval fixtures, and `agents/openai.yaml`.
- Skill metadata is enforced across files: the directory name must match frontmatter `name`, the frontmatter `description` is trigger text, and `agents/openai.yaml` `interface.short_description` must match that description exactly.
- The validator expects the canonical workflow headings `Use this skill when`, `Do not use this skill when`, `Inputs to gather`, `First move`, and `Guardrails`.
- Support files under `references/`, `scripts/`, and `assets/` must be linked from `SKILL.md`.
- Release-managed skills need `license`, `metadata.version`, and `metadata.maturity`; `metadata.version` must match `.release-please-manifest.json` and keep the `# x-release-please-version` marker.
- Treat eval fixtures as a paired contract: when adding eval coverage for a skill, add both `evals/trigger-queries.json` and `evals/evals.json`.
- Keep active skills portable: avoid hard-coded local install paths inside `SKILL.md`; put harness-specific installation details in repo docs or harness metadata instead.
