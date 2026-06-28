const sinon = require('sinon');
const { expect } = require('chai');
const cache = require('../src/cache');
const metrics = require('../src/metrics');
const { DataLoader } = require('../src/data-loader');

describe('DataLoader', () => {
  let getStub;
  let setStub;
  let recordStub;

  beforeEach(() => {
    getStub = sinon.stub(cache, 'get');
    setStub = sinon.stub(cache, 'set').resolves();
    recordStub = sinon.stub(metrics, 'record');
  });

  afterEach(() => sinon.restore());

  describe('cache hit path', () => {
    beforeEach(() => {
      getStub.resolves({ value: 'cached' });
    });

    it('returns cached data without calling set', async () => {
      const loader = new DataLoader(cache, metrics);
      const result = await loader.load('key-1');

      expect(result).to.deep.equal({ value: 'cached' });
      expect(setStub.called).to.equal(false);
    });

    it('resets call history between retries without changing the implementation', async () => {
      const loader = new DataLoader(cache, metrics);
      await loader.load('key-1');

      // Reset call history only — the stub still resolves { value: 'cached' }
      getStub.resetHistory();

      await loader.load('key-1');
      expect(getStub.calledOnce).to.equal(true);
    });
  });

  describe('cache miss path', () => {
    beforeEach(() => {
      getStub.resolves(null);
    });

    it('fetches from source and populates cache', async () => {
      const loader = new DataLoader(cache, metrics);
      await loader.load('key-2');

      expect(getStub.calledOnce).to.equal(true);
      expect(setStub.calledOnce).to.equal(true);
    });

    it('clears stub state to simulate a different response mid-test', async () => {
      const loader = new DataLoader(cache, metrics);
      await loader.load('key-3');

      // Full reset — clears both calls and return value; spy stays in place
      getStub.reset();
      getStub.resolves({ value: 'fresh' });

      const result = await loader.load('key-3');
      expect(result).to.deep.equal({ value: 'fresh' });
    });

    it('clears only the set return value to apply a new one mid-test', async () => {
      const loader = new DataLoader(cache, metrics);
      await loader.load('key-4');

      // Remove the .resolves() so a new return value can be applied cleanly
      setStub.resetBehavior();
      setStub.resolves({ stored: true });

      await loader.load('key-4');
      expect(setStub.callCount).to.equal(2);
    });
  });

  it('records a metric on every load regardless of cache result', async () => {
    getStub.resolves({ value: 'hit' });
    const loader = new DataLoader(cache, metrics);

    await loader.load('key-4');
    await loader.load('key-4');

    expect(recordStub.callCount).to.equal(2);
  });
});
