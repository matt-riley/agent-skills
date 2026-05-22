# PR lifecycle commands

Use these commands as a compact sequence for branch-to-PR workflow in this skill.

## 1. Confirm branch + head SHA

```bash
git --no-pager rev-parse --abbrev-ref HEAD
git --no-pager rev-parse HEAD
```

## 2. Push branch if needed

```bash
git push -u origin <branch>
```

## 3. Create PR

```bash
gh pr create --base <base> --title "<title>" --body "<summary>"
```

## 4. Update PR metadata

```bash
gh pr edit <pr-number> --title "<title>" --body "<summary>"
```

## 5. Watch checks on current head

```bash
gh pr checks --watch
```

If explicit SHA scoping is needed:

```bash
gh run list --commit <head-sha>
```

## 6. Report status

Always include:

- PR URL or number
- head SHA used for status
- check outcome (`pass`, `fail`, `blocked`, `running`)
- route recommendation when handoff is required
