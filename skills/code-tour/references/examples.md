# Code tour reference: personas, depth, step types, and real-world examples

## Persona and intent map

Infer persona, depth, and focus from the user's request. Ask only when you genuinely cannot infer.

| User says | Persona | Depth | Action |
|-----------|---------|-------|--------|
| "tour for this PR" / "PR review" / "#123" | pr-reviewer | standard | Add `uri` step for PR; use `ref` for the branch |
| "why did X break" / "RCA" / "incident" | rca-investigator | standard | Trace the failure causality chain |
| "debug X" / "bug tour" / "find the bug" | bug-fixer | standard | Entry → fault points → tests |
| "onboarding" / "new joiner" / "ramp up" | new-joiner | standard | Directories, setup, business context |
| "quick tour" / "vibe check" / "just the gist" | vibecoder | quick | 5–8 steps, fast path only |
| "explain how X works" / "feature tour" | feature-explainer | standard | UI → API → backend → storage |
| "architecture" / "tech lead" / "system design" | architect | deep | Boundaries, decisions, tradeoffs |
| "security" / "auth review" / "trust boundaries" | security-reviewer | standard | Auth flow, validation, sensitive sinks |
| "refactor" / "safe to extract?" | refactorer | standard | Seams, hidden deps, extraction order |
| "contributor" / "open source onboarding" | external-contributor | quick | Safe areas, conventions, landmines |

When the user says "bug tour" but doesn't describe the bug, ask. When "feature tour" but no feature is named, ask. Otherwise infer silently.

---

## Step count calibration

Match steps to depth and repo size. These are targets, not hard limits.

| Depth | Total steps | Core path steps | Notes |
|-------|-------------|-----------------|-------|
| Quick | 5–8 | 3–5 | Vibecoder, fast explorer — cut ruthlessly |
| Standard | 9–13 | 6–9 | Most personas — breadth and enough detail |
| Deep | 14–18 | 10–13 | Architect, RCA — every tradeoff surfaced |

| Repo size | Recommended standard depth |
|-----------|---------------------------|
| Tiny (< 20 files) | 5–8 steps |
| Small (20–80 files) | 8–11 steps |
| Medium (80–300 files) | 10–13 steps |
| Large (300+ files) | 12–15 steps (scoped to relevant subsystem) |

A focused 10-step tour of the right files beats a scattered 25-step tour of everything.

---

## Step type decision guide

| Situation | Step type |
|-----------|-----------|
| Tour intro or closing | content |
| "Here's what lives in this folder" | directory |
| One line tells the whole story | file + line |
| A function or class body is the point | selection |
| Line numbers shift, file is volatile | pattern |
| PR / issue / doc gives the "why" | uri |
| Reader should open terminal or explorer | view or commands |

**Path rule:** `"file"` and `"directory"` must be relative to repo root. No absolute paths, no leading `./`.

**`commands`** only executes VS Code commands (e.g. `workbench.action.terminal.focus`), not shell commands.

---

## Narrative arc structure

1. **Orientation** — must be a `file` or `directory` step, never content-only. A content-only first step renders as a blank page in VS Code CodeTour.
2. **High-level map** (1–3 directory or uri steps) — major modules and how they relate.
3. **Core path** (file/line, selection, pattern, uri steps) — the specific code that matters.
4. **Closing** (content) — what the reader can now *do*, what to avoid, and 2–3 suggested follow-up tours.

Do not summarize in the closing — the reader just read it. Tell them what they can *do* next.

---

## Writing step descriptions: the SMIG formula

Every description should answer four questions:

- **S — Situation:** What is the reader looking at?
- **M — Mechanism:** How does this code work?
- **I — Implication:** Why does this matter for this persona's goal specifically?
- **G — Gotcha:** What would a smart person get wrong here?

Descriptions should tell the reader something they couldn't learn by reading the file themselves.

---

## Real-world examples

### microsoft/codetour — Contributor orientation

**Tour file:** https://github.com/microsoft/codetour/blob/main/.tours/intro.tour  
**Persona:** New contributor | **Steps:** ~5 | **Depth:** Standard

What makes it good:
- Intro step with an embedded SVG architecture diagram (raw GitHub URL inside the description)
- Rich markdown per step with emoji section headers
- Inline cross-file links inside descriptions

Technique: embed images and cross-links in descriptions to make them self-contained.

```json
{
  "file": "src/player/index.ts",
  "line": 436,
  "description": "### 🎥 Tour Player\n\nThe CodeTour player ...\n\n![Architecture](https://raw.githubusercontent.com/.../overview.svg)\n\nSee also: [Gutter decorator](./src/player/decorator.ts)"
}
```

---

### a11yproject/a11yproject.com — New contributor onboarding

**Tour file:** https://github.com/a11yproject/a11yproject.com/blob/main/.tours/code-tour.tour  
**Persona:** External contributor | **Steps:** 26 | **Depth:** Deep

What makes it good:
- Almost entirely `directory` steps — orients to every `src/` subdirectory without getting lost in files
- `selection` on the opening step to highlight the exact entry in `package.json`
- Closes with a genuine call-to-action

Technique: use directory steps as the skeleton of an onboarding tour.

```json
{
  "directory": "src/_data",
  "description": "This folder contains the **data files** for the site. Think of them as a lightweight database — YAML files that power the resource listings, posts index, and nav."
}
```

---

### github/codespaces-codeql — Technically complete example

**Tour file:** https://github.com/github/codespaces-codeql/blob/main/.tours/codeql-tutorial.tour  
**Persona:** Security engineer / concept learner | **Steps:** 12 | **Depth:** Standard

What makes it good:
- `isPrimary: true` — auto-launches when the Codespace opens
- `commands` array to run real VS Code commands mid-tour
- `view` property to switch the sidebar panel
- `pattern` instead of `line` for resilient matching
- `selection` to highlight the exact clause in a query file

**Canonical reference for `commands`, `view`, and `pattern`.**

```json
{
  "file": "tutorial.ql",
  "pattern": "import tutorial.*",
  "view": "codeQLDatabases",
  "commands": ["codeQL.setDefaultTourDatabase", "codeQL.runQuery"],
  "title": "Run your first query",
  "description": "Click the **▶ Run** button above. The results appear in the CodeQL Query Results panel."
}
```

---

### lucasjellema/cloudnative-on-oci-2021 — Multi-tour architecture series

**Persona:** Platform engineer / architect | **Steps:** ~12 per tour | **Depth:** Standard

What makes it good:
- Three separate tours for three concerns (function code, IaC, CI/CD), each standalone but linked via `nextTour`
- `selection` coordinates used in Terraform files where a block is the point
- Designed to be browsed via `vscode.dev` without cloning

Technique: for complex systems, write one tour per layer and chain with `nextTour`. Don't cover infrastructure + application + CI/CD in one tour.

---

### github/codespaces-learn-with-me — Minimal interactive tutorial

**Persona:** Total beginner | **Steps:** 4 | **Depth:** Quick

What makes it good: only 4 steps — proves that less is more for quick/vibecoder personas. Each step tells the reader to **do something**, not just read.

Technique: for quick/vibecoder tours, cut mercilessly. Four steps that drive action beat twelve that explain everything.

---

### blackgirlbytes/copilot-todo-list — Long interactive tutorial with checkpoint steps

**Persona:** Concept learner | **Steps:** 28 | **Depth:** Deep

What makes it good:
- Content-only checkpoint steps as progress milestones between coding tasks
- Each file step shows the exact expected output in a markdown code fence

Technique: checkpoint steps (content-only, milestone title) break up long tours and give the reader a sense of progress.

```json
{
  "title": "Check out your page! 🎉",
  "description": "Open the **Simple Browser** tab to see your to-do list. You should see all three tasks rendering from your data array.\n\nOnce you're happy with it, continue to add interactivity."
}
```

---

## Technique quick-reference

| Feature | When to use | Real example |
|---------|-------------|--------------|
| `isPrimary: true` | Auto-launch tour when repo opens | codespaces-learn-with-me, codespaces-codeql |
| `commands: [...]` | Run a VS Code command when reader arrives at this step | codespaces-codeql (`codeQL.runQuery`) |
| `view: "..."` | Switch VS Code sidebar/panel at this step | codespaces-codeql (`codeQLDatabases`) |
| `pattern: "regex"` | Match by line content, not number — use for volatile files | codespaces-codeql |
| `selection: {start, end}` | Highlight a block (function body, config section) | a11yproject, oci-2021 |
| `directory: "path/"` | Orient to a folder without reading every file | a11yproject |
| `uri: "https://..."` | Link to PR, issue, RFC, ADR, external doc | any PR review tour |
| `nextTour: "Title"` | Chain tours in a series | oci-2021 (3-part series) |
| Checkpoint steps (content-only) | Progress milestones in long interactive tours | copilot-todo-list |

---

## Discover more real tours on GitHub

Search all `.tour` files on GitHub: https://github.com/search?q=path%3A**%2F*.tour+&type=code

Use this to find tours for repos in the same language/framework, study how other authors handle a persona or step type, or look up how a specific field is used in practice.
