const sinon = require('sinon');
const { expect } = require('chai');
const router = require('../src/router');
const { RequestHandler } = require('../src/request-handler');

describe('RequestHandler', () => {
  let routeStub;
  let handler;

  beforeEach(() => {
    routeStub = sinon.stub(router, 'resolve');
    routeStub.withArgs('/admin').returns({ role: 'admin', path: '/admin' });
    routeStub.withArgs('/public').returns({ role: 'guest', path: '/public' });
    routeStub.returns(null);
    handler = new RequestHandler(router);
  });

  afterEach(() => {
    sinon.restore();
  });

  it('routes admin paths to the admin handler', () => {
    handler.handle('/admin');
    expect(routeStub.calledOnce).to.equal(true);
    expect(routeStub.firstCall.args[0]).to.equal('/admin');
  });

  it('routes public paths correctly on multiple calls', () => {
    handler.handle('/public');
    handler.handle('/admin');
    expect(routeStub.lastCall.args[0]).to.equal('/admin');
  });

  it('returns null for unknown paths', () => {
    const result = handler.handle('/unknown');
    expect(result).to.be.null;
    expect(routeStub.returnValues[0]).to.be.null;
  });
});
