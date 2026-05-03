# Validation checklist for Example Skill

Replace every placeholder before treating this file as part of a real skill.

## Final checks

- The frontmatter `description` matches `Use this skill when` and `Do not use this skill when`.
- `SKILL.md` mentions every support file the skill expects the agent to read.
- The representative prompts in `references/examples.md` match the trigger evals in `evals/trigger-queries.json`.
- The workflow assertions in `evals/evals.json` still match the current `SKILL.md`.
- The new skill stays distinct from the nearest overlapping skill or non-skill surface.

## Commands

Run these commands against the finished skill package:

```bash
python _shared/validate-skills.py skills
python _shared/run-trigger-evals.py skills/<your-skill-name>/evals/trigger-queries.json
python _shared/run-functional-evals.py skills/<your-skill-name>/evals/evals.json
```

## Ready-to-ship reminder

- Replace `<your-skill-name>` in both commands and file content.
- Replace generic example prompts with real expected user requests.
- Drop unused support files instead of leaving dead scaffolding in the new skill.
