---
name: go-docker-builds
description: "Containerize Go services with production-ready multi-stage Docker builds. Use when writing or debugging a Dockerfile for a Go service, setting up static compilation for scratch/distroless images, adding health checks, or wiring image builds into CI — not for Docker Compose local dev stacks or non-Go Dockerfiles."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: go
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Go Docker builds

Use this skill when containerizing a Go service for production. It covers the canonical multi-stage build pattern, static compilation, minimal base images, health checks, secrets handling, and CI integration for image builds.

## Use this skill when

- Writing a new Dockerfile for a Go service or API.
- Debugging a Go Docker build that fails during compilation, linking, or the final image stage.
- Switching a Go Docker image from a full base image to scratch or distroless.
- Adding health checks, signals, or graceful shutdown handling to a Go container.
- Pushing Go images to a registry from CI (GitHub Actions).
- Handling CGO dependencies in a Go Docker build.
- Setting up multi-platform builds for Go services.

## Do not use this skill when

- The task is running a local multi-service stack for development — use [`docker-compose-dev`](../docker-compose-dev/SKILL.md).
- The Dockerfile is for a non-Go service (Node, Python, Ruby, etc.).
- The Go service fails to build outside Docker — use [`go-build-and-test`](../go-build-and-test/SKILL.md).
- The main task is configuring CI workflows that happen to include a Docker step — use [`github-actions-failure-triage`](../github-actions-failure-triage/SKILL.md).

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| New Dockerfile for a Go API, starting from scratch | Yes | — |
| Go Docker build fails on `go build` inside the builder stage | Yes | — |
| Switching from `golang:alpine` base to `scratch` for a Go binary | Yes | — |
| Local dev with `docker compose up` for PostgreSQL + app | No | [`docker-compose-dev`](../docker-compose-dev/SKILL.md) |
| `go build` fails locally, outside Docker | No | [`go-build-and-test`](../go-build-and-test/SKILL.md) |

## Inputs to gather

**Required before editing**

- The Go module path and binary name (from `go.mod` and `main.go`).
- Whether the service uses CGO (check for `import "C"`, `CGO_ENABLED`, or C library dependencies).
- The target registry and image name (e.g. `ghcr.io/owner/repo`).
- Whether the build is single-platform or multi-platform.

**Helpful if present**

- The existing `Dockerfile` and any `.dockerignore`.
- The Go version pinned in `go.mod` (`go 1.26` → use `golang:1.26-alpine`).
- The CI workflow that builds and pushes the image.

**Only investigate if encountered**

- Whether the service needs CA certificates in the final image (scratch images lack them).
- Whether the binary needs to run as non-root.
- Whether timezone data is required in the final image.

## First move

1. Check `go.mod` for the Go version, `CGO_ENABLED` usage, and the binary name.
2. Identify whether the existing Dockerfile follows the canonical multi-stage pattern or needs restructuring.
3. Determine the minimal base image needed: `scratch` for pure Go, `alpine` for CGO or CA certs, `distroless` for extra hardening.

## Workflow

### 1. Canonical multi-stage build

The standard Go Dockerfile for a pure-Go service with no CGO:

```dockerfile
FROM golang:1.26-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM scratch

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
ENTRYPOINT ["/server"]
```

Key rules:
- Pin the Go version to match `go.mod` (e.g. `go 1.26` → `golang:1.26-alpine`).
- `go mod download` as a separate layer before `COPY . .` so dependency changes don't invalidate the source cache.
- `CGO_ENABLED=0` for static binaries that run on `scratch`.
- `-ldflags="-s -w"` strips debug info, reducing binary size (~30% smaller).
- `COPY --from=builder /etc/ssl/certs/ca-certificates.crt` is required when the service makes HTTPS outbound calls from a scratch image.
- The `scratch` base has no shell, no package manager, and no CA certs — only add what the binary actually needs.

### 2. CGO builds

When the service requires CGO (sqlite via `go-sqlite3`, etc.):

```dockerfile
FROM golang:1.26-alpine AS builder

RUN apk add --no-cache gcc musl-dev

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

RUN CGO_ENABLED=1 go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM alpine:3.21

RUN apk add --no-cache ca-certificates tzdata

COPY --from=builder /app/server /server

EXPOSE 8080
ENTRYPOINT ["/server"]
```

Key differences from pure-Go:
- `gcc` and `musl-dev` are required in the builder stage for CGO compilation.
- The final image must be `alpine`, not `scratch`, because CGO binaries dynamically link musl libc.
- `tzdata` is often needed for timezone-aware applications; add it explicitly.

### 3. Non-root user

Run the binary as a non-root user for defense in depth:

```dockerfile
FROM alpine:3.21

RUN apk add --no-cache ca-certificates tzdata
RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /app/server /server

USER app
EXPOSE 8080
ENTRYPOINT ["/server"]
```

For `scratch` images, copy `/etc/passwd` from the builder or use a numeric UID:

```dockerfile
FROM scratch
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /app/server /server
USER 1000:1000
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### 4. Health checks

Add a health check that calls the service's own `/health` endpoint:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /server health || exit 1
```

For scratch images with no shell, the binary must support a `health` subcommand that exits 0 on success. For alpine images, use `wget` or the binary directly. Read [`references/health-check-patterns.md`](references/health-check-patterns.md) for alternatives.

### 5. Multi-platform builds

For multi-platform images (amd64 + arm64), use `docker buildx`:

```bash
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag ghcr.io/owner/repo:latest \
    --push .
```

In `.goreleaser.yaml`, multi-platform Docker builds are configured under `dockers`:

```yaml
dockers:
  - image_templates:
      - "ghcr.io/owner/repo:{{ .Tag }}"
      - "ghcr.io/owner/repo:latest"
    dockerfile: Dockerfile
    build_flag_templates:
      - "--platform=linux/amd64,linux/arm64"
```

### 6. CI integration (GitHub Actions)

The canonical GitHub Actions job for building and pushing a Go Docker image:

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }},ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

Key rules:
- Set `packages: write` permission for GHCR pushes.
- Use `${{ secrets.GITHUB_TOKEN }}` — no need for a personal access token.
- Enable GitHub Actions cache for faster rebuilds.
- Tag with both `${{ github.sha }}` for traceability and `latest` for convenience.

### 7. .dockerignore

Always include a `.dockerignore` to keep the build context small:

```
.git
.github
*.md
.env
.env.*
tmp/
*.log
node_modules/
```

The builder only needs Go source — keep everything else out of the context.

## Outputs

- A production-ready multi-stage Dockerfile for a Go service.
- A `.dockerignore` that keeps the build context minimal.
- CI workflow configuration for building and pushing the image on push/PR.
- Health check wired in the Dockerfile or documented as a binary subcommand.

## Guardrails

- **Must** use `CGO_ENABLED=0` for static binaries targeting `scratch`.
- **Must** pin the Go version in the builder stage to match `go.mod`.
- **Must not** use `:latest` Go image tags; pin to a specific minor version.
- **Must** add CA certificates to `scratch` images when the service makes outbound HTTPS calls.
- **Should** run as non-root in the final image.
- **Should** separate `go mod download` into its own layer before `COPY . .`.
- **Should** strip debug info with `-ldflags="-s -w"`.
- **May** use `distroless` instead of `scratch` when additional hardening is desired.

## Validation

- Run `docker build -t test .` from the repo root and confirm the image builds without errors.
- Run `docker run --rm test` and confirm the binary starts and responds on the expected port.
- Run `docker run --rm test /server health` (or the health endpoint) to verify the health check works.
- If CI is configured, confirm the workflow pushes to the registry on merge to main.
- Smoke test:
  - should trigger: "Write a Dockerfile for this Go API service that builds a static binary and runs on scratch."
  - should trigger: "This Go Docker build fails because of CGO linking — it needs sqlite3."
  - should trigger: "Add a health check and non-root user to this Go service's Dockerfile."
  - should not trigger: "Run `docker compose up` to start PostgreSQL and the app for local dev." (→ `docker-compose-dev`)
  - should not trigger: "`go build` fails outside Docker with a GOROOT mismatch." (→ `go-build-and-test`)

## Examples

- "Containerize this Go chi API — I want a minimal scratch image with a health check."
- "My Go service uses go-sqlite3 and the Docker build fails on `CGO_ENABLED=0`. Fix the Dockerfile."
- "Set up GitHub Actions to build and push this Go service's Docker image to GHCR on every push to main."

## Reference files

- [`references/health-check-patterns.md`](references/health-check-patterns.md) — Health check alternatives for scratch, alpine, and distroless images.
- [`../docker-compose-dev/SKILL.md`](../docker-compose-dev/SKILL.md) — Adjacent skill for local multi-service development with Docker Compose.
- [`../go-build-and-test/SKILL.md`](../go-build-and-test/SKILL.md) — Route here when the Go binary fails to build outside Docker.
