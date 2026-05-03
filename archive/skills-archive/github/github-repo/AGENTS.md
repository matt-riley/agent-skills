# GitHub Repository Optimizer — Implementation recipes

Detailed recipes for Phase 2 (Generate or Improve Files). Read this file when you need to implement a specific fix flagged by the audit. The parent `SKILL.md` has the workflow and audit checklist.

## README generation

When writing or rewriting a README:

- Start with the project name and a one-liner that clearly states what it does
- Include a badge row — at minimum: build status, license, version. Use shields.io format
- Add a quick start section that gets someone running in 3 steps or fewer
- Code examples should be complete, copy-pasteable, and use appropriate syntax highlighting
- If the project has a visual component, strongly recommend adding a screenshot or GIF
- Keep it under 500 lines; point to `/docs` for detailed documentation
- Use collapsible `<details>` sections for optional/advanced content

## Community health files

When generating these files, tailor them to the specific project — avoid generic boilerplate that ignores the project's language, tooling, and conventions.

### CONTRIBUTING.md

Should cover:

- How to set up the development environment
- Code style and linting rules (reference actual tools the project uses)
- How to run tests
- PR process and expectations
- Issue labeling conventions if applicable

### SECURITY.md

Should include:

- Supported versions (which versions receive security fixes)
- How to report a vulnerability (private email or GitHub Private Vulnerability Reporting)
- Expected response timeline
- Explicit instruction to NOT use the public issue tracker for security issues

### CODE_OF_CONDUCT.md

Use the Contributor Covenant 2.1 unless the user has a different preference.

## Issue templates

Generate YAML-based issue forms, not markdown templates. Example structure for a bug report:

```yaml
name: Bug Report
description: Report a bug to help us improve
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: Thanks for reporting a bug! Please fill out the sections below.
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear description of what the bug is
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Low (cosmetic, minor inconvenience)
        - Medium (feature partially broken)
        - High (feature completely broken)
        - Critical (data loss, security issue)
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Version, OS, browser, etc.
```

Adapt the fields to the specific project type (e.g., a CLI tool wouldn't ask for browser info).

## Organization-level setup

If the user mentions they're setting up an organization (not just a single repo), guide them through:

### 1. Create a `.github` repository

Public, with default community health files that apply org-wide:

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md` (generic enough for all repos)
- `SECURITY.md`
- `SUPPORT.md`
- `FUNDING.yml`
- Issue and PR templates (note: if an individual repo has ANY files in `.github/ISSUE_TEMPLATE/`, none of the org defaults apply for that repo)

### 2. Organization profile README

Create `profile/README.md` in the `.github` repo — this is the organization's public profile page. Different from personal profiles:

- Should explain what the organization does
- Link to key repositories
- Include contact/social links
- Can use the same enhancement tools as personal profiles (badges, stats)

### 3. Private member profile (optional)

Create a `.github-private` repository with `profile/README.md` — visible only to org members. Use this for internal resources, onboarding links, and private repo navigation.

### 4. Verify the organization's domain

Settings -> Verified & approved domains. This displays a verified badge that significantly boosts credibility.

### 5. Repository rulesets

Consider repository rulesets — the newer, more flexible alternative to branch protection. They support multiple concurrent rulesets, Evaluate mode for testing, and can be imported/exported as JSON. Start in Evaluate mode, track violations, then enforce.
