# Reverse prompt decision rules

Use these rules to decide whether to return an improved prompt, proceed with the work, or stop on a blocker.

## Mode selection

### Use `rewrite-and-return` when

- The user explicitly asks to improve, rewrite, sharpen, or reverse-prompt a request.
- The user asks for the "best prompt," "better prompt," or "what prompt should I use" without also asking you to do the underlying work.
- Prompt-help intent is clear but execution intent is absent.

### Use `rewrite-and-proceed` when

- The user asks for prompt improvement and also asks you to act on it.
- The prompt contains explicit action wording such as:
  - `then do it`
  - `then execute`
  - `before you start`
  - `improve this prompt and act on it`
  - `rewrite this and then implement it`
- The improved brief is clearly meant to drive the next phase immediately.

## Precedence and ambiguous fallback

- If prompt-help wording and explicit action wording both appear, prefer `rewrite-and-proceed`.
- If prompt-help wording is explicit and action wording is missing, prefer `rewrite-and-return`.
- If the user's underlying need is a formal execution contract rather than a loose prompt critique, use the contract-shaped brief variant of this skill instead of falling back to generic prompt cleanup.
- If intent is still ambiguous after rewriting, prefer `rewrite-and-return` rather than silently starting work.

## Blocking ambiguity

Treat the request as blocked when one or more of these apply:

- A required target surface is unknown and cannot be safely inferred from repository context.
- The request contains conflicting goals or constraints that would materially change the work.
- The next phase is unclear enough that choosing `research`, `plan`, or `implement` would be guesswork instead of a reasonable default.
- Validation expectations are missing for a change that clearly needs a completion check and no safe repository default can be inferred.

## Phase routing

- Route to **research** when codebase state, dependency behavior, or surrounding system context is still unknown enough that discovery should happen first.
- Route to **plan** when the desired outcome is clear but the work is multi-step, cross-file, or risky enough to benefit from an explicit execution plan before editing.
- Route to **implement** when the target surface, constraints, and likely validation path are concrete enough to begin direct work safely.
- If the request is blocked, return the rewritten brief plus the blocker instead of forcing a phase transition.

## Output expectations

- `rewrite-and-return`: improved brief + assumptions or blockers + recommended next phase
- `rewrite-and-proceed`: improved brief used internally + concise assumptions or blockers note + immediate transition into the next phase

## Non-goals

- Do not turn this into an always-on prompt policy.
- Do not silently inject hidden prompt rewrites through an extension.
- Do not expand the skill into a plan/contract orchestrator.
- Do not add repository-specific one-off playbook steps that would make the skill less reusable.
