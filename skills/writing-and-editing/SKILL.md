---
name: writing-and-editing
description: "Draft structured documents, audit prose readability, and review short audience-facing metadata strings — solo writing quality work. Use when the primary task is writing, editing, or copy quality, not iterative co-authoring with reader feedback (use doc-coauthoring for that)."
license: GNU GPL v3
metadata:
  version: 1.2.0 # x-release-please-version
  owner: mattriley
  maturity: draft
  kind: task
---

# Writing and editing

## Use this skill when

- The user wants to draft, rewrite, or substantially restructure a document such as a proposal, spec, RFC, README, migration guide, onboarding doc, or runbook.
- The user wants a readability audit on already-written multi-paragraph prose.
- The user wants a short-string audit on metadata such as titles, descriptions, bios, taglines, schema descriptions, or README blurbs.
- Another skill produced human-facing prose or copy and the remaining work is writing quality rather than code or workflow design.

## Do not use this skill when

- The main deliverable is an implementation plan, rollout plan, or reviewer-gated plan artifact — use [`plan-review`](../plan-review/SKILL.md).
- The main task is to sharpen a rough ask into a repository-grounded execution brief or contract-shaped prompt before work starts — use [`reverse-prompt`](../reverse-prompt/SKILL.md).
- The main task is GitHub profile or repository surface setup rather than the writing itself — use [`github-presence`](../github-presence/SKILL.md).
- The output is primarily code, config, generated files, or a structured workflow handoff artifact rather than human-facing prose.

## Inputs to gather

**Required before editing**

- Which mode applies: `draft`, `readability-audit`, or `metadata-audit`.
- The target document or strings.
- The intended audience and publishing surface.
- Any constraints on tone, length, or structure.

**Helpful if present**

- Existing notes, outline, or rough draft.
- Any paired fields that should be reviewed together, such as title + description.
- Whether the user wants review-only output or an actual rewrite.

**Only investigate if encountered**

- Whether a repo, product, or org-specific template should shape the document.
- Whether a broader repo-quality or profile-surface audit belongs to [`github-presence`](../github-presence/SKILL.md) instead.

## First move

1. Classify the task as `draft`, `readability-audit`, or `metadata-audit`.
2. Confirm the audience and target surface before changing wording.
3. Pick the matching reference file and stay inside that mode unless the user explicitly wants a cross-mode pass.

## Workflow

1. **Route to the right mode first.**
   - `draft`: a structured document needs to be created or substantially reshaped.
   - `readability-audit`: the structure is mostly settled and the user wants prose-quality feedback.
   - `metadata-audit`: the task is about short audience-facing strings.

2. **Draft mode.**
   - Confirm document type and audience.
   - Propose an outline before drafting body sections.
   - Draft iteratively instead of front-loading the full document unless the user asks for a full first pass.
   - Run a fresh-reader pass once a complete draft exists.

3. **Readability-audit mode.**
   - Read the full prose before judging sentence-level issues.
   - Report concrete issues with quoted evidence and a Flesch Reading Ease score.
   - Keep domain terms that the intended audience would reasonably expect.

4. **Metadata-audit mode.**
   - Review strings in batches when possible.
   - Check front-loading, concreteness, filler, duplication, and truncation fit for the target surface.
   - Provide a concrete rewrite whenever a string fails an important check.

5. **Handle cross-mode work deliberately.**
   - Draft first, then run readability or metadata review only after the structure or field set is stable.
   - If the user really wants only one narrow pass, do not broaden into the other modes automatically.

## Outputs

- A mode-specific deliverable: drafted document sections, a readability audit with evidence and score, or concrete metadata rewrites.
- Audience-aware structure or grouped feedback that stays aligned to the chosen `draft`, `readability-audit`, or `metadata-audit` mode.
- A final pass result for the selected mode without drifting into unrelated review or planning workflows.


## Guardrails

- **Must** classify the task correctly before applying guidance.
- **Must not** treat short metadata strings as if they were full-document prose.
- **Must not** treat a settled readability audit as an excuse to redesign the whole document unless the user asks.
- **Must not** replace planning, prompt-sharpening, or GitHub-surface skills when those are the true deliverables.
- **Should** keep drafting iterative and outline-first.
- **Should** keep readability feedback evidence-based and specific.
- **Should** keep metadata feedback terse, concrete, and surface-aware.

## Validation

- Confirm the chosen mode matches the actual deliverable.
- In draft mode, confirm the outline matches the document type and audience before filling body sections.
- In readability-audit mode, provide a Flesch score and quoted evidence.
- In metadata-audit mode, keep the output actionable in seconds and provide rewrites only where needed.

## Examples

- `Draft a migration guide for customers moving from v2 to v3 of our API.`
- `Audit this README for readability — it's too dense and our audience is not all engineers.`
- `Review these 12 OpenAPI description strings for clarity, front-loading, and truncation fit.`

## Reference files

- Read `references/doc-types-and-boundaries.md` when the task sounds like document work but may belong to another skill.
- Read `references/review-loop.md` when a complete draft needs a fresh-reader pass before handoff.
- Read `references/readability-audit.md` when running a prose audit on multi-paragraph text.
- Read `references/metadata-audit.md` when auditing titles, descriptions, bios, taglines, or similar short strings.
