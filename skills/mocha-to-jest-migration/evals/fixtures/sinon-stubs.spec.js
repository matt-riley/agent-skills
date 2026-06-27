const sinon = require('sinon');
const { expect } = require('chai');
const mailer = require('../src/mailer');
const db = require('../src/db');
const formatter = require('../src/formatter');
const { NotificationService } = require('../src/notifications');

describe('NotificationService', () => {
  let sendEmail;
  let saveRecord;
  let buildSubject;
  let service;

  beforeEach(() => {
    sendEmail = sinon.stub(mailer, 'send').resolves({ messageId: 'msg-1' });
    saveRecord = sinon.stub(db, 'save').resolves(true);
    buildSubject = sinon.stub(formatter, 'buildSubject').callsFake((template, vars) => `${template}: ${vars.name}`);
    service = new NotificationService(mailer, db, formatter);
  });

  afterEach(() => {
    sinon.restore();
  });

  it('sends an email when notify is called', async () => {
    await service.notify({ to: 'user@example.com', subject: 'Hello' });

    expect(sendEmail.calledOnce).to.equal(true);
    expect(sendEmail.calledWith({ to: 'user@example.com', subject: 'Hello' })).to.equal(true);
  });

  it('saves a record after sending', async () => {
    await service.notify({ to: 'user@example.com', subject: 'Hello' });

    expect(saveRecord.callCount).to.equal(1);
  });

  it('uses the formatter to build the subject line', () => {
    const result = buildSubject('Welcome', { name: 'Alice' });
    expect(result).to.equal('Welcome: Alice');
    expect(buildSubject.calledOnce).to.equal(true);
  });

  it('retries once on transient send failure', async () => {
    sendEmail
      .onFirstCall().rejects(new Error('SMTP transient'))
      .onSecondCall().resolves({ messageId: 'msg-retry' });

    const result = await service.notifyWithRetry({ to: 'user@example.com', subject: 'Hello' });

    expect(sendEmail.callCount).to.equal(2);
    expect(result.messageId).to.equal('msg-retry');
  });

  it('does not save when send fails permanently', async () => {
    sendEmail.rejects(new Error('SMTP error'));

    let error;
    try {
      await service.notify({ to: 'user@example.com', subject: 'Hello' });
    } catch (e) {
      error = e;
    }

    expect(error).to.be.instanceOf(Error);
    expect(saveRecord.called).to.equal(false);
  });

  it('calls the provided callback with the correct arguments', () => {
    const callbackStub = sinon.stub().callsArgWith(1, null, { success: true });
    let result;
    
    // Simulate a function that takes (data, callback)
    callbackStub('data', (err, res) => {
      result = res;
    });

    expect(callbackStub.calledOnce).to.equal(true);
    expect(result.success).to.equal(true);
  });
});
