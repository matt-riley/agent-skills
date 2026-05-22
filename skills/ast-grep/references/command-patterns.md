# ast-grep command patterns

Use these templates to keep `ast-grep` usage scoped, reviewable, and portable.

## Search mode (read-only)

### Minimal scoped search

```bash
ast-grep --pattern '<PATTERN>' --lang <LANG> <PATH>
```

Example:

```bash
ast-grep --pattern 'console.log($X)' --lang ts src/
```

### Search with file globs

```bash
ast-grep --pattern '<PATTERN>' --lang <LANG> --glob '<GLOB>' <PATH>
```

Example:

```bash
ast-grep --pattern 'new Promise(($RESOLVE, $REJECT) => $BODY)' --lang ts --glob '**/*.ts' src/
```

### Search as JSON output

```bash
ast-grep --pattern '<PATTERN>' --lang <LANG> --json <PATH>
```

Use this when downstream tooling needs structured match data.

## Rewrite mode (mutation)

### Inline rewrite template

```bash
ast-grep --pattern '<PATTERN>' --rewrite '<REWRITE>' --lang <LANG> --glob '<GLOB>' <PATH>
```

Example:

```bash
ast-grep --pattern 'oldFn($A)' --rewrite 'newFn($A)' --lang ts --glob '**/*.ts' src/
```

### Rule-file rewrite template

```bash
ast-grep scan --rule <RULE_FILE> <PATH>
```

Use this when rewrite or lint logic is too complex for inline replacement.

## Scope controls

- Always set `--lang` explicitly for rewrites and rule-file scans.
- Prefer the narrowest path first, then widen.
- Add `--glob` include filters before excluding by convention.

## Exclusions

Common exclusion targets for codemods:

- generated output directories
- vendored third-party code
- build artifacts

Apply scope at the command level instead of relying on post-hoc diff filtering.
