# Evaluation Implementation Checklist

Work through this checklist before shipping an evaluation loop. Every unchecked item is a potential runaway loop or silent failure.

## Setup

- [ ] Evaluation criteria are defined before any generation begins
- [ ] Score threshold is set (`score_threshold`, e.g. `0.8`) and documented
- [ ] Max iterations are set (`max_iterations`, e.g. `3`) and enforced
- [ ] Evaluation output format is structured (JSON schema confirmed)

## Loop wiring

- [ ] `generate()` step produces the initial output
- [ ] `evaluate()` step returns structured output with a numeric or boolean quality signal
- [ ] `optimize()` step consumes the critique and returns a revised output
- [ ] Loop advances `output` from the result of `optimize()`, not from a side effect

## Convergence and safety

- [ ] Loop exits when score meets the threshold
- [ ] Loop exits when `max_iterations` is reached
- [ ] Convergence check is present: loop exits early if score does not improve between iterations
- [ ] Evaluation parse failure is handled: malformed JSON from the evaluate step falls back to a failing score rather than crashing

## Logging and observability

- [ ] Each iteration logs: iteration number, output (or a hash), score, and critique
- [ ] Final iteration and exit reason are logged (`threshold_met`, `max_iterations`, `convergence`)
- [ ] Log output is accessible for debugging without re-running the full loop

## Post-implementation smoke check

- [ ] Run with a known-good input and confirm the loop exits at `threshold_met` before `max_iterations`
- [ ] Run with a known-bad input and confirm the loop exhausts `max_iterations` without crashing
- [ ] Introduce a malformed evaluate response and confirm the fallback fires correctly
