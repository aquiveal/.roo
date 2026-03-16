# @Domain
Trigger these rules when the user requests assistance with architecting, writing, reviewing, or organizing JavaScript automated tests, or when asking for guidance on test strategy, test types (Unit, Integration, End-to-End), and balancing test maintenance costs.

# @Vocabulary
- **Automated Test**: A program that automates the verification of software by interfacing with the application, performing actions, and comparing actual results with previously defined expected outputs.
- **Testing Pyramid (Revised)**: A mental framework dividing tests into End-to-End (top), Integration (middle), and Unit (bottom) based strictly on their scope and level of isolation, not their specific targets (e.g., UI vs Service).
- **Unit Test**: The most atomic test type, located at the base of the pyramid. Targets individual functions in isolation. Highly numerous, extremely fast, cheap, and provides narrow, precise feedback.
- **Integration Test**: A test targeting observable behavior and the integration between multiple functions or between the software and third-party libraries/dependencies (e.g., databases, filesystems, external APIs).
- **End-to-End (E2E) Test**: A coarse test treating the application as a black box. Interacts with the software from an external user's perspective (e.g., via GUI or HTTP API). Slowest, most expensive, but provides the strongest quality guarantees.
- **Black Box Test**: A test that is unaware of the application's internal code or implementation details.
- **White Box Test**: A test that requires direct access to and knowledge of the application's internal code.
- **Acceptance Test**: A test validating whether the application works from a business perspective and fulfills functional requirements for end users. (Distinct from E2E tests, which validate correctness from an engineering perspective).
- **Exploratory Testing**: Manual testing investigating curious scenarios, edge cases, and user delight that machines cannot replicate. Automated tests free up humans to perform this.
- **Three A's Pattern (Arrange, Act, Assert)**: The standard formula for tests: setup the scenario (Arrange), execute the target code (Act), and verify the output (Assert).
- **Deep Equality vs. Strict Equality**: Deep equality (`toEqual`) verifies if two different objects have equal values. Strict equality (`toBe`) verifies if two references point to the same exact object in memory.
- **Transitive Guarantee**: Encapsulation at the testing level. If Function A is fully tested, tests for Function B (which calls Function A) only need to verify that Function A was invoked, rather than redundantly re-testing Function A's behavior.
- **Flaky Test**: A test that provides inconsistent results (sometimes passing, sometimes failing) without changes to the underlying code.

# @Objectives
- Implement testing strategies aligned with the revised Testing Pyramid, choosing the correct test type based on desired scope, speed, cost, and required quality guarantees.
- Reduce test maintenance costs by maximizing test readability, avoiding code duplication, and decreasing coupling between tests and application implementation details.
- Provide quick, precise feedback during development via granular unit tests, while relying on integration and E2E tests for robust behavioral guarantees.
- Ensure automated tests focus on what the code does (observable behavior) rather than how it does it (implementation details), except when explicitly testing required side effects.
- Facilitate human exploratory testing by automating all repetitive, procedural testing tasks.

# @Guidelines

### Test Strategy & Selection
- **Determine Test Scope**: Use Unit tests for individual functions. Use Integration tests when interacting with third-party libraries, databases, or combined functions. Use End-to-End tests for user-facing workflows and full-stack validation.
- **Avoid Testing Third-Party Code**: NEVER write tests targeting the internal behavior of a third-party library. Only test that the application interacts with the third-party library correctly.
- **Prefer Integration over Excessive Mocking**: When mocking a dependency is too complicated or time-consuming, opt for an integration test using the real dependency (e.g., a test database) to balance cost and benefit.

### Test Structure & Organization
- **Three A's Pattern**: MUST explicitly structure tests sequentially: Setup scenario (Arrange), trigger action (Act), check results (Assert).
- **Test Abstraction**: MUST abstract repetitive test setup, promise chains, or complex request logic into separate utility/helper functions.
- **Test Namespacing**: MUST use `test()` functions to isolate tests. Test names must be descriptive of the exact behavior being verified.

### Assertions & Verifications
- **Deep vs Strict Equality**: MUST use Jest's `toBe()` for strict reference/primitive equality, and `toEqual()` for deep object value equality.
- **Testing Side Effects**: Implementation details SHOULD NOT be tested unless they are critical side effects (e.g., logging services). In those cases, assert that the side effect was triggered using Transitive Guarantees.

### Asynchronous Testing & Resource Cleanup
- **Async Handling**: MUST use `async/await` for asynchronous tests. If using a `done` callback, NEVER forget to invoke it, and NEVER invoke it with a truthy argument, or the test will time out/fail.
- **Teardown Hooks**: MUST explicitly clean up resources in `afterAll` or `afterEach` hooks. (e.g., close database connection pools using `db.destroy()`, stop HTTP servers using `app.close()`).
- **Test Isolation**: MUST clean state in `beforeEach` or `beforeAll` (e.g., truncating database tables) so that tests run predictably and independently. Do not pollute production databases; always use a separate testing database.
- **Open Handles**: Use Jest's `--detectOpenHandles` to find unclosed resources. AVOID using `--forceExit`; instead, gracefully close servers and connections.

### Test Maintenance & Costs
- **Decoupling**: Tests MUST NOT fail during application refactors if the observable output/behavior remains the same.
- **Transitive Guarantees**: Reduce overlap between tests. If `loggingService` is comprehensively unit tested, the test for `addItemToCart` should only verify `loggingService` was called, not assert the log file's exact contents.

# @Workflow
1. **Analyze the Request**: Determine the target scope (single function, service integration, or full application workflow).
2. **Select Pyramid Level**: 
   - Choose Unit Test for algorithmic logic or single isolated functions.
   - Choose Integration Test if the target involves database queries, filesystem access, or API integration.
   - Choose E2E Test if the user requires HTTP API validation or GUI workflow validation.
3. **Setup the Environment**: 
   - Define database connections or import `isomorphic-fetch` if testing APIs.
   - Define `beforeEach` hooks for state resetting (e.g., `db("table").truncate()`).
   - Define `afterAll` hooks for graceful shutdown (e.g., `app.close()`).
4. **Implement the Three A's**:
   - **Arrange**: Set the exact system state required (e.g., adding prerequisites to the DB).
   - **Act**: Invoke the target function or send the HTTP request. Wait for async operations.
   - **Assert**: Use Jest matchers (`expect().toEqual()` or `expect().toBe()`) to validate the new state or the returned payload.
5. **Refactor for Maintenance**: Review the generated test. Extract duplicated logic (like HTTP fetch boilerplate) into helper functions. Verify that the test is checking behavior, not fragile internal implementation details.

# @Examples (Do's and Don'ts)

### 1. Abstracting Repetitive Test Logic
**[DO] Create abstractions for repetitive test actions:**
```javascript
const fetch = require("isomorphic-fetch");
const apiRoot = "http://localhost:3000";

const addItem = (username, item) => {
  return fetch(`${apiRoot}/carts/${username}/items/${item}`, { method: "POST" });
};

const getItems = username => {
  return fetch(`${apiRoot}/carts/${username}/items`, { method: "GET" });
};

test("adding items to a cart", async () => {
  const initialItemsResponse = await getItems("lucas");
  expect(initialItemsResponse.status).toEqual(404);

  const addItemResponse = await addItem("lucas", "cheesecake");
  expect(await addItemResponse.json()).toEqual(["cheesecake"]);
});
```

**[DON'T] Write convoluted, repetitive logic in the test body:**
```javascript
test("adding items to a cart", done => {
  return fetch(`http://localhost:3000/carts/lucas/items`, { method: "GET" })
    .then(initialItemsResponse => {
      expect(initialItemsResponse.status).toEqual(404);
      return fetch(`http://localhost:3000/carts/lucas/items/cheesecake`, { method: "POST" })
        .then(response => response.json());
    })
    .then(addItemResponse => {
      expect(addItemResponse).toEqual(["cheesecake"]);
      done();
    });
});
```

### 2. Transitive Guarantees vs Coupled Implementations
**[DO] Use transitive guarantees to verify side effects without tight coupling:**
```javascript
// Test for addItemToCart using the logging service
test("logs errors when adding an item fails", async () => {
  const loggingServiceSpy = jest.spyOn(loggingService, "logError");
  
  try {
    await addItemToCart("invalid_item");
  } catch(error) {
    // We trust loggingService works because it has its own tests.
    // We only assert it was called.
    expect(loggingServiceSpy).toHaveBeenCalledWith(error);
  }
});
```

**[DON'T] Redundantly test internal behavior of dependencies in the parent function test:**
```javascript
test("logs errors when adding an item fails", async () => {
  try {
    await addItemToCart("invalid_item");
  } catch(error) {
    // Anti-pattern: Reading the log file in the addItemToCart test 
    // couples this test to the loggingService's internal implementation.
    const logs = fs.readFileSync('/var/log/app.log', 'utf8');
    expect(logs).toContain("invalid_item");
  }
});
```

### 3. Graceful Teardown
**[DO] Ensure resources are gracefully closed:**
```javascript
const app = require("./server");
const { db, closeConnection } = require("./dbConnection");

afterAll(async () => {
  await closeConnection();
  app.close();
});
```

**[DON'T] Leave open handles or rely on forceExit:**
```javascript
// Missing afterAll hook!
// This will cause Jest to hang with: "Jest has detected open handles..."
const app = require("./server");

test("server responds", async () => {
  // test logic
});
```

### 4. Database Test Isolation
**[DO] Truncate tables to ensure deterministic test state:**
```javascript
beforeEach(async () => {
  await db("carts").truncate();
  await db("carts_items").truncate();
});

test("createCart creates a cart for a username", async () => {
  await createCart("Lucas da Costa");
  const result = await db.select("username").from("carts");
  expect(result).toEqual([{ username: "Lucas da Costa" }]);
});
```

**[DON'T] Rely on leftover state from previous tests:**
```javascript
// No beforeEach hook to truncate tables!
test("createCart creates a cart for a username", async () => {
  await createCart("Lucas da Costa");
  const result = await db.select("username").from("carts");
  // This will fail if another test already added "Lucas da Costa" or other users!
  expect(result).toEqual([{ username: "Lucas da Costa" }]); 
});
```