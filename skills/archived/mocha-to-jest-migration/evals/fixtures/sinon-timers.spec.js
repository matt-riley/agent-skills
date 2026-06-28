const sinon = require('sinon');
const { expect } = require('chai');
const { RetryScheduler } = require('../src/retry-scheduler');

describe('RetryScheduler', () => {
  let clock;
  let scheduler;

  beforeEach(() => {
    clock = sinon.useFakeTimers({ now: new Date('2024-06-01T00:00:00Z').getTime() });
    scheduler = new RetryScheduler();
  });

  afterEach(() => {
    clock.restore();
    sinon.restore();
  });

  it('does not fire before the delay elapses', () => {
    const callback = sinon.stub();

    scheduler.schedule(callback, 1000);
    clock.tick(500);

    expect(callback.called).to.equal(false);
  });

  it('fires exactly once when the delay elapses', () => {
    const callback = sinon.stub();

    scheduler.schedule(callback, 1000);
    clock.tick(1000);

    expect(callback.calledOnce).to.equal(true);
  });

  it('stamps scheduled tasks with the frozen clock time', () => {
    const ts = scheduler.timestamp();
    expect(ts).to.equal(new Date('2024-06-01T00:00:00Z').getTime());
  });

  it('retries once after an async failure', async () => {
    const callback = sinon.stub()
      .onFirstCall().rejects(new Error('transient'))
      .onSecondCall().resolves('ok');

    const run = scheduler.scheduleWithRetry(callback, { delay: 2000 });
    await clock.tickAsync(2000);
    await clock.tickAsync(2000);
    await run;

    expect(callback.callCount).to.equal(2);
  });
});
