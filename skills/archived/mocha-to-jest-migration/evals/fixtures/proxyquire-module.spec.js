const proxyquire = require('proxyquire');
const sinon = require('sinon');
const { expect } = require('chai');

describe('OrderProcessor', () => {
  let inventoryStub;
  let paymentStub;
  let OrderProcessor;

  beforeEach(() => {
    inventoryStub = { reserve: sinon.stub().resolves(true) };
    paymentStub = { charge: sinon.stub().resolves({ transactionId: 'txn-123' }) };

    ({ OrderProcessor } = proxyquire('../src/order-processor', {
      '../inventory': inventoryStub,
      '../payment': paymentStub,
    }));
  });

  afterEach(() => sinon.restore());

  it('reserves inventory then charges payment', async () => {
    const result = await new OrderProcessor().process({ sku: 'A1', amount: 50 });

    expect(inventoryStub.reserve.calledOnce).to.equal(true);
    expect(paymentStub.charge.calledWith(sinon.match.object({ amount: 50 }))).to.equal(true);
    expect(result.transactionId).to.equal('txn-123');
  });

  it('does not charge if inventory reservation fails', async () => {
    inventoryStub.reserve.resolves(false);

    const result = await new OrderProcessor().process({ sku: 'A1', amount: 50 });

    expect(paymentStub.charge.called).to.equal(false);
    expect(result).to.be.null;
  });
});
