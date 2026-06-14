---
name: aws-sdk-v2-to-v3-migration
description: "Use when the codebase still imports from 'aws-sdk' v2, uses new AWS.*() constructors, .promise() calls, AWS.config.update(), DocumentClient, or s3.upload() — and needs a safe modular v3 migration without changing runtime behavior."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: migrations
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# AWS SDK v2 to v3 migration

## Use this skill when

- The codebase still imports `aws-sdk` v2 clients or constructs them with `new AWS.*`.
- You see v2 patterns like `.promise()`, `AWS.config.update(...)`, `DocumentClient`, or `s3.upload(...)`.
- You need to move a service surface to the modular v3 packages without changing runtime behavior.
- The work includes updating tests, mocks, helpers, or wrappers tied to v2 client behavior.

## Do not use this skill when

- The codebase already uses `@aws-sdk/client-*` packages — it is already on v3.
- The task is about AWS infrastructure or CDK, not SDK client calls.

## Inputs to gather

**Required before editing**
- Which services are in use (S3, DynamoDB, SQS, STS, etc.).
- The module system in use (ESM, CJS) and whether TypeScript is involved.

**Helpful if present**
- Existing config sources for region, credentials, endpoints, retries, and timeouts.
- Custom wrappers, pagination helpers, stream handling, or document marshalling logic.

**Only investigate if encountered**
- Non-standard credential chain or custom endpoint configuration.

## First move

Inventory the v2 imports and service constructors before editing any files:

```sh
grep -r "require('aws-sdk')\|from 'aws-sdk'" --include="*.ts" --include="*.js" -l
grep -r "new AWS\." --include="*.ts" --include="*.js" -l
```

List the services found, then start with the smallest self-contained service surface.
Consult [`references/service-mappings.md`](references/service-mappings.md) for the
correct v3 package names and API shapes before writing any code.

## Workflow

1. Inventory all `aws-sdk` v2 imports and the services in use.
2. Group changes by service so imports and call sites stay coherent.
3. Pick the smallest self-contained service as the pilot and complete steps 4-9 for that service before widening to the next one.
4. Map each v2 client, helper, and API call to the v3 equivalent using the service mappings reference.
5. Install the required `@aws-sdk/client-<service>` packages (and any utility packages such as `@aws-sdk/lib-storage`).
6. Replace `new AWS.Service()` with the corresponding v3 client and explicit configuration.
7. Replace method calls with `client.send(new Command(...))`, preserving input shapes and response handling.
8. Update helpers, mocks, and tests to fit the v3 client-and-command model using the testing mocks reference.
9. Validate pagination, streaming, document marshalling, retries, and error handling where used.

## Outputs

- Migrated code using v3 clients/commands (no v2 .promise() or DocumentClient patterns left in changed paths).
- Tests or manual verification that the new shape works equivalently.

## Guardrails

- **Must** preserve region, credentials, endpoint, and retry configuration explicitly.
- **Must** not mix v2 and v3 patterns in the same migrated surface unless a staged migration plan exists.
- **Should** prefer incremental service-by-service migrations when the surface area is large.
- **Should** not replace typed wrappers with `unknown` or `any` shortcuts just to clear type errors.

## Validation

- Run the existing tests or targeted checks that cover the migrated services.
- Confirm no imports still pull from the v2 `aws-sdk` package on the migrated surface.
- Spot-check real behavior for pagination, streams, uploads, marshalling, and expected error types.

- Smoke test:
  - should trigger: "Replace new AWS.S3() and .promise() calls with AWS SDK v3."
  - should not trigger: "Change our Terraform S3 module to add versioning." (→ `terraform-skill`)

## Examples

- "Migrate a Lambda that does `const s3 = new AWS.S3()` and `s3.upload(...)` to `S3Client` plus `Upload` from `@aws-sdk/lib-storage`, then update the mocks."
- "Convert our DynamoDB document helper to AWS SDK v3 and keep the existing pagination and marshalling behavior."
- "I upgraded `aws-sdk` and now `new AWS.SQS()` is everywhere — help me finish the v3 migration safely."
- ```ts
  // v2
  const s3 = new AWS.S3({ region: 'us-east-1' });
  await s3.upload({ Bucket, Key, Body }).promise();

  // v3
  import { S3Client } from '@aws-sdk/client-s3';
  import { Upload } from '@aws-sdk/lib-storage';
  const s3 = new S3Client({ region: 'us-east-1' });
  await new Upload({ client: s3, params: { Bucket, Key, Body } }).done();
  ```

## Reference files

- [`references/service-mappings.md`](references/service-mappings.md) — v2→v3 package names, client construction, API call patterns, pagination, DynamoDB DocumentClient, streaming, and error handling.
- [`references/testing-mocks.md`](references/testing-mocks.md) — replacing v2 mock patterns with `@aws-sdk/client-mock`, `jest.spyOn`, or dependency injection.
