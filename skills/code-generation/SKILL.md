---
name: code-generation
description: Run and troubleshoot project code generation after detecting the repository's
  generator contract. Use when changing schema/query/template inputs that feed a generator,
  or before building/testing if generated output might be stale.
license: Proprietary
compatibility: Agent Skills-compatible coding agents with file and shell tools; assumes bash, git, make, go, and project-specific
  generator CLIs such as sqlc or templ.
metadata:
  owner: mattriley
  version: 1.1.0
  maturity: draft
---

## Use this skill when

- The task changes generator inputs such as SQL, proto, OpenAPI, templates, or generator config.
- Build/test output points at stale generated packages, missing generated types, or outdated artifacts.
- You need to verify whether generated output should be refreshed, checked in, or left to CI/runtime generation.

## Do not use this skill when

- The request is to design a schema/spec/template format from scratch rather than run the repo's generator workflow.
- The task is a generic explanation of code generation.
- The failing area has no generator-backed inputs and no stale-generation symptoms.

## Inputs to gather

- Which generators the repo uses and what inputs feed them.
- The canonical generation command(s): wrapper target, script, or direct CLI.
- Repo contract for outputs:
  - generated files committed to Git
  - generated locally for validation but ignored in Git
  - regenerated in CI/runtime from source inputs
- Validation path: diff check, `check-generated` script, build/test target, or CI job.

## First move

Inspect the repo's build docs, CI workflow, and `.gitignore` before regenerating or committing anything. Detect whether generated output is checked in, ignored, or only rebuilt in CI/runtime.

## Workflow

1. Identify the real generation entrypoints.
   - Prefer repo wrappers such as `make generate`, `task generate`, or checked-in scripts.
   - If wrappers are absent, locate the exact generator command for each tool (`sqlc generate`, `templ generate`, `buf generate`, `protoc`, etc.).

2. Regenerate only when it matches the repo contract.
   - Run generation after changing generator-backed inputs or when failures point to stale output.
   - If the repo uses multiple generators, run only the affected ones unless the wrapper target is the canonical path.

3. Branch on output handling.
   - **Committed output:** regenerate, inspect the diff, and keep the generated changes with the source changes.
   - **Ignored or CI-only output:** regenerate locally when needed for validation, but do not commit ignored artifacts unless the repo explicitly expects snapshots.
   - **Mixed repos:** follow per-generator rules; some outputs may be committed while others are ephemeral.

4. If tooling is missing or behaving differently, recover safely.
   - Install or invoke the pinned tool version the repo expects.
   - Check generator config, tool versions, and source inputs before blaming generated files.

5. Run the repo's follow-on checks.
   - Use the repo's diff or cleanliness check for generated files.
   - Build/test the affected area after generation succeeds.

## Guardrails

- Never edit generated files by hand; change the generator inputs or config instead.
- Do not assume `make generate` exists or that one command covers every generator in the repo.
- Do not assume generated output belongs in Git; check `.gitignore`, CI, and repo docs first.
- If no generator-backed inputs changed, do not force regeneration as the first move unless the failure clearly points to stale output.
- Unexpected generated diffs usually mean changed inputs, config drift, or tool-version drift; inspect those before patching outputs.

## Verification

- The relevant generation command completes successfully.
- The diff or status matches the repo contract:
  - expected generated files changed and are ready to commit, or
  - ignored/ephemeral output was verified locally without being staged accidentally.
- Follow-on build/test/check-generated steps pass.

## Support files

- Read `references/examples.md` when you need examples of stale-generation diagnosis or "regenerate before test" prompts.
- Read `references/edge-cases.md` when the repo's committed-vs-ephemeral generation contract is unclear.
- Run `scripts/check-generated.sh --help` when you need a deterministic generation + diff check for committed-output workflows.
