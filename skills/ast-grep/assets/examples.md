# ast-grep skill activation examples

## Should trigger

- `Use ast-grep to search for console.log($X) in src/ with --lang ts and report JSON output.`
- `Use ast-grep to rewrite obj.val && obj.val() to obj.val?.() in TypeScript, preview first.`
- `Use ast-grep to rewrite var code = $PAT to let code = $PAT in JavaScript after previewing matches.`
- `Use ast-grep to author a lint rule for deprecated API calls in lib/**/*.ts.`

## Should not trigger

- `Find the exact string "TODO: remove" in this repository.` (plain text search)
- `This unit test fails intermittently; help me diagnose root cause.` (debugging workflow)
- `Implement this new endpoint with TDD from failing test to green.` (TDD workflow)
- `My request is vague; rewrite it into a better implementation prompt.` (reverse-prompt workflow)
