---
name: code-intelligence
description: "Use when navigating or refactoring code — choosing between LSP, rg, or semantic search tools; an LSP call returns empty and you need to know if it failed; or a tool substitution needs disclosure."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: workflow
  audience: general-coding-agent
  maturity: draft
  kind: reference
---

# Code Intelligence

Pick the search tool by task, not by habit. Generic and language-agnostic —
domain skills may extend it with server capability matrices and ecosystem
prerequisites. This is model-triggered guidance, not enforcement.

## Use this skill when

- Navigating code: finding definitions, references, callers, or rename impact
- Choosing between LSP, `rg`, `grep`, or semantic search for a specific task
- An LSP call returns empty and you are unsure whether it represents failure or a degraded workspace
- A tool substitution or omission needs to be disclosed to the reader
- Verifying a tool is genuinely missing before falling back

## Do not use this skill when

- The task is pure text search for a known literal with no symbol-scope concern — use `rg` directly
- You are building a structural rewrite or codemod — use the `ast-grep` skill
- You need a pre-edit map of all files involved in a change — use the `context-map` skill

## Inputs to gather

**Required before querying**

- The symbol, file, or workspace to investigate.
- The LSP language (TypeScript, Go, Lua, Terraform, or YAML).

**Helpful if present**

- Whether a language server is available for the target file type.

## First move

1. Check that an LSP server is available for the target language.
2. Prefer LSP operations (goToDefinition, findReferences) over grep when available.
3. Fall back to grep/glob when no language server supports the file type.

## Routing boundary

| Situation | Use this skill? | Route instead |
|-----------|----------------|---------------|
| Navigating to a symbol definition or finding all references | Yes | — |
| Counting occurrences of an exact string | No | `rg` directly |
| Syntax-aware structural search or codemod | No | `ast-grep` |
| Mapping all files and tests before a broad edit | No | `context-map` |
| Terraform-specific LSP (terraform-ls) capability matrix | Partial | Defer ecosystem-specific setup to infrastructure skills |

## Tool Precedence

| Goal | Use | Tradeoff |
|------|-----|----------|
| Symbol relationships (definition, references, call sites, rename safety) | Language server (LSP) at a `file:line:character` position | Needs a running server + indexed workspace |
| Exact text, known name, exhaustive enumeration, config/value files | `rg` then Read | No semantic scope; matches strings in comments too |
| Conceptual / fuzzy / "where might this live" / cross-repo discovery | Semantic/neural search tool (if the host provides one) | Not exact; never use for counts or completeness claims |

Detail: [references/tool-precedence.md](references/tool-precedence.md#precedence-table)

## Calling the LSP

- **DO** call at a position (`file:line:character`). Anchor the position with a text search first.
- **DON'T** pass a bare symbol name and expect resolution — empty result = usage defect, not server failure.
- **DO** Read the returned locations for source text; LSP returns positions, not lines.
- **DO** retry once on cold start (server may be indexing).
- **DO** prefer the server's own `rename`/`prepareRename` for renames; call hierarchy for callers.
- **DON'T** report an unsupported operation as a finding — redirect instead.

Detail: [references/lsp-calls.md](references/lsp-calls.md#position-anchoring)

## Degradation Gate

Two cases before declaring LSP unavailable:

- **No LSP at all** (no tool exposed, server won't start) → genuine unavailability. Disclose on line 1 and use text search. Gate does not apply.
- **LSP callable but position-anchored call returns empty** → run all three checks before falling back:
  1. `documentSymbol` on an in-scope file returns symbols → server is responsive
  2. The failing call was position-anchored, not symbol-name-only
  3. That anchored call still returned empty after a cold-start retry

Only after all three pass is a disclosed text fallback warranted.

Detail: [references/degradation-and-disclosure.md](references/degradation-and-disclosure.md#degradation-gate)

## Disclose Substitutions

State any tool substitution or omission on the **first line** of the response:

```
Intended: <tool>. Actual: <tool>. Reason: <why>. Impact: <completeness/confidence>.
```

## Do Not Invent a Missing Tool

Before claiming a tool is shimmed, aliased, or absent, prove it:
`type -a <tool>`, `ls -l <resolved-path>`, `<tool> --version`. An unproven claim followed by a fallback is a verification failure, not a sanctioned substitution.

Detail: [references/degradation-and-disclosure.md](references/degradation-and-disclosure.md#anti-phantom-shim-proof)

## Workflow

See the body and references for LSP/grep routing and code intelligence steps.

## Guardrails

- **Must not** invent symbol definitions or call relationships not found by a tool.
- **Should** prefer code intelligence tools over text search for semantic queries.
- **Should** disclose when falling back from LSP to grep/glob and why.
- **Should** not claim a symbol is unused unless a language server confirms no references.

## Validation

**Should trigger this skill:**
- "Find all callers of `parseConfig` in the Go codebase"
- "Rename `UserSession` everywhere it's used safely"
- "LSP returned empty — is the server down?"
- "Which tool should I use to find where rate-limiting is implemented?"

**Should NOT trigger this skill:**
- "Count how many times `TODO` appears in this repo" → `rg 'TODO' | wc -l`
- "Show me the file tree for this module" → `glob` / `find`
- "Before I edit auth, map all the related files" → `context-map`

## Examples

Apply the three-tier tool-selection discipline and degradation gate in practice.

### Example 1 — Finding callers of a function

Task: "Find all callers of `validateToken` in the TypeScript service"

1. `rg -n 'validateToken'` → get a line/column position (e.g. `src/auth.ts:42:10`)
2. LSP `incomingCalls` at `src/auth.ts:42:10`
3. Read each returned caller location for source context

### Example 2 — LSP returns empty, applying the gate

Task: LSP `findReferences` at a known position returns `[]`

1. Run `documentSymbol` on any `.ts` file → receives a symbol list → server is responsive ✓
2. Confirm the failing call used `file:line:character` (not a bare name) ✓
3. Retry the call once after a short pause → still empty ✓
4. All three pass → disclosed text fallback is warranted:
   `Intended: findReferences (LSP). Actual: rg. Reason: position-anchored LSP call returned empty on responsive server after retry. Impact: text matches only, may include comments and strings.`

## Reference files


| [`PROVENANCE.md`](PROVENANCE.md) | Skill provenance, changelog, and authorship |
- [references/tool-precedence.md](references/tool-precedence.md) — Full precedence table with 7 task rows; when LSP is wrong; semantic search scope limits
- [references/lsp-calls.md](references/lsp-calls.md) — Position anchoring detail; cold-start/retry; unsupported operations; reading results (offset drift warning)
- [references/degradation-and-disclosure.md](references/degradation-and-disclosure.md) — Gate algorithm in full; disclosure format; anti-phantom-shim proof procedure
