# Health check patterns for Go Docker images

## Pattern overview

| Base image | Health check approach | Command |
|---|---|---|
| `scratch` | Binary subcommand | `CMD ["/server", "health"]` |
| `alpine` | `wget` to localhost | `CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health \|\| exit 1` |
| `distroless` | Binary subcommand (same as scratch) | `CMD ["/server", "health"]` |
| `alpine` with curl | `curl` to localhost | `CMD curl -f http://localhost:8080/health \|\| exit 1` |

## scratch (binary subcommand)

The binary must implement a `health` subcommand or flag:

```go
// cmd/server/health.go
var healthCmd = &cobra.Command{
    Use:   "health",
    Short: "Run health check and exit",
    RunE: func(cmd *cobra.Command, args []string) error {
        // Perform health checks: DB ping, dependency status, etc.
        // On failure: os.Exit(1)
        // On success: os.Exit(0)
        fmt.Println("healthy")
        return nil
    },
}
```

Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["/server", "health"]
```

This is the preferred pattern for production images — no external dependencies, works on scratch.

## alpine (wget or curl)

For services that don't have a health subcommand but expose an HTTP `/health` endpoint:

```dockerfile
FROM alpine:3.21

RUN apk add --no-cache wget

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

Or with `curl`:

```dockerfile
RUN apk add --no-cache curl

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

## HEALTHCHECK flags

| Flag | Recommended value | Purpose |
|---|---|---|
| `--interval` | `30s` | Time between health checks |
| `--timeout` | `3s` | Max time for a single check to complete |
| `--start-period` | `5s` | Grace period after container start before checks begin |
| `--retries` | `3` | Consecutive failures before marking unhealthy |

Adjust `--start-period` upward (15-30s) for services with slow startup (DB migrations, cache warming).

## Testing health checks

```bash
# Build and run the image
docker build -t test-health .
docker run -d --name test-health -p 8080:8080 test-health

# Check health status
docker inspect --format='{{.State.Health.Status}}' test-health
# Expected: "healthy"

# Check the last 5 health check results
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' test-health

# Clean up
docker rm -f test-health
```

## Go `/health` endpoint (chi example)

```go
r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
})
```

Keep the health endpoint simple: return 200 if the process is running. Add dependency checks (DB ping, Redis ping) only when the health check drives orchestration decisions (restart on DB failure). For most services, a simple 200 is sufficient.
