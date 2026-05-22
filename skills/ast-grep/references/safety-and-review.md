# ast-grep safety and review

Use this checklist around rewrite work to avoid accidental broad edits.

## Preview-before-apply checklist

1. Confirm mode (`search` vs `rewrite`) and expected target shape.
2. Confirm explicit `--lang` and narrow path scope.
3. Run search preview and inspect representative matches.
4. Validate exclusions (generated/vendor/build surfaces).
5. Only then run rewrite.

## Diff review checklist

1. Confirm changed files are in expected directories only.
2. Spot-check multiple edits for semantic correctness.
3. Check for formatting churn unrelated to the structural change.
4. Confirm no accidental rewrites in tests or fixtures unless intended.

## Rollback and retry

If rewrite output is wrong or noisy:

1. Revert current rewrite changes.
2. Tighten pattern and/or scope.
3. Re-run preview.
4. Re-apply rewrite only after preview aligns with intent.

## Common failure modes

| Failure mode | Likely cause | Corrective action |
| --- | --- | --- |
| Too many files changed | Pattern too broad or scope too wide | Narrow `--lang`, path, and `--glob` before retry |
| No matches returned | Pattern mismatch or language mismatch | Verify pattern placeholders and parser language |
| Partially correct rewrites | Inline replacement too simplistic | Move to rule-file mode for richer matching |
| Repeated cleanup passes needed | Rewrite introduces secondary matches | Stage rewrites in smaller passes with review gates |
