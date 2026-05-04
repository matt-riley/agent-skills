---
name: github-presence
description: Audit and improve GitHub profile and repository presentation, including profile READMEs, pinned repositories, README quality, community health files, templates, and metadata. Use when the task is to make GitHub surfaces more credible, scannable, and complete.
license: Proprietary
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: draft
---

# GitHub presence

## Use this skill when

- The user wants to improve a GitHub profile, organization profile page, or repository presentation.
- The task mentions profile README content, pinned repositories, profile metadata, repo README quality, community health files, issue templates, PR templates, or repository metadata.
- The goal is to make a GitHub surface feel more polished, credible, welcoming, or conversion-oriented.
- The work spans both a profile surface and repository surfaces and needs one audit that coordinates them.

## Do not use this skill when

- The task is only about polishing prose or short strings with no broader GitHub-surface audit — use [`writing-and-editing`](../writing-and-editing/SKILL.md).
- The main task is diagnosing a failing GitHub Actions run rather than improving GitHub presentation or health files — use [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md).
- The task is about permissions, billing, or other account administration outside the profile or repository presentation surfaces.
- The task is generic open-source strategy with no concrete profile or repository surface to improve.

## Inputs to gather

**Required before editing**

- Whether the target is a personal profile, organization profile, single repository, or org-wide `.github` repository.
- The target audience and what the surface should optimize for.
- The current README, metadata, pinned-repo, template, and community-file state.
- The strongest projects, proof points, or public signals worth surfacing.

**Helpful if present**

- `gh` CLI access or a local checkout.
- Existing CI, release, or publishing setup that should be reflected in the public-facing repo contract.
- Whether the user wants review-only output or actual file generation.

**Only investigate if encountered**

- Whether org defaults live in a separate `.github` repo.
- Whether weak pinned repositories need their own deeper cleanup after the profile work is done.

## First move

1. Classify the target as `profile`, `repository`, or `org-defaults`.
2. Audit the current public surface before generating files.
3. Prioritize the highest-impact missing pieces: README clarity, metadata quality, pinned repos, and health or template files.

## Workflow

1. **Profile mode.**
   - Distinguish personal profile surfaces from organization profile surfaces.
   - Audit README presence, bio and links, pinned repositories, and any profile widgets.
   - Generate or improve the profile README and recommend precise metadata and pinning changes.

2. **Repository mode.**
   - Audit README quality, repository metadata, community health files, issue and PR templates, release signals, and `.github` automation surfaces that affect public trust.
   - Improve only the missing or weak surfaces that matter most for the repo's audience and maturity.

3. **Org-defaults mode.**
   - Decide whether the task belongs in an organization-wide `.github` repository.
   - Generate or refine shared health files, templates, and the org profile surface without confusing them with one repo's local files.

4. **Writing follow-through.**
   - Use [`writing-and-editing`](../writing-and-editing/SKILL.md) when generated bios, descriptions, README prose, or taglines need a dedicated writing-quality pass.
   - Keep the broader GitHub-surface audit here; do not outsource the main routing decision.

## Guardrails

- **Must** distinguish profile surfaces from repository surfaces before generating files.
- **Must not** generate a generic open-source or profile bundle without checking the target's actual audience, stack, and maturity.
- **Must not** confuse organization-wide `.github` defaults with a single repository's local files.
- **Must not** treat GitHub Actions failure triage as the same task as GitHub-surface improvement.
- **Should** keep recommendations concrete: exact bio text, which repos to pin, which health files to add, and where they belong.
- **Should** prioritize the most visible and trust-building surfaces first.

## Validation

- Confirm files are generated in the correct profile, repo, or org-defaults location.
- Check README links, badge URLs, widget URLs, usernames, and template paths.
- Make manual metadata changes explicit when they cannot be expressed through files alone.

## Reference files

- Read `references/profile-surface.md` when the task is about a personal or organization GitHub profile.
- Read `references/repository-surface.md` when the task is about repo README, metadata, community files, or templates.
- Read `AGENTS.md` when you need concrete file-generation recipes for profile or repository surfaces.
