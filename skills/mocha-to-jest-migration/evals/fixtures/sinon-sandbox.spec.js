const sinon = require('sinon');
const { expect } = require('chai');
const db = require('../src/db');
const mailer = require('../src/mailer');
const { UserService } = require('../src/user-service');

describe('UserService', () => {
  let sandbox;
  let queryStub;
  let sendStub;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    queryStub = sandbox.stub(db, 'query').resolves([{ id: 1, name: 'Alice' }]);
    sendStub = sandbox.stub(mailer, 'send').resolves({ messageId: 'msg-1' });
  });

  afterEach(() => sandbox.restore());

  it('returns users from the database', async () => {
    const svc = new UserService(db, mailer);
    const users = await svc.list();

    expect(users).to.deep.equal([{ id: 1, name: 'Alice' }]);
    expect(queryStub.calledOnce).to.equal(true);
  });

  it('sends a welcome email with name and subject fields', async () => {
    const svc = new UserService(db, mailer);
    await svc.notifyNew();

    expect(sendStub.calledOnce).to.equal(true);
    expect(
      sendStub.calledWith(sinon.match({ to: sinon.match.string, subject: sinon.match.string }))
    ).to.equal(true);
  });

  it('resets call history mid-test without changing stub return values', async () => {
    const svc = new UserService(db, mailer);
    await svc.list();

    // Clear call counts only — queryStub still resolves [{ id: 1, name: 'Alice' }]
    sandbox.resetHistory();

    await svc.list();
    expect(queryStub.calledOnce).to.equal(true);
  });

  it('overrides the db response after a history reset to simulate a stale result', async () => {
    const svc = new UserService(db, mailer);
    await svc.list(); // first call returns Alice

    sandbox.resetHistory();
    queryStub.resolves([]); // override return value for the next call

    const users = await svc.list();
    expect(users).to.deep.equal([]);
    expect(queryStub.calledOnce).to.equal(true);
    expect(sendStub.called).to.equal(false);
  });
});
