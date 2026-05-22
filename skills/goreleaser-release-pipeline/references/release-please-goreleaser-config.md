# Release Please + GoReleaser Configuration Reference

## Annotated workflow template

```yaml
name: release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: go

  publish:
    needs: release-please
    if: ${{ needs.release-please.outputs.release_created }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required: GoReleaser needs full git history for changelog generation
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: goreleaser/goreleaser-action@v6
        with:
          version: latest
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GORELEASER_CURRENT_TAG: ${{ needs.release-please.outputs.tag_name }}
```

## `include-component-in-tag` setting

For single-package Go repositories, Release Please v4 defaults to component-prefixed tags like `my-repo-v1.2.3`. GoReleaser v2 requires plain semver (`v1.2.3`).

In `release-please-config.json`:

```json
{
  "packages": {
    ".": {
      "release-type": "go",
      "include-component-in-tag": false
    }
  }
}
```

This produces plain `vX.Y.Z` tags that GoReleaser accepts without remapping.

## `release_created` job gate

The publish job must be gated on `release_created: true`. Without this gate:

- The publish job runs on every push to main (not just releases).
- GoReleaser will fail if there is no matching tag at HEAD.

Correct gate pattern:
```yaml
if: ${{ needs.release-please.outputs.release_created }}
```

Do **not** use a separate `release: published` trigger when Release Please uses the default `GITHUB_TOKEN` — the token cannot trigger downstream workflows.

## `fetch-depth: 0` — why it matters

GoReleaser generates changelogs by walking git history between the current and previous tag. A shallow clone (`fetch-depth: 1`, the default for `actions/checkout`) only contains the latest commit, so GoReleaser either:

- Produces an empty changelog, or
- Fails with "could not find previous tag"

Always set `fetch-depth: 0` in the publish job's checkout step.

## `goreleaser check` command

Run before committing any `.goreleaser.yaml` change to catch schema and config errors locally:

```sh
goreleaser check
```

This validates the config without running a release. It catches:
- Deprecated fields (v1 → v2 migration)
- Missing required archive or build targets
- Invalid template syntax in `name_template`

Do not rely on a failed GitHub Actions run to discover config errors — check locally first.
