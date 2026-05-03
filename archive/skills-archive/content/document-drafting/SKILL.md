---
name: document-drafting
description: Draft, structure, and iteratively refine documents such as proposals, specs, RFCs, READMEs, decision docs, and migration guides. Use when the user needs to produce or substantially reshape a structured document.
license: Proprietary
metadata:
  owner: mattriley
  version: 1.0.0
  maturity: draft
---

# Document Drafting

## Use this skill when

- The user asks to draft, write, or substantially reshape a structured document (proposal, spec, RFC, README, decision doc, migration guide, onboarding doc, runbook).
- A rough outline or scattered notes need to be turned into a structured draft.
- An existing document needs a major structural revision rather than a prose polish pass.
- The user wants section-by-section drafting with iterative feedback.

## Do not use this skill when

- The main need is a prose readability audit on an already-drafted document — use `readability-check`.
- The main need is reviewing a short metadata string such as a title, bio, or tagline — use `metadata-check`.
- The main need is sharpening a rough prompt into an executable brief — use `reverse-prompt`.
- The main need is defining an explicit task contract with GOAL/CONSTRAINTS/FORMAT/FAILURE — use `prompt-contracts`.
- The main need is creating a stable planner/review/execution handoff artifact — use `workflow-contracts`.
- The request is for a migration **plan** (step-by-step task breakdown with owners, dependencies, or acceptance criteria) rather than a migration **guide** (audience-facing prose explaining how to migrate) — use `plan-review` for the former.
- The document is primarily code, configuration, or generated output rather than human-facing prose.

## Inputs to gather

**Required before drafting**

- Document type (proposal, spec, RFC, README, decision doc, migration guide, or other).
- Intended audience and their likely prior knowledge.
- The core message or decision the document must convey.
- Any existing draft, outline, or notes to build from.

**Helpful if present**

- Publishing surface or destination (GitHub, Confluence, internal wiki, public site).
- Length or depth expectations.
- Sections the user already considers settled versus sections needing most work.
- Related documents, prior decisions, or context the audience will expect the doc to reference.

**Only investigate if encountered**

- Whether the document will feed a downstream review gate that requires a specific schema or template.
- Whether visual structure (tables, diagrams, code blocks) will matter for the target rendering surface.

## First move

1. Confirm document type and audience before proposing any structure.
2. Propose a section outline and get explicit agreement before drafting body content.
3. Draft section by section; do not front-load every section at once unless the user asks.

## Workflow

1. Gather context: document type, audience, core message, and any existing draft or notes.
2. Propose a section outline and confirm it before writing body content.
3. Draft each section, pausing at natural checkpoints for feedback.
4. Run a fresh-reader validation pass once a complete draft exists.
5. Incorporate feedback and tighten; hand off to `readability-check` when prose polish is the remaining need.

## Guardrails

- **Must** confirm the document type and audience before proposing a structure.
- **Must** get outline agreement before drafting body sections.
- **Must not** replace audit, review, or handoff skills listed in the exclusions above — defer to the appropriate skill.
- **Should** draft iteratively with explicit checkpoints rather than producing a full document in one pass.
- **Should** flag assumptions about audience, scope, or constraints when they would materially change the structure.
- **May** hand off to `readability-check` once drafting is complete and prose polish is the remaining need.

## Validation

- Confirm the proposed structure matches the document type and stated audience before drafting body sections.
- After a complete draft, run a fresh-reader pass: read `references/review-loop.md` for the checklist.
- If prose polish is the remaining gap, defer to `readability-check` rather than extending this skill's scope.

## Reference files

- Read `references/doc-types-and-boundaries.md` when clarifying whether this skill owns the document type or another skill is a better fit.
- Read `references/review-loop.md` when conducting a fresh-reader validation pass on a complete draft.
