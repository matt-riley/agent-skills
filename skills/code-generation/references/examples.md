# Examples for Code Generation

Use these as concrete patterns when the skill should activate.

## Example 1 - Regenerate Before Test

User says: "I edited query files and templates. What should happen before I run tests?"

Expected behaviour:
- The response says generation may need to happen before build/test, identifies the repo's generator commands, and checks whether generated output is committed or ephemeral.
Key checks:
- Says to detect the repo's generation contract first.
- Says generation should run before tests when generator-backed inputs changed.
- Mentions generator commands or make generate.
- Warns not to edit generated files directly.

## Example 2 - Generated Diff Check

User says: "Generated files changed unexpectedly after regeneration. How should I verify the diff?"

Expected behaviour:
- The response tells the user to inspect the diff/stat, confirm whether the output is meant to be committed, and trace the change back to generator inputs rather than patching generated output manually.
Key checks:
- Mentions inspecting git diff or diff stat.
- Mentions committed-vs-ignored output handling.
- Suggests checking generator inputs/config.
- Does not recommend hand-editing generated output.
