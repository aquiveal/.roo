# @Domain
Trigger these rules when tasked with creating, modifying, architecting, or configuring tests for Node.js backend applications. This includes testing HTTP API endpoints, writing and testing middleware, dealing with database integrations, and interacting with third-party external APIs within a backend context.

# @Vocabulary
- **Unit Test (Backend)**: Tests targeting individual functions in isolation (e.g., business logic controllers, pure helper functions) without interacting with external dependencies like databases or the filesystem.
- **Integration Test (Backend)**: Tests covering interactions between multiple functions and external components controlled by the application, such as local databases, global pieces of state, or the filesystem.
- **End-to-End (E2E) Test (Backend)**: Tests validating the backend application from a consumer's perspective by treating the application as a black box and interacting with it exclusively via HTTP requests to its exposed API routes.
- **Testable Architecture**: A software design approach where monolithic routes are broken down into smaller, accessible pieces (controllers, services) that are explicitly exported to allow granular testing.
- **supertest**: The required library for testing HTTP endpoints, combining HTTP request execution with built-in assertion capabilities.
- **nock**: The required library for intercepting and stubbing outbound HTTP requests to third-party APIs.
- **Fixture**: A baseline scenario or initial database state set up before tests run to guarantee repeatable results.
- **Pristine State**: The condition of a database or global state before a test runs, ensuring no residual data from previous tests causes flakiness or cross-test interference.

# @Objectives
- Architect backend code to prioritize testability by decoupling business logic from routing logic and exposing internal states or instances as needed for tests.
- Ensure all automated tests interacting with shared resources (like databases) execute deterministically and start from a strictly enforced pristine state.
- Prevent tests from making live network requests to third-party APIs to avoid rate limits, monetary costs, network-related flakiness, and security leaks.
- Avoid hanging test processes by systematically closing all open handles, server connections, and database connection pools, strictly avoiding the use of force-exit flags.
- Optimize the testing feedback loop by utilizing the correct test type (Unit, Integration, E2E) for the appropriate layer of the backend application.

# @Guidelines

## Architectural Guidelines for Testability
- The AI MUST separate business logic from route definitions by moving logic into standalone controller modules.
- The AI MUST export the running server instance (e.g., `app.listen()`) and necessary internal state structures (like maps or databases) from the main server file to grant tests access to the application context.
- The AI MUST NOT hesitate to export internal functions or states exclusively for the sake of testing, even if the production application code does not strictly require them to be exported.

## HTTP Endpoint Testing Rules
- The AI MUST use `supertest` for testing HTTP endpoints.
- The AI MUST pass the exported application instance (e.g., Express or Koa app) directly into `supertest`'s `request(app)` method to avoid hardcoding API port numbers and URLs.
- The AI MUST NOT use standard HTTP clients like `isomorphic-fetch` or `axios` to test the application's own API endpoints.

## Middleware Testing Rules
- The AI MUST adopt a multi-layered approach to testing middleware:
  1. Extract and unit-test pure functions used by the middleware (e.g., password hashing, credential validation).
  2. Test the middleware function in isolation by passing mocked `ctx` (or `req`/`res`) objects and a mocked `next` function (e.g., `jest.fn()`).
  3. E2E test the middleware dynamically by configuring `supertest` to send valid and invalid headers (e.g., `.set('authorization', authHeader)`) to protected routes.

## Database Integration Testing Rules
- The AI MUST enforce a pristine state for database testing. Tests modifying databases MUST NOT use the same database instance as the local development environment.
- The AI MUST configure database connections to dynamically select the database file/URI based on `process.env.NODE_ENV` (e.g., utilizing `NODE_ENV=test`).
- The AI MUST run database-dependent tests sequentially using Jest's `--runInBand` CLI flag to prevent parallel threads from interfering with shared database state.
- The AI MUST automate database migrations using Jest's `globalSetup` configuration to ensure the schema is always up-to-date before any test runs.
- The AI MUST automate database cleanup (truncating tables) and seeding using files defined in Jest's `setupFilesAfterEnv`. The AI MUST NOT duplicate database truncation hooks (`beforeEach(() => db.truncate())`) across multiple test files.
- The AI MUST systematically close all database connection pools (e.g., `db.destroy()`) using an `afterAll` hook inside a `setupFilesAfterEnv` script.
- The AI MUST NOT solve hanging test processes by adding the `--forceExit` flag to test scripts. Instead, the AI MUST gracefully close server instances (`app.close()`) and database connections.

## External/Third-Party API Testing Rules
- The AI MUST NOT allow tests to execute real HTTP requests to third-party external APIs.
- The AI MUST NOT manually stub or mock the application's HTTP client (e.g., replacing `fetch` with a `jest.fn()`) to handle third-party calls, as this tightly couples the test to the implementation details.
- The AI MUST use `nock` to intercept external HTTP requests and provide deterministic, canned responses.
- The AI MUST clear all `nock` interceptors before every test by executing `nock.cleanAll()` in a `beforeEach` hook.
- The AI MUST assert that all defined `nock` interceptors were consumed by executing `nock.isDone()` in an `afterEach` hook. If `nock.isDone()` returns false, the AI MUST throw an explicit error to fail the test.

# @Workflow
When tasked with implementing and testing a backend feature, the AI MUST execute the following steps in order:
1. **Refactor for Testability**: If modifying existing code, extract monolithic route logic into separate controller modules. Export the server instance and the controller functions.
2. **Configure Database Environment (If applicable)**: 
   - Verify `NODE_ENV` dynamically switches the database connection to a test-specific instance.
   - Create or update a `globalSetup` script to run database migrations.
   - Create or update `setupFilesAfterEnv` scripts to truncate all tables before each test and destroy the connection pool after all tests.
3. **Write Unit Tests**: Target pure functions and isolated business logic inside the controllers.
4. **Write Integration Tests**: Target functions interacting with the database. Assert on both the function's return value and the resulting state of the database.
5. **Configure Nock (If applicable)**: If the route interacts with an external API, implement `nock` interceptors in `beforeEach`, and enforce `nock.isDone()` checks in `afterEach`.
6. **Write E2E Endpoint Tests**: Use `supertest` to hit the application's routes. Send varying requests (valid payloads, invalid inputs, missing auth) and assert on the HTTP status codes, headers, and JSON response bodies.

# @Examples (Do's and Don'ts)

## HTTP Endpoint Testing
**[DO]** Use `supertest` passing the app instance directly.
```javascript
const request = require("supertest");
const { app } = require("./server.js");

test("adding items to a cart", async () => {
  const response = await request(app)
    .post("/carts/test_user/items/cheesecake")
    .expect(200)
    .expect("Content-Type", /json/);

  expect(response.body).toEqual(["cheesecake"]);
});
```

**[DON'T]** Hardcode server URLs and use generic HTTP clients for endpoint testing.
```javascript
const fetch = require("isomorphic-fetch");

test("adding items to a cart", async () => {
  // Anti-pattern: Hardcoded URL, requires server to be manually started, verbose assertions
  const response = await fetch("http://localhost:3000/carts/test_user/items/cheesecake", {
    method: "POST"
  });
  expect(response.status).toEqual(200);
  const body = await response.json();
  expect(body).toEqual(["cheesecake"]);
});
```

## Database State Management
**[DO]** Centralize table truncation and connection teardown in `setupFilesAfterEnv`.
```javascript
// jest.config.js
module.exports = {
  setupFilesAfterEnv: ["<rootDir>/truncateTables.js", "<rootDir>/disconnectDb.js"]
};

// truncateTables.js
const { db } = require("./dbConnection");
beforeEach(() => {
  return Promise.all(["users", "inventory"].map(t => db(t).truncate()));
});

// disconnectDb.js
const { db } = require("./dbConnection");
afterAll(() => db.destroy());
```

**[DON'T]** Repeat truncation hooks manually in every test file or use `--forceExit`.
```javascript
// Anti-pattern: Duplicated across files, prone to being forgotten
const { db } = require("./dbConnection");

beforeEach(async () => {
  await db("users").truncate();
  await db("inventory").truncate();
});
// Anti-pattern: Missing db.destroy(), forcing the use of jest --forceExit
```

## Third-Party API Interception
**[DO]** Use `nock` to intercept network-level requests and verify interceptor consumption.
```javascript
const nock = require("nock");
const request = require("supertest");
const { app } = require("./server");

beforeEach(() => nock.cleanAll());

afterEach(() => {
  if (!nock.isDone()) {
    nock.cleanAll();
    throw new Error("Not all mocked endpoints received requests.");
  }
});

test("fetches data from third-party API", async () => {
  nock("http://third-party-api.com")
    .get("/data")
    .reply(200, { success: true });

  const res = await request(app).get("/my-route").expect(200);
  expect(res.body.externalData).toEqual(true);
});
```

**[DON'T]** Manually mock the HTTP client implementation.
```javascript
// Anti-pattern: Tightly couples the test to `isomorphic-fetch` and obscures network behavior.
const fetch = require("isomorphic-fetch");
jest.mock("isomorphic-fetch");

test("fetches data", async () => {
  fetch.mockResolvedValue({
    json: jest.fn().mockResolvedValue({ success: true })
  });
  
  // App logic...
});
```