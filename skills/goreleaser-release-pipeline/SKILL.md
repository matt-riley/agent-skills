---
name: goreleaser-release-pipeline
description: "Use when setting up, debugging, or fixing a GoReleaser v2 release pipeline — especially Release Please tag issues, missing release assets, or publish jobs that fail after a release is created, not when the main task is generic CI triage or PR handling."
metadata:
  category: ci
  audience: general-coding-agent
  maturity: beta
  kind: task
---

# GoReleaser release pipeline

Use this skill when a repository already has, or is adding, a GoReleaser v2 release flow and the important question is how Release Please, tags, GitHub releases, and publish jobs fit together without losing versioned releases or assets.

## Use this skill when

- You are wiring Release Please to a GoReleaser v2 publish flow.
- A release is created, but the GitHub release has no binary assets.
- A GoReleaser publish job fails because the tag is not plain semver.
- You need to fix tag shape, publish-job conditions, or Release Please outputs without redesigning the whole CI system.
- The team cares about preserving release numbers for downstream monitoring or release correlation.

## Do not use this skill when

- The main task is generic GitHub Actions runner, cache, permission, or environment triage with no release-pipeline-specific evidence.
- The main task is deciding how to merge, keep, or discard a finished branch.
- The main task is creating, updating, or managing a pull request.
- The repository is not using GoReleaser or Release Please.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Release Please and GoReleaser need to publish versioned Go artifacts from the same workflow | Yes | - |
| GitHub Actions run is failing for runner, cache, permissions, or environment reasons outside the release design itself | No | [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md) |
| The implementation is done and the question is how to integrate or clean up the branch | No | [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) |
| The main task is PR creation, update, or checks-watching | No | [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) |

## Inputs to gather

**Required before editing**

- The current release workflow file and any called reusable workflow that actually publishes artifacts.
- The Release Please configuration, especially tag-format settings such as `include-component-in-tag`.
- The `.goreleaser.yaml` or equivalent GoReleaser config.
- The concrete failure signal: run URL, failed step, missing assets on a release, or the exact invalid tag.
- The expected release contract: plain semver tags, GitHub release assets, and any requirement to preserve numbered releases.

**Helpful if present**

- The values emitted by Release Please outputs such as `release_created` and `tag_name`.
- The latest release page, tag list, and whether the release exists before publish starts.
- The repository's existing workflow linting or release validation commands.
- Monitoring or downstream consumers that rely on stable release numbers.

**Only investigate if encountered**

- Whether the workflow uses the default `GITHUB_TOKEN` or an explicit publishing token.
- Job `if:` conditions, `needs:` wiring, and artifact handoff between release and publish jobs.
- History requirements such as checkout depth or tag availability if GoReleaser cannot resolve the version.

## First move

1. Read the live release workflow, Release Please config, and GoReleaser config together before editing any one file in isolation.
2. Confirm whether Release Please is generating a plain semver tag and whether the publish job is chained directly from Release Please outputs.
3. Run `goreleaser check` before committing any `.goreleaser.yaml` change.

## Workflow

1. Anchor the failure mode first: invalid tag, release with no assets, or publish job failure after release creation.
2. Validate the tag format. For single-package repositories that feed GoReleaser v2, set `include-component-in-tag: false` so Release Please emits `vX.Y.Z` instead of component-prefixed tags such as `gh-depdash-v1.1.1`.
3. Inspect how the publish job starts. If the workflow relies on a separate `release: published` trigger created by Release Please with the default `GITHUB_TOKEN`, move the publish job into the same workflow and gate it with `${{ steps.release.outputs.release_created }}`.
4. Pass the release context forward from Release Please, especially `${{ steps.release.outputs.tag_name }}`, so the publish job builds against the exact created release rather than guessing from a later event.
5. When a release exists but has no binary assets, check whether the GoReleaser job ran at all before changing `.goreleaser.yaml`; missing assets usually mean `release_created` was false, the job condition was wrong, or the job lived behind the wrong trigger.
6. Preserve defined releases and version numbers when simplifying the pipeline. If the team uses release numbers for Datadog or other correlation, simplify around main-based tags, numbered releases, and immutable artifact promotion rather than removing release granularity.
7. If the remaining failure is really a runner, permission, or environment problem in GitHub Actions rather than a release-pipeline design issue, stop and hand off to the GitHub Actions triage path.

## Outputs

- A release workflow design that chains Release Please and GoReleaser in the same workflow when `GITHUB_TOKEN` is creating the release.
- Plain semver tags that GoReleaser v2 accepts.
- A validated GoReleaser config and a short explanation of why missing assets or failed publish jobs occurred.
- A clear route-away decision when the problem belongs to GitHub Actions triage, PR handling, or branch integration instead.

## Guardrails

- Do not rely on a separate `release: published` workflow when Release Please is using the default `GITHUB_TOKEN`; chain the publish job in the same workflow instead.
- Do not leave component-prefixed tags enabled for a single-package GoReleaser v2 release flow.
- Do not treat an empty release page as a GoReleaser schema bug until you have confirmed the publish job actually ran.
- Do not remove defined releases or renumber version history if downstream monitoring depends on those release numbers.
- Do not absorb generic GitHub Actions runner troubleshooting or PR lifecycle work into this skill.
- Ensure `actions/checkout` uses `fetch-depth: 0` when GoReleaser generates a changelog; shallow clones silently produce incomplete or missing changelogs.

## Validation

- Run `goreleaser check` after editing `.goreleaser.yaml`.
- Run the repository's existing workflow validation command when workflow files change.
- Confirm the publish job is gated by the Release Please outputs you expect, especially `release_created` and `tag_name`.
- Confirm the target tag format is plain semver (`vX.Y.Z`) before calling the pipeline fixed.
- If the release previously existed without assets, confirm the revised workflow would actually execute the GoReleaser job for that release path.
- Smoke test:
  - should trigger: "Release Please created `v1.4.0`, but the GitHub release has no binaries and our GoReleaser publish job never ran."
  - should not trigger: "This Actions run is failing on a self-hosted runner bootstrap step; diagnose the workflow job first." (→ `github-actions-failure-triage`)

## Examples

- "Set up Release Please and GoReleaser v2 so a single-package Go repo publishes binaries on each numbered release."
- "Fix this release flow: Release Please created the GitHub release, but no assets were uploaded and the publish workflow never fired."
- "GoReleaser rejects our new tag as invalid semver after Release Please cut `gh-depdash-v1.1.1`; fix the tag strategy without changing our release numbering scheme."

## Reference files

- [`references/release-please-goreleaser-config.md`](references/release-please-goreleaser-config.md) — annotated workflow template, `include-component-in-tag` setting, `release_created` job gate, `fetch-depth: 0` note, and `goreleaser check` command
- [`../../instructions/github-actions.instructions.md`](../../instructions/github-actions.instructions.md) — source rules for Release Please chaining, semver tag shape, and preserving numbered releases
- [`../github-actions-failure-triage/SKILL.md`](../github-actions-failure-triage/SKILL.md) — route here when the failure is generic workflow or runner triage instead of release-pipeline design
- [`../finishing-a-development-branch/SKILL.md`](../finishing-a-development-branch/SKILL.md) — route here when the question is branch integration rather than release publishing
- [`../github-cli-pr-workflow/SKILL.md`](../github-cli-pr-workflow/SKILL.md) — route here when the work is PR lifecycle rather than release pipeline behavior
