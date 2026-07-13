# Metadata contract for local skills

This document defines the canonical frontmatter contract for every skill under `skills/*/SKILL.md`. The validator (`scripts/validate-skill-library.mjs`) encodes the required and forbidden rules mechanically. This file documents the decisions behind them.

## Allowed top-level keys

The following top-level keys are valid in a skill frontmatter block:

| Key | Status | Notes |
| --- | --- | --- |
| `name` | **Required** | Kebab-case, matches the directory name exactly. |
| `description` | **Required** | Identifies purpose and concrete activation conditions without summarising procedural workflow. |
| `metadata` | **Optional** (block) | Contains lifecycle and classification fields when the skill needs them; some fields become required under the conditions below. |
| `license` | **Required by repo policy** | Use `GNU GPL v3`; see AGENTS.md Learned Rule 1. |
| `compatibility` | **Optional** | Concise environment or product assumptions when they materially affect use. |

**Any other top-level key is forbidden.** The following keys are explicitly banned because they belong elsewhere:

| Banned key | Why banned | Where it belongs instead |
| --- | --- | --- |
| `argument-hint` | Runtime hint, not skill identity | Reference file or `## Inputs to gather` |
| `author` | Attribution, not skill identity | Commit message or `PROVENANCE.md` |
| `inspired-by` | Attribution, not skill identity | Commit message or `PROVENANCE.md` |

## Required `metadata` fields

| Field | Status | Valid values |
| --- | --- | --- |
| `metadata.category` | **Recommended** | `authoring`, `ci`, `migrations`, `typescript`, `version-control`, `workflow`, or another concise domain label. |
| `metadata.audience` | **Recommended** | `general-coding-agent` for most skills. Use a more specific value only for narrowly specialized skills. |
| `metadata.maturity` | **Recommended** | `draft` for new or unvalidated skills; `stable` after smoke-test validation and live use. |
| `metadata.kind` | **Required for `draft` skills** | `task` or `reference`. Required before a draft skill can be promoted to stable. |

### What `metadata.kind` means

- `task` — a multi-step playbook with explicit inputs, outputs, and validation steps. The skill body should include `## Inputs to gather`, `## First move`, `## Workflow`, and `## Outputs`.
- `reference` — lookup-heavy guidance where the main value is navigation, conventions, or examples. Replace the task-specific sections with a concise navigation block and direct links to support files.

## Allowed optional `metadata` fields

Skill-specific behavioral flags may be added under `metadata` as documented optional extensions. Each optional extension must be:

1. Documented here with its name, meaning, and the skill(s) that use it.
2. Validated or checked by the validator when it affects workflow behavior.

| Optional field | Status | Meaning | Used by |
| --- | --- | --- | --- |
| `metadata.reader_testing` | **Documented optional extension** | Signals that reader-testing is a required stage in the skill workflow. Valid value: `required`. | `doc-coauthoring` |
| `metadata.version` | **Release-managed skills only** | Mirrors the skill's semver from Release Please. Set via `# x-release-please-version` comment. Do not bump manually. | Release-managed skills |

**Do not add arbitrary skill-specific fields** to `metadata` without documenting them here first. If a field applies to only one skill and does not change how the validator or authoring system reasons about the skill, consider moving it to a `references/` file instead.

## Forbidden `metadata` fields

The following `metadata` keys are explicitly banned because they carry upstream provenance rather than local lifecycle information:

| Banned key | Source | Where it belongs instead |
| --- | --- | --- |
| `metadata.github-path` | Upstream awesome-copilot import | Remove. Preserve attribution in a `PROVENANCE.md` or commit message if needed. |
| `metadata.github-ref` | Upstream awesome-copilot import | Remove. |
| `metadata.github-repo` | Upstream awesome-copilot import | Remove. |
| `metadata.github-tree-sha` | Upstream awesome-copilot import | Remove. |
| `metadata.author` | Upstream attribution | Commit message or `PROVENANCE.md`. |
| `metadata.inspired-by` | Upstream attribution | Commit message or `PROVENANCE.md`. |
| `metadata.enhancements` | Upstream feature list | Move to `## Reference files` or a `references/` file. |

## Special-case decisions

The historical special cases for imported skills (`acquire-codebase-knowledge`, `agent-governance`, `agent-supply-chain`) have been normalized to the local contract (category/audience/maturity/kind + license at top level, provenance moved to PROVENANCE.md or commit history where appropriate). No further exceptions are active.

### `doc-coauthoring`

This skill uses `metadata.reader_testing: required` as a skill-specific behavioral flag.

**Resolution:** This is the accepted pattern for skill-specific behavioral extensions. The field is documented in the optional extensions table above. Future skill-specific flags should follow the same pattern: add to `metadata`, document here, and add a validator check if the field is meaningful to automation.

## Description and body policy

The description must be a YAML string. Quoted scalars and valid multiline block scalars are accepted. Keep it concise: identify what the skill is for and the concrete conditions that should activate it, but leave procedural steps in the body. Complex routing detail belongs in `## Use this skill when` or `## Do not use this skill when`.

Canonical body headings are optional. Use only headings that add signal, and keep any canonical headings that are present in the semantic order taught by the catalog standard. A `## Reference files` section may contain local support-file links, inter-skill routing links, or both; all local targets must exist.

## Frontmatter shape reference

### Minimal valid frontmatter (stable skill)

```yaml
---
name: my-skill
description: "Use when <trigger phrase>. Not when <adjacent skill> is more appropriate."
license: GNU GPL v3
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: stable
  kind: task
---
```

### Minimal valid frontmatter (new draft skill)

```yaml
---
name: my-skill
description: "Use when <trigger phrase>. Not when <adjacent skill> is more appropriate."
license: GNU GPL v3
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: task
---
```

### Stable skill with documented optional extension

```yaml
---
name: my-skill
description: "Use when <trigger phrase>."
license: GNU GPL v3
metadata:
  category: authoring
  audience: general-coding-agent
  maturity: stable
  kind: task
  reader_testing: required
---
```

## Validator enforcement

The validator (`scripts/validate-skill-library.mjs`) currently enforces:

| Rule | Scope | Error or warning |
| --- | --- | --- |
| `name` must match directory | All skills | Error |
| `description` must be ≥ 20 characters | All skills | Error |
| `description` must include a trigger phrase | `draft` skills | Error |
| `metadata.kind` must be `task` or `reference` if present | All skills | Error |
| `metadata` must be a string-to-string map when present | All skills | Error |
| `license` must equal `GNU GPL v3` | All skills | Error |
| **Forbidden top-level keys** (anything other than `name`, `description`, `metadata`, `license`, `compatibility`) | All skills | **Error** |
| Present canonical headings remain in semantic order | All skills | Error |
| Referenced local support and inter-skill targets exist | All skills | Error |
| **Forbidden provenance keys in `metadata`** (`github-*`, `author`, `inspired-by`, `enhancements`) | All skills | **Error** |
| **`metadata.kind` required for `draft` skills** | Draft skills | **Error** (added wave 2) |
