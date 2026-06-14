---
name: ast-grep
description: "Use when you need ast-grep structural search, linting, or safe codemod rewrites, especially for requests that mention ast-grep, sg, codemod, rule files, or syntax-aware edits instead of plain-text search."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# ast-grep

Use this skill when the task benefits from AST-based search, linting, or rewrites instead of regex- or line-based editing.

## Use this skill when

- You need structural search over code, lint-rule authoring, or rewrite changes with AST-aware patterns.
- You want repeatable, reviewable edits across many files.
- You want to preview candidate matches before applying a codemod.
- A request explicitly mentions `ast-grep`, `sg`, codemod, rule files, or syntax-aware edit work.

## Do not use this skill when

- The task is simple literal string search; route to normal `rg`/`glob` usage.
- The request is under-specified and needs sharpening first; route to `reverse-prompt`.
- The main work is root-cause analysis of a failure; route to `systematic-debugging`.
- The task is writing behavior tests first for a feature or bugfix; route to `test-driven-development`.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| "Author a lint rule for a structural pattern" | Yes | - |
| "Replace a JS API call pattern across all TS files safely" | Yes | - |
| "Find where this exact string appears" | No | direct `rg` search |
| "I have a failing test and do not know why" | No | `systematic-debugging` |
| "Before coding, rewrite my vague request into an executable brief" | No | `reverse-prompt` |
| "Implement feature X with failing test first" | No | `test-driven-development` |

## Inputs to gather

**Required before editing**

- Goal: search, lint, or rewrite.
- Target language(s) and search scope (paths/directories).
- Structural pattern and, for rewrites, replacement pattern or rule file.

**Helpful if present**

- Existing ast-grep rule files in the repository.
- Known exclusions (`dist`, generated code, vendored directories).
- Expected output format (human-readable vs JSON for tooling).

**Only investigate if encountered**

- Parser/language mismatch warnings.
- Rewrite collisions where one pass affects later matches.
- File-encoding or formatting side effects.

## First move

1. Choose mode: search, lint, or rewrite.
2. Build a narrow command from the reference templates and run a preview first.
3. Expand scope only after the preview matches the intended shape.

## Workflow

1. Build a search or rewrite command from [`references/command-patterns.md`](references/command-patterns.md) and constrain it by language/path.
2. For search or lint work, inspect representative results before broadening scope.
3. If rewrite is needed, choose replacement (`-r`) or rule-file mode (`--rule`) and re-run preview.
4. Apply rewrite only after preview is clean and exclusions are explicit.
5. Review resulting diffs and check for unintended changes using the safety checklist in [`references/safety-and-review.md`](references/safety-and-review.md).
6. If output is noisy, roll back and tighten pattern/scope before retrying.

## Outputs

- A documented ast-grep command (or rule invocation) used for the task.
- For rewrites, a clean diff showing intended structural edits only.
- For linting, a tested rule file or rule invocation.
- A short summary of matched scope, applied exclusions, and any rollback/retry decisions.

## Guardrails

- Default to non-destructive flow: preview before apply.
- Never run broad rewrites without explicit language and scope constraints.
- Prefer the full `ast-grep` binary name in docs and generated commands; use `sg` only if local shell compatibility requires it.
- Keep command examples portable (repo-relative paths only, no user-specific absolute paths).
- Treat helper automation as optional convenience; do not require it to use this skill.
- If pattern intent is ambiguous, narrow to search mode first instead of guessing rewrite behavior.

## Validation

- Run metadata/structure validation:
  - `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/ast-grep/SKILL.md`
  - `node skills/skill-authoring/scripts/validate-skill-library.mjs`
- Confirm every support file listed in `## Reference files` exists and is linked.
- Smoke-test description-level routing with one trigger and one near-miss:
  - should trigger: `Use ast-grep to rewrite obj.val && obj.val() to obj.val?.() in TypeScript, preview first`
  - should not trigger: `Find the exact string "obj.val && obj.val()" in this repository.`

## Examples

- `Use ast-grep to search for \`console.log($X)\` in \`src/\` with \`--lang ts\` and return JSON output.`
- `Use ast-grep to rewrite \`var code = $PAT\` to \`let code = $PAT\` in JavaScript after previewing matches.`
- `Use ast-grep to rewrite \`obj.val && obj.val()\` to optional chaining in TypeScript after a narrow preview.`

## Reference files

- [`references/command-patterns.md`](references/command-patterns.md) - search/rewrite command templates and scoped usage patterns
- [`references/safety-and-review.md`](references/safety-and-review.md) - review checklist, rollback flow, and failure-mode handling
- [`assets/examples.md`](assets/examples.md) - trigger and near-miss prompt matrix for activation tuning
- [`scripts/scaffold-ast-grep-command.mjs`](scripts/scaffold-ast-grep-command.mjs) - optional helper to scaffold portable ast-grep commands
