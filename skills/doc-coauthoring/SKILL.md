---
name: doc-coauthoring
description: "Use when user wants to write, refactor, or expand documentation (README, guides, API docs, runbooks, specification documents)."
metadata:
  category: authoring
  audience: general-coding-agent
  maturity: beta
  kind: task
  reader_testing: required
---

# Doc-Coauthoring

Use this skill when the user wants to author, improve, or expand documentation through structured co-authoring. Documentation benefits from separated concerns—context discovery, structural design, content iteration, and validation through real readers—rather than a single linear draft-and-polish pass.

This skill splits the work into three stages: gather context and constraints, refine structure and content, and validate with reader feedback.

## Use this skill when

- The user wants to write a new document (README, guide, API reference, runbook, specification, architecture decision record).
- The user wants to significantly improve or refactor existing documentation.
- The user wants to expand documentation to cover new features, breaking changes, or updated workflows.
- The user wants structured feedback on documentation clarity or completeness before releasing it.
- The documentation will be read by multiple audiences (contributors, operators, end users) and needs to serve different goals.

## Do not use this skill when

- The task is code-comment or inline-documentation work (single-file changes). Use repository coding skills instead.
- The task is a one-off typo fix or minor style pass. Make the fix directly.
- The task is purely copyediting without structural or scope changes. Make the edits directly.
- The user explicitly wants a quick single-pass draft without iteration or feedback.
- The documentation is internal workspace notes meant for one person only (not a shared resource).

## Iron Law

> **Documentation deserves structured co-authoring.**
>
> Good documentation emerges from clear audience intent, structured iteration, and validation with real readers—not from a single authorial pass. Separation of concerns—context gathering, design, content, validation—keeps documentation coherent, complete, and trusted by its readers.
>
> A document written with reader feedback loops will always outpace one revised only by the author alone.

## Routing boundary

| Scenario | Use Doc-Coauthoring | Route Away |
|---|---|---|
| **New README or user guide** | Yes — gather context, design structure, write, test with readers | N/A |
| **API or reference documentation** | Yes — capture current state, organize logically, validate with examples | N/A |
| **Architectural decision record** | Yes — gather context, document decision + rationale, reader validation | N/A |
| **Runbook or operational guide** | Yes — gather workflows, organize by task, validate with operators | N/A |
| **Inline code comments** | No — edit directly or use code documentation skills | Use repository coding skills |
| **Minor typos or style fixes** | No — edit directly | Make the fix directly without skill invocation |
| **Single-file tech spec update** | No if scope is clear and unchanged; Yes if scope is ambiguous or will affect multiple readers | Ask user to clarify scope first |
| **Copyediting or phrasing polish** | No — edit directly in final review phase | Use a dedicated style pass, not this skill |

## Inputs to gather

Before starting the workflow:

1. **Audience and purpose**: Who will read this? What are they trying to do? (End users? Contributors? Operators? Decision makers?)
2. **Scope and content**: What topics must the document cover? What is out of scope? Are there related documents?
3. **Existing state**: Is this a new document or a revision of existing work? If existing, what problems are you fixing?
4. **Constraints**: Length expectations? Format preferences? Required sections or examples?
5. **Reader validation**: Who could provide real feedback? (e.g., new team member, operator, end user using the software)
6. **Integration**: Where will this live in the repository? Will it link to other docs?

## First move

1. **Do not start writing content yet.**
2. Ask clarifying questions about audience, purpose, scope, and constraints (see **Inputs to gather** above).
3. Confirm whether this is a **new document** or a **revision** of existing work.
4. Document the answers and move to **Stage 1: Context Gathering** in the workflow below.

## Workflow

Documentation authoring proceeds through three stages. Each stage has a clear input, goal, and output. Follow the references below for detailed guidance on each stage.

### Stage 1: Context Gathering

**Goal**: Establish audience, purpose, scope, and constraints so the structure is grounded in real reader needs.

**Input**: Answers to the inputs listed above.

**Output**: A context document capturing:
- Audience segments and what they are trying to do
- Core topics and scope boundaries  
- Key constraints (length, format, examples needed)
- Related documents and integration points
- Success criteria for reader validation

**Reference**: See [`references/stage-1-context-gathering.md`](references/stage-1-context-gathering.md) for detailed guidance and checklist.

### Stage 2: Refinement & Structure

**Goal**: Draft, organize, and refine content based on the context from Stage 1.

**Input**: Context document from Stage 1.

**Output**: A structured draft document with:
- Clear headings and logical flow  
- Complete sections addressing all scope items
- Examples, code samples, or references where needed
- Placeholder notes for sections needing review or expansion
- Links to related documentation

**Reference**: See [`references/stage-2-refinement-structure.md`](references/stage-2-refinement-structure.md) for detailed guidance on organizing content, handling multiple audiences, and drafting sections.

### Stage 3: Reader Testing

**Goal**: Validate the document with real readers before finalizing and publishing.

**Input**: Structured draft from Stage 2.

**Output**: Finalized document incorporating reader feedback:
- Clarifications based on confusion points  
- Reorganization if readers struggled to find information
- Removed redundancy or clarified jargon
- Verification that all audiences can extract their needed information
- Final review and publication

**Reference**: See [`references/stage-3-reader-testing.md`](references/stage-3-reader-testing.md) for guidance on planning reader sessions, capturing feedback, and prioritizing changes.

## Outputs

After completing all three stages, you will have:

1. **Finalized document** – ready for publication or merge into the repository
2. **Reader feedback summary** – notes on what was unclear, what worked, and what changed based on feedback
3. **Integration checklist** – links updated, related docs cross-referenced, new doc discoverable

## Guardrails

- **Do not skip Stage 1.** Without clear audience and scope, the document will be unfocused and try to serve all readers equally (and satisfy none).
- **Do not write content in Stage 1.** Context gathering is discovery, not writing. Answer the questions; collect constraints; capture goals.
- **Stage 2 drafting should be rapid.** Aim for completeness over perfection. Refinement happens with reader feedback in Stage 3.
- **Stage 3 requires real readers.** At minimum, one person from a different role or expertise area should read the draft. Their confusion is data.
- **Defer copyediting to after validation.** Do not polish prose while the document's structure or completeness is still uncertain.
- **Keep it focused.** If the document tries to serve too many audiences, split it into separate documents with clear audience boundaries.
- **Link everything.** Every reference document, related guide, or dependency should be hyperlinked so readers can discover related information.

## Validation

The skill workflow is complete when:

- [ ] Stage 1 context is documented and user confirms it captures their intent.
- [ ] Stage 2 draft is structured, complete, and ready for reader feedback.
- [ ] Stage 3 reader feedback has been collected from at least one real reader outside the original authoring team.
- [ ] Feedback has been incorporated and the document is finalized.
- [ ] The document is published or merged into the repository.
- [ ] Related documentation is updated with cross-references to the new or updated document.

- Smoke test:
  - should trigger: "Rewrite our README with reader feedback for new contributors."
  - should not trigger: "Refresh copilot-instructions.md for this repo's new conventions." (→ `agent-instructions`)

## Examples

- "Write a README for my new CLI tool for first-time users" → gather audience, scope, and constraints (Stage 1), draft structure (Stage 2), share with a first-time user for feedback (Stage 3).
- "Improve our API reference so developers can get started in 5 minutes" → identify the developer audience goal, reorganize around their entry points, validate with a developer new to the API.
- "Refactor our runbook so on-call engineers can follow it under pressure" → capture current workflows from operators (Stage 1), restructure around tasks not systems (Stage 2), test with an on-call engineer who did not write it (Stage 3).

## Reference files

- [`references/stage-1-context-gathering.md`](references/stage-1-context-gathering.md) — context gathering checklist and detailed guidance for Stage 1
- [`references/stage-2-refinement-structure.md`](references/stage-2-refinement-structure.md) — guidance on organizing content and drafting sections in Stage 2
- [`references/stage-3-reader-testing.md`](references/stage-3-reader-testing.md) — guidance on planning reader sessions and prioritizing changes in Stage 3
- [`assets/document-scaffold-template.md`](assets/document-scaffold-template.md) — reusable document scaffold template
- [`assets/feedback-capture-template.md`](assets/feedback-capture-template.md) — reader testing feedback capture template
