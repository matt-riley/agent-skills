# Context-needs output

Use this structure when the main blocker is missing repository context rather than missing user intent.

## Output buckets

### Must See

- Files that are required before answering accurately or changing code safely.
- Keep this list short and justify each file.

### Should See

- Helpful files that would improve completeness, confidence, or edge-case coverage.
- These are not blockers for an initial answer, but they matter for a strong one.

### Already Have

- Files or directories already seen in the current conversation that reduce duplicate asks.

### Uncertainties

- The questions you still cannot resolve without more code or config context.
- Use this section instead of guessing.

## Example stub

```md
## Files I Need

### Must See
- `src/router.ts` - main dispatch logic for the reported behavior

### Should See
- `src/router.test.ts` - nearest tests for the same surface

### Already Have
- `package.json` - confirms the package entrypoints and scripts

### Uncertainties
- Whether the behavior is configured indirectly through a shared helper or directly in `src/router.ts`
```
