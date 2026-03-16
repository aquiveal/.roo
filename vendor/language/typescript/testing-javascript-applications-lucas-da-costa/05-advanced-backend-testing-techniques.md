## @Domain
These rules MUST be activated when the AI is tasked with writing, updating, reviewing, or optimizing automated tests for backend systems. Triggering conditions include tasks related to test suite performance, test flakiness, concurrency, mocking time-dependent functions (`setTimeout`, `setInterval`, `Date`), dealing with shared testing resources (databases, file systems), or refactoring tests to reduce maintenance overhead and overlap.

## @Vocabulary
*   **Deterministic Tests**: Tests that guarantee the exact same results on every execution given the same inputs, regardless of network availability, time, or execution order.
*   **Flaky Tests**: Tests that intermittently fail without any application code changes, primarily caused by unmocked time, shared resource collisions, or reliance on real third-party APIs.
*   **Transitive Guarantees**: A testing pattern where a dependency (e.g., a logger) is thoroughly tested once in isolation, and dependent tests merely assert that the dependency was invoked correctly (using a spy) rather than re-evaluating the dependency's side effects.
*   **Preconditions (Implicit Assertions)**: Embedding expected behavior into test setup or mocks (e.g., requiring exact arguments in a `nock` interceptor) so that the test fails implicitly if the preconditions are unmet, eliminating the need for explicit assertion lines.
*   **Fake Timers**: Test doubles that replace native browser/Node.js time functions to allow the synchronous progression of time within tests (e.g., `@sinonjs/fake-timers`).
*   **Test Overlap**: The redundant execution of identical code paths and identical assertions across multiple tests of varying scope (e.g., unit, integration, and E2E tests checking the exact same logic).

## @Objectives
*   **Eliminate Nondeterminism**: Mock or isolate every factor outside the control of the test logic, including time, randomness, and network APIs.
*   **Enable Safe Parallelism**: Ensure tests can run concurrently without race conditions by dynamically isolating shared resources per worker thread.
*   **Optimize Speed and Robustness**: Eliminate fixed-time delays (`sleep` or `wait`) in favor of programmatic time manipulation and recursive retry loops.
*   **Reduce Maintenance Costs**: Strategically eliminate redundant overlapping tests and replace expensive side-effect assertions with transitive guarantees and implicit preconditions.

## @Guidelines
*   **Mock Uncontrollable Factors**: The AI MUST stub or mock APIs, randomness (`Math.random`), and time when testing backend logic to ensure tests are 100% deterministic. 
*   **Resource Isolation for Concurrency**: The AI MUST NOT hardcode database names, file paths, or port numbers if tests are designed to run in parallel. The AI MUST use `process.env.JEST_WORKER_ID` to generate unique resources (e.g., `/tmp/test_state_${process.env.JEST_WORKER_ID}.txt`) for each test thread.
*   **Sequential Fallback**: If true resource isolation is impossible, the AI MUST configure the test runner to execute sequentially (e.g., `jest --runInBand`).
*   **Time Manipulation over Waiting**: The AI MUST NOT use fixed time delays (e.g., `await new Promise(r => setTimeout(r, 5000))`). The AI MUST use fake timers (e.g., `FakeTimers.install()`) and manually advance time using `clock.tick(ms)`.
*   **Selective Timer Faking**: When using fake timers alongside retry loops, the AI MUST explicitly declare which timers to fake (e.g., `{ toFake: ["Date", "setInterval"] }`) so that `setTimeout` can still be utilized for recursive retry delays.
*   **Retry Mechanisms for Async Side-Effects**: When asserting on database updates or background jobs triggered by time without an awaitable promise, the AI MUST wrap assertions in a recursive retry function (`withRetries`) that catches assertion errors and retries until passing or timing out.
*   **Minimize Test Overlap**: To reduce maintenance costs, the AI MUST evaluate the dependency tree of the tests. If a higher-level test (e.g., end-to-end route test) adequately covers the execution paths and assertions of lower-level unit tests, the AI MUST centralize the assertions in the top node and delete the redundant lower-level tests.
*   **Implement Transitive Guarantees**: For orthogonal dependencies (e.g., logging systems, notification dispatchers), the AI MUST thoroughly test the dependency in its own file. In consumer files, the AI MUST mock the dependency and assert only that it was called with the correct arguments, strictly avoiding reading the side-effect (e.g., reading the log file).
*   **Turn Assertions into Preconditions**: The AI MUST encode assertions into test doubles. When using tools like `nock` or `jest-when`, the AI MUST match exact paths, queries, and bodies. This forces the test to implicitly fail if the underlying code behaves incorrectly, reducing redundant `expect(spy).toHaveBeenCalledWith(...)` boilerplate.

## @Workflow
1.  **Analyze Determinism**: Scan the unit under test for interactions with external APIs, databases, file systems, randomness, and time.
2.  **Isolate Shared State**: If running concurrently, inject `process.env.JEST_WORKER_ID` into any resource connection string or file path factory.
3.  **Control Time**: 
    * Install fake timers in a `beforeEach` hook.
    * In the test body, trigger the time-dependent function.
    * Use `clock.tick(ms)` to instantly advance time.
    * Restore original timers in an `afterEach` hook.
4.  **Implement Smart Retries**: If testing detached asynchronous updates (e.g., background cleanup jobs), implement a `withRetries` recursive loop that catches `JestAssertionError` and delays for a few milliseconds using a *real* `setTimeout` before trying again.
5.  **Audit and Reduce Overlap**: Review the test suite for duplicated assertion logic. Consolidate validations into the highest-level integrated test that makes sense, and remove brittle, low-level overlapping tests.
6.  **Apply Transitive Guarantees**: Replace file-system reads, database checks, or expensive assertions on shared utility modules with spies (`expect(spy).toHaveBeenCalledWith(...)`).
7.  **Embed Preconditions**: Configure network intercepts (`nock`) to accept strictly the expected payload. Do not assert on the fetch payload manually if the mock library can handle the rejection implicitly.

## @Examples (Do's and Don'Don'ts)

### 1. Parallelism and Shared Resources
**[DO]** Use the worker ID to dynamically provision isolated test resources.
```javascript
const { init } = require("./countModule");
const pool = {};

const getInstance = (workerId) => {
  if (!pool[workerId]) {
    // Each Jest worker thread gets a totally isolated file
    pool[workerId] = init(`/tmp/test_state_${workerId}.txt`);
  }
  return pool[workerId];
};

const instance = getInstance(process.env.JEST_WORKER_ID);
```

**[DON'T]** Hardcode shared resources that will collide when test files are parallelized by the runner.
```javascript
// ANTIPATTERN: Will cause race conditions and flaky tests
const filepath = "/tmp/test_shared_state.txt";
const getState = () => parseInt(fs.readFileSync(filepath, "utf-8"), 10);
```

### 2. Dealing with Time and Asynchronicity
**[DO]** Use fake timers to advance time instantly, combined with a retry loop using the real `setTimeout` for assertions that depend on background processing.
```javascript
const FakeTimers = require("@sinonjs/fake-timers");

let clock;
beforeEach(() => {
  // Fake Date and setInterval, but keep setTimeout real for our retry loop
  clock = FakeTimers.install({ toFake: ["Date", "setInterval"] });
});

afterEach(() => {
  clock.uninstall();
});

test("removing stale items", async () => {
  // Trigger logic
  timer = monitorStaleItems();
  
  // Instantly advance time
  clock.tick(1000 * 60 * 60 * 2);

  // Smart retry loop instead of fixed waiting
  await withRetries(async () => {
    const dbContent = await fetchDatabaseState();
    expect(dbContent).toEqual([]);
  });
});

const withRetries = async (fn) => {
  try {
    await fn();
  } catch (e) {
    if (e.message.includes("expect")) { // Basic JestAssertionError check
      await new Promise(resolve => setTimeout(resolve, 100));
      await withRetries(fn);
    } else {
      throw e;
    }
  }
};
```

**[DON'T]** Use fixed `sleep` or `wait` commands to test time-dependent logic.
```javascript
// ANTIPATTERN: Slows down tests and remains flaky if processing takes 4001ms
timer = monitorStaleItems();
await new Promise(resolve => setTimeout(resolve, 4000));
const dbContent = await fetchDatabaseState();
expect(dbContent).toEqual([]);
```

### 3. Creating Transitive Guarantees
**[DO]** Thoroughly test the dependency once, and use spies in dependent systems to verify interactions.
```javascript
// In addItemToCart.test.js
jest.spyOn(logger, "logInfo").mockImplementation(jest.fn());

test("logs when adding item", () => {
  addItemToCart("test_user", "cheesecake");
  
  // Transitive guarantee: We trust the logger works, we just ensure it was called
  expect(logger.logInfo).toHaveBeenCalledWith(
    { item: "cheesecake", quantity: 1 }, 
    "item added to the inventory"
  );
});
```

**[DON'T]** Re-evaluate the side-effects of an orthogonal dependency across every test.
```javascript
// ANTIPATTERN: Testing the file system write in the cart controller test
test("logs when adding item", () => {
  fs.writeFileSync("/tmp/logs.out", "");
  addItemToCart("test_user", "cheesecake");
  
  const logs = fs.readFileSync("/tmp/logs.out", "utf-8");
  expect(logs).toContain("cheesecake added to test_user's cart\n");
});
```

### 4. Turning Assertions into Preconditions
**[DO]** Embed assertions directly into the mock boundaries.
```javascript
test("fetches inventory using correct query", async () => {
  const expectedResponse = { recipes: [] };
  
  // Precondition: If the URL or exact query is wrong, nock will throw an error automatically.
  nock("http://third-party-api.com")
    .get("/api")
    .query({ item: "cheesecake" })
    .reply(200, expectedResponse);

  const response = await fetchInventory("cheesecake");
  expect(response).toEqual(expectedResponse);
});
```

**[DON'T]** Manually spy on network adapters to assert on arguments when the mocking library can enforce it.
```javascript
// ANTIPATTERN: Redundant assertion boilerplate
fetch.mockResolvedValue({ json: () => Promise.resolve(expectedResponse) });
await fetchInventory("cheesecake");
expect(fetch.mock.calls[0][0]).toBe("http://third-party-api.com/api?item=cheesecake");
```