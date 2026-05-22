---
name: example-skill
description: Replace this with what the skill does and when to use it from the user's point of view. Name the task, the activation conditions, and the main boundary in one concise description.
license: GNU GPL v3
compatibility: Agent Skills-compatible coding agents; adjust only if this skill depends on a narrower environment or workflow.
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: draft
---

# Example skill

Replace `example-skill` and every placeholder in this starter before copying it into the live catalog.

## Use this skill when

- The user asks to `<primary task this skill owns>`.
- The request needs `<special workflow, guardrail, or local knowledge>` that is reusable across tasks.
- The surrounding ask matches this skill more directly than nearby skills such as `<adjacent-skill>` or `<another-adjacent-skill>`.

## Do not use this skill when

- The main need is `<near-miss task>`; route that to `<other-surface-or-skill>` instead.
- The guidance should always apply and belongs in `copilot-instructions.md`, `instructions/`, or `AGENTS.md`.
- The request is a one-off answer or prompt that does not need a reusable catalog asset.

## Inputs to gather

**Required before editing**

- The exact user problem this skill solves.
- 2-3 representative prompts the skill should trigger on.
- The nearest overlapping skills and the boundary this skill should keep.

**Helpful if present**

- Common failure modes or false-trigger cases.
- Existing validation commands or support files worth reusing.
- Environment assumptions the skill can rely on safely.

**Only investigate if encountered**

- Whether a script would remove repeated fragile reconstruction instead of adding maintenance.
- Whether extra assets or evals would catch a real regression instead of adding noise.

## First move

1. Lock the boundary first: frontmatter description, `Use this skill when`, and `Do not use this skill when`.
2. Add only the support files this workflow genuinely needs.
3. Validate the finished package with the shared tooling before treating it as ready.

## Workflow

1. Compare this proposed skill against `skills/README.md` and nearby skills so the routing boundary is explicit.
2. Write the frontmatter and trigger sections before drafting the deeper workflow.
3. Add or refine the support files under `references/` and `evals/` only when they improve execution, measurement, or false-trigger resistance.
4. Keep file names purpose-specific so the agent knows why to read them.
5. Re-test the skill against real prompts and adjust the wording until the right tasks trigger cleanly.

## Guardrails

- **Must** keep the frontmatter description aligned with the body trigger language.
- **Must** define at least one clear anti-trigger against a nearby skill or non-skill surface.
- **Must not** add scripts, assets, or evals by default unless they clearly add value.
- **Should** keep support-file names explicit about what the agent learns there.
- **Should** use real representative prompts instead of generic placeholders before calling the skill complete.
- **May** add more references, assets, or scripts if they materially improve deterministic execution.

## Validation

- Run `python _shared/validate-skills.py skills` from the catalog root after copying the finished skill into the live catalog.
- If you changed trigger wording, anti-triggers, or frontmatter description, run `python _shared/run-trigger-evals.py skills/<your-skill-name>/evals/trigger-queries.json`.
- If you changed workflow guidance, guardrails, or support-file load conditions, run `python _shared/run-functional-evals.py skills/<your-skill-name>/evals/evals.json`.
- Read `references/validation-checklist.md` before calling the new skill ready.
- Re-read the finished `SKILL.md` beside `skills/README.md` to confirm the new boundary is still crisp.

## Reference files

- Read `references/examples.md` when drafting or testing trigger language against representative prompts.
- Read `references/edge-cases.md` when the request is ambiguous, overlaps another surface, or risks overbuilding support files.
- Read `references/validation-checklist.md` when preparing the final command bundle and ready-to-ship checks for the new skill.
