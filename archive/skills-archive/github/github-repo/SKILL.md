---
name: github-repo
description: Audit and improve GitHub repository quality, including README structure, community health files, templates, metadata, releases, and repository presentation.
---

# GitHub repository

## Use this skill when

- The user wants to improve, audit, review, or set up a GitHub repository.
- The task mentions README quality, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, LICENSE, issue templates, PR templates, CODEOWNERS, releases, or repository metadata.
- The goal is to make a repository feel more polished, welcoming, and open-source ready.

## Do not use this skill when

- The main task is improving a GitHub profile page rather than a repository. Use [`github-profile`](../github-profile/SKILL.md).
- The main task is only a short tagline, description, or metadata-string review. Use [`metadata-check`](../metadata-check/SKILL.md).
- The main task is readability review of already written long-form docs. Use [`readability-check`](../readability-check/SKILL.md).
- The main task is diagnosing a failing GitHub Actions run rather than repository presentation and health files.

## Inputs to gather

**Required before editing**

- The repository name, purpose, audience, and technology stack.
- Current README state, metadata state, and which community health files already exist.
- Current `.github` templates, automation, and release setup.
- Whether the task targets a single repository or an organization-wide `.github` repository.

**Helpful if present**

- Access to the live repository through `gh` or a local checkout.
- Existing CI, release automation, or package publishing setup.
- Any specific open-source posture goals such as contributor growth, recruiter visibility, or customer trust.

**Only investigate if encountered**

- Organization defaults stored in a separate `.github` repo.
- Rulesets, branch hygiene details, or broader release automation decisions when they materially affect the repository contract.

## First move

1. Gather the actual repo state before drafting files so the audit is grounded in facts.
2. Identify the highest-impact missing surfaces first: README clarity, community health files, templates, and repository metadata.
3. Decide whether the task is repo-local or org-wide before generating files in the wrong place.

## Workflow

1. Audit the repository across the main public-quality surfaces:
   - README quality
   - repository metadata
   - community health files
   - issue and PR templates
   - CI and automation signals
   - releases and branch hygiene
2. Generate or improve the missing files using `AGENTS.md` for concrete implementation guidance.
3. Recommend manual metadata changes that cannot be fully expressed through files alone, such as About text, topics, website URL, or social preview image.
4. Run [`metadata-check`](../metadata-check/SKILL.md) on short audience-facing strings you produced, especially repo descriptions and README opening blurbs.
5. Run [`readability-check`](../readability-check/SKILL.md) on prose-heavy files you wrote, such as README, CONTRIBUTING, or SECURITY content.

## Guardrails

- **Must not** generate a generic open-source file bundle without checking the repository's actual stack, audience, and maturity.
- **Must not** confuse organization-wide `.github` defaults with a single repository's local files.
- **Must not** rewrite healthy existing files just to force a new template shape.
- **Must not** treat repository metadata and documentation polish as the same task as CI failure triage or release engineering redesign.
- **Should** prioritize the surfaces with the biggest public impact first: README, community files, templates, and About metadata.
- **Should** tailor recommendations to the repository type rather than using one-size-fits-all boilerplate.
- **Should** call out when repository-level cleanup also suggests profile-level follow-up via [`github-profile`](../github-profile/SKILL.md).

## Validation

- Confirm generated files are in the correct locations and align with the repository type.
- Check internal README links, badge URLs, and template paths.
- Verify that recommended metadata changes are explicit when they cannot be automated via files.

## Examples

- "Make my repo look professional."
- "Add contributing and security docs to this project."
- "Review this open-source repo and tell me what it's missing."
- "Set up issue templates and a PR template for our org."

## Reference files

- `AGENTS.md` - concrete generation guidance for README, health files, templates, and org-level setup
