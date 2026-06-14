---
name: code-tour
description: "Use when asked to create a .tour walkthrough — onboarding, PR review, RCA, architecture, or any persona-targeted step-by-step code narrative. Not for codebase exploration without a .tour file output."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# Code tour

Use this skill when the goal is to produce a `.tour` JSON file — a persona-targeted, step-by-step walkthrough that links directly to real files and line numbers and works with the VS Code CodeTour extension.

## Use this skill when

- The user asks for a "code tour", "onboarding tour", "PR review tour", "RCA tour", "architecture tour", or any named walkthrough through the codebase.
- The user asks to "explain how X works", "help someone ramp up", or "create a contributor guide" where a structured, navigable artifact is the intended output.
- The user says "vibe check", "just give me the gist", or "walk me through this" in a way that implies a persisted, shareable walkthrough rather than a chat answer.
- The request names a persona (new joiner, security reviewer, refactorer, vibecoder, etc.) and a codebase to walk through.

## Do not use this skill when

- The goal is codebase exploration or documentation without a `.tour` file artifact — route to `acquire-codebase-knowledge` instead.
- The user wants a pre-edit map of relevant files and patterns before making changes — route to `context-map` instead.
- The request is a plain explanation or analysis that can be answered in a chat response without writing a file.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| "Create a tour so new joiners can ramp up on the API" | Yes | — |
| "Explain how auth works" (chat answer is sufficient) | No | answer directly |
| "Map the files involved in this refactor before I touch anything" | No | `context-map` |
| "Document the architecture and create ARCHITECTURE.md" | No | `acquire-codebase-knowledge` |
| "Create an onboarding tour and also write the CONVENTIONS.md" | Split | `code-tour` for the `.tour` file; `acquire-codebase-knowledge` for the docs |

## Inputs to gather

**Required before starting**

- The target codebase root (confirm it is accessible and not empty).
- The persona or audience for the tour — infer from the request before asking.

**Helpful if present**

- The depth or length preference (quick, standard, deep).
- Specific files or areas the user wants covered.
- A PR number, branch, or commit to set as `ref`.
- Whether the tour should be marked `isPrimary` or chain to a `nextTour`.

**Only investigate if encountered**

- Existing `.tours/` directory content (check for title conflicts and `nextTour` cross-references).
- `stepMarker` requirements (only when the user asks for source-embedded anchors).

## First move

1. Explore the codebase: list the root, read the README, and map the top-level directory structure 1–2 levels deep.
2. Infer persona, depth, and focus area from the user's request — ask only for a bug description or feature name if you genuinely cannot infer them.
3. Find entry points for the inferred persona before writing any step.

## Workflow

1. **Discover the repo.** Read entry points, the README, and key config files. Note which files actually exist — every path in the tour must be verified. For repos with 100+ files, identify the 2–3 modules most relevant to the persona and read those deeply rather than skimming everything.
2. **Read intent and infer the tour shape.** Use the intent map in [`references/examples.md`](references/examples.md) to select persona, depth, and step count. Infer `ref`, `isPrimary`, and `nextTour` silently from the request; ask only when you genuinely cannot infer.
3. **Read every file you plan to reference.** Verify every file path and line number. A tour pointing to a wrong file or non-existent line is worse than no tour.
4. **Write the tour.** Save to `.tours/<persona>-<focus>.tour`. Follow the schema in [`references/codetour-schema.json`](references/codetour-schema.json). Structure: orientation step (must have `file` or `directory` anchor) → high-level map → core path → closing content step. Use step types that fit the situation; the [`references/examples.md`](references/examples.md) file shows each type in practice.
5. **Validate.** Run `python skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .`. Fix every error before continuing. Re-run until the validator reports only warnings or passes clean.
6. **Summarize.** Tell the user: the output file path, a one-paragraph summary of who the tour is for and what it covers, the `vscode.dev` share URL for public repos, and any requested files that did not exist.

## Outputs

- `.tours/<persona>-<focus>.tour` — the validated CodeTour JSON file.
- A brief summary message: file path, audience summary, share URL if applicable, and any missing-file notices.

## Guardrails

- Only create `.tour` JSON files. Do not create, modify, or scaffold any other file during this skill.
- Every `file` and `directory` path in the tour must be relative to the repo root — no leading `/` or `./`, no absolute paths.
- Every `line` number must be verified by reading the file. Never guess or estimate.
- Every `pattern` regex must compile and match at least one real line in the target file before you include it.
- The first step must have a `file` or `directory` anchor. A content-only first step renders as a blank page in VS Code CodeTour.
- Do not suggest `stepMarker` unless the user asks — it requires editing source files, which this skill does not do.
- `commands` only executes VS Code commands, not shell commands. Do not suggest shell execution through a `commands` step.
- Do not hallucinate files. If a user-requested file does not exist, say so and skip the step rather than substituting silently.
- Use the SMIG formula for every step description: Situation, Mechanism, Implication, Gotcha. A description that only names the file adds no value.

## Validation

**Mechanical:**

```bash
python skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .
```

Checks JSON validity, file/directory existence, line-number bounds, pattern regex matches, URI format, `nextTour` cross-references, content-step count, and narrative arc. Fix every error; re-run until clean.

**Manual fallback** (if Python is unavailable): confirm step 1 has a `file` or `directory` anchor, all paths exist and are relative, all line numbers are in bounds, and `nextTour` matches an existing tour title exactly.

**Smoke test:**

- should trigger: "Create an onboarding tour for new engineers joining this repo"
- should not trigger: "Map the files I need to read before refactoring the auth module"

## Examples

- "Create a new-joiner onboarding tour for this repo that covers the directory structure, setup steps, and the main request lifecycle."
- "Generate a PR review tour for branch `feature/auth-refactor` — highlight the changed files and flag anything risky for the reviewer."
- "Write an architecture tour for the tech lead persona. It should cover module boundaries, key design decisions, and the data flow from ingestion to storage."

## Reference files

- [`references/codetour-schema.json`](references/codetour-schema.json) — authoritative JSON schema for `.tour` files; check this for valid field names, types, and step structure
- [`references/examples.md`](references/examples.md) — real-world `.tour` files from production repos, annotated by step type and technique; also includes the persona→depth→step-count calibration table and step-type decision guide
- [`scripts/validate_tour.py`](scripts/validate_tour.py) — run after writing any tour to check paths, line numbers, patterns, and narrative arc; generic and self-contained, requires Python 3.8+
