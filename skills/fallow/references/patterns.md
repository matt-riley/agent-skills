# Fallow patterns

Use these recipes when you need more than a one-off command.

## Full project audit

1. Run dead-code analysis:

   ```bash
   fallow dead-code --format json --quiet || true
   ```

2. Run duplication analysis:

   ```bash
   fallow dupes --format json --quiet || true
   ```

3. If cleanup is in scope, preview fixes:

   ```bash
   fallow fix --dry-run --format json --quiet || true
   ```

4. Use trace commands before deleting anything that looks unexpectedly unused.

## PR or changed-file gate

Use this when the user wants to know whether a branch introduces new issues in touched files:

```bash
fallow dead-code --format json --quiet --changed-since main --fail-on-issues || true
```

For a broader changed-file quality pass:

```bash
fallow audit --format json --quiet --base main --gate new-only --fail-on-issues || true
```

## Safe auto-fix cycle

1. Preview:

   ```bash
   fallow fix --dry-run --format json --quiet || true
   ```

2. Review what would change.
3. Apply only after the preview matches the intended cleanup:

   ```bash
   fallow fix --yes --format json --quiet || true
   ```

4. Re-run dead-code analysis to confirm the cleanup landed as expected.

## Baseline adoption for noisy repos

When the repo already has a lot of findings and the goal is "block new issues, not all historical ones":

```bash
fallow dead-code --format json --quiet --save-baseline fallow-baselines/dead-code.json || true
fallow dead-code --format json --quiet --baseline fallow-baselines/dead-code.json --fail-on-issues || true
```

The same pattern works for duplication baselines with `fallow dupes`.

## Monorepo-focused analysis

Use a workspace name or pattern when you only want findings reported for part of a monorepo:

```bash
fallow dead-code --format json --quiet --workspace web || true
fallow dead-code --format json --quiet --workspace 'apps/*' || true
```

Use changed workspaces when the scope should follow the diff automatically:

```bash
fallow dead-code --format json --quiet --changed-workspaces origin/main || true
```

## GitHub Actions starter step

For a simple changed-file dead-code gate in Actions:

```yaml
- name: Fallow dead-code check
  run: npx fallow dead-code --format json --quiet --changed-since "${{ github.event.pull_request.base.sha }}" --fail-on-issues
```

For a local skill workflow, keep the JSON output if you need to summarize findings in chat; otherwise a human-facing CI step can omit JSON and let the tool format its own report.
