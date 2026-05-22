---
name: secret-scan-triage
description: Use when secret scanning with gitleaks reports findings that need fast triage, containment, and false-positive adjudication before code changes or merges continue.
metadata:
  category: workflow
  audience: general-coding-agent
  maturity: beta
---

# Secret scan triage

Use this skill when `gitleaks` findings need a disciplined triage path so real exposures are contained quickly and false positives are handled without weakening scanning.

## Use this skill when

- `gitleaks` reports findings in local hooks, CI, or a manual scan.
- A branch is blocked by secret scan failures and needs evidence-based triage.
- You need to separate real credential exposure from known-safe test fixtures or synthetic tokens.
- You need a consistent remediation path that preserves scanning quality.

## Do not use this skill when

- The task is implementing a new scanner or replacing the security toolchain.
- There are no scan findings and the ask is general security hardening.
- The user explicitly requests incident response actions outside repository scope.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Active `gitleaks` findings require triage and remediation | Yes | - |
| Secret was confirmed leaked in production systems requiring org-level incident handling | No | security incident owner / platform process |
| Task is dependency or policy redesign unrelated to concrete findings | No | `agent-governance` |

## Inputs to gather

- Scanner output (rule ID, file, line, fingerprint, commit scope).
- Whether findings are in tracked source, history, generated files, or test fixtures.
- Expected allowlist or baseline policy already used by the repository.
- Whether the branch is public/shared and if containment steps already happened.

## First move

1. Run `gitleaks` with the repo's expected mode and capture raw findings.
2. Classify each finding as confirmed secret, probable secret, or probable false positive.
3. Contain confirmed/probable secrets first, then address false-positive tuning.

## Workflow

1. Reproduce findings with a deterministic command so triage output is stable.
2. Triage each finding:
   - confirmed/probable secret: revoke or rotate externally, then remove from code/history as required by policy
   - probable false positive: document reason and scope-limited allowlist entry
3. Apply smallest safe remediation:
   - redact or replace values with non-sensitive fixtures
   - move sensitive values to approved secret-management surfaces
   - keep allowlists precise to a rule/file/fingerprint when possible
4. Re-run scan and ensure only justified, documented exceptions remain.
5. Summarize finding-by-finding outcome and remaining external actions (for example rotation ownership).

## Outputs

- Triage table of findings and disposition.
- Repo changes for remediation or narrow allowlist updates.
- Explicit external follow-ups for any credential rotation/revocation.

## Guardrails

- Never paste raw secret values into chat, commits, or docs.
- Never blanket-ignore a rule just to unblock a branch.
- Do not treat "looks fake" as sufficient; require evidence for false-positive classification.
- Keep allowlist scope minimal and reviewable.

## Validation

- `gitleaks` output is clean or contains only justified, documented exceptions.
- Any new allowlist entry is narrow and tied to specific evidence.
- Repository checks relevant to touched files still pass.

- Smoke test:
  - should trigger: "Triage these gitleaks hits and narrow any allowlist changes."
  - should not trigger: "Add secret-handling policy checks to this agent." (→ `agent-governance`)

## Examples

- "CI is blocked by gitleaks in two files; triage each finding, remediate real exposures, and keep exceptions minimal."
- "Local pre-commit gitleaks flagged test fixtures; confirm which are false positives and add the narrowest possible allowlist."

## Reference files

- [`references/gitleaks-triage-patterns.md`](references/gitleaks-triage-patterns.md) - repeatable disposition patterns for real leaks, probable leaks, and false positives
