---
name: find-skills
description: Helps users discover skills in the local agent-skills catalog when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an already-available local skill.
license: GNU GPL v3
---

# Find Skills

This skill helps you discover relevant skills already available in the local agent-skills catalog. All skills are directories under `skills/` with a `SKILL.md` — no external install needed.

Start with `skills/README.md` for the family-organized chooser, then drill into individual `skills/<name>/SKILL.md` files for full workflows.

## Use this skill when

- The user asks "how do I do X" where X might be a common task with an existing skill
- The user says "find a skill for X" or "is there a skill for X"
- The user asks "can you do X" where X is a specialized capability
- The user expresses interest in extending agent capabilities
- The user wants to search for tools, templates, or workflows
- The user mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## Do not use this skill when

- The user asks you to perform a task directly and is not asking about skills discovery
- The user has already identified a specific skill and wants you to use it
- The user is asking for general programming advice, not skill lookup

## Inputs to gather

- What domain does the user need help with? (e.g., React, testing, design, deployment)
- What specific task do they want to accomplish?
- Is this a common enough task that a skill likely exists in the local catalog?

## First move

Read `skills/README.md` — the family-organized chooser. It groups skills by domain (governance, testing, git, CI/CD, database, etc.) so you can quickly find where the user's need fits. If the chooser doesn't cover the domain well, proceed to the workflow below for deeper search.

## Workflow

### Step 1: Understand what they need

Identify the domain, the specific task, and whether this is a common enough task that a skill likely exists in the local catalog.

### Step 2: Search the local catalog

Search the local `skills/` directory for matching skills. Use `search_files` to grep for keywords across `SKILL.md` frontmatter (names, descriptions) and the chooser table in `skills/README.md`.

Three search strategies, in priority order:

1. **Keyword match in skill descriptions** — grep `skills/*/SKILL.md` for the user's domain or task terms in the `description:` field
2. **Family match in the chooser** — read `skills/README.md` to find where the topic fits (Governance, Testing, Git, CI/CD, etc.)
3. **Fuzzy fallback** — list `skills/` directory names and skim their `SKILL.md` frontmatter when the match isn't obvious

### Step 3: Present matches

When you find relevant skills, present them with:

1. The skill name and what it does (from its `description` frontmatter)
2. Its maturity level if listed in `metadata.maturity` (draft, stable)
3. Its kind if listed in `metadata.kind` (task, reference)
4. What the skill would do if activated — a one-sentence summary

Example response format:

```
I found a skill in your catalog that might help!

`implementation-review` — finished-code review workflow (stable, task)
This walks you through a structured post-implementation review and approval.

`plan-review` — plan drafting, hardening, and approval gates (stable, task)
This helps draft and harden a plan before coding starts.
```

### Step 4: Offer to activate

If the user wants to proceed, load the skill with `skill_view(name='<skill-name>')` and follow its workflow. No installation required — all skills in the local catalog are already available.

### When no skills are found

If no relevant local skills exist:

1. Acknowledge that no existing skill was found in the local catalog
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create a custom skill using the `skill-creator` skill

## Guardrails

- Search the local catalog thoroughly before concluding no skill exists
- Prefer stable skills over draft skills when both cover the same task
- Never invent or hallucinate skills that don't exist in the catalog
- Present at most 3-4 matches to avoid overwhelming the user

## Validation

- Confirm the user's need is understood before searching
- Verify each match actually exists by reading its `SKILL.md` frontmatter
- Present options clearly with skill name, description, and maturity
- Let the user choose before loading a skill

## Examples

| Domain          | Example Query            | Likely Local Skill(s)       |
| --------------- | ------------------------ | --------------------------- |
| Testing         | "find a skill for testing" | `testing-workflows`, `api-smoke-validation` |
| Code review     | "skill for PR review"    | `implementation-review`, `plan-review` |
| Git             | "git workflow skill"     | `finishing-a-development-branch`, `git-worktrees`, `resolve-open-loops` |
| CI/CD           | "debug CI failure"       | `github-actions-failure-triage`, `github-actions-local-repro` |
| Database        | "database migration"     | `database-migrations`, `cloudflare-d1-migrations` |
| Code generation | "generate code"          | `code-generation` |
| Planning        | "plan before coding"     | `rpi-workflow`, `reverse-prompt`, `plan-review` |
| Security        | "security review"        | `security-basics` |
| Agent authoring | "create a skill"         | `skill-creator`, `agentic-eval` |
| Documentation   | "write docs"             | `doc-coauthoring` |
| Code search     | "find code in repo"      | `ast-grep`, `code-intelligence`, `code-tour` |

## Reference files

- `skills/README.md` — the family-organized chooser for the full catalog
- `skills/<name>/SKILL.md` — each skill's source of truth
