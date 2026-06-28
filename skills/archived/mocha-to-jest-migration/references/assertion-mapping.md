# Chai → Jest assertion mapping

Direct substitution table for the most common Chai BDD assertions.
Chai's `expect` and `should` styles map directly; the `assert` style maps less cleanly — prefer `expect` in Jest.

## Equality

| Chai | Jest |
|------|------|
| `expect(a).to.equal(b)` | `expect(a).toBe(b)` — strict (`===`) |
| `expect(a).to.deep.equal(b)` | `expect(a).toEqual(b)` — deep equality |
| `expect(a).to.eql(b)` | `expect(a).toEqual(b)` |
| `expect(a).to.not.equal(b)` | `expect(a).not.toBe(b)` |
| `expect(a).to.not.deep.equal(b)` | `expect(a).not.toEqual(b)` |
| `assert.equal(a, b)` | `expect(a).toBe(b)` |
| `assert.deepEqual(a, b)` | `expect(a).toEqual(b)` |
| `assert.strictEqual(a, b)` | `expect(a).toBe(b)` |

## Truthiness

| Chai | Jest |
|------|------|
| `expect(x).to.be.true` | `expect(x).toBe(true)` |
| `expect(x).to.be.false` | `expect(x).toBe(false)` |
| `expect(x).to.be.ok` | `expect(x).toBeTruthy()` |
| `expect(x).to.not.be.ok` | `expect(x).toBeFalsy()` |
| `expect(x).to.be.null` | `expect(x).toBeNull()` |
| `expect(x).to.be.undefined` | `expect(x).toBeUndefined()` |
| `expect(x).to.exist` | `expect(x).toBeDefined()` |
| `expect(x).to.not.exist` | `expect(x).toBeUndefined()` or `toBeNull()` |

## Numbers

| Chai | Jest |
|------|------|
| `expect(n).to.be.above(x)` | `expect(n).toBeGreaterThan(x)` |
| `expect(n).to.be.below(x)` | `expect(n).toBeLessThan(x)` |
| `expect(n).to.be.at.least(x)` | `expect(n).toBeGreaterThanOrEqual(x)` |
| `expect(n).to.be.at.most(x)` | `expect(n).toBeLessThanOrEqual(x)` |
| `expect(n).to.be.closeTo(x, d)` | `expect(n).toBeCloseTo(x, decimals)` |

## Strings and arrays

| Chai | Jest |
|------|------|
| `expect(s).to.include(sub)` | `expect(s).toContain(sub)` |
| `expect(arr).to.include(item)` | `expect(arr).toContain(item)` |
| `expect(arr).to.deep.include(obj)` | `expect(arr).toContainEqual(obj)` |
| `expect(s).to.match(/re/)` | `expect(s).toMatch(/re/)` |
| `expect(arr).to.have.length(n)` | `expect(arr).toHaveLength(n)` |
| `expect(arr).to.be.empty` | `expect(arr).toHaveLength(0)` |
| `expect(obj).to.have.property('k')` | `expect(obj).toHaveProperty('k')` |
| `expect(obj).to.have.property('k', v)` | `expect(obj).toHaveProperty('k', v)` |

## Type checks

| Chai | Jest |
|------|------|
| `expect(x).to.be.a('string')` | `expect(typeof x).toBe('string')` |
| `expect(x).to.be.an('array')` | `expect(Array.isArray(x)).toBe(true)` |
| `expect(x).to.be.instanceof(Cls)` | `expect(x).toBeInstanceOf(Cls)` |

## Throwing

| Chai | Jest |
|------|------|
| `expect(fn).to.throw()` | `expect(fn).toThrow()` |
| `expect(fn).to.throw('msg')` | `expect(fn).toThrow('msg')` |
| `expect(fn).to.throw(ErrorClass)` | `expect(fn).toThrow(ErrorClass)` |
| `expect(fn).to.not.throw()` | `expect(fn).not.toThrow()` |
| `await expect(promise).to.be.rejected` | `await expect(promise).rejects.toThrow()` |
| `await expect(promise).to.be.rejectedWith(Err)` | `await expect(promise).rejects.toThrow(Err)` |
| `await expect(promise).to.be.fulfilled` | `await expect(promise).resolves.toBeDefined()` (or `.resolves.not.toThrow()`) |

> **Note:** `chai-as-promised` patterns must all be converted — Jest handles
> promise assertions natively.

## assert-style Chai

Chai's `assert.*` style has no direct Jest counterpart beyond plain `expect`.
Map it by looking at what the assertion actually checks, then write the
equivalent `expect(actual).toXxx(expected)` form.

```js
// Chai
assert.isString(x);
assert.isArray(arr);
assert.isAbove(n, 0);

// Jest
expect(typeof x).toBe('string');
expect(Array.isArray(arr)).toBe(true);
expect(n).toBeGreaterThan(0);
```
