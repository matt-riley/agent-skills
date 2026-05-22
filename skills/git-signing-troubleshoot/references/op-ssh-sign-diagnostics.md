# op-ssh-sign Diagnostics

## Diagnostic command sequence

Run these in order; stop at the first that unblocks the commit:

```sh
# 1. Confirm the configured signing binary
git config --get gpg.ssh.signingkey
git config --get gpg.program
git config --get core.sshCommand

# 2. Inspect the 1Password SSH agent socket
echo $SSH_AUTH_SOCK
ls -la "$SSH_AUTH_SOCK"

# 3. List keys available to the agent (expects your signing key to appear)
ssh-add -L

# 4. Run the signing binary directly — matches what Git calls
/Applications/1Password.app/Contents/MacOS/op-ssh-sign -Y sign -n git -f /tmp/test_payload <<< "test"
# Expected: exits 0 and emits a PEM-wrapped SSH signature to stdout

# 5. Attempt a real commit — this is the authoritative source of truth
git commit --allow-empty -m "chore: signing smoke test"
```

## 1Password SSH agent states

| State | Symptom | Fix |
|-------|---------|-----|
| 1Password locked | `op-ssh-sign` exits with `failed to fill whole buffer` | Unlock 1Password app |
| Socket not set | `SSH_AUTH_SOCK` empty or path missing | Enable SSH agent in 1Password → Settings → Developer → SSH Agent |
| Key not in agent | `ssh-add -L` returns empty or wrong key | Add the key item to the 1Password SSH agent section |
| Agent running, key present | `git commit` fails despite `ssh-add -L` showing key | Try `git commit` directly — `op whoami` can give false negatives (see below) |

## `op whoami` false-negative pattern

`op whoami` can report `account is not signed in` even when the 1Password SSH agent is healthy and `op-ssh-sign` is functional. This happens when:

- The CLI session token has expired but the desktop app (and its agent socket) is still running.
- The CLI and the desktop app use separate auth contexts.

**Resolution:** Use `git commit` directly as the test, not `op whoami`. If `git commit` succeeds, signing is working regardless of `op whoami` output.

## When to stop

Stop investigation and surface the blocker if:

- `ssh-add -L` returns the correct key AND a real `git commit` still fails with the same error after unlocking 1Password.
- The user's global Git signing config is overridden by a repo-local config pointing at a different key or program — surface the conflict.
- `op-ssh-sign` is not at the expected path — do not suggest an alternate binary or disabling signing.

**Never** suggest `--no-gpg-sign`, `commit.gpgsign=false`, or swapping `gpg.program` to work around the failure.
