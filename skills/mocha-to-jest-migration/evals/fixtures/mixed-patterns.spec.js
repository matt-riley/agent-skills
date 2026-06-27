const sinon = require('sinon');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
const cache = require('../src/cache');
const { DataService } = require('../src/data-service');

chai.use(chaiAsPromised);
const { expect } = chai;

describe('DataService', () => {
  let clock;
  let fetchData;
  let evictSpy;
  let service;

  before(async () => {
    await cache.init();
  });

  after(async () => {
    await cache.close();
  });

  beforeEach(() => {
    clock = sinon.useFakeTimers();
    fetchData = sinon.stub(cache, 'fetch').resolves({ items: [1, 2, 3] });
    evictSpy = sinon.spy(cache, 'onEvict');
    service = new DataService(cache);
  });

  afterEach(() => {
    clock.restore();
    sinon.restore();
  });

  it('returns data from the cache', async () => {
    const result = await service.getData('key-1');

    expect(result).to.deep.equal({ items: [1, 2, 3] });
    expect(fetchData.calledOnce).to.equal(true);
  });

  it('re-fetches after the TTL expires', async () => {
    await service.getData('key-1');
    await clock.tickAsync(5000);
    await service.getData('key-1');

    expect(fetchData.callCount).to.equal(2);
  });

  it('calls the eviction hook when TTL expires', async () => {
    await service.getData('key-1');
    await clock.tickAsync(5000);

    expect(evictSpy.calledOnce).to.equal(true);
  });

  it('throws when the key is not a string', () => {
    expect(() => service.getData(null)).to.throw(TypeError, 'key must be a string');
  });

  it('rejects when the cache is unavailable', async () => {
    fetchData.rejects(new Error('cache unavailable'));

    await expect(service.getData('key-1')).to.be.rejectedWith('cache unavailable');
  });
});
