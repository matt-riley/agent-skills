# Examples for Skill Creator

Use these as concrete patterns when the skill should activate.

## Example 1 - New Skill Package

User says: "Help me create a new skill, including frontmatter, references, eval files, and validation guidance."

Expected behaviour:
- The response explains the standard skill shape, frontmatter, progressive disclosure, eval schemas, and no-script-by-default guidance.
- The response points to or provides a concrete starter scaffold instead of only abstract advice.
- The response uses the existing starter bundle directly and includes target-skill validation commands rather than `skill-creator`-only commands.
Key checks:
- Mentions frontmatter and when-to-use descriptions.
- Mentions references or evals and progressive disclosure.
- Mentions scripts as selective rather than default.
- Mentions a starter scaffold or template bundle with `SKILL.md`, `references/`, and `evals/`.
- Mentions the validation checklist/reference file and target-skill eval commands.

## Example 2 - Upgrade Existing Skill

User says: "Update an existing skill so it has better metadata, examples, and trigger coverage."

Expected behaviour:
- The response covers frontmatter metadata, in-file examples, anti-triggers, evals, validation tooling, and iteration based on real execution.
Key checks:
- Mentions metadata or versioning and maturity when relevant.
- Mentions examples in `SKILL.md` or representative example prompts in support files.
- Mentions trigger wording or anti-triggers, not just workflow prose.
- Mentions evals and validation tooling.
- Mentions iterative improvement using real tasks.

## Example 3 - Tighten Trigger Contract

User says: "Tighten this skill's description, anti-triggers, and example prompts so it routes more reliably."

Expected behaviour:
- The response starts with the trigger contract: frontmatter description plus `Use this skill when` and `Do not use this skill when`.
- The response improves examples or eval prompts so they cover both true triggers and near misses.
Key checks:
- Mentions the frontmatter description as a trigger surface.
- Mentions anti-triggers or false positives.
- Mentions trigger evals as part of validation.

## Example 4 - Choose the Right Customization Surface

User says: "I have reusable workflow guidance. Should this be a skill, instructions, an agent, or an extension?"

Expected behaviour:
- The response compares the nearby customization surfaces before assuming the answer is a skill.
- If it does belong in a skill, the response describes the minimal useful package instead of overbuilding it.
Key checks:
- Mentions at least one non-skill alternative such as instructions, an agent, or an extension.
- Mentions keeping the package minimal unless references/evals/scripts clearly add value.
