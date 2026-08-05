# Common Failures and Routing

## Routing Boundary

| Your situation | Use this skill? | Routing |
|---|---|---|
| "I think I fixed the bug" (no command run yet) | ✅ Yes | Run the test that reproduces the bug, read output |
| "All tests pass" (from yesterday's run) | ✅ Yes | Rerun tests fresh, capture current output |
| "The linter should be happy" (no check run) | ✅ Yes | Run linter fresh, capture full output |
| "I've understood the codebase" | ❌ No | Continue exploration or code inspection |
| "The build failed; here's why" + no rebuild | ✅ Yes | Rebuild, read full error output |
| "This PR is ready" (untested) | ✅ Yes | Run tests, linting, build before claiming readiness |

## Common Failures Table

| Claim | Requires | Not sufficient |
|---|---|---|
| **Tests pass** | Test command output: all pass, 0 failures, exit code 0 | "I think they pass," previous run, linter passing, code reviewed |
| **Linter clean** | Linter stdout: no errors, 0 errors total | Partial file checks, "should be clean," no syntax errors |
| **Build succeeds** | Build command: exit code 0, no build errors in output | Linter passing, code compiles locally, "should build" |
| **Bug fixed** | Reproduction test now passes; symptom gone in live run | Code changed, test file created but not run, review approved |
| **Agent completed** | VCS diff shows actual committed changes or agent output shows execution | Agent log says "success," agent says it ran the command |
| **Formatting applied** | Formatter command: exit code 0, or git diff shows changes applied | Formatter installed, "should work," no actual check run |
| **Dependency installed** | `npm list`/`pip list`/`cargo tree` shows version, or import succeeds | `npm install` ran, "should be installed," no verification |

## Notes

- This skill applies to all verification scenarios: test passes, build succeeds, lint clean, bug fixed, command execution, agent completion.
- If you are uncertain, state the uncertainty as part of your verification result.

See main SKILL.md for the canonical Iron Law, Inputs, Gate, Workflow, Guardrails, and Validation. Long examples live here in `examples.md`.
