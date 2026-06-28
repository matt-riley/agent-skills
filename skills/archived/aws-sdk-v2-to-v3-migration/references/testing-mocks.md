# AWS SDK v3 testing and mock patterns

How to replace v2 mock patterns with v3 equivalents. Covers the most common approaches.

## Why mocking changes

v2 clients expose chainable `.promise()` methods on the class prototype, making
`jest.spyOn` and `aws-sdk-mock` straightforward. v3 clients use a `send(command)`
dispatch model, so mocking targets either the `send` method or specific command
handlers via `@aws-sdk/client-mock`.

---

## Option A — `@aws-sdk/client-mock` (preferred)

Install once per project:

```
npm install --save-dev @aws-sdk/client-mock @aws-sdk/client-mock-jest
```

### Basic pattern

```ts
import { mockClient } from '@aws-sdk/client-mock';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import '@aws-sdk/client-mock-jest'; // adds .toHaveReceivedCommand() etc.

const s3Mock = mockClient(S3Client);

beforeEach(() => s3Mock.reset());

it('returns the object', async () => {
  s3Mock.on(GetObjectCommand).resolves({ Body: 'hello' });
  const result = await myFunction(); // internally calls s3.send(new GetObjectCommand(...))
  expect(s3Mock).toHaveReceivedCommand(GetObjectCommand);
});
```

### Matching specific input shapes

```ts
s3Mock
  .on(GetObjectCommand, { Bucket: 'my-bucket', Key: 'my-key' })
  .resolves({ Body: 'expected content' });
```

### Simulating errors

```ts
import { NoSuchKey } from '@aws-sdk/client-s3';

s3Mock.on(GetObjectCommand).rejects(
  Object.assign(new NoSuchKey({ message: 'not found', $metadata: {} }), {
    name: 'NoSuchKey',
  })
);
```

---

## Option B — `jest.spyOn` on `send`

When you cannot add `@aws-sdk/client-mock` or need a quick inline mock:

```ts
import { S3Client } from '@aws-sdk/client-s3';

jest.spyOn(S3Client.prototype, 'send').mockResolvedValueOnce({ Body: 'hello' });
```

Limitations: does not distinguish between command types; harder to assert on input.

---

## Option C — dependency injection

Pass the client as a constructor or function argument and substitute a fake in tests:

```ts
// production code
export async function getObject(client: S3Client, bucket: string, key: string) {
  return client.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
}

// test
const fakeClient = { send: jest.fn().mockResolvedValue({ Body: 'hello' }) } as unknown as S3Client;
await getObject(fakeClient, 'b', 'k');
expect(fakeClient.send).toHaveBeenCalledWith(expect.any(GetObjectCommand));
```

---

## Replacing `aws-sdk-mock`

| v2 pattern (`aws-sdk-mock`) | v3 equivalent |
|-----------------------------|---------------|
| `AWSMock.mock('S3', 'getObject', fn)` | `s3Mock.on(GetObjectCommand).resolves(...)` |
| `AWSMock.restore('S3')` | `s3Mock.reset()` |
| `AWSMock.setSDKInstance(AWS)` | Not needed |

---

## DynamoDB DocumentClient mocks

```ts
import { mockClient } from '@aws-sdk/client-mock';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

const ddbMock = mockClient(DynamoDBDocumentClient);

beforeEach(() => ddbMock.reset());

it('fetches item', async () => {
  ddbMock.on(GetCommand).resolves({ Item: { id: '1', name: 'test' } });
  const item = await myRepo.findById('1');
  expect(item.name).toBe('test');
});
```

---

## Common pitfalls

- **Forget to `reset()`** — stale mock responses bleed across tests. Always call
  `mock.reset()` in `beforeEach`.
- **Wrong client instance** — `mockClient` patches the client class, not an instance.
  If your module creates a new client internally, the mock still applies; if it
  imports a shared singleton, mock the same client object.
- **Stream body** — when mocking `GetObjectCommand` for S3, `Body` in v3 is a
  `Readable` stream. Return a real `Readable` or use `sdkStreamMixin` from
  `@aws-sdk/util-stream` if your code calls `.transformToString()` or pipes the body.
- **`$metadata`** — some code checks `$metadata.httpStatusCode`. Include it in
  mock responses when your code reads it.
