---
name: readability-check
description: Audit multi-paragraph prose for readability, especially for readers who use English as a second language, and report concrete fixes plus a Flesch Reading Ease score.
---

# Readability check

## Use this skill when

- The user asks for a readability check, readability pass, or asks whether a post or document is readable.
- A substantial draft is complete and needs a prose-quality pass before publication.
- Another skill produced multi-paragraph content such as a README, article, guide, or contributor document that now needs readability review.

## Do not use this skill when

- The input is a short metadata string such as a title, bio, description, or tagline. Use [`metadata-check`](../metadata-check/SKILL.md).
- The main task is still active drafting or broad content strategy rather than reviewing existing prose.
- The text is mostly technical identifiers, code, or configuration rather than prose.

## Inputs to gather

**Required before editing**

- The full prose to review.
- The document title or a useful label for the audit.
- The target audience, with the default assumption that many readers use English as a second language.

**Helpful if present**

- Whether the document is technical, non-technical, or mixed.
- Whether intro or conclusion quality matters disproportionately for the publishing surface.

**Only investigate if encountered**

- Whether heading structure, table of contents, or section ordering contributes to readability issues.

## First move

1. Read the full text before judging any one sentence in isolation.
2. Calibrate for an English-as-a-second-language audience by default.
3. Separate prose issues from domain terms the intended audience would reasonably expect.

## Workflow

1. Review the document against the nine rubric areas:
   - paragraph structure
   - opening paragraph strength
   - sentence length
   - passive voice
   - difficult words
   - filler and hedging
   - transitions
   - variation
   - subheadings and heading hierarchy
2. For each issue, quote the relevant text, name its location, explain the problem, and suggest a concrete fix.
3. Compute and report a Flesch Reading Ease score plus per-category pass / needs-work / problem status.
4. Call out what is already working well so the writer can preserve strong patterns.

## Guardrails

- **Must not** use this skill on short strings where paragraph-level analysis does not apply.
- **Must not** flag expected domain terms as difficult words in technical sections just because they are technical.
- **Must not** rely on the Flesch score alone; paragraph and structure issues still matter.
- **Should** hold non-technical paragraphs in technical pieces to a stricter plain-English standard.
- **Should** favor specific quoted evidence over generic prose advice.
- **Should** treat intro and conclusion quality as especially important because readers and AI systems overweight them.

## Output format

```markdown
## Readability audit: [post title]

### Score
- Flesch Reading Ease: [n] ([band])
- Intro: [n] · Conclusion: [n]
- Per-category: 1. ✓  2. ⚠  3. ✓  4. ✗  5. ⚠  6. ✓  7. ✓  8. ⚠  9. ✓

### Summary
[Overall readability, biggest issues, and who the draft currently serves.]

### Issues found
[Grouped by category. For each: location, quoted text, why it is a problem, concrete fix.]

### What's working
[Specific strong sentences, transitions, headings, or paragraphs worth keeping.]
```

## Validation

- Confirm the input is substantial prose and not a metadata-only task.
- Make the feedback specific enough that a writer can revise immediately without guesswork.

## Examples

- "Run a readability pass on this post."
- "Is this README readable for non-native English speakers?"
- "Audit this guide before I publish it."
