# Agent Skills Catalog Remediation Design

## Goal

Resolve every actionable issue found in the 2026-07-13 catalog audit so the active skill catalog is reproducibly valid, internally consistent, discoverable across supported harnesses, and efficient to load.

## Scope

The remediation covers four connected areas:

1. Make the documented validation entry point work from a fresh checkout with repository-declared dependencies.
2. Reconcile the Python and JavaScript validators around one canonical authoring contract, including valid multiline YAML, optional headings, inter-skill references, and `compatibility` metadata.
3. Repair catalog drift in Codex metadata, chooser routing, Release Please paths, and broken support links.
4. Reduce context cost in oversized skills and normalize trigger descriptions and section structure without changing their intended operational behavior.

The work does not add new skill domains, redesign unrelated workflows, or casually bump skill versions. Release metadata changes are limited to correcting archived package paths and any updates mechanically required by the repository's existing release contract.

## Architecture

The catalog will have one documented authoring contract, expressed in the authoring guidance and enforced consistently by both validators. The validators may retain different implementation languages and levels of strictness, but they must agree on schema validity and must not reject locally supported constructs.

Repository-level catalog metadata remains derived from active skill directories:

- `skills/README.md` routes every active skill.
- Every active skill has `agents/openai.yaml`, matching the README's Codex metadata promise.
- Release Please files point at the actual package locations.
- Every local Markdown link resolves.

Large `SKILL.md` files retain activation, first action, workflow, guardrails, validation, and support-file routing. Lookup-heavy command tables, mode-specific procedures, and long examples move to directly linked, purpose-named files under `references/`.

## Workstreams

### Validation and authoring contract

- Declare the Python dependency needed by `_shared/validate-skills.py`, and document or script a reproducible installation path.
- Add regression coverage before changing validator behavior.
- Align accepted top-level metadata with the repository contract, including `compatibility`.
- Parse valid YAML rather than rejecting legal continuation indentation.
- Treat canonical headings as a recommended shape where the authoring standard says they are optional; enforce ordering only for headings that are present and semantically ordered.
- Distinguish support-file references from inter-skill routing links instead of treating either as an empty section.
- Consolidate contradictory description guidance into a single rule: descriptions identify purpose and concrete activation conditions but do not encode procedural workflow steps.

### Catalog metadata and routing

- Generate or repair `agents/openai.yaml` for every active skill using the local metadata conventions.
- Add `find-skills` and `graphify` to the active chooser with boundaries that avoid crowding out direct task skills.
- Update archived Release Please entries to their real filesystem paths, or remove them from release management if the existing configuration shows archived packages are intentionally excluded. Apply the same decision consistently to both release files.
- Remove or replace the broken root `copilot-instructions.md` link in `git-signing-troubleshoot` with a real repository-owned source.

### Skill content efficiency and consistency

- Split `graphify` and `agent-governance` so their main skill files provide a concise executable route and their detailed reference material is progressively disclosed.
- Review `agent-supply-chain` and split it only where doing so clearly lowers context cost without obscuring its workflow.
- Repair duplicated or out-of-order canonical sections identified by the stricter validator.
- Normalize descriptions that fail the canonical trigger contract, including `api-smoke-validation` and `modern-web-guidance`.
- Preserve existing examples, safety constraints, and operational commands unless they are duplicated, stale, or contradicted by the canonical contract.

### Integration and publication

- Use independent subagents for the validation, catalog-metadata, and skill-content workstreams.
- Review each workstream for scope compliance and code/content quality before integration.
- Run the primary validator, the detailed authoring validator, every active static trigger eval, and every active static functional eval.
- Confirm the worktree contains only remediation changes, commit them intentionally, and push the resulting commit or commits directly to `origin/main` as explicitly requested.

## Error Handling and Safety

- Existing user changes, if any appear, must not be overwritten or staged silently.
- Validator changes require regression fixtures demonstrating both the former failure and the intended accepted behavior.
- If generating Codex metadata exposes an unresolved product-policy choice, preserve current invocation defaults and document the decision rather than inventing a new policy.
- If direct push is rejected by branch protection, report the exact rejection and stop rather than bypassing protection.
- No production services, external data, or live user accounts are involved.

## Verification

Completion requires fresh successful results from:

```bash
npm run validate
node skills/skill-authoring/scripts/validate-skill-library.mjs
```

Every active eval fixture must also pass its static runner:

```bash
python _shared/run-trigger-evals.py --static skills/<skill>/evals/trigger-queries.json
python _shared/run-functional-evals.py --static skills/<skill>/evals/evals.json
```

Additional assertions must verify:

- every active skill appears in `skills/README.md`
- every active skill contains `agents/openai.yaml`
- all Release Please paths resolve to real skill directories
- all Markdown links in active skills resolve
- oversized skill content has been moved, not silently discarded
- `git diff --check` reports no whitespace errors

## Success Criteria

- A fresh checkout has a documented, repository-owned route to install validation dependencies and run `npm run validate`.
- Both catalog validators pass and agree on the supported authoring contract.
- All active static eval fixtures pass.
- Catalog documentation, harness metadata, release metadata, and filesystem layout agree.
- The main skill files for the audited context outliers are materially smaller and retain direct links to all moved guidance.
- The complete reviewed remediation is committed and pushed to `origin/main`.
