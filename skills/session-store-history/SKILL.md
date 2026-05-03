---
name: session-store-history
description: Search and summarize past work from the `session_store` database when the user asks what they worked on before, how a similar problem was handled, or which session, PR, issue, branch, or file changed something.
license: Proprietary
compatibility: Harnesses that expose a read-only `sql` tool and a `session_store`-style history database.
metadata:
  owner: mattriley
  version: 1.0.0
  maturity: draft
---

# Session store history

## Use this skill when

- The user asks what they worked on recently or in the past.
- The user asks whether they have worked on a topic, repository, file, issue, PR, or branch before.
- The user asks how a similar problem was handled in an earlier session.
- The user wants to trace a session back to a PR, issue, commit, file path, or checkpoint.
- The main task is retrieving or summarizing historical session evidence rather than changing the current workspace.

## Do not use this skill when

- The main task is exploring the current repository or finding code in the current checkout; use direct repo tools instead.
- The user wants implementation, planning, review, or debugging work rather than historical recall.
- The request is generic conversation memory with no need for session evidence or structured history.
- The answer can be read directly from the current turn or current workspace without querying `session_store`.

## Inputs to gather

**Required before querying**

- The user's actual history question.
- Any explicit repo, branch, PR, issue, commit, file path, or time-range hint.
- The core topic terms plus likely synonyms, neighboring concepts, or failure words for query expansion.

**Helpful if present**

- Whether the user wants a summary, exact session IDs, referenced files, or linked PRs and issues.
- Whether the user cares more about recent work, first occurrence, or the best matching prior example.
- Known spelling variants, abbreviations, package names, or subsystem names.

**Only investigate if encountered**

- Whether the first search should be FTS, `LIKE`, or a structured join based on the user's wording.
- Whether the answer depends on checkpoints, refs, or edited-file evidence rather than turn text alone.
- Whether multiple similarly named repositories or concepts need disambiguation in the final summary.

## First move

1. Translate the user's question into 3 query shapes: keywords, structured filters, and likely synonyms.
2. Start broad in `session_store`, then narrow once you see real candidates.
3. Say so explicitly in your first progress update: mention `session_store`, the broad-to-narrow plan, and the evidence surfaces you are checking.
4. Return evidence-backed findings with timestamps, session IDs, and refs instead of answering from memory.

## Workflow

1. Classify the request:
   - **recent activity** -> recent sessions and turns ordered by timestamp
   - **have I worked on X** -> broad keyword expansion with FTS and `LIKE`
   - **how did I handle X** -> search turns and checkpoints, then extract the concrete approach
   - **which session changed Y** -> join `session_files` and `session_refs` with sessions
   - **which PR or issue was tied to Z** -> search refs first, then pull nearby turns or checkpoints
2. Read `references/query-patterns.md` when you need query-expansion patterns, table choice, or SQL shapes for the request.
3. Read `references/request-examples.md` when the wording is ambiguous and you want representative prompt-to-query translations before composing SQL.
4. Expand conceptual searches manually. Use FTS5 `OR` terms plus `LIKE` fallbacks instead of relying on a single literal phrase.
5. Combine text search with structure:
   - `turns` for what the user asked and what was answered
   - `checkpoints` for durable session summaries
   - `session_files` for file-change evidence
   - `session_refs` for PR, issue, and commit linkage
   - `sessions` for repo, branch, summary, and timestamps
6. Start with a recall-oriented query that favors finding candidates, then tighten with repo, branch, time, file, or ref filters once the likely sessions appear.
7. If you send a progress update before the final answer, make it concrete enough to name the database and evidence surfaces, for example: `I'm querying session_store turns and checkpoints first, then I'll narrow with refs and files if needed.`
8. Synthesize the result into a short evidence-backed answer that names the most relevant sessions, what happened there, and any uncertainty or ambiguity.

## Guardrails

- **Must** use the read-only `session_store` database for cross-session history instead of the scratch `session` database.
- **Must** expand topic searches with synonyms or neighboring terms when the user's request is conceptual.
- **Must** cite the evidence surface you used: recent turns, checkpoints, refs, or edited files.
- **Must** make partial or in-progress updates explicit about `session_store` usage and which evidence surfaces are being searched.
- **Must not** answer history questions from model memory alone when `session_store` can provide evidence.
- **Must not** stop at one narrow literal query if the first result set is empty and the concept can be expanded safely.
- **Should** prefer structured joins when the user names a file, PR, issue, commit, or branch.
- **Should** make uncertainty explicit when multiple sessions are plausible matches.
- **May** quote short snippets from matched turns or checkpoints when they clarify why a session is relevant.

## Validation

- Confirm the final answer matches the user's requested timeframe, repo, or ref scope when one was provided.
- Confirm the findings come from `session_store` tables that actually support the claim you are making.
- When the first query returns nothing, retry with expanded terms before concluding there is no history.
- Run `python _shared/validate-skills.py skills` from the catalog root after editing this skill.
- If you changed trigger wording, anti-triggers, or the frontmatter description, run `python _shared/run-trigger-evals.py skills/session-store-history/evals/trigger-queries.json`.
- If you changed workflow guidance, guardrails, or support-file load conditions, run `python _shared/run-functional-evals.py skills/session-store-history/evals/evals.json`.
- Re-read `skills/README.md` beside this skill to confirm the boundary stays distinct from current-workspace exploration and non-history tasks.

## Examples

- "What did I work on last week in my Go repos?"
- "Have I touched auth token refresh before?"
- "Which session created PR #42?"
- "Did I ever edit `internal/auth/service.go` in a previous session?"

## Reference files

- Read `references/query-patterns.md` when you need table-selection rules, query expansion tactics, or reusable SQL shapes.
- Read `references/request-examples.md` when the user's wording needs to be translated into keywords, filters, and expected evidence surfaces.
