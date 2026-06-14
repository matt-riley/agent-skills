---
name: agent-instructions
description: "Use when creating or updating agent instruction files (AGENTS.md for Pi, copilot-instructions.md for Copilot, per-path guides, or AGENTS.md router) — especially when instruction files are too long, generic, or stale, or when agents repeatedly make the same avoidable mistakes."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: authoring
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# agent-instructions Skill

**Purpose:** Create or refresh instruction files that guide agent behavior and reduce repeated mistakes without rewriting the repository or enforcing tool choices that contradict the codebase.

## Use this skill when

- Instruction files are missing, incomplete, or stale (no recent audit or updates)
- Agents repeatedly make the same mistake in a repository (e.g., always choosing a tool not suitable for this codebase, using wrong file paths, or using anti-patterns)
- A file-type or path-specific instruction file does not exist but the codebase has clear conventions (e.g., a TypeScript project with strict tsconfig, or a Terraform repo with specific backend patterns)
- Agent instruction files (AGENTS.md for Pi, copilot-instructions.md for Copilot) have grown large or overly generic and need to be split into focused per-path guides
- You need to document non-obvious operational constraints (signing requirements, security policies, deployment gates, testing procedures, environment setup)
- A repository has learned rules (lessons from prior corrections) that should be captured proactively

## Do not use this skill when

- The instructions already exist and are current (recent audit, regular updates)
- The guidance needed is already enforced by tooling (linters, type checkers, build config)
- The task is to change the actual repository code, configuration, or behavior (use other skills for that)
- The instructions would just be a tutorial or generic best-practice collection (not repository-specific)
- You are authoring for a role or context outside agent work (e.g., end-user documentation)

## Discoverability Filter

> **Before adding any line to an instruction file, ask:** "Can an agent discover this by reading the repo — README, code, config, scripts, directory tree?"
>
> If YES: do not include. If NO, and it materially affects task success: include.

This filter ensures instruction files stay focused, reduce duplication, and remain a source of truth for the non-obvious and operationally critical.

### What earns a line in the instruction file

1. **Non-discoverable from repository files alone**
   - Patterns not visible in code or config (e.g., an undocumented deployment gate, a security signing requirement, a hidden per-repository convention)
   - Lessons from prior agent mistakes that are not baked into tooling or naming

2. **Operationally significant**
   - Changes which commands agents run, which tools they reach for, or how they validate work
   - Affects the outcome of the task or the safety of the work
   - Alters the priority of conflicting tools or approaches in this specific repository

3. **Actionable and specific**
   - Concrete enough to execute; not a general principle or philosophy
   - References actual file paths, tool names, or specific repository state
   - Includes enough context that an agent can act on it immediately

### What to exclude (anti-patterns)

- Tech stack summaries or directory structure overviews (discoverable from README and filesystem)
- Architecture descriptions or design rationale (belongs in ADR or design documents, not instruction files)
- Generic best-practice advice (e.g., "write clean code," "test thoroughly")
- Rules already enforced by tooling (linters, type checkers, CI gates)
- Tutorials, examples, or learning resources (use project docs for that)
- Motivational statements or explanations of why something matters (keep instructions direct)

See [discoverability-filter.md](references/discoverability-filter.md) for deeper guidance and worked examples.

## Routing Boundary

| Signal | Route to this skill | Route elsewhere |
|--------|---------------------|-----------------|
| "Instructions need auditing" | ✓ | Review existing files first |
| "Agents keep doing X wrong" | ✓ | Check if a skill already addresses this |
| "I need a new instruction file" | ✓ | If the instruction is about code changes, use the relevant coding skill |
| "Update the README" | ✗ | User documentation belongs in README or project docs |
| "Enforce a linter or rule" | ✗ | Use tsconfig, eslint config, tooling setup (not instructions) |
| "Change the actual code" | ✗ | Use a coding or debugging skill |
| "Create or revise a reusable skill package" | ✗ | [`skill-authoring`](../skill-authoring/SKILL.md) |

## Inputs to gather

Before starting, clarify:

1. **Scope:** Which instruction files are in scope?
   - **Pi Coding Agent:**
     - Global: `~/.pi/agent/AGENTS.md` or `~/.pi/agent/CLAUDE.md`
     - Project-level: `AGENTS.md` or `CLAUDE.md` in repo root or parent directories (discovered upward from cwd)
   - **GitHub Copilot CLI:**
     - Global: `~/.copilot/copilot-instructions.md`
     - Project-level: `.github/copilot-instructions.md` (repo root)
     - Per-path guides: `.github/instructions/*.md` (with YAML frontmatter `description` and `applyTo` fields)
   - **Other harnesses:** Check your harness documentation for instruction file conventions
   - `AGENTS.md` (agent roster and routing)
   - Per-project files (if this is a multi-project workspace)

2. **Problem:** What mistake or gap triggers this work?
   - Give a concrete example of an agent mistake or missing guidance
   - How often does it happen?
   - Does it block work or just create extra review cycles?

3. **Constraints:** What is off-limits?
   - Are there existing tool choices or conventions that must not be overridden?
   - Does the repository have security, signing, or deployment gates that must be preserved?
   - Are there previous decisions documented elsewhere that should not be repeated?

## First move

1. **Audit current state:**
   - List all existing instruction files and their last update date
   - Skim each for stale or overly generic sections
   - Note any gaps (e.g., a TypeScript project with no typescript.instructions.md)

2. **Identify patterns:**
   - What mistakes or questions do agents keep hitting?
   - What non-obvious repository conventions exist?
   - Are there learned rules from past corrections that are not yet captured?

3. **Apply the Discoverability Filter:**
   - For each candidate instruction, ask: "Is this discoverable from the repository itself?"
   - Mark each line as keep, archive, or move-to-docs

## Workflow

### Phase 1: Audit
- Read all existing instruction files
- Identify duplicates, stale content, and gaps
- Gather examples of agent mistakes (from task history, prior sessions, or explicit user report)

### Phase 2: Filter
- For each instruction candidate: Apply the Discoverability Filter
- Group related instructions by file (global vs. per-path)
- Prioritize based on operational impact (high-impact non-discoverable info first)

### Phase 3: Write or Update
- Create new file or update existing file
- Follow the file-type structure (YAML frontmatter with both `description` and `applyTo`, sections, learned rules)
- Use concrete examples from the repository (actual file names, commands, configs)
- Link to reference docs where appropriate

### Phase 4: Validate
- Read each instruction aloud; would an agent understand it immediately?
- Cross-check against the Discoverability Filter (any line that is discoverable should be removed)
- Verify links and examples still exist in the repository
- Run any existing instruction linter or validator if available

## Quality Gate: The 3-Question Check

For each line in the instruction file:

1. **Non-discoverable?** Can an agent find this info by reading the repo (code, config, README, scripts)?
   - If NO (not mentioned anywhere): include it.
   - If YES (visible in the code or config): delete it.

2. **Accurate?** Does this reflect the actual repository state right now?
   - Test against actual file paths, actual tools, actual commands.
   - If it's a learned rule: has it actually been validated, or is it still speculation?
   - If NO: fix or delete it.

3. **Materially reduces mistakes?** Would an agent make a noticeably better decision with this line?
   - If YES: keep it.
   - If NO (nice-to-know but not mission-critical): consider archiving it or moving to docs.

**Delete the line if any answer is NO.**

## Outputs

- Updated or new instruction file (AGENTS.md, copilot-instructions.md, or per-path guide) with clear scope and examples.
- Validation that the instructions are discoverable and reduce repeated mistakes.

## Guardrails

- **Not a code walkthrough:** Do not use instruction files as a substitute for comments, docstrings, or architecture documentation. Agents can read the code; tell them what the code cannot tell them.

- **Not a tool override:** Do not use instructions to forbid a tool or force a specific choice unless the repository genuinely cannot use that tool (e.g., a Go project banning Node-only packages). If the tool is suitable here, say why and under what conditions.

- **Not a duplicate of automation:** If a rule is already enforced by a linter, pre-commit hook, or CI gate, do not repeat it in instructions. Instead, instruct agents to run that tool and trust its feedback.

- **Not a policy engine:** Do not use instructions to police coding style, commit message formatting, or PR review etiquette. Those belong in contributing guidelines or automated linting. Instruction files are for repository-specific non-obvious operational knowledge.

- **Stable before sharing:** Do not create instruction files for code or patterns that are still in flux. Wait for the repository state to settle, then document it. Otherwise, agents will get stale guidance and waste time on outdated advice.

## Validation

After writing or updating an instruction file:

1. **Checklist:**
   - [ ] Every `*.instructions.md` file in scope keeps both `description` and `applyTo` in YAML frontmatter
   - [ ] Each line passes the 3-Question Check (non-discoverable, accurate, materially useful)
   - [ ] No duplicates with existing documentation (README, ADRs, config files)
   - [ ] All file paths and command examples are correct (spot-check in the repo)
   - [ ] Learned rules are linked to specific sessions or issues where the lesson was learned
   - [ ] Any new file-type guide matches the structure of existing guides

2. **Test with an agent:**
   - If possible, hand off a small task in this repository to an agent and see if the new instructions prevent or reduce mistakes
   - If the agent ignores the instruction, refine it for clarity

3. **Schedule review:**
   - Add a note about next review date (recommend quarterly for large codebases, biannually for small projects)
   - Link to related learned rules or decision records

- Smoke test:
  - should trigger: "Split stale copilot-instructions.md into focused per-path instruction files."
  - should not trigger: "Create a reusable skill package for instruction upkeep." (→ `skill-authoring`)

## Examples

The examples below each pass the 3-Question Check: non-discoverable, accurate, and materially useful to an agent.

### Example 1: Adding a TypeScript-specific instruction

**Scenario:** A TypeScript project repeatedly sees agents use `any` in main code, even though the repo has strict `noImplicitAny` and a clear pattern of using `unknown` at boundaries.

**Discoverable?** Partially — the tsconfig shows `noImplicitAny: true`, but the pattern of "use `unknown` at boundaries and narrow with guards" is a convention, not a rule.

**Include?** YES, because it's non-obvious to a new agent why `any` fails and how to fix it.

**Line:**
```
- Avoid `any` in source files; use `unknown` at module boundaries and narrow with type guards. The tsconfig enforces `noImplicitAny`, so use it as feedback for where to add guards.
```

### Example 2: Excluding a directory-structure overview

**Scenario:** Someone wants to add: "The repository has src/, tests/, docs/, and scripts/. Use src/ for source code, tests/ for test files, etc."

**Discoverable?** YES — the directory names are self-documenting.

**Include?** NO — delete this line. It's visible in the tree.

### Example 3: Adding a deployment gate

**Scenario:** The repository has a 1Password-backed Git signing requirement. Commits without a valid signature will be rejected. This is not mentioned in any config file or script.

**Discoverable?** NO — there's no comment in the Git config or README explaining this.

**Include?** YES, because it materially affects whether a commit will be accepted.

**Line:**
```
- All commits must be signed via 1Password SSH signing; unsigned or GPG-signed commits will be rejected. If signing fails, validate the 1Password setup and approve the authorization in the app.
```

See [instruction-examples.md](references/instruction-examples.md) for more worked examples.

## Reference files

- [`references/discoverability-filter.md`](references/discoverability-filter.md) — deeper guidance and worked examples for applying the discoverability filter
- [`references/instruction-examples.md`](references/instruction-examples.md) — real examples of good vs. bad instruction lines across several repositories
