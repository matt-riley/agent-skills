This repository has a Release Please -> GoReleaser pipeline. Releases are created
but the GitHub releases end up without binary assets, and the publish job reports
an invalid tag.

Fix the pipeline so versioned releases publish assets. Keep the publish job and
its gating intact.
