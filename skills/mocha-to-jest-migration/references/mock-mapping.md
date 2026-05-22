# Sinon → Jest mock mapping

Direct substitution table for the most common Sinon patterns.
Jest provides built-in equivalents for nearly everything; no extra library is needed.

## Spies

| Sinon | Jest |
|-------|------|
| `sinon.spy(obj, 'method')` | `jest.spyOn(obj, 'method')` |
| `sinon.spy(fn)` | `jest.fn()` (wrap the function) |
| `spy.callCount` | `spy.mock.calls.length` |
| `spy.calledOnce` | `expect(spy).toHaveBeenCalledTimes(1)` |
| `spy.calledWith(a, b)` | `expect(spy).toHaveBeenCalledWith(a, b)` |
| `spy.calledWithMatch(...)` | `expect(spy).toHaveBeenCalledWith(expect.objectContaining(...))` |
| `spy.firstCall.args` | `spy.mock.calls[0]` |
| `spy.lastCall.args` | `spy.mock.calls[spy.mock.calls.length - 1]` |
| `spy.returnValues[0]` | `spy.mock.results[0].value` |
| `spy.restore()` | `spy.mockRestore()` |

## Stubs

| Sinon | Jest |
|-------|------|
| `sinon.stub(obj, 'method')` | `jest.spyOn(obj, 'method').mockImplementation(...)` |
| `stub.returns(val)` | `.mockReturnValue(val)` |
| `stub.resolves(val)` | `.mockResolvedValue(val)` |
| `stub.rejects(err)` | `.mockRejectedValue(err)` |
| `stub.returnsThis()` | `.mockReturnThis()` |
| `stub.onFirstCall().returns(a)` | `.mockReturnValueOnce(a)` |
| `stub.onSecondCall().returns(b)` | `.mockReturnValueOnce(a).mockReturnValueOnce(b)` |
| `stub.callsFake(fn)` | `.mockImplementation(fn)` |
| `stub.withArgs(a).returns(b)` | `.mockImplementation((x) => x === a ? b : undefined)` |
| `stub.restore()` | `spy.mockRestore()` |

## Mocks (object-level expectations)

Sinon mocks combine expectations with stubs. In Jest, set up the spy/stub
and then assert on it after the fact:

```js
// Sinon
const mock = sinon.mock(obj);
mock.expects('method').once().returns(42);
obj.method();
mock.verify();

// Jest
const spy = jest.spyOn(obj, 'method').mockReturnValue(42);
obj.method();
expect(spy).toHaveBeenCalledTimes(1);
```

## Reset and restore

| Sinon | Jest |
|-------|------|
| `sinon.restore()` | `jest.restoreAllMocks()` — call in `afterEach` |
| `stub.reset()` | `spy.mockReset()` — clears calls and return values |
| `stub.resetBehavior()` | `spy.mockReset()` |
| `sinon.resetHistory()` | `jest.clearAllMocks()` — clears calls only, keeps implementation |

Recommended pattern:

```js
afterEach(() => {
  jest.restoreAllMocks(); // restores original implementations from spyOn
});
```

Or configure globally in `jest.config`:

```js
// jest.config.js
module.exports = {
  restoreMocks: true,   // equivalent to jest.restoreAllMocks() after each test
  clearMocks: true,     // equivalent to jest.clearAllMocks() after each test
};
```

## Fake timers

| Sinon | Jest |
|-------|------|
| `sinon.useFakeTimers()` | `jest.useFakeTimers()` |
| `sinon.useFakeTimers({ now: Date })` | `jest.useFakeTimers({ now: Date })` |
| `clock.tick(ms)` | `jest.advanceTimersByTime(ms)` |
| `await clock.tickAsync(ms)` | `await jest.advanceTimersByTimeAsync(ms)` |
| `clock.next()` | `jest.runOnlyPendingTimers()` |
| `clock.runAll()` | `jest.runAllTimers()` |
| `clock.restore()` | `jest.useRealTimers()` |

> **Tip:** Jest's fake timers also fake `Date` by default. If your code checks
> the current time, set `jest.setSystemTime(new Date(...))` to control it.

## Sandbox pattern

Sinon sandboxes scope fakes to a block. In Jest the equivalent is a
`beforeEach`/`afterEach` pair:

```js
// Sinon
const sandbox = sinon.createSandbox();
afterEach(() => sandbox.restore());
const stub = sandbox.stub(obj, 'method').returns(1);

// Jest
let spy;
beforeEach(() => { spy = jest.spyOn(obj, 'method').mockReturnValue(1); });
afterEach(() => jest.restoreAllMocks());
```

## Module mocking

Sinon does not mock ES or CommonJS modules directly; libraries like `proxyquire`
or `rewire` were often paired with it. Jest has first-class module mocking:

```js
// replaces the whole module
jest.mock('../db', () => ({ query: jest.fn() }));

// replaces a single export, keeping the rest real
jest.mock('../db', () => ({
  ...jest.requireActual('../db'),
  query: jest.fn(),
}));
```

Call `jest.resetModules()` in `beforeEach` if module state bleeds across tests.

## Common pitfalls

- **`spy.mockRestore()` vs `spy.mockReset()`** — `mockRestore` also removes the
  spy and restores the original; `mockReset` clears call history and return values
  but keeps the spy in place.
- **Sinon `callCount` is a number; Jest `mock.calls` is an array** — use
  `spy.mock.calls.length` or the `toHaveBeenCalledTimes` matcher.
- **`stub.withArgs`** — Jest has no direct equivalent; use a custom
  `mockImplementation` that branches on arguments.
- **`sinon.match`** — replace with Jest asymmetric matchers such as
  `expect.objectContaining`, `expect.arrayContaining`, `expect.stringContaining`,
  or `expect.any(Type)`.
