# Query patterns for session-store-history

Use this file when you need to decide **which `session_store` tables to query**, how to expand a concept into keywords, or how to combine FTS with structured filters.

## Table choice by question type

### "What did I work on recently?"

Start with:

- `sessions`
- `turns`

Pattern:

- Filter by `timestamp` or `created_at`
- Order descending by time
- Prefer `turn_index = 0` for the original ask when you need the task headline

### "Have I worked on X before?"

Start with:

- `search_index`
- `turns`
- `checkpoints`

Pattern:

- Expand `X` into synonyms, abbreviations, and related failure words
- Use `MATCH 'term1 OR term2 OR term3'`
- Add `LIKE` filters for broader substring matching when exact tokenization may miss a result

### "How did I handle X?"

Start with:

- `search_index`
- `checkpoints`
- `turns`

Pattern:

- Search broadly for the concept
- Pull the surrounding checkpoint summary or assistant response
- Extract the approach rather than just listing sessions

### "Which session changed file Y?"

Start with:

- `session_files`
- `sessions`

Pattern:

- Filter `session_files.file_path LIKE '%Y%'`
- Join back to `sessions` for repo, branch, and timestamp
- Pull related turns only after you identify candidate sessions

### "Which PR / issue / commit was tied to Z?"

Start with:

- `session_refs`
- `sessions`

Pattern:

- Filter `ref_type` and `ref_value` when they are known
- If the ref is only hinted at indirectly, search turns or checkpoints for the concept first, then inspect refs for the matching sessions

## Query expansion rules

Do not search only the user's literal phrase when the request is conceptual.

Examples:

- `bug` -> `bug OR fix OR error OR crash OR regression OR debug`
- `auth` -> `auth OR login OR token OR JWT OR session OR OAuth`
- `performance` -> `performance OR perf OR slow OR optimize OR latency OR cache`
- `UI` -> `UI OR component OR layout OR styling OR CSS OR rendering`

Combine:

1. FTS5 with `OR`
2. `LIKE` for broad substring coverage
3. Structured filters when the user gives a repo, branch, file, issue, or PR

## Query shapes

### Broad concept search

```sql
SELECT content, session_id, source_type
FROM search_index
WHERE search_index MATCH 'auth OR login OR token OR JWT OR session'
ORDER BY rank
LIMIT 10;
```

### Recent history with original asks

```sql
SELECT s.id, s.repository, s.branch, t.timestamp, substr(t.user_message, 1, 200) AS ask
FROM sessions s
JOIN turns t ON t.session_id = s.id AND t.turn_index = 0
WHERE t.timestamp >= date('now', '-7 days')
ORDER BY t.timestamp DESC
LIMIT 20;
```

### File-based lookup

```sql
SELECT s.id, s.repository, s.branch, s.summary, sf.file_path
FROM session_files sf
JOIN sessions s ON s.id = sf.session_id
WHERE sf.file_path LIKE '%auth/service.go%'
ORDER BY s.created_at DESC
LIMIT 20;
```

### PR linkage

```sql
SELECT s.id, s.repository, s.branch, s.summary
FROM session_refs sr
JOIN sessions s ON s.id = sr.session_id
WHERE sr.ref_type = 'pr' AND sr.ref_value = '42';
```

## Result synthesis checklist

- Name the strongest matching session or top few sessions.
- Say **why** each one matched: turn text, checkpoint, file edit, or ref.
- Preserve the user's scope: recent, historical, repo-specific, or ref-specific.
- Call out ambiguity when multiple sessions plausibly fit.
