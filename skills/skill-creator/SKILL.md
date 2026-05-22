---
name: skill-creator
description: "Create or upgrade a reusable skill in the current skills catalog. Use when adding a skill, improving metadata/examples/evals, tightening trigger boundaries, or deciding if guidance belongs in a skill."
metadata:
  owner: mattriley
  maturity: stable
---

# Skill Creator

## Use this skill when

- Creating a new skill in the current catalog `skills/` directory
- Upgrading an existing skill so its trigger boundaries, workflow, and support files are easier to use correctly
- Refreshing an existing skill so its frontmatter metadata, examples, anti-triggers, or eval coverage better match real user requests
- Tightening a skill's trigger language, validation steps, or support-file layout so it routes more reliably
- Deciding whether reusable guidance belongs in a skill instead of instructions, an agent, an extension, or MCP configuration
- Standardising a skill's structure, metadata, validation steps, or support-file layout for this personal catalog

## Do not use this skill when

- The task is a one-off answer or prompt and does not need a reusable catalog asset
- The guidance should always apply and belongs in repository instruction files, `instructions/`, or `AGENTS.md`
- The main need is a named specialist role, which belongs in `agents/`
- The main need is deterministic runtime behavior, which belongs in `extensions/`
- The change is primarily an external integration or live-data connection, which belongs in MCP config

## Inputs to gather

**Required before editing**

- The user problem the skill is meant to solve
- 2-3 representative user requests the skill should trigger on
- The nearest overlapping skills in this catalog and how this skill will stay distinct
- Whether the reusable asset is really a skill rather than instructions, an agent, an extension, or MCP

**Helpful if present**

- Common failure modes, anti-triggers, or false positives
- Repo or environment assumptions the skill can rely on
- Existing validation commands, checklists, or deterministic procedures worth capturing
- Any current support files that already contain useful examples, edge cases, or reference material

**Only investigate if encountered**

- Whether `scripts/` would remove repeated fragile reconstruction rather than just add maintenance
- Whether `evals/` would catch meaningful trigger/workflow regressions instead of becoming noise
- Whether the skill's maturity should stay `draft` or move to `stable` / `experimental`

## First move

1. If the user only wants a generic new-skill starter package, load `references/new-skill-package.md` and use `assets/new-skill-starter/` as the default response shape instead of blocking on domain-specific discovery.
2. Otherwise, check whether the guidance belongs in a skill at all.
3. Compare the proposed skill against `skills/README.md` and nearby skills so the boundary is explicit before you draft content.
4. Write the trigger language first: the frontmatter description plus `Use this skill when` and `Do not use this skill when`.
5. Only then draft the workflow, support files, and validation steps.

## Workflow

1. Confirm the guidance really belongs in a skill; check `skills/README.md` and nearby skills to establish the boundary before drafting.
2. Gather 2-3 concrete user tasks, key constraints, and known failure modes before writing body content; include upgrade prompts when the work is about metadata, examples, or trigger gaps.
3. Update the trigger contract first: frontmatter description, `Use this skill when`, and `Do not use this skill when`.
4. If the request is a generic starter-package ask with no specific skill domain yet, stop discovery there and hand back the minimal copy-ready bundle from `assets/new-skill-starter/`: frontmatter, the smallest useful `references/` set, eval stubs, and target-skill validation commands.
5. In that starter-package response, say explicitly that `SKILL.md` holds the main workflow while `references/` and `evals/` are the progressive-disclosure layer, and say that `scripts/` are omitted by default unless they remove repeated fragile reconstruction.
6. Otherwise, choose the minimal useful package — decide which of `references/`, `evals/`, `scripts/`, and `assets/` are actually needed before creating them.
7. Draft or refine body sections that change execution: workflow, guardrails, validation, and support-file load conditions.
8. Add support files only when they materially improve execution; name them for what the agent learns there, not generic labels.
9. Validate with the shared tooling; iterate against real prompts, false triggers, and weak outputs before broadening.

> Read `assets/skill-template.md` for the canonical `SKILL.md` outline and eval file schemas.
> Read `references/catalog-standard.md` for authoring principles, frontmatter spec, and directory conventions.

## Guardrails

- **Must** define the skill boundary against nearby skills before finalizing wording.
- **Must** put trigger guidance in both the frontmatter description and the body.
- **Must** adapt the standard to this personal catalog rather than copying another repository wholesale.
- **Must** hand back the existing starter scaffold directly when the user asks for a generic new-skill package and has not named a domain-specific skill yet.
- **Must** state the progressive-disclosure split (`SKILL.md` for the workflow, `references/` and `evals/` for deeper support) when handing back the generic starter package.
- **Must not** import Anthropic-specific `.claude`, `claude`, `.skill`, packaging, or benchmark machinery into this catalog unless the local catalog explicitly adopts that workflow.
- **Must not** add empty headings, dead reference sections, or generic support-file instructions that do not help the agent choose what to read.
- **Must not** stall on extra discovery or force domain-specific clarification when the user only asked for the reusable starter package.
- **Must not** imply that `scripts/` are part of the default starter bundle; call them out only as an opt-in extension when prose and evals are not enough.
- **Should** give the agent one clear first move before the longer workflow.
- **Should** prefer precise boundaries and anti-triggers over broad or "pushy" trigger wording when adjacent local skills could plausibly overlap.
- **Should** keep support-file names purpose-specific when a generic `examples.md` or `edge-cases.md` name would hide the real reason to load the file.
- **May** add `evals/`, `scripts/`, or `assets/` when they clearly improve determinism, trigger precision, or reuse.

## Support files

- Read support files only when the current task matches their purpose; state that purpose explicitly in `SKILL.md`.
- Prefer specific load conditions like `Read the repo-contract reference when the repository may be spec-first or code-first` over generic phrases like `Read examples when you need examples`.
- If a support file would only repeat one short checklist or one obvious warning, keep that guidance in `SKILL.md` instead.

## Validation

- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs` from `~/.copilot/` after editing `skills/`; this checks frontmatter compliance, required headings, orphaned support files, and reference targets.
- Eval runner scripts have not yet been ported to Node.js; skip trigger-eval and functional-eval commands until a replacement is available.
- When delivering or documenting a new skill scaffold, confirm the new skill passes the validator:
  - `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/<new-skill-name>/SKILL.md`
- Re-read `skills/README.md` alongside the changed skill to confirm the boundary does not overlap ambiguously with nearby skills.

## Examples

- `Update an existing skill so it has better metadata, examples, and trigger coverage.`
- `Tighten this skill's description, anti-triggers, and eval prompts so it routes more reliably.`
- `Help me decide whether this reusable workflow belongs in a skill, instructions, an agent, or an extension.`

## Reference files

- Read `references/examples.md` when drafting trigger language or checking whether a revised description still matches representative create-or-upgrade requests.
- Read `references/edge-cases.md` when the request is ambiguous, overlaps another customization surface, or risks adding scripts or assets without clear justification.
- Read `references/new-skill-package.md` when the task is to hand back a copy-ready starter bundle with frontmatter, support files, evals, and validation commands for the new skill.
- Read `references/catalog-standard.md` when you need authoring principles, frontmatter spec, or directory structure guidance.
- Read `assets/skill-template.md` when you need the canonical `SKILL.md` outline, section headings, or eval file schemas.
- Copy `assets/new-skill-starter/` into the new skill directory when creating a skill from scratch; replace all placeholders before treating it as ready.
