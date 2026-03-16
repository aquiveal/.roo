# @Domain
Trigger these rules when writing test code, configuring CI/CD test pipelines, designing testing architectures, writing test doubles (stubs/mocks), or refactoring existing test suites for microservice-based applications.

# @Vocabulary
- **Brian Marick’s Testing Quadrant**: A categorization of tests divided into Technology-Facing (unit, property), Business-Facing (end-to-end, manual exploratory), supporting programming, and critiquing the project.
- **Mike Cohn’s Test Pyramid**: A model dictating the proportion of automated tests. Base = Unit (fast, highly isolated, high volume), Middle = Service (isolated to one service, stubs dependencies), Top = End-to-End (slow, brittle, high confidence, low volume).
- **Test Snow Cone (Inverted Pyramid)**: An anti-pattern where a system has little to no small-scoped unit tests and relies entirely on large-scoped end-to-end tests.
- **Unit Test**: A test scoped to a single function or method call that does not launch microservices or hit external networks/files. 
- **Service Test**: A test designed to bypass the UI and test a single microservice's capabilities in complete isolation by stubbing all external collaborators.
- **End-to-End (E2E) Test**: A test run against the entire system routing through multiple microservices. High confidence, but slow and brittle.
- **Integration Test**: An overloaded, ambiguous term. MUST be explicitly redefined as either a Service Test or an End-to-End test.
- **Test Double**: The overarching term for fakes, spies, dummies, stubs, and mocks (per Gerard Meszaros).
- **Stub**: A test double that responds with canned data to known requests. It does not verify how many times it was called.
- **Mock**: A test double that verifies that specific interactions (e.g., call counts) occurred.
- **Mountebank**: A programmable software appliance/stub server (via HTTP) used to create "imposters" to mock protocols like TCP, HTTP, HTTPS, and SMTP.
- **Flaky Test**: A non-deterministic test that occasionally fails due to external factors (networks, threads) rather than broken functionality. 
- **Normalization of Deviance**: The human tendency to accept failing/flaky tests as "normal" over time, destroying trust in the test suite.
- **Fan-in Pipeline**: A CI/CD architecture where successful builds of multiple individual microservices trigger a shared downstream End-to-End test stage.
- **Metaversion**: An anti-pattern where changes across multiple services are versioned and deployed together to satisfy E2E tests, destroying independent deployability.
- **Consumer-Driven Contracts (CDCs)**: Tests written by a consumer microservice defining expectations of a producer microservice's API. Used to detect semantic breakages without E2E testing.
- **Pact**: An open-source tool for implementing CDCs. It generates a JSON specification of consumer expectations and acts as a local stub server.
- **Pact Broker**: A centralized repository to store and version CDC Pact JSON files, allowing producers to verify contracts against multiple consumer versions.
- **MTBF (Mean Time Between Failures)**: A metric measuring how long a system runs before failing. Traditional testing optimizes for this.
- **MTTR (Mean Time To Repair)**: A metric measuring how fast a system recovers. In-production testing and fast rollbacks optimize for this.
- **Synthetic Transactions**: Fake user behavior injected into a live production system with known inputs and expected outputs to verify system health.
- **Cross-Functional Requirements (CFRs)**: System properties like latency, security, and scalability. Replaces the term "non-functional requirements".

# @Objectives
- Optimize test suites for the fastest possible feedback cycles by pushing test coverage as low down the Test Pyramid as possible.
- Ensure strict independent testability of microservices; developers MUST NOT need to run the entire system locally to test their service.
- Eradicate flaky, brittle, and non-deterministic tests to prevent the normalization of deviance.
- Replace slow, cross-team End-to-End tests with explicit schemas and Consumer-Driven Contracts (CDCs).
- Safely extend testing into production via synthetic transactions, prioritizing MTTR (recovery) over MTBF (prevention).

# @Guidelines
### Test Pyramid & Scope Constraints
- The AI MUST optimize test suites according to the Test Pyramid: heavy volume of Unit Tests, moderate Service Tests, and minimal End-to-End Tests.
- If an End-to-End test fails, the AI MUST attempt to reproduce the failure via a smaller-scoped Service or Unit test to speed up future feedback.
- The AI MUST NOT use or accept the term "Integration Test" without asking for clarification; it MUST define the test explicitly as a Service Test or an End-to-End Test.
- The AI MUST avoid generating the "Test Snow Cone" anti-pattern (relying heavily on E2E testing).

### Service Testing & Isolation
- When generating Service Tests, the AI MUST isolate the microservice completely. All external downstream microservices and network calls MUST be stubbed out.
- The AI MUST prefer Stubs (returning canned data) over Mocks (verifying call counts) in Service Tests to prevent brittle tests. Mocks SHOULD ONLY be used to verify expected state-changing side effects (e.g., verifying a credit was issued).
- The AI MUST recommend `mountebank` for stubbing downstream HTTP/HTTPS/TCP/SMTP interactions.
- The AI MUST only require the developer to run the specific microservice they are currently working on locally, using stubs for the rest of the architecture.

### End-to-End (E2E) Testing
- The AI MUST NOT create "Metaversions" (versioning multiple independent microservices as a single release entity) to satisfy E2E test environments.
- The AI MUST immediately identify and target Flaky Tests for eradication, quarantine, or refactoring. The AI MUST NOT implement "retry" loops in tests as a substitute for fixing non-determinism.
- The AI MUST avoid threaded or sleep-based timing dependencies in test assertions to prevent race conditions.
- The AI MUST NOT assign ownership of E2E tests to a dedicated testing team; tests MUST be owned by the stream-aligned teams writing the code.

### Consumer-Driven Contracts (CDCs)
- The AI MUST replace cross-boundary E2E functional API verification with Consumer-Driven Contracts using tools like `Pact`.
- When generating a CDC, the AI MUST write the consumer expectation first, utilize the generated local stub server, and output the expectation as a serialized contract (e.g., a Pact JSON file).
- The AI MUST instruct the producer microservice to pull consumer contracts (e.g., via Pact Broker) and run them as part of its isolated CI build to catch semantic breakages early.

### In-Production & Cross-Functional Testing
- The AI MUST use the term "Cross-Functional Requirements (CFRs)" instead of "Non-functional requirements".
- The AI MUST generate Performance Tests that measure specific percentiles (e.g., "90th-percentile response time < 2s at 200 concurrent connections") rather than vague load tests.
- The AI MUST write Robustness Tests that intentionally inject faults (e.g., network timeouts) to verify circuit breakers and fail-fast mechanisms.
- The AI MUST generate safe Synthetic Transactions for production semantic monitoring (e.g., injecting a fake order using a designated test account that does not trigger physical shipping/billing).

# @Workflow
1. **Analyze Test Scope**: When asked to test a feature, the AI MUST first determine the lowest possible level on the Test Pyramid where the feature can be confidently verified (Unit > Service > E2E).
2. **Implement Unit Tests**: Write fast, single-function tests prioritizing algorithmic logic and internal state.
3. **Implement Service Tests**: 
   - Deploy the single microservice in isolation.
   - Configure `mountebank` (or similar tools) to provide canned stub responses for all downstream network calls.
   - Execute tests against the isolated service API.
4. **Define Contract (CDC)**: If the microservice consumes external APIs, write consumer expectations using `Pact`. Ensure the generated JSON contract is available to the producer's CI pipeline.
5. **Eradicate Flakiness**: Review the test suite for race conditions, sleep statements, and multi-process dependencies. Remove or rewrite non-deterministic tests immediately.
6. **Production Testing Design**: Implement a synthetic transaction or smoke test script that safely verifies the core domain logic against the live production environment.

# @Examples (Do's and Don'ts)

### Test Scope & Naming
- **[DO]**: Name test directories and suites explicitly: `unit/`, `service/`, `e2e/`.
- **[DON'T]**: Create a generic `integration_tests/` folder without defining whether it isolates the service or tests the entire network topology.

### Service Test Isolation
- **[DO]**: Use a local stub server to provide canned responses for downstream dependencies during a Service Test.
  ```javascript
  // DO: Use mountebank or similar to stub downstream responses
  await mountebank.createImposter({
    port: 4545,
    protocol: 'http',
    stubs: [{
      predicates: [{ equals: { path: '/loyalty/123' } }],
      responses: [{ is: { statusCode: 200, body: { points: 15000 } } }]
    }]
  });
  // Execute test against local service pointing to port 4545
  ```
- **[DON'T]**: Launch multiple real microservices to test a single service's logic.
  ```javascript
  // DON'T: Rely on the real downstream loyalty service in a service test
  const loyaltyService = require('../../loyalty-service/start');
  await loyaltyService.start({ port: 4545 }); 
  ```

### Mocks vs. Stubs
- **[DO]**: Use stubs to provide necessary data to the system under test without caring about implementation details.
- **[DON'T]**: Over-mock by asserting the exact number of times a dependency was called, unless verifying a specific business side-effect (like emitting a billing event).
  ```javascript
  // DON'T: Brittle mock verification that breaks on internal refactoring
  expect(mockLoyaltyService.getBalance).toHaveBeenCalledTimes(1); 
  ```

### Consumer-Driven Contracts
- **[DO]**: Use Pact to define the consumer's expectations and generate a contract.
  ```javascript
  // DO: Pact consumer test defining the contract
  provider.addInteraction({
    state: 'customer 123 exists',
    uponReceiving: 'a request for customer details',
    withRequest: { method: 'GET', path: '/customer/123' },
    willRespondWith: { status: 200, body: { email: 'sam@magpiebrain.com' } }
  });
  ```
- **[DON'T]**: Rely on heavy E2E GUI tests to verify that API payloads haven't changed semantically between two microservices.

### Production Testing
- **[DO]**: Inject explicitly marked synthetic transactions into production to verify system health.
  ```javascript
  // DO: Synthetic transaction using a safe test account
  const response = await api.post('/orders', { 
    customerId: 'SYNTHETIC_TEST_USER_001', 
    item: 'CD_01' 
  });
  expect(response.status).toBe(201);
  ```
- **[DON'T]**: Run tests in production that mutate real user data or trigger irreversible real-world side effects (e.g., shipping a physical item).

### Dealing with Flaky Tests
- **[DO]**: Immediately quarantine or delete a test that passes 90% of the time and fails 10% of the time, replacing it with a smaller-scoped, deterministic test.
- **[DON'T]**: Accept "Normalization of Deviance" by wrapping tests in retry blocks.
  ```javascript
  // DON'T: Masking flaky architecture with retries
  jest.retryTimes(3); 
  test('Places order end-to-end', async () => { ... });
  ```