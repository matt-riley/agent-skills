# Agent Skills Catalog Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the active Agent Skills catalog reproducibly valid, internally consistent, fully discoverable, and more context-efficient, then publish the reviewed remediation to `origin/main`.

**Architecture:** Three independent workstreams modify disjoint areas: validator/tooling contracts, catalog metadata/routing, and oversized or structurally inconsistent skill content. The root agent integrates the workstreams, runs catalog-wide verification, requests a final review, and publishes the verified commits.

**Tech Stack:** Python 3, Node.js, YAML/JSON, Markdown, Release Please, Git.

## Global Constraints

- Follow the repository-root `AGENTS.md`, including `license: GNU GPL v3` and no casual version bumps.
- Preserve active skill behavior unless the approved design explicitly identifies ambiguous triggers, contradictory authoring rules, stale links, or duplicated content.
- Do not add empty scaffolding or hard-coded local paths to active skills.
- Keep `SKILL.md` workflow-oriented and move lookup-heavy detail to shallow, directly linked `references/` files.
- Write regression coverage before changing validator behavior.
- Do not stage, overwrite, or discard unrelated user changes.
- Direct push target is `origin/main`; never bypass branch protection.

---

### Task 1: Reproducible validation and one canonical authoring contract

**Files:**
- Modify: `package.json`
- Create or modify: repository-owned Python dependency/bootstrap files as appropriate
- Modify: `_shared/validate-skills.py`
- Modify: `skills/skill-authoring/scripts/validate-skill-library.mjs`
- Create or modify: validator regression fixtures/tests under `_shared/` or `skills/skill-authoring/scripts/`
- Modify: `skills/skill-authoring/SKILL.md`
- Modify: `skills/skill-authoring/references/metadata-contract.md`
- Modify: `skills/skill-creator/references/catalog-standard.md`
- Modify if needed: `README.md`

**Interfaces:**
- Consumes: active `skills/*/SKILL.md` packages and existing release metadata.
- Produces: reproducible `npm run validate`; a JavaScript authoring validator that agrees with the canonical metadata, YAML, heading, and reference contract.

- [ ] **Step 1: Add failing validator regression cases**

Cover valid multiline YAML, optional omitted headings, present-heading order, inter-skill-only reference sections, `compatibility`, invalid support links, and invalid metadata. Demonstrate the current failures before implementation.

- [ ] **Step 2: Make Python dependencies repository-owned**

Add the smallest conventional dependency declaration and npm bootstrap path needed so a fresh checkout can install PyYAML and run the primary validator. Do not hide global environment assumptions.

- [ ] **Step 3: Reconcile validator behavior**

Use real YAML parsing for valid frontmatter, allow the canonical top-level fields, make optional-heading handling match the authoring contract, and distinguish support links from inter-skill routing links.

- [ ] **Step 4: Reconcile authoring documentation**

State one description rule: identify purpose and concrete activation conditions without encoding the procedural workflow. Align `compatibility`, optional-heading, and reference-section guidance everywhere.

- [ ] **Step 5: Verify Task 1**

Run the new regression suite, install/bootstrap validation dependencies through the documented repository command, run `npm run validate`, and run the detailed JavaScript validator. Record exact results.

---

### Task 2: Catalog metadata, chooser, release paths, and broken links

**Files:**
- Modify: `README.md`
- Modify: `skills/README.md`
- Create or modify: `skills/*/agents/openai.yaml`
- Modify: `.release-please-manifest.json`
- Modify: `release-please-config.json`
- Modify: `skills/git-signing-troubleshoot/SKILL.md`

**Interfaces:**
- Consumes: every active skill's frontmatter description and current release configuration.
- Produces: complete active Codex metadata, complete chooser routing, filesystem-correct archived release configuration, and no broken active-skill links.

- [ ] **Step 1: Add or run failing coverage assertions**

Demonstrate missing OpenAI metadata, chooser omissions, nonexistent release paths, and broken Markdown links before changing files.

- [ ] **Step 2: Complete Codex metadata**

Add `agents/openai.yaml` to every active skill that lacks it. Derive concise display names and copy each frontmatter description exactly as `interface.short_description`; preserve `policy.allow_implicit_invocation: true` unless an existing local contract explicitly requires otherwise.

- [ ] **Step 3: Repair routing and release metadata**

Add `find-skills` and `graphify` to the chooser with non-overlapping boundaries. Update both Release Please files so archived skill entries point to their real directories, or consistently remove them if repository evidence proves archived packages are intentionally unmanaged.

- [ ] **Step 4: Repair broken documentation**

Remove or replace the nonexistent `copilot-instructions.md` link in `git-signing-troubleshoot`, preserving the safety policy in a real repository-owned location.

- [ ] **Step 5: Verify Task 2**

Run deterministic assertions that every active skill is routed, every active skill has valid OpenAI metadata, every release package path resolves, and every local Markdown link resolves.

---

### Task 3: Skill context efficiency, triggers, and structural cleanup

**Files:**
- Modify: `skills/graphify/SKILL.md`
- Create or modify: `skills/graphify/references/*.md`
- Modify: `skills/agent-governance/SKILL.md`
- Create or modify: `skills/agent-governance/references/*.md`
- Modify if justified: `skills/agent-supply-chain/SKILL.md`
- Create if justified: `skills/agent-supply-chain/references/*.md`
- Modify: structurally failing active `skills/*/SKILL.md` files reported by the detailed validator
- Modify: `skills/api-smoke-validation/SKILL.md`
- Modify: `skills/modern-web-guidance/SKILL.md`

**Interfaces:**
- Consumes: current skill content and the canonical contract established by Task 1.
- Produces: smaller main files with directly linked moved content, canonical trigger descriptions, and clean section structure without lost operational guidance.

- [ ] **Step 1: Capture content-preservation baselines**

Record headings, commands, safety requirements, and support links for each oversized skill before moving content. Add or adapt structural assertions that fail on the current duplicate/out-of-order sections.

- [ ] **Step 2: Split oversized skills**

Keep activation, first move, core workflow, guardrails, validation, and load conditions in each main skill. Move long patterns, command reference, and mode-specific procedures to purpose-named shallow references. Split `agent-supply-chain` only if the result materially improves progressive disclosure.

- [ ] **Step 3: Normalize triggers and sections**

Rewrite the two descriptions that fail trigger validation and repair duplicate/out-of-order canonical sections across the detailed validator's reported active skills. Do not change unrelated domain instructions.

- [ ] **Step 4: Verify Task 3**

Run the detailed authoring validator on every changed skill. Confirm every moved section is linked from its main skill, key safety language remains present, and `graphify` plus `agent-governance` are materially shorter.

---

### Task 4: Integrate, review, verify, commit, and publish

**Files:**
- Modify only files needed to resolve integration findings.
- Update: `.superpowers/sdd/progress.md` as ignored execution state.

**Interfaces:**
- Consumes: reviewed outputs of Tasks 1-3.
- Produces: one internally consistent, verified `main` branch pushed to `origin/main`.

- [ ] **Step 1: Review each workstream**

Review Task 1 for spec compliance and code quality, Task 2 for complete deterministic coverage, and Task 3 for content preservation and progressive disclosure. Return important findings to a fixing subagent and re-review.

- [ ] **Step 2: Run full verification**

Run `npm run validate`, the detailed authoring validator, every active static trigger eval, every active static functional eval, the deterministic coverage assertions, `git diff --check`, and `git status --short`.

- [ ] **Step 3: Request final whole-change review**

Provide the full diff from the pre-remediation base to the reviewer. Fix all critical and important findings in one coordinated pass, then repeat applicable verification.

- [ ] **Step 4: Commit intentionally**

Stage only remediation files and commit with conventional messages that accurately describe the changes. Do not manually bump release versions.

- [ ] **Step 5: Push main**

Confirm local `main` is based on the current `origin/main`, then run `git push origin main`. If rejected, report the exact protection or non-fast-forward error without bypassing it.
