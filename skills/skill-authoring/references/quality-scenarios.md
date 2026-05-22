# Skill quality scenarios

Use these scenarios to keep the authoring benchmark concrete, shallow, and easy to hand off.

| Scenario | Quality call | Expected move |
| --- | --- | --- |
| `SKILL.md` is concise, has clear activation and non-use rules, and links shallow support files. | good | Approve the shape and keep the package small. |
| The file inlines lookup tables, templates, or long examples that belong in `references/`. | needs revision | Move the detail into shallow support files. |
| The workflow is narrow, stateful, or dedicated to one operator persona. | handoff trigger | Promote it to a specialized agent instead of widening the skill. |
| The skill has no concrete example or no validation step. | needs revision | Add one example and one obvious validation action. |
| The skill has explicit outputs for a task workflow or obvious lookup paths for a reference workflow. | good | Keep the shape aligned with the skill kind. |
| The package starts embedding repo policy or environment-specific branching. | red flag | Pull that material back out of the reusable skill. |
| The description names the skill's domain but lists no concrete trigger phrases or situations. | needs revision | Rewrite to include specific trigger phrases so the skill activates reliably — lean toward over-triggering, but pair with at least one disambiguator (a scope boundary or route-away condition) to keep routing clean. |

## Maintenance loop

- Update this file whenever the benchmark shape or anti-pattern list changes.
- If a new pattern becomes a reusable review rule, add it here before copying it into other skills.
