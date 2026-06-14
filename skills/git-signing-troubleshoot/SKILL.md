---
name: git-signing-troubleshoot
description: "Use when commits, tags, or pushes are blocked by GPG or SSH signing failures — including 1Password op-ssh-sign errors, failed to fill whole buffer, or misleading op whoami output, not when the main task is branch integration, PR handling, or secret-scan triage."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: version-control
  audience: general-coding-agent
  maturity: draft
  kind: task
  kind: task
---

# Git signing troubleshoot

Use this skill when local Git signing is the blocker and the job is to diagnose the trusted signing path safely, especially for 1Password-backed SSH signing, without bypassing GPG or SSH signing requirements.

## Use this skill when

- A commit, tag, or push is blocked by a GPG or SSH signing failure.
- Git is configured for SSH signing and the error mentions `op-ssh-sign`, `failed to fill whole buffer`, or another 1Password signing failure.
- `op whoami` says the account is not signed in, but the 1Password app is open and the real question is whether signed Git operations still work.
- You need to confirm the configured signing format or program path without swapping to an alternate signing route.
- The safest useful outcome is either a successful signed Git operation or a precise blocker that the user must clear in their trusted signing setup.

## Do not use this skill when

- Signing already works and the real task is how to merge, push, or clean up the branch.
- The main blocker is PR creation, PR review, or remote checks rather than local signing.
- The push is blocked by secret scanning, not signing.
- The request is to bypass signing with `--no-gpg-sign`, config overrides, or alternate credentials.

## Routing boundary

| Situation | Use this skill? | Route instead |
| --- | --- | --- |
| Local commit, tag, or push fails because the trusted signing path is broken or uncertain | Yes | - |
| Signing works and the next question is how to integrate the branch | No | [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) |
| The work is PR creation, update, or check watching after the branch is already signed and pushed | No | [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) |
| The push is blocked by secret scanning or leaked-secret policy, not signing | No | [`secret-scan-triage`](../secret-scan-triage/SKILL.md) |

## Inputs to gather

**Required before changing config**

- The exact error from the real Git command that failed, preferably `git commit`, `git tag -s`, or `git push` rather than a proxy diagnostic.
- The current signing settings from `git config --get gpg.format` and `git config --get gpg.ssh.program`.
- Whether the configured signing program exists at that exact path.
- Whether the 1Password app is open and whether its SSH agent integration is enabled.
- Whether the failure happens on commit, tag, push, or all three.

**Helpful if present**

- The repository path, branch, and whether a previous signed operation succeeded recently.
- The exact configured signer binary path such as `op-ssh-sign`.
- Whether `op whoami` disagrees with the real Git command result.
- Whether the failure is persistent or only occurs after the 1Password app locks.

**Only investigate if encountered**

- Safe key metadata such as title or item ID using fields-only `op item get` queries.
- SSH agent environment details if the configured signer path exists but the app still cannot service requests.
- Whether a local config override is shadowing the intended global signing config.

## First move

1. Retry the real signed Git command first and treat that result as the source of truth.
2. Read `gpg.format` and `gpg.ssh.program`, then confirm the configured signer exists at that exact path.
3. If the real command still fails, check whether the 1Password app is unlocked and its SSH agent integration is enabled before proposing any other action.

## Workflow

1. Start with the real signed Git operation. If `git commit`, `git tag`, or `git push` succeeds, stop: the signing path is working, even if a secondary probe such as `op whoami` looks unhealthy.
2. If the real Git command fails, inspect `git config --get gpg.format` and `git config --get gpg.ssh.program` so you know whether Git is actually using SSH signing and which program it expects.
3. Confirm that the configured signing program exists at the configured path. If the path is wrong or missing, restore the trusted configured signer path instead of substituting a different signing backend.
4. If the error is `failed to fill whole buffer` from `op-ssh-sign`, treat it as a 1Password app-interop blocker. Ask the user to unlock 1Password, confirm the SSH agent is enabled in the app settings, and retry the same Git command.
5. Do not declare signing broken based on `op whoami` alone. That command can report not-signed-in even when the 1Password app is delegating signed commits correctly.
6. If you need to inspect a 1Password SSH key item, request only non-secret fields such as `title` and `id` with `op item get "<item>" --fields title,id`; never dump the full item payload.
7. If the trusted signer path is confirmed and the real Git command still fails, surface the exact blocker and stop for user action. The next step belongs to the user restoring or approving the trusted signing setup, not to the agent inventing an alternate route.

## Outputs

- A verified answer about whether the real signed Git operation works.
- The exact trusted signing configuration in use and whether the configured signer path is valid.
- A precise external blocker when 1Password app approval, unlock state, or SSH agent setup is the real issue.
- A safe route-away decision when the problem is actually branch integration, PR handling, or secret-scan policy.

## Guardrails

- Never suggest `--no-gpg-sign`, `git -c commit.gpgsign=false`, credential-helper swaps, or alternate signing programs just to get a commit through.
- Treat the real signed Git command as the source of truth; do not overrule it with `op whoami`.
- Treat `failed to fill whole buffer` as a 1Password app or SSH-agent interop issue, not as a reason to change Git to an unsigned path.
- Never fetch a full 1Password SSH key item payload just to confirm metadata.
- Stop and surface the blocker clearly when the trusted signing path needs user approval or repair.

## Validation

- Retry the real signed Git command after any user-visible fix such as unlocking 1Password or enabling the SSH agent.
- Confirm `git config --get gpg.format` and `git config --get gpg.ssh.program` match the intended trusted setup.
- Confirm the configured signer path exists before blaming Git for a missing executable.
- If metadata inspection was needed, confirm only non-secret fields were requested.
- If the command still fails, record the exact error and hand back the blocker instead of proposing a bypass.
- Smoke test:
  - should trigger: "My signed commit fails with `op-ssh-sign: failed to fill whole buffer`; diagnose it without bypassing 1Password signing."
  - should not trigger: "The push was rejected because GitHub secret scanning found an AWS key in the diff." (→ `secret-scan-triage`)

## Examples

- "A signed `git commit` failed even though 1Password is open; check the trusted SSH signing path and tell me whether the issue is Git config or 1Password interop."
- "`op whoami` says not signed in, but I need to know whether my signed commit path is actually broken before I touch any config."
- "Our repo uses SSH signing with 1Password and `op-ssh-sign`; troubleshoot the failure safely and do not suggest disabling signing."

## Reference files

- [`references/op-ssh-sign-diagnostics.md`](references/op-ssh-sign-diagnostics.md) — diagnostic command sequences, 1Password SSH agent states, `op whoami` false-negative pattern, and when to stop
- [`finishing-a-development-branch`](../finishing-a-development-branch/SKILL.md) — route here when signing works and the remaining question is branch integration
- [`github-cli-pr-workflow`](../github-cli-pr-workflow/SKILL.md) — route here when the signed branch is ready and the remaining work is PR lifecycle
- [`secret-scan-triage`](../secret-scan-triage/SKILL.md) — route here when push rejection is caused by secret scanning rather than signing
- [`copilot-instructions.md`](../../copilot-instructions.md) — source rules for never bypassing trusted signing, fields-only 1Password metadata checks, and treating real Git commands as the source of truth
