---
name: ci-images
description: Validate CI checks locally and manage Docker image publishing workflows.
  Use when changing build inputs (generated code, formatting, tests), preparing a
  release, or verifying that image tags are correct.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes bash, git, make, go, docker, and repo-local
  CI equivalent commands.
metadata:
  owner: mattriley
  version: 1.0.0 # x-release-please-version
  maturity: draft
---

# CI images

## Use this skill when

- Pre-flighting the same checks CI runs (generation, formatting, static analysis, tests) before pushing.
- Preparing a release or validating Docker image tags and publishing workflow.
- Investigating why CI rejects a change that appeared to work locally.

## Do not use this skill when

- The task is diagnosing an already-failing Actions run (use `github-actions-failure-triage`).
- The change is pure application code with no build or release impact.

## Inputs to gather

- The repository's local CI equivalents (`make` targets, scripts, or documented commands).
- Whether the release is triggered by tag, release publish, or manual dispatch.
- The current image tagging convention (floating aliases, `latest` pointer, semver pins).

## First move

- Run the local equivalents of each CI check in order and fix each one before moving on.

## CI checks → local equivalents

CI fails fast on these in order. Run them locally before pushing:

| CI check                  | Local command                              |
| ------------------------- | ------------------------------------------ |
| Generated code up-to-date | `make generate` (or your code-gen command) |
| Formatting                | `make fmt` (or `gofmt -l .`)               |
| Static analysis           | `make vet` (or `go vet ./...`)             |
| Tests                     | `make test`                                |

If any fail locally, they will fail in CI. Fix before pushing.

## Docker image publishing

Typical trigger: GitHub Release publish, or `workflow_dispatch` for manual runs.

Standard tagging strategy on release:

- `vX.Y.Z` — exact semver
- `X.Y`, `X` — floating semver aliases
- `latest` — points to newest release

## Pre-release checklist

1. All tests pass: `make test`
2. Generated code committed: run `make generate`, confirm `git diff` is clean
3. Schema/spec validation passes (if applicable): `make validate-openapi` or equivalent

## Guardrails

- Never publish an image from a dirty working tree.
- Never publish with stale generated code — generation output must be committed.
- CI is the authoritative gate; local checks mirror it but do not replace it.

## Support files

- Read `references/examples.md` when you need concrete user utterances, expected behaviour, or a model answer shape to mirror.
- Read `references/edge-cases.md` when the request is a near miss, partially matches this skill, or the first attempt fails.
- Run `scripts/release-readiness.sh --help` when you want a parameterised release-readiness check.
