---
name: mocha-to-jest-migration
description: "Use when a JavaScript or TypeScript suite still depends on Mocha, Chai, or Sinon and needs an incremental Jest migration."
license: GNU GPL v3
metadata:
  version: 1.0.0 # x-release-please-version
  category: migrations
  audience: general-coding-agent
  maturity: draft
  kind: task
---

# Mocha to Jest migration

## Use this skill when

- The suite still uses Mocha, Chai, or Sinon and needs a staged migration to Jest.
- You find `describe`/`it` tests using Chai assertions or Sinon stubs that need Jest equivalents.
- The work includes runner config, setup files, fake timers, spies, or snapshots.

## Do not use this skill when

- The test suite already uses Jest — the task is not a migration.
- The ask is to add new tests to an existing Mocha suite without converting it.

## Inputs to gather

**Required before editing**
- The existing Mocha, Chai, and Sinon versions and test bootstrap configuration.
- The repository's current or planned Jest configuration and conventions.

**Helpful if present**
- Any test utilities, global setup, environment assumptions, or module mocking patterns.
- The subset of tests to migrate first and the commands used to run them.

**Only investigate if encountered**
- Non-standard Chai plugins (e.g., `chai-as-promised`, `chai-http`) that need separate handling.

## First move

Inventory what needs to migrate before touching any test files:

```sh
grep -r "require('chai')\|from 'chai'\|require('sinon')\|from 'sinon'" --include="*.ts" --include="*.js" -l
grep -r "require('mocha')\|\.mocharc" --include="*.ts" --include="*.js" --include="*.json" -l
```

Then convert a **single small representative file** first, run it under Jest, and confirm the project's Jest setup works before migrating more files.
Consult [`references/assertion-mapping.md`](references/assertion-mapping.md) and [`references/mock-mapping.md`](references/mock-mapping.md) before rewriting patterns.

## Workflow

1. Identify all Mocha, Chai, and Sinon patterns in use.
2. Convert a small representative file first and verify the project's Jest setup.
3. Replace assertion styles with idiomatic Jest expectations using the assertion mapping reference.
4. Replace mocks, spies, and stubs with Jest equivalents using the mock mapping reference.
5. Convert shared setup and teardown patterns carefully (`before`/`after` → `beforeAll`/`afterAll`, `beforeEach`/`afterEach` stay the same).
6. Update test utilities, config, or setup files only where required for parity.
7. Migrate incrementally and run the relevant tests after each batch.

## Worked migration slice

Use this as the shape for one end-to-end file before scaling out:

```js
// Mocha + Chai + Sinon
describe("retries", () => {
  let clock;

  beforeEach(() => {
    clock = sinon.useFakeTimers();
  });

  afterEach(() => {
    clock.restore();
    sinon.restore();
  });

  it("waits and retries once", async () => {
    const request = sinon.stub(api, "request").rejects(new Error("nope"));
    const retry = sinon.stub(api, "retry").resolves({ ok: true });

    const run = service.run();
    await clock.tickAsync(1000);
    await run;

    expect(request.calledOnce).to.equal(true);
    expect(retry.calledOnce).to.equal(true);
    expect(retry.firstCall.args[0]).to.deep.equal({ delay: 1000 });
  });
});
```

```js
// Jest
describe("retries", () => {
  beforeEach(() => {
    jest.useFakeTimers();
    jest.spyOn(api, "request").mockRejectedValue(new Error("nope"));
    jest.spyOn(api, "retry").mockResolvedValue({ ok: true });
  });

  afterEach(() => {
    jest.useRealTimers();
    jest.restoreAllMocks();
  });

  it("waits and retries once", async () => {
    const run = service.run();
    await jest.advanceTimersByTimeAsync(1000);
    await run;

    expect(api.request).toHaveBeenCalledTimes(1);
    expect(api.retry).toHaveBeenCalledTimes(1);
    expect(api.retry).toHaveBeenCalledWith({ delay: 1000 });
  });
});
```

## Outputs

- Test files and config updated to Jest (imports, lifecycle, matchers, runners).
- Evidence that the suite runs under Jest with equivalent or improved coverage.

## Guardrails

- **Must** preserve async behavior, timer behavior, and module mocking semantics explicitly.
- **Must not** do bulk mechanical rewrites without validation — migrate in small batches.
- **Should** keep test names and intent stable unless the user asks for broader cleanup.
- **Should** watch for memory or environment differences in CI after migration.
- **Red flag:** if the first converted file needs new Jest setup, treat that as the migration gate and stop before touching the rest of the suite.
- **Handoff trigger:** if the migration exposes a broader runner/config problem, route that follow-up into the repository's Jest setup work instead of burying it in the test rewrite.

## Validation

- Run the migrated Jest tests after each batch using the repository's existing commands.
- Confirm fake timers, async failures, setup hooks, and mock reset behavior still match intent.
- Check CI behavior if the migration changes test environment defaults or coverage collection.

- Smoke test:
  - should trigger: "Migrate this Mocha + Sinon test file to Jest without changing behavior."
  - should not trigger: "Add a new test to our existing Jest suite for this parser." (→ `test-driven-development`)

## Examples

- "Convert `user.spec.ts` from `sinon.stub(api, 'fetch')` and `expect(value).to.equal(...)` to `jest.spyOn(api, 'fetch')` and `expect(value).toBe(...)`."
- "Migrate our Sinon-heavy unit tests to Jest mocks and keep the shared setup and fake timers behaving the same."
- "Help me finish converting our Mocha suite to Jest — some files are already done and need the same runner setup."

## Reference files

- [`references/assertion-mapping.md`](references/assertion-mapping.md) — Chai BDD and assert-style assertions mapped to Jest matchers.
- [`references/mock-mapping.md`](references/mock-mapping.md) — Sinon spies, stubs, mocks, fake timers, and sandbox patterns mapped to Jest equivalents.
