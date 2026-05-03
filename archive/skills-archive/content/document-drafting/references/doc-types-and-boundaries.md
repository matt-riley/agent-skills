# Document types and skill boundaries

## Document types this skill owns

These are the primary document shapes this skill handles end-to-end — from blank slate or rough notes through a structured, reviewer-ready draft.

| Document type | Typical signals |
| --- | --- |
| Feature or project proposal | "I need to write up a proposal for X", requests for buy-in or approval |
| Technical spec or design doc | Architecture decisions, API contracts, system-level designs |
| RFC (request for comments) | Explicit feedback solicitation, numbered proposal with alternatives |
| README (project, library, or service) | Onboarding/orientation docs for a codebase or product surface |
| Decision document / ADR | Recording a choice with context, alternatives considered, and rationale |
| Migration guide | Step-by-step instructions for a breaking change, upgrade, or platform move |
| Onboarding document | Explains a system, team, or process to a new participant |
| Runbook | Step-by-step operational procedure tied to an incident, deployment, or task |
| Engineering blog post or internal post-mortem | Long-form narrative document meant for a technical audience |

## Near-miss tasks that should route elsewhere

Use this table when the initial request sounds like document work but fits a more specific skill better.

| Task | Route to | Why |
| --- | --- | --- |
| Prose readability audit on an already-drafted document | `readability-check` | Structure is settled; only prose quality needs attention |
| Short metadata string review (title, bio, tagline, schema description) | `metadata-check` | Single-string clarity checks, not full document structure |
| Sharpening a rough prompt into an AI-executable brief | `reverse-prompt` | The output is for an AI, not a human reader |
| Defining an explicit task contract (GOAL / CONSTRAINTS / FORMAT / FAILURE) | `prompt-contracts` | The deliverable is a task contract, not a prose document |
| Creating a stable planner/review/execution handoff artifact with structured sections | `workflow-contracts` | The deliverable is a durable structured workflow record, not a narrative document |
| Writing, hardening, or getting approval for an implementation plan | `plan-review` | The deliverable is a reviewable plan before or during implementation, not a finished standalone document |
| Migration plan (step-by-step task breakdown with owners, dependencies, or acceptance criteria) | `plan-review` | The deliverable is an executable plan, not audience-facing prose explaining how to migrate |

## Overlap notes

### readability-check

- **Split point:** this skill owns structure and content; `readability-check` owns prose quality.
- **When to overlap:** use `document-drafting` to produce the draft, then hand off to `readability-check` when the only remaining gap is sentence clarity, reading-ease score, or ESL accessibility.
- **When not to stack:** do not add `readability-check` during drafting — audit prose only after the structure is settled.
- **Edge case:** if the request is explicitly "make this document easier to read for non-native English speakers," route to `readability-check` even when the document is already fully structured.

### metadata-check

- **Split point:** this skill handles full documents; `metadata-check` handles short, audience-facing metadata strings (title, description, tagline, bio, schema label).
- **When to overlap:** a README or proposal often has a title + short description that could benefit from `metadata-check` after the full document draft is stable.
- **When not to stack:** if the request is specifically "review my README title and description" without asking for the whole document, route to `metadata-check` alone.
- **Edge case:** package README short descriptions that appear in registries are `metadata-check` work, even though they live in a README file.

### reverse-prompt

- **Split point:** this skill writes documents for human readers; `reverse-prompt` rewrites prompts or instructions for AI execution.
- **They are not interchangeable.** A well-structured product spec and a well-structured AI task prompt have different audiences, success criteria, and failure modes.
- **When to overlap:** if the user wants to write a prompt document (e.g., a reusable LLM prompt stored in a repo), use `document-drafting` for the file structure and `reverse-prompt` for the prompt wording itself.

### prompt-contracts

- **Split point:** `prompt-contracts` defines task success criteria (GOAL / CONSTRAINTS / FORMAT / FAILURE) before a task runs; `document-drafting` produces a deliverable document.
- **When to overlap:** if the user wants to write a task contract as a named document stored for later reuse, both skills are relevant — `prompt-contracts` drives the content contract, `document-drafting` handles the file structure and prose.
- **When not to stack:** if the user just wants an explicit success definition for the current task and is not producing a reusable doc, `prompt-contracts` alone is sufficient.

### workflow-contracts

- **Split point:** `workflow-contracts` produces structured planner/review/execution handoff artifacts with versioned sections and durable status fields; `document-drafting` produces human-facing narrative prose documents.
- **When to overlap:** rarely. These serve different reader goals. Occasionally a workflow may need an accompanying narrative design doc, in which case both can be active.
- **When not to stack:** if the request is "capture the plan and execution record for this task," that is `workflow-contracts`. If the request is "write a design doc for this feature," that is `document-drafting`.

### plan-review

- **Split point:** `plan-review` governs the create-review-approve cycle for implementation plans before or during code changes; `document-drafting` produces finished standalone documents.
- **When to overlap:** a design doc may feed into an implementation plan. Draft the design doc first with `document-drafting`, then use `plan-review` when the implementation planning phase begins.
- **When not to stack:** if the deliverable is an implementation plan ready for reviewer gates, use `plan-review`. If the deliverable is a design document that will inform a plan later, use `document-drafting`.
