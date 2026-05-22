---
name: context-map
description: Use when a task may span multiple files, when dependencies or tests are unclear, or when you need a pre-edit map of likely files and patterns before planning or implementation.
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
  kind: reference
---

# Context map

Use this skill when the next step is figuring out what to read or touch before changing code.

## Use this skill when

- A task may touch multiple files, packages, or layers and the likely blast radius is not obvious yet.
- You need to identify candidate files, nearby tests, and reference patterns before editing.
- A user or reviewer asks for a context map before implementation.
- You want to scope a feature, refactor, or bugfix enough to hand off to planning or implementation cleanly.

## Do not use this skill when

- The exact files are already named and the scope is narrow enough to execute directly.
- The user wants a phased implementation plan with tasks, dependencies, rollout notes, or handoff artifacts; route to `implementation-planner` or `workflow-contracts`.
- The main problem is sharpening the user's ask rather than mapping the codebase; route to `reverse-prompt` first.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Multi-file task, but likely files/tests/patterns are still unclear | Yes | - |
| User asks "what files do you need to see first?" while the brief is still under-specified | No | `reverse-prompt` |
| The code surface is known and the user wants a full execution plan | No | `implementation-planner` |
| A narrow single-file edit is already well scoped | No | execute directly |

## Inputs to gather

**Required before mapping**

- The task or question you are trying to scope.
- Any file, symbol, directory, or package hints already present in the request.
- Whether the next phase is likely to be `answer`, `plan`, or `implement`.

**Helpful if present**

- Entry-point files, commands, or failing tests that anchor the investigation.
- Similar existing features, modules, or prior art the request should follow.

**Only investigate if encountered**

- Build, configuration, or generated files that expand the blast radius.
- Cross-package ownership boundaries that may change who should implement the work.

## First move

1. Find the most likely entry-point files or directories for the task.
2. Trace direct dependencies, usages, or adjacent files from those entry points.
3. Find nearby tests and at least one reference pattern before suggesting edits.

## Workflow

1. Use [`references/search-playbook.md`](references/search-playbook.md) to discover candidate files in a consistent order.
2. Group the results into the context-map structure from [`references/output-shape.md`](references/output-shape.md).
3. Distinguish confirmed files from likely follow-up files instead of flattening everything into one undifferentiated list.
4. Name the nearby tests and reference patterns that should guide any later implementation.
5. Stop once the next action is obvious: read a specific set of files, route to planning, or proceed with a tightly scoped implementation.

## Guardrails

- Do not start implementing just because you found plausible files; finish the map first.
- Do not invent files, dependencies, or tests that you have not actually found.
- Keep the top-level skill concise; detailed formats and search heuristics belong in support files.
- Prefer the smallest map that makes the next step obvious over exhaustive cataloguing of the whole repo.
- Call out uncertainty explicitly when the map still depends on reading one or two key files.

## Validation

- Read the skill once as the target agent and confirm the next action is obvious within a few seconds.
- Confirm the top-level file links every support file directly from `## Reference files`.
- Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/context-map/SKILL.md`.
- Smoke test with one request that should trigger the skill and one near-miss that should not:
  - should trigger: `Before editing, map the files, tests, and patterns involved in adding retry logic to @extensions/lore/`
  - should not trigger: `Update the typo in @README.md`

## Examples

- `Before you touch anything, map the files, tests, and reference patterns involved in adding a new Lore memory tool.`
- `Create a context map for this refactor before we plan it: split the shared validation helper across @skills/ and @extensions/.`
- `What files are likely involved in this multi-package TypeScript error, and which tests should I read first?`

## Reference files

- [`references/output-shape.md`](references/output-shape.md) - the required sections and example structure for a context-map response
- [`references/search-playbook.md`](references/search-playbook.md) - discovery order for candidate files, dependencies, tests, patterns, and risks
- [`assets/examples.md`](assets/examples.md) - concrete request examples showing when the skill should trigger
