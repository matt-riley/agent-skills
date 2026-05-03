# Readability audit reference

Use this file when the task is a prose audit on already-written multi-paragraph text.

## What to check

1. paragraph structure
2. opening paragraph strength
3. sentence length
4. passive voice
5. difficult words
6. filler and hedging
7. transitions
8. variation
9. subheadings and heading hierarchy

## Output shape

```markdown
## Readability audit: [document title]

### Score
- Flesch Reading Ease: [n] ([band])
- Intro: [n] · Conclusion: [n]
- Per-category: 1. ✓  2. ⚠  3. ✓  4. ✗  5. ⚠  6. ✓  7. ✓  8. ⚠  9. ✓

### Summary
[Overall readability, biggest issues, and who the draft currently serves.]

### Issues found
[Location, quoted text, why it is a problem, concrete fix.]

### What's working
[Specific strong sentences, transitions, headings, or paragraphs worth keeping.]
```

## Guardrails

- Read the full text before making sentence-level judgments.
- Keep expected domain terms when the audience would reasonably know them.
- Do not use this mode for titles, bios, taglines, or other short metadata strings.
