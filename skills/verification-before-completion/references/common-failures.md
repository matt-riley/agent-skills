# Common Failures, Iron Law, Routing, and Gate Details

## Iron Law

> **NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**
>
> A claim like "tests pass," "build succeeds," or "bug is fixed" requires you to have actually run the relevant command, read the full output, and confirmed the claim matches that evidence. Assumptions, previous runs, or code inspection alone do not count.

## Routing Boundary

| Your situation | Use this skill? | Routing |
|---|---|---|
| "I think I fixed the bug" (no command run yet) | ✅ Yes | Run the test that reproduces the bug, read output |
| "All tests pass" (from yesterday's run) | ✅ Yes | Rerun tests fresh, capture current output |
| "The linter should be happy" (no check run) | ✅ Yes | Run linter fresh, capture full output |
| "I've understood the codebase" | ❌ No | Continue exploration or code inspection |
| "The build failed; here's why" + no rebuild | ✅ Yes | Rebuild, read full error output |
| "This PR is ready" (untested) | ✅ Yes | Run tests, linting, build before claiming readiness |

## Inputs to Gather

1. **Claim**: What are you about to claim? (e.g., "tests pass", "bug is fixed", "build works")
2. **Command**: What single command proves or disproves this claim?
3. **Success Criteria**: What does success look like in the output? (exit code 0, "0 failures", "All tests passed", etc.)
4. **Scope**: Which tests, files, or targets? (e.g., "all tests" vs. "one unit test" vs. "integration suite")

## First move / Gate (Summary)

Before proceeding:
1. **State the claim clearly**: "I am about to claim: [specific claim]"
2. **Identify the proof command**: "The command that proves this is: `[command]`"
3. **Describe success**: "Success means: [specific output pattern or exit code]"
4. **Check if ready**: "Am I ready to run this now?"

**BEFORE claiming any status or marking work complete:**
- IDENTIFY the command
- RUN the full command fresh (capture complete output)
- READ the full output carefully (exit codes, counts, warnings)
- VERIFY: does the output confirm the claim?
- ONLY THEN make the claim with direct evidence (quote the output)

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
- Do not skip the Gate. The Gate is the entire point of this skill.
- If you are uncertain, state the uncertainty as part of your verification result.

See main SKILL.md for the concise Workflow/Guardrails/Validation and the Reference files section (links to systematic-debugging and test-driven-development). Long examples live here in `examples.md`.