# Context-map output shape

Use this structure when returning a context map.

## Required sections

### Files to modify

- The primary files that are most likely to need edits.
- Include one short reason per file.

### Dependencies

- Files that may need updates because they import, configure, call, or otherwise constrain the primary files.
- Note the relationship, not just the path.

### Test files

- The closest existing tests that cover the relevant surface.
- If no tests are found nearby, say that directly.

### Reference patterns

- One or more files that show the house pattern to follow.
- Say what pattern each file demonstrates.

### Risk notes

- The likely ripple effects, unknowns, or boundaries that could widen the scope.
- Keep this focused on real risks, not generic warnings.

## Example

```md
## Context Map

### Files to modify
- `extensions/lore/extension.mjs` - tool registration and routing entry point
- `extensions/lore/lib/router.mjs` - request classification and dispatch logic

### Dependencies
- `extensions/lore/package.json` - runtime entrypoint and dependency surface
- `extensions/lore/tests/unit/router.test.mjs` - current route expectations

### Test files
- `extensions/lore/tests/unit/router.test.mjs` - routing behavior
- `extensions/lore/tests/integration/tools.test.mjs` - exposed tool surface

### Reference patterns
- `skills/reverse-prompt/SKILL.md` - shallow support-file linking pattern
- `skills/workflow-contracts/SKILL.md` - explicit routing-boundary table

### Risk notes
- Tool-surface changes may also require README catalog updates.
- Routing logic may already be shared with another extension helper; confirm before editing.
```
