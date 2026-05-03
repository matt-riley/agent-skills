---
name: metadata-check
description: Review short audience-facing metadata strings such as titles, descriptions, bios, taglines, and schema descriptions for clarity, specificity, duplication, and truncation fit.
---

# Metadata check

## Use this skill when

- The user wants to review metadata, a tagline, a bio, a title, a description, or other short audience-facing strings.
- Another skill generated short strings with outsized user-facing impact, such as SEO titles, profile bios, repo descriptions, or FAQ answers.
- The core task is improving clarity, front-loading, specificity, and truncation fit in short text.

## Do not use this skill when

- The text is multi-paragraph prose or a long document. Use [`readability-check`](../readability-check/SKILL.md).
- The value is a URL, filename, enum, schema `@id`, technical identifier, or another non-copy field.
- The string is upstream content the user cannot change.

## Inputs to gather

**Required before editing**

- The exact strings to review.
- The target surface, such as SERP, GitHub, Twitter/X, Open Graph, schema description, or app UI.
- Any length or truncation constraint that matters for that surface.

**Helpful if present**

- The page title or paired description when checking for duplication.
- The intended audience and whether domain terms are expected.

**Only investigate if encountered**

- Whether a sibling field should be rewritten in tandem because the two strings duplicate or contradict each other.

## First move

1. Separate true metadata strings from prose or technical identifiers.
2. Confirm the target surface so truncation guidance is anchored to the right limit.
3. Review the strings in batches when possible so duplication and consistency are easier to spot.

## Workflow

1. For each string, evaluate:
   - front-loading
   - concreteness
   - filler and hedging
   - active voice
   - duplication against related fields
   - difficult or vague word choice
   - truncation fit for the target platform
   - one-idea-per-field discipline
2. Mark each dimension clearly and explain failures briefly.
3. When a string needs work, provide a concrete rewrite rather than a vague suggestion.
4. Keep the audit terse enough that the user can act on it quickly across a batch of strings.

## Guardrails

- **Must not** apply paragraph-level readability rules to short metadata strings.
- **Must not** spend time auditing technical identifiers that the user is not meant to rewrite.
- **Must not** repeat the title inside the description unless that duplication is intentionally required by the surface.
- **Should** prefer concrete rewrites over abstract writing advice.
- **Should** treat length as surface-specific rather than using one global character limit.
- **Should** preserve expected domain terms when the audience will search for or recognize them.

## Output format

For each string, return:

```markdown
### [Field name] — [length] chars

> [The string itself]

- Front-loading: [✓/⚠/✗] [reason if needed]
- Concreteness: [✓/⚠/✗] [reason]
- Filler: [✓/⚠/✗] [reason]
- Active voice: [✓/⚠/✗] [reason]
- Duplication: [✓/⚠/✗] [reason]
- Word choice: [✓/⚠/✗] [reason]
- Truncation fit: [✓/⚠/✗] [reason] — platform: [SERP/GitHub/Twitter/OG]
- One idea: [✓/⚠/✗] [reason]

**Rewrite:** [only when needed]
```

## Validation

- Confirm every reviewed item is actually a short copy field rather than prose or a technical identifier.
- Keep the output actionable in seconds; if a string is already clean, do not pad the audit.

## Examples

- "Check these page titles and descriptions."
- "Review my GitHub bio."
- "Tighten these repo taglines."
- "Audit the FAQ answers and schema descriptions we just wrote."
