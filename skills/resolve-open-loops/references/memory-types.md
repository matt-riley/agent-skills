# Memory Types Reference

Quick reference for the Lore memory types this skill works with, the tool calls to retrieve and resolve them, and the correct `supersededBy` phrasing for each resolution outcome.

## Relevant types

| Type | What it represents | Typical resolution |
| --- | --- | --- |
| `open_loop` | A task, investigation, or question that was started but not finished | Completed, abandoned, or superseded by a newer item |
| `assistant_goal` | A standing goal or commitment the assistant is tracking | Achieved, withdrawn, or replaced by a more specific goal |

## How to retrieve them

```
memory_search  query="open loops and pending goals"  type="open_loop"     limit=50
memory_search  query="open loops and pending goals"  type="assistant_goal" limit=50
```

Search output format per row:

```
- [<id> <type>/<scope>/<scope_source>] <content> (<repository>)
```

- `id` — used as the first argument to `memory_forget`
- `scope` — `repo`, `global`, or `transferable`; never forget `global` without explicit user confirmation
- `scope: transferable` — cross-repo patterns; treat as read-only during triage

## How to resolve an item

```
memory_forget  id=<id>  supersededBy="<human-readable reason>"
```

### Recommended `supersededBy` phrases

| Outcome | Example phrase |
| --- | --- |
| Work completed | `"resolved: <one-line outcome>"` |
| Replaced by newer item | `"superseded by <id or brief description>"` |
| Stale / never relevant | `"stale: removed during triage"` |
| Explicitly abandoned | `"abandoned: <reason>"` |

Keep the phrase short (< 80 chars) and human-readable — it appears in audit history.

## Scope rules

- `repo` items: safe to forget after user confirms the work is done.
- `global` items: always ask the user explicitly before forgetting — they affect every repository.
- `transferable` items: leave them alone; they were captured in another repository's context.
