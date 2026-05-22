# Worktree Naming Conventions

This document defines the formal naming scheme for Git worktrees. The goal: keep parallel development organized, make cleanup easy, and never (ever) commit `.worktrees/` to the repo.

**The Golden Rule:** One worktree per agent lane, task, or quick experiment. Worktrees are **never committed**.

---

## Naming Scheme

All worktrees live in `.worktrees/` and follow this structure:

### `.worktrees/agent/<AGENT_ID>` — Long-Running Agent Lanes

These are the workhorse worktrees. An agent (or a person acting like one) lands here for days or weeks, chipping away at a feature area or major refactor.

**Characteristics:**
- Persistent across sessions — this is a lane, not a one-off
- Tied to a specific agent or team working on a feature area
- Branch pattern: `agent/<AGENT_ID>`
- Typical lifecycle: days to weeks
- Think: "We're shipping this, incrementally"

**Examples:**
- `.worktrees/agent/ci-migration-orchestrator` — Multi-session CircleCI→GitHub Actions migration
- `.worktrees/agent/typescript-api-test-generator` — Building comprehensive test coverage over time
- `.worktrees/agent/coherence-browser` — Building a memory browsing UI feature

### `.worktrees/task/<TASK_ID>` — Feature/Fix Tasks

Scoped, reviewable work. You have a clear goal, a PR ready, and you'll be done in hours or a day or two.

**Characteristics:**
- Scoped work with clear completion criteria
- Feature branches that get reviewed and merged to main
- Branch pattern: `task/<TASK_ID>` (e.g., `task/fix-lore-backfill-ordering`)
- Typical lifecycle: hours to 1–2 days
- Think: "This is one logical unit of work"

**Examples:**
- `.worktrees/task/fix-lore-backfill-ordering` — Bug fix, PR, merge, done
- `.worktrees/task/skills-ecosystem-documentation` — Write skill docs in isolation
- `.worktrees/task/router-core-validation` — Validate one router improvement, test, ship

### `.worktrees/temp/<PURPOSE>` — Throwaway Exploration

Quick experiments that might not live past the current session. No commitment. No branch (usually). Just you, the code, and a hypothesis.

**Characteristics:**
- Ephemeral — expect to throw it away
- No formal branch; local experiments only
- Branch pattern: optional, or `temp/<PURPOSE>` if you want to track it
- Typical lifecycle: minutes to a few hours
- **ID uniqueness:** Use semi-unique names to avoid collisions if multiple people spike in parallel (e.g., `temp/debug-2025-04-21` instead of just `temp/debug`)

**Examples:**
- `.worktrees/temp/quick-test` — Reproduce an issue fast
- `.worktrees/temp/schema-spike` — Try out a schema change locally without committing
- `.worktrees/temp/debug-session` — Isolated debugging environment
- `.worktrees/temp/debug-2025-04-21` — Timestamped to avoid collision during parallel testing

---

## Rationale

### Why three categories?

1. **Agent lanes** cluster related work (they'll be active for days) and signal that progress is collaborative and incremental. "Check back here" implicitly.
2. **Task worktrees** make scope crystal clear: one logical unit of work, one branch, one PR, done. Prevents scope creep.
3. **Temp worktrees** are your escape hatch for experiments. No judgment. Throw it away when you're done.

### Why `.worktrees/` directory at all?

- **Git worktrees are fast checkouts** — no thrashing between branches or merge state confusion
- **Explicit `.worktrees/` root makes management obvious** — `ls .worktrees/` shows your active work landscape
- **Keeps main checkout clean** — no stray branches cluttering `git branch` output, no checkout conflicts
- **Cleanup is straightforward** — old worktrees are easy to find and remove without hunting the filesystem

---

## Lifecycle Examples

### Example 1: Agent Lane (Multi-Week)

**Worktree:** `.worktrees/agent/lore-integration-verification`  
**Branch:** `agent/lore-integration-verification`  
**Start:** Monday 09:00 — agent begins integration testing  
**Activity:** Daily commits (3–5 per day)  
**Audit at week 4:** Branch shows recent activity → keep  
**Conclusion:** Merge to main after code review; worktree can be removed  

### Example 2: Task Worktree (1–2 Days)

**Worktree:** `.worktrees/task/fix-lore-backfill-ordering`  
**Branch:** `task/fix-lore-backfill-ordering`  
**Start:** Tuesday 14:00 — developer identifies ordering bug  
**Activity:** 3 commits in 4 hours  
**Completion:** PR merged Wednesday 10:00  
**Cleanup:** Remove worktree Wednesday 11:00 with `mr_worktree_remove fix-lore-backfill-ordering`  

### Example 3: Temp Worktree (1 Hour)

**Worktree:** `.worktrees/temp/debug-memory-leak`  
**Branch:** None (local changes only)  
**Start:** Friday 16:45 — reproduce memory leak in isolation  
**Activity:** Edit files, run profiler, confirm root cause  
**Completion:** Root cause identified 17:30  
**Cleanup:** Remove worktree with `git worktree remove .worktrees/temp/debug-memory-leak`  

---

## Never Commit `.worktrees/`

Per Git best practices and this repository's enforcement:

> [GIT] Always ignore local `.worktrees/` directories and never commit them in repositories that use git worktrees.

### Why This Matters

- **Worktrees are local and ephemeral** — each developer's set of active lanes is unique
- **Committing worktree state would cause merge conflicts** across developers' machines
- **Worktree branches themselves are tracked** — only the `.worktrees/` directory is ignored
- **Clean `.gitignore` enforcement** keeps diffs focused on real code changes, not directory clutter

### Enforcement Mechanism

**`.gitignore` exclusion** — The repository root `.gitignore` contains:

```
.worktrees/
```

This ensures:
- Git will not stage files under `.worktrees/`
- CI/linting does not traverse `.worktrees/`
- Release/publish workflows exclude `.worktrees/` from artifacts

### How to Verify Enforcement

```bash
# Check .gitignore includes .worktrees/
grep "\.worktrees/" .gitignore

# Verify git will not stage anything under .worktrees/
git status | grep -i worktree  # Should return nothing if working tree is clean

# Double-check by attempting to add .worktrees/ (should fail)
git add .worktrees/
# Expected: "The following pathspec didn't match any files"

# Confirm git will ignore .worktrees/ paths:
git check-ignore .worktrees/
# Expected: `.worktrees/` (prints the ignored path if enforcement is active)
```

### If `.worktrees/` is accidentally staged

```bash
git reset .worktrees/
git status  # Verify it is unstaged
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Create agent lane | `mr_worktree_create <AGENT_ID>` |
| Create task lane | `mr_worktree_create <TASK_ID>` |
| Create temp lane | `mr_worktree_create temp/<PURPOSE>` |
| Check worktree status | `mr_worktree_status` or `mr_worktree_status <ID>` |
| Remove worktree | `mr_worktree_remove <ID>` |
| List all worktrees | `git worktree list` |
| Verify .gitignore | `grep "\.worktrees/" .gitignore` |
| Monthly audit | `git for-each-ref --sort=-committerdate refs/heads/` |
