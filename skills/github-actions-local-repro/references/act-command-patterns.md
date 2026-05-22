# act command patterns

Use these patterns to keep local repro narrow and comparable to hosted Actions runs.

## Fast intake

- Lint workflow first: `action-validator .github/workflows/<workflow>.yml`
- List events/jobs: `act -l`
- Run one event with one job: `act pull_request -j <job>`
- Use specific workflow file: `act pull_request -W .github/workflows/<workflow>.yml -j <job>`

## Matrix and environment targeting

- Prefer a minimal `.env` or `--var` set for deterministic repro.
- Use a dedicated secrets file with placeholders for local-only values.
- Keep command and inputs identical between reruns while debugging.

## Exit criteria

- Stop local repro when hosted-only dependencies make behavior non-representative.
- Document the exact mismatch (runner image, protected env, org secret policy) before handoff.
