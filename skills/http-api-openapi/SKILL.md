---
name: http-api-openapi
description: "Keep OpenAPI contracts in sync with HTTP behavior. Use when you need to update spec files, code annotations, or both after changing endpoints, schemas, auth, or error shapes — not for writing or running integration tests."
license: GNU GPL v3
metadata:
  version: 1.3.0 # x-release-please-version
  owner: mattriley
  maturity: stable
  kind: task
---

## Use this skill when

- The task adds or changes a public HTTP endpoint and the OpenAPI contract must stay aligned.
- Request/response schemas, status codes, auth requirements, or documented errors are changing together.
- Code and API contract have drifted and the repo needs the correct sync workflow.

## Do not use this skill when

- The request is a generic REST/OpenAPI tutorial.
- The task is only to generate a client SDK from an existing spec with no server-contract change.
- The change is internal-only code with no HTTP contract or no OpenAPI surface in play.

## Inputs to gather

- Where the API contract lives:
  - hand-authored spec files
  - code annotations/types/routes that generate the spec
  - a hybrid flow that updates both
- Validation/generation commands for the repo (`make validate-openapi`, `swagger-cli`, codegen targets, etc.).
- The exact endpoint surface being changed: path, method, auth, request body, success responses, error responses.
- Whether the endpoint is public/external, internal-only, or intentionally undocumented.

## First move

Determine the repo's contract flow before editing anything: spec-first, code-first, or hybrid. Do not assume `openapi.yaml` is the source of truth or that it should be hand-edited.

## Workflow

1. Identify the contract owner.
   - Read the repo docs, build targets, and generation tooling to see whether the spec is hand-maintained, generated from code, or maintained in both places.

2. Follow the repo's contract path.
   - **Spec-first repos:** update the OpenAPI contract first, validate it, then implement handlers/middleware/tests to match.
   - **Code-first repos:** update the handler/types/annotations first, regenerate the spec/artifacts, then verify the generated contract matches the intended behavior.
   - **Hybrid repos:** update both authored surfaces in the order the repo expects, then run validation/generation to reconcile them.

3. Verify the behavior-contract alignment.
   - Match auth requirements, request validation, response schemas, status codes, and documented error shapes.
   - Confirm the changed endpoint is included or intentionally excluded from the OpenAPI surface.

4. Run the repo's API checks.
   - Validate the spec when the repo has a validator.
   - Run the relevant integration/unit/contract tests for the changed surface.

## Outputs

- Updated contract-owner artifacts for the changed API surface, including spec, handler/type inputs, and any generated OpenAPI output the repo expects.
- A documented behavior-to-contract alignment for auth requirements, request validation, response schemas, status codes, and error shapes.
- Spec validation, generation, and/or API test evidence confirming the handler behavior and OpenAPI contract stay in sync.


## Workflow

See the body and references for OpenAPI/handler sync steps.

## Examples

See references and the skill body for http-api-openapi examples.

## Reference files

See the references/ directory and linked files in the main content.

## Guardrails

- Do not hand-edit generated OpenAPI output in code-first repos; change the source inputs that own it.
- Do not change public endpoint behavior without the matching contract update or regeneration.
- Auth requirements, status codes, and error shapes must align with the contract owner the repo actually uses.
- If the repo has no OpenAPI contract for this surface, do not invent one unless the user asks for that design decision; document the gap instead.
- When handler changes also affect generated clients/server stubs, coordinate with the code-generation workflow rather than patching generated artifacts directly.

## Validation

- The repo's spec validation or generation step succeeds.
- Handler behavior, tests, and contract artifacts agree on auth, schemas, and status codes.
- Any generated contract files or checked-in specs show only the expected diff.

## Support files

- Read `references/examples.md` when you need examples of drift repair or endpoint changes that must keep contract and implementation aligned.
- Read `references/edge-cases.md` when the repo lacks a spec, uses generated specs, or the request may really be SDK generation or a non-HTTP change.
