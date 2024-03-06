import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  // Using sinon to spy on console methods
  const consoleSpy = sinon.spy(console);
  // Creating a test queue
  const testQueue = createQueue({ name: 'push_notification_code_test' });

  // Setup before running the test suite
  before(() => {
    testQueue.testMode.enter(true);
  });

  // Teardown after running the test suite
  after(() => {
    testQueue.testMode.clear();
    testQueue.testMode.exit();
  });

  // Reset console spy after each test
  afterEach(() => {
    consoleSpy.log.resetHistory();
  });

  it('throws an error if jobs is not an array', () => {
    expect(
      createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, testQueue)
    ).to.throw('Jobs is not an array');
  });

  it('adds jobs to the queue with the correct type', (done) => {
    // Asserting that the test queue initially has no jobs
    expect(testQueue.testMode.jobs.length).to.equal(0);
    // Sample job data
    const jobInfos = [
      {
        phoneNumber: '44556677889',
        message: 'Use the code 1982 to verify your account'
      },
      {
        phoneNumber: '98877665544',
        message: 'Use the code 1738 to verify your account'
      }
    ];
    // Calling the function to create jobs
    createPushNotificationsJobs(jobInfos, testQueue);
    // Asserting that the test queue now has two jobs
    expect(testQueue.testMode.jobs.length).to.equal(2);
    // Asserting that each job has the correct data and type
    expect(testQueue.testMode.jobs[0].data).to.deep.equal(jobInfos[0]);
    expect(testQueue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    // Processing the first job in the queue
    testQueue.process('push_notification_code_3', () => {
      // Asserting that the job creation message is logged to the console
      expect(
        consoleSpy.log
          .calledWith('Notification job created:', testQueue.testMode.jobs[0].id)
      ).to.be.true;
      done();
    });
  });

  it('registers the progress event handler for a job', (done) => {
    // Adding a progress event listener to the first job
    testQueue.testMode.jobs[0].addListener('progress', () => {
      // Asserting that the progress message is logged to the console
      expect(
        consoleSpy.log
          .calledWith('Notification job', testQueue.testMode.jobs[0].id, '25% complete')
      ).to.be.true;
      done();
    });
    // Emitting a progress event with 25% progress
    testQueue.testMode.jobs[0].emit('progress', 25);
  });

  it('registers the failed event handler for a job', (done) => {
    // Adding a failed event listener to the first job
    testQueue.testMode.jobs[0].addListener('failed', () => {
      // Asserting that the failed message is logged to the console
      expect(
        consoleSpy.log
          .calledWith('Notification job', testQueue.testMode.jobs[0].id, 'failed:', 'Failed to send')
      ).to.be.true;
      done();
    });
    // Emitting a failed event with an error message
    testQueue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('registers the complete event handler for a job', (done) => {
    // Adding a complete event listener to the first job
    testQueue.testMode.jobs[0].addListener('complete', () => {
      // Asserting that the completed message is logged to the console
      expect(
        consoleSpy.log
          .calledWith('Notification job', testQueue.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });
    // Emitting a complete event
    testQueue.testMode.jobs[0].emit('complete');
  });
});
