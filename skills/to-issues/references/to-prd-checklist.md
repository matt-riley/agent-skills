# PRD checklist

Use this checklist before treating a PRD as ready to publish or hand off.

## Content quality

- `Problem Statement` describes the current problem from the user's perspective.
- `Solution` describes the desired user-visible outcome rather than implementation mechanics.
- `User Stories` are extensive enough to cover primary actors, edge cases, and any operator/admin flows that matter.
- `Implementation Decisions` describe modules, interfaces, contracts, schema or API implications, and architectural decisions without file paths or code snippets.
- `Testing Decisions` describe external behavior, target surfaces, and the closest prior art in the repository when it exists.
- `Out of Scope` is explicit enough to prevent scope creep during implementation.
- `Further Notes` captures open questions, dependencies, rollout notes, or follow-ups without hiding blockers.

## Repository grounding

- Domain vocabulary matches the repository and any existing design language or ADRs in the area.
- Candidate module boundaries prefer deep, stable interfaces when the codebase supports them.
- Technical decisions reflect current repository evidence rather than generic patterns copied from elsewhere.
- Any uncertainty is labeled explicitly instead of being written as settled fact.

## Publication readiness

- The issue title and body follow any known project conventions.
- Labels, assignees, projects, or triage fields are applied only when they are verified.
- If publication is blocked by missing tracker configuration or permissions, the markdown artifact is still complete and the blocker is stated explicitly.
