@Domain  
These rules MUST trigger whenever the AI is tasked with writing automated tests, configuring CI/CD testing pipelines, designing QA strategies, writing mock or stub servers, managing API contracts between services, troubleshooting flaky tests, or setting up developer testing environments within a microservice architecture.

@Vocabulary

*   **Brian Marick’s Testing Quadrant:** A categorization system splitting tests into technology-facing (aiding developers) vs. business-facing (aiding non-technical stakeholders), and automated vs. manual/exploratory.
*   **Test Pyramid (Mike Cohn):** A model dictating the proportion and scope of automated tests: a large base of fast, small-scoped Unit Tests, a middle layer of Service Tests, and a tiny peak of slow, broad-scoped End-to-End (E2E) Tests.
*   **Test Snow Cone / Inverted Pyramid:** An anti-pattern where a system has little to no small-scoped tests and relies almost entirely on slow, brittle large-scoped E2E tests.
*   **Unit Tests:** Technology-facing, highly localized tests covering a single function or method without launching microservices or establishing network/file connections.
*   **Service Tests:** Tests targeting a single microservice's capabilities while bypassing the UI. All external collaborators (other microservices) MUST be stubbed out.
*   **End-to-End (E2E) Tests:** Tests covering multiple deployed microservices, typically driving a GUI or full system interaction.
*   **Stub:** A fake downstream collaborator that returns canned, pre-defined responses to known requests. It does not verify if or how many times it was called.
*   **Mock:** A fake downstream collaborator that enforces expectations (e.g., asserts that a specific call was made exactly once).
*   **Mountebank:** A recommended over-the-wire stub/mock server appliance programmable via HTTP.
*   **Flaky Tests:** Tests that exhibit non-determinism, failing intermittently due to environmental factors, race conditions, or timeouts rather than broken functionality.
*   **Normalization of Deviance:** The human tendency to become accustomed to broken things (like flaky tests) and accept them as normal.
*   **Fan-In:** A CI pipeline stage where successful builds of multiple independent microservices trigger a shared downstream E2E test stage.
*   **Metaversion:** An anti-pattern in microservices where multiple independent services are tied to a single overarching version number, eliminating independent deployability.
*   **Consumer-Driven Contracts (CDCs):** An integration testing approach where the consumer of an API writes tests defining its expectations, which are then used to verify the producer's compliance (e.g., using Pact).
*   **Mean Time Between Failures (MTBF):** A metric measuring the time between system breakdowns.
*   **Mean Time To Repair (MTTR):** A metric measuring the speed of recovery from a system failure.
*   **Testing in Production:** Safe, post-deployment testing techniques including synthetic transactions, smoke tests, parallel runs, and canary releases.
*   **Synthetic Transactions:** Fake user interactions injected into a live production system to semantically monitor system health.
*   **Cross-Functional Requirements (CFR):** Non-functional system properties (e.g., latency, throughput, accessibility, security) that must be tested, often via performance or robustness testing.

@Objectives

*   Optimize for rapid feedback cycles by pushing test coverage as far down the Test Pyramid as possible.
*   Enforce absolute isolation in Service Tests by replacing all external network calls with stubs.
*   Eradicate non-determinism by immediately fixing, isolating, or deleting flaky tests.
*   Guarantee independent deployability by replacing cross-team, shared E2E tests with Consumer-Driven Contracts (CDCs).
*   Prioritize MTTR (fast recovery and rollback) over MTBF (attempting to catch 100% of bugs pre-production).
*   Implement safe, automated Testing in Production to monitor actual system semantics rather than relying solely on pre-production environments.

@Guidelines

**Test Pyramid & Scope Limitations**

*   The AI MUST ensure an order of magnitude more tests exist as it descends the test pyramid (Unit > Service > E2E).
*   When a broad-scoped test (Service or E2E) fails due to a bug, the AI MUST write a smaller-scoped Unit Test to catch that specific breakage in the future.
*   The AI MUST NOT create "Test Snow Cones" (heavy reliance on E2E tests with few unit tests).

**Unit Testing Rules**

*   The AI MUST write unit tests to cover isolated, single-function/method behavior.
*   The AI MUST NOT launch microservices, spin up databases, or make external network/filesystem calls within Unit Tests.

**Service Testing & Stubbing Rules**

*   The AI MUST test individual microservices in complete isolation.
*   The AI MUST replace all external microservice collaborators with stubs or fakes.
*   The AI MUST explicitly favor Stubs (returning canned data) over Mocks (validating call execution/counts) to prevent brittle tests.
*   The AI MUST treat the microservice under test as a black box accessed via its network API, bypassing the UI.

**End-to-End (E2E) Testing Constraints**

*   The AI MUST treat E2E tests as a last resort due to their brittleness, long execution times, and tendency to cause deployment pile-ups.
*   The AI MUST NOT assign ownership of an E2E test suite to a centralized "Testing Team." The team that builds the software MUST write and own the tests.
*   The AI MUST NOT allow "metaversioning" (deploying/testing all microservices in lockstep as a single versioned entity).
*   The AI MUST immediately target flaky tests for removal, rewriting, or isolation. Do not allow non-deterministic tests to remain in the CI suite.

**Consumer-Driven Contracts (CDCs)**

*   The AI MUST replace multi-service E2E integration tests with CDCs (using tools like `Pact`) to detect semantic contract breakages.
*   The AI MUST instruct the consumer microservice to generate the contract (e.g., a JSON specification) and instruct the producer microservice to validate against that contract in its own isolated CI build.

**Developer Experience (Local Testing)**

*   The AI MUST configure local development environments so that developers only need to run the specific microservice they are modifying.
*   The AI MUST configure local stubs (e.g., using `mountebank`) for all downstream dependencies to ensure lightning-fast local developer feedback.
*   The AI MUST NOT force developers to spin up the entire microservice ecosystem locally.

**Testing in Production & Semantic Monitoring**

*   The AI MUST implement Semantic Monitoring by writing Synthetic Transactions (automated scripts injecting fake user interactions into production).
*   The AI MUST ensure Synthetic Transactions are safely isolated (e.g., using test accounts) so they do not taint production data analytics or trigger real-world side effects (e.g., shipping physical products).
*   The AI MUST utilize correlation IDs in all tests that span multiple services or execute in production to trace test execution paths.

**Cross-Functional Requirements (CFRs)**

*   The AI MUST implement performance tests (load/latency) based on specific Service-Level Objectives (SLOs) (e.g., 90th percentile response time under X load).
*   The AI MUST run CFR tests continuously, failing builds if performance degrades beyond acceptable delta thresholds.
*   The AI MUST write robustness tests that intentionally simulate network timeouts and unreachable downstream stubs to verify that Circuit Breakers and bulkheads function correctly.

@Workflow

1.  **Determine Test Scope:** Upon receiving a testing task, evaluate the target behavior. Force the test into the lowest possible layer of the Test Pyramid (Unit > Service > CDC > E2E).
2.  **Unit Implementation:** Write technology-facing unit tests for all business logic, strictly mocking/stubbing all out-of-process boundaries.
3.  **Service Isolation:** When writing Service Tests, write a deployment configuration that launches the single microservice alongside a stub server (e.g., `mountebank`). Program the stub server to return required HTTP/RPC responses.
4.  **Contract Generation:** If testing an integration between Service A (Consumer) and Service B (Producer), generate a Consumer-Driven Contract using `Pact`. Add the verification step to Service B's CI pipeline.
5.  **Flakiness Eradication:** If analyzing a failing CI pipeline, identify tests that fail intermittently. Isolate them, rewrite them to remove asynchronous race conditions, or delete them and replace them with smaller-scoped tests.
6.  **Production Readiness:** Draft a Synthetic Transaction script to be run periodically in production. Ensure the script authenticates as a dedicated "Test User" and cleans up its own state.
7.  **Performance Baseline:** Construct load tests tailored to defined SLOs. Add assertions that fail the pipeline if latency exceeds the target percentile.

@Examples (Do's and Don'ts)

**Test Pyramid Balance**  
\[DO\] Write a test suite comprising 2,000 unit tests, 150 service tests, and 5 E2E smoke tests.  
\[DON'T\] Write an inverted "Test Snow Cone" containing 0 unit tests and 500 slow UI-driven E2E tests.

**Service Testing & Stubs**  
\[DO\] Configure a `mountebank` imposter to return `{"balance": 15000}` when `GET /loyalty/123` is called, allowing the Customer service to be tested in isolation.  
\[DON'T\] Write a mock that explicitly fails the test if `GET /loyalty/123` is called twice instead of once, creating a brittle test tied to internal implementation details.

**Handling Flaky Tests**  
\[DO\] Quarantine or delete a test that occasionally fails due to network latency, replacing it with a localized unit test.  
\[DON'T\] Rerun a failing CI pipeline multiple times hoping the flaky test turns green, normalizing deviance.

**Microservice Integration Testing**  
\[DO\] Use `Pact` to define the Helpdesk UI's expectations of the Customer API, and run those pacts during the Customer API's independent CI build.  
\[DON'T\] Maintain a shared E2E test repository where changes from the Web team frequently break the API team's builds.

**Developer Testing Environment**  
\[DO\] Provide a `docker-compose` or script that spins up the active microservice and a lightweight stub container simulating the rest of the ecosystem.  
\[DON'T\] Require a developer to pull and build 30 distinct repositories just to run tests for a single microservice locally.

**Testing in Production**  
\[DO\] Run a scheduled background job in production that creates a user named `test_synthetic_user`, adds a fake item to the cart, verifies the cart total, and deletes the user.  
\[DON'T\] Run an automated E2E test in production that purchases real items and triggers actual fulfillment/shipping logic.