# RPI-V prompt templates

Copy-paste starters for agent-compatible interactive harnesses.

## Phase 1 — Research

```
TASK: <one sentence describing the goal>

Research questions:
1) Where is the current implementation of <X>?
2) What patterns and conventions should the solution follow (architecture, naming, error handling)?
3) What tests cover this area today, and what new tests will be needed?

Rules:
- Do NOT propose code changes yet.
- Provide file paths and line numbers.
- Note any commands that must run after changes (e.g. code generation, migrations).

Output:
- Short summary
- Bulleted list of relevant files with reason each matters
- Open questions / unknowns
```

## Phase 2 — Plan

```
Use the current research notes and update `plan.md`.

Optional input if you saved research notes:
files/research-<topic>.md

Create a phased implementation plan (Phase 1..N) that:
- Lists exact files to edit per phase
- Includes verification commands per phase (automated and manual)
- Has clear success criteria per phase

Do not make code changes yet. Stop after producing the plan.
```

## Phase 3 — Implement (single phase)

```
Implement ONLY Phase <N> from the current `plan.md`.

Rules:
- Make minimal changes.
- Follow existing repo conventions and architecture.
- Run the phase's verification commands after implementing.
- When done, summarise: what changed, any follow-ups needed before the next phase.
```

## Phase 4 — Validate

```
Validate the implementation against the current `plan.md`.

I implemented: Phase <list>

Please:
1) Compare the diff to the plan and note any deviations (intentional or not).
2) Run and report on the verification commands.
3) Produce a pass/fail checklist against the plan's success criteria.
```
