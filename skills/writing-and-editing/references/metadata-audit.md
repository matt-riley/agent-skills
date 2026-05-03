# Metadata audit reference

Use this file when the task is about short audience-facing strings rather than full prose.

## Typical fields

- page titles
- meta descriptions
- bios
- taglines
- repo descriptions
- schema descriptions
- README opening blurbs

## What to check

- front-loading
- concreteness
- filler
- active voice
- duplication against paired fields
- word choice
- truncation fit for the target surface
- one-idea-per-field discipline

## Output shape

```markdown
### [Field name] — [length] chars

> [The string itself]

- Front-loading: [✓/⚠/✗] [reason if needed]
- Concreteness: [✓/⚠/✗] [reason]
- Filler: [✓/⚠/✗] [reason]
- Active voice: [✓/⚠/✗] [reason]
- Duplication: [✓/⚠/✗] [reason]
- Word choice: [✓/⚠/✗] [reason]
- Truncation fit: [✓/⚠/✗] [reason] — platform: [surface]
- One idea: [✓/⚠/✗] [reason]

**Rewrite:** [only when needed]
```

## Guardrails

- Review strings in batches when possible so duplication is visible.
- Keep the audit terse and actionable.
- Do not expand this into a full document or repo-surface review unless the user asks.
