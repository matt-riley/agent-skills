# AWS SDK v2 → v3 service mappings

Quick-reference table for the most common v2 patterns and their v3 equivalents.
Use this alongside the main workflow — it is not exhaustive.

## Package renames

| v2 import | v3 client package | v3 utility packages (if any) |
|-----------|-------------------|------------------------------|
| `aws-sdk` (whole SDK) | Install only the packages you need | — |
| `aws-sdk/clients/s3` | `@aws-sdk/client-s3` | `@aws-sdk/lib-storage` (multipart), `@aws-sdk/s3-request-presigner` |
| `aws-sdk/clients/dynamodb` | `@aws-sdk/client-dynamodb` | `@aws-sdk/lib-dynamodb` (DocumentClient equivalent) |
| `aws-sdk/clients/sqs` | `@aws-sdk/client-sqs` | — |
| `aws-sdk/clients/sns` | `@aws-sdk/client-sns` | — |
| `aws-sdk/clients/sts` | `@aws-sdk/client-sts` | — |
| `aws-sdk/clients/lambda` | `@aws-sdk/client-lambda` | — |
| `aws-sdk/clients/secretsmanager` | `@aws-sdk/client-secrets-manager` | — |
| `aws-sdk/clients/ssm` | `@aws-sdk/client-ssm` | — |
| `aws-sdk/clients/cloudwatch` | `@aws-sdk/client-cloudwatch` | — |
| `aws-sdk/clients/cloudwatchlogs` | `@aws-sdk/client-cloudwatch-logs` | — |
| `aws-sdk/clients/eventbridge` | `@aws-sdk/client-eventbridge` | — |
| `aws-sdk/clients/kinesis` | `@aws-sdk/client-kinesis` | — |
| `aws-sdk/clients/kms` | `@aws-sdk/client-kms` | — |
| `aws-sdk/clients/iam` | `@aws-sdk/client-iam` | — |
| `aws-sdk/clients/ecr` | `@aws-sdk/client-ecr` | — |
| `aws-sdk/clients/ecs` | `@aws-sdk/client-ecs` | — |
| `aws-sdk/clients/codepipeline` | `@aws-sdk/client-codepipeline` | — |
| `aws-sdk/clients/cognitoidentityserviceprovider` | `@aws-sdk/client-cognito-identity-provider` | — |

## Client construction

```ts
// v2
import AWS from 'aws-sdk';
const s3 = new AWS.S3({ region: 'us-east-1' });

// v3
import { S3Client } from '@aws-sdk/client-s3';
const s3 = new S3Client({ region: 'us-east-1' });
```

Configuration keys are largely the same (`region`, `credentials`, `endpoint`, `maxAttempts`).
`httpOptions.timeout` becomes `requestHandler` with a configured timeout in v3.

## Calling API methods

```ts
// v2 — callback style
s3.getObject({ Bucket, Key }, (err, data) => { ... });

// v2 — promise style
const data = await s3.getObject({ Bucket, Key }).promise();

// v3 — always explicit command
import { GetObjectCommand } from '@aws-sdk/client-s3';
const data = await s3.send(new GetObjectCommand({ Bucket, Key }));
```

## Pagination

```ts
// v2
s3.listObjectsV2({ Bucket }, callback);

// v3 — use the paginator helper
import { paginateListObjectsV2 } from '@aws-sdk/client-s3';
for await (const page of paginateListObjectsV2({ client: s3 }, { Bucket })) {
  console.log(page.Contents);
}
```

## DynamoDB DocumentClient

```ts
// v2
import { DynamoDB } from 'aws-sdk';
const doc = new DynamoDB.DocumentClient();
await doc.get({ TableName, Key }).promise();

// v3
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';
const raw = new DynamoDBClient({});
const doc = DynamoDBDocumentClient.from(raw);
await doc.send(new GetCommand({ TableName, Key }));
```

## S3 streaming response body

```ts
// v2 — Body is a Buffer or readable stream
const { Body } = await s3.getObject({ Bucket, Key }).promise();

// v3 — Body is a ReadableStream (Node.js: Readable, browser: Web ReadableStream)
import { GetObjectCommand } from '@aws-sdk/client-s3';
const { Body } = await s3.send(new GetObjectCommand({ Bucket, Key }));
const text = await Body.transformToString(); // helper available in v3
```

## S3 multipart / managed uploads

```ts
// v2
await s3.upload({ Bucket, Key, Body }).promise();

// v3
import { Upload } from '@aws-sdk/lib-storage';
await new Upload({ client: s3, params: { Bucket, Key, Body } }).done();
```

## Error handling

v3 errors carry `$metadata.httpStatusCode` and a typed `name` field.
Catch with `instanceof` checks against the imported error class:

```ts
import { NoSuchKey } from '@aws-sdk/client-s3';
try {
  await s3.send(new GetObjectCommand({ Bucket, Key }));
} catch (err) {
  if (err instanceof NoSuchKey) { ... }
}
```

v2's `err.code` string checks should become `err instanceof SpecificErrorClass` or
`err.name === 'SpecificErrorName'` checks in v3.

## Credentials and config

```ts
// v2 — global config
AWS.config.update({ region: 'us-east-1' });

// v3 — per-client; no global state
const client = new S3Client({ region: 'us-east-1' });
```

Custom credential providers use `@aws-sdk/credential-providers`
(e.g., `fromIni`, `fromEnv`, `fromInstanceMetadata`).
