# Replacement patterns

Use these patterns when replacing `any` so the new type matches real usage instead of only satisfying the compiler.

## 1. Reuse an existing shared type first

Prefer an existing domain type, DTO, schema-derived type, or helper type when one already models the value.

**Before**

```ts
function sendUser(user: any) {
  return api.post("/users", user);
}
```

**After**

```ts
function sendUser(user: UserPayload) {
  return api.post("/users", user);
}
```

Use this when a shared type already exists and the value is not an untrusted boundary.

## 2. Replace `any` with a constrained generic

Use a generic when the function shape is reusable and the return type should follow the input type.

**Before**

```ts
function getProperty(obj: any, key: string): any {
  return obj[key];
}
```

**After**

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

Use this when the caller supplies the structure and the function should preserve that structure.

## 3. Use `unknown` plus a guard at an untrusted boundary

Use `unknown` when the data shape is not trustworthy at the boundary, then narrow it before use.

**Before**

```ts
async function fetchUser(): Promise<any> {
  const res = await fetch("/api/user");
  return res.json();
}
```

**After**

```ts
interface User {
  id: number;
  name: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

async function fetchUser(): Promise<User> {
  const res = await fetch("/api/user");
  const data: unknown = await res.json();
  if (!isUser(data)) {
    throw new Error("Invalid user shape");
  }
  return data;
}
```

Use this when runtime validation is required to make the new type truthful.

## 4. Prefer a discriminated union over a permissive catch-all

Use an explicit union when the value can be one of a small number of known states.

**Before**

```ts
type Result = any;
```

**After**

```ts
type Result =
  | { status: "ok"; data: Payload }
  | { status: "error"; message: string };
```

Use this when the runtime shape already follows named states or status fields.

## 5. Use `Record` only when the key and value space are actually open

`Record<string, unknown>` is better than `Record<string, any>`, but it is still too vague when the key set or value types are known.

**Before**

```ts
type Metadata = Record<string, any>;
```

**After**

```ts
type Metadata = {
  requestId: string;
  retryable: boolean;
  source?: "cache" | "origin";
};
```

Use `Record<string, unknown>` only when the shape is genuinely open-ended and consumers narrow values before use.
