# Request examples for session-store-history

Use this file when the user's wording is vague and you want a quick prompt-to-query translation before composing SQL.

## Example 1 - recent work summary

User says:

> What did I work on yesterday?

Translate to:

- **Primary tables:** `sessions`, `turns`
- **Keywords:** none required unless the user adds a topic
- **Filters:** timestamp window for yesterday
- **Evidence to return:** session timestamps, repo or cwd, original ask, short summary

## Example 2 - prior topic recall

User says:

> Have I worked on auth refresh tokens before?

Translate to:

- **Primary tables:** `search_index`, `turns`, `checkpoints`
- **Expanded terms:** `auth`, `login`, `token`, `refresh`, `JWT`, `session`, `OAuth`
- **Fallbacks:** `LIKE '%refresh%'`, `LIKE '%token%'`
- **Evidence to return:** strongest matching sessions plus the approach or result from those sessions

## Example 3 - file-level history

User says:

> Did I ever change `src/api/auth.ts` in a previous session?

Translate to:

- **Primary tables:** `session_files`, `sessions`
- **Expanded terms:** path fragments like `auth.ts`, `src/api`, `api/auth`
- **Evidence to return:** session IDs, timestamps, repo, and whether the file was first seen via edit or create

## Example 4 - ref tracing

User says:

> Which session created PR #42?

Translate to:

- **Primary tables:** `session_refs`, `sessions`
- **Filters:** `ref_type = 'pr'`, `ref_value = '42'`
- **Evidence to return:** matching session plus nearby summary or checkpoint details

## Example 5 - false-positive boundary

User says:

> Search this repo for `AuthService`.

Do **not** use this skill.

Why:

- This is current-workspace exploration, not cross-session history.
- Use repo-local search tools like `lsp`, `glob`, `rg`, or `view` instead.
