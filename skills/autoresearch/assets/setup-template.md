# Autoresearch setup template

Fill in this table before starting the experiment loop. Paste the completed version into chat and confirm with the user before Phase 2 begins.

## Setup parameters

| Parameter | Value |
| --- | --- |
| **Goal** | _What are you trying to improve? (e.g., reduce p95 latency, increase test pass rate, shrink bundle size)_ |
| **Metric command** | _The exact shell command to run (e.g., `npm run benchmark`, `go test -bench=. ./...`, `hyperfine './build.sh'`)_ |
| **Metric extraction** | _How to pull a number from the output (e.g., "JSON field `.mean`", "line matching `ns/op`", "count of `PASS` lines")_ |
| **Direction** | _`lower_is_better` or `higher_is_better`_ |
| **In-scope files/dirs** | _Which files or directories the agent may edit_ |
| **Out-of-scope files/dirs** | _Which files must not be touched_ |
| **Max experiments** | _A count, or `unlimited` (stop on interrupt only)_ |
| **Constraints** | _Time budget per run, dependency policy, test-passing requirement, API compatibility, memory limits — or `none`_ |
| **Simplicity policy** | _Default: simpler is better; weigh complexity cost against metric gain. Note any overrides here._ |

## Baseline record

Fill in after Phase 2 baseline run:

| Field | Value |
| --- | --- |
| Branch | `autoresearch/` |
| Baseline commit | |
| Baseline metric value | |
| Measurement timestamp | |

## Notes

Add any per-session notes here, such as known constraints discovered during setup, early hypotheses, or areas to avoid.
