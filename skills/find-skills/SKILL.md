---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
license: GNU GPL v3
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**
- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

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
- The user is asking for general programming advice, not skill installation

## Inputs to gather

- What domain does the user need help with? (e.g., React, testing, design, deployment)
- What specific task do they want to accomplish?
- Is this a common enough task that a skill likely exists?

## First move

Check the [skills.sh leaderboard](https://skills.sh/) to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

## Workflow

### Step 1: Understand what they need

Identify the domain, the specific task, and whether this is a common enough task that a skill likely exists.

### Step 2: Search for skills

If the leaderboard doesn't cover the user's need, run:

```bash
npx skills find [query]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

### Step 3: Verify quality before recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.

### Step 4: Present options to the user

When you find relevant skills, present them with:

1. The skill name and what it does
2. The install count and source
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 5: Offer to install

If the user wants to proceed, install the skill:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

### When no skills are found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

## Guardrails

- Never recommend a skill without verifying quality (install count, source reputation, stars)
- Never install a skill without the user's explicit consent
- Do not recommend skills from unknown authors with low install counts

## Validation

- Confirm the user's need is understood before searching
- Verify skill quality metrics before recommending
- Present options clearly with install counts, source, and commands
- Ensure the user explicitly opts in before installing anything

## Examples

See the leaderboard at https://skills.sh/ for curated, popular skills. Common categories include:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Reference files

- Browse skills at https://skills.sh/
- Skills CLI: `npx skills --help`
