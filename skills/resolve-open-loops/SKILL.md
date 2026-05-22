---
name: resolve-open-loops
description: "Use when the stabilisation-guard blocks the session because of active open_loop or assistant_goal memories, or when the user explicitly asks to review and close out pending items in Lore."
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
---

# Resolve Open Loops

Use this skill to work through active `open_loop` and `assistant_goal` memories in Lore for the current repository, so the stabilisation-guard stands down and the session can proceed cleanly.

## Use this skill when

- The stabilisation-guard fired during `onSessionStart` or blocked a tool call with a message ending in "use `/resolve-open-loops` to work through these items".
- The user explicitly asks to review, triage, or close open loops for the current repo.
- The user wants a pre-session hygiene pass before starting a large piece of work.

## Do not use this skill when

- The goal is to browse or search Lore generally (use `memory_search` directly).
- The goal is to onboard a new repo's history into Lore (use `lore_onboard`).
- The session is already unblocked and the user wants to start implementation immediately.

## Inputs to gather

**Required before starting**

- Confirmation that Lore is available in the current session (check `memory_status` if unsure).
- The current repository — Lore's `memory_search` scopes results to it automatically.

**Helpful if present**

- The guard's count from the session-start message (tells you how many items to expect).
- Any indication from the user whether items in a particular area are already done.

## First move

Call `memory_search` for both types in parallel and present the combined list before asking the user anything:

```
memory_search  query="open loops and pending goals"  type="open_loop"     limit=50
memory_search  query="open loops and pending goals"  type="assistant_goal" limit=50
```

If both searches return zero results, tell the user the guard should not fire next session and stop — there is nothing to triage.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Guard fired — "X active items, use `/resolve-open-loops`" | Yes | — |
| User says "let's clear the Lore backlog before we start" | Yes | — |
| User wants to search what Lore knows about a topic | No | `memory_search` directly |
| User wants to recall recent session history | No | `lore_recall` |
| Lore is unavailable or not initialised | No | surface the error to the user |

## Workflow

### 1. Retrieve active items

Call `memory_search` twice in parallel — once for each type — to surface the full active list for the current repo:

```
memory_search  query="open loops and pending goals"  type="open_loop"   limit=50
memory_search  query="open loops and pending goals"  type="assistant_goal"  limit=50
```

Present the results as a numbered list grouped by type. For each item show: **id**, **content summary** (first 120 chars), and **scope** (`repo` / `global`).

### 2. Triage each item with the user

Work through items one at a time (or in small thematic groups). For each, ask what resolution applies:

| Outcome | Action |
| --- | --- |
| **Done** — the work was completed | `memory_forget id=<id> supersededBy="resolved: <brief outcome>"` |
| **Superseded** — a newer item replaces it | `memory_forget id=<id> supersededBy="<newer-id or description>"` |
| **Still open** — genuinely unfinished | Leave it; acknowledge it in context so the user can decide to tackle it now |
| **Invalid** — stale or wrong scope | `memory_forget id=<id> supersededBy="stale: removed during triage"` |

Never bulk-forget all items without user confirmation. Resolve one item (or one confirmed batch) at a time.

### 3. Confirm guard will stand down

After the triage pass, recheck the count:

```
memory_search  query="open loops and pending goals"  type="open_loop"   limit=50
memory_search  query="open loops and pending goals"  type="assistant_goal"  limit=50
```

If the remaining count is zero, tell the user the guard will not fire next session.  
If items remain, tell the user how many are left and that the guard will still warn — the user decides whether to continue.

### 4. Optionally save new memories

If the triage revealed something worth retaining (a resolved commitment, a pattern that kept recurring), offer to save it:

```
memory_save  content="<what was learned>"  type="commitment"  scope="repo"
```

Only save when the user agrees — do not create memories speculatively.

## Guardrails

- **Never forget a `global`-scope item** without explicit user confirmation — global memories affect all repositories.
- **Never bulk-forget** in a single call without the user reviewing the list first.
- **Keep `supersededBy` human-readable** — a terse phrase like `"resolved: deployed to prod"` beats a raw UUID.
- If `memory_search` returns Lore unavailable (extension not loaded, db locked), surface the error and stop — do not attempt direct DB access.
- Items with `scope=transferable` should be treated as read-only during this skill; they were written from another repo and the user should resolve them in context.

## Validation

Run `node skills/skill-authoring/scripts/validate-skill-library.mjs skills/resolve-open-loops/SKILL.md`.

Smoke test:
- should trigger: "The guard blocked me again — let's clear those open loops."
- should trigger: "Before we start, let's do a quick Lore hygiene pass."
- should not trigger: "Search Lore for everything we know about the auth module." (→ `memory_search` directly)
- should not trigger: "Onboard this new repo into Lore." (→ `lore_onboard`)

## Examples

- "The guard fired with 12 items. Walk me through them so we can clear the ones that are done."
- "I want to do a pre-session sweep of my open goals before starting the refactor."
- "Half these open loops are stale — help me triage and mark the dead ones."

## Reference files

- [`references/memory-types.md`](references/memory-types.md) — memory type definitions, `memory_search` output format, `memory_forget` call shapes, and recommended `supersededBy` phrases for each resolution outcome
