# @Domain
These rules are triggered when the AI is asked to write, modify, configure, or review UI-based end-to-end (E2E) tests. Activation occurs specifically when interacting with Cypress (`cypress.json`, `cypress/integration/**/*.spec.js`, `cypress/support/*`), setting up cross-browser test execution, configuring automated visual regression testing (e.g., Percy), or applying E2E design patterns like Page Objects and Application Actions.

# @Vocabulary
*   **UI-Based End-to-End Test**: A test that covers an entire application's software stack by interacting with the application through its Graphical User Interface (GUI) in a real browser environment.
*   **Cypress**: A testing tool that directly interfaces with a browser’s remote-control APIs to find elements and carry out actions, running entirely within the browser while spawning a Node.js process for backend tasks.
*   **Flaky Test**: A nondeterministic test that may fail sometimes and succeed at other times without any changes to the application code, usually caused by timing issues, unmocked uncontrollable factors, or shared state.
*   **Deterministic Test**: A test that, given the same unit under test and the same initial conditions, will always yield the exact same result.
*   **Page Object**: A design pattern that encapsulates a page's selectors and interactions into a separate module (usually a static class). Tests use these objects in terms of what they do, abstracting away the page's HTML structure.
*   **Application Action (App Action)**: A pattern where tests directly invoke the application's internal functions (exposed to the `window` object) to bypass the UI for fast test setup, decoupling tests from UI elements that are not currently under test.
*   **Cypress Command Queue**: The mechanism by which Cypress serializes actions. Commands like `cy.get()` and `cy.click()` do not return promises; they immediately queue actions that are executed serially by Cypress.
*   **Visual Regression Testing**: A testing technique that compares image snapshots of an application's UI against approved baseline snapshots to catch unintended visual inconsistencies.
*   **Percy**: A third-party tool integrated with Cypress to automate visual regression testing and manage snapshot approvals.
*   **Fixture / Pristine State**: The baseline scenario set up before tests run, usually achieved by truncating database tables to ensure tests do not interfere with one another.

# @Objectives
*   Ensure all UI-based E2E tests are strictly deterministic, executing reliably without flakiness.
*   Decouple test semantics from HTML structure to minimize maintenance costs when the UI changes.
*   Simulate user behaviors accurately without using test doubles for internal application code.
*   Accelerate test execution by bypassing repetitive UI workflows using Application Actions during the setup/arrange phase.
*   Catch visual regressions automatically while ignoring dynamic, uncontrollable UI data (like timestamps).
*   Enforce a pristine initial state before every single test execution to prevent test pollution.

# @Guidelines

## 1. Test Environment & Configuration
*   **Use `baseUrl`**: Always define `"baseUrl"` in `cypress.json` to avoid hardcoding the application's host and port in every `cy.visit()` call.
*   **Separate Databases for Tests**: E2E tests MUST run against a dedicated testing database (e.g., using `NODE_ENV=development` or `test`), never production or a shared local dev database.
*   **Node System Execution**: When integrating Node.js database drivers (like `sqlite3` and `knex`) inside Cypress plugins, MUST set `"nodeVersion": "system"` in `cypress.json` to avoid Electron compatibility build issues.
*   **Fetch Interception**: To allow Cypress to intercept the native browser `fetch` API, MUST set `"experimentalFetchPolyfill": true` in `cypress.json` (or use the equivalent intercept method in modern Cypress versions as applicable, adhering to the principle of tracking external network calls).

## 2. Establishing Pristine State
*   **Never Mock Internal APIs**: Do not mock the internal server responses for fetching or adding items in E2E tests. Simulate user actions and let the request hit the real backend.
*   **Truncate Database**: Enforce deterministic states by emptying/truncating the database before each test. Use `cy.task` to invoke a Node.js script in `cypress/plugins/index.js` that connects to the database via `knex` and truncates the tables. Use `beforeEach(() => cy.task("emptyDatabase"))`.
*   **Seed via HTTP/App Actions**: Use HTTP requests (wrapped in custom Cypress commands via `Cypress.Commands.add`) or Application Actions to quickly seed data or achieve an initial state, bypassing the UI.

## 3. Cypress Execution Mechanics
*   **Commands Are Not Promises**: Do NOT use `async`/`await` with Cypress commands. Cypress queues commands synchronously and executes them serially.
*   **Do Not Rely on Synchronous Side Effects**: Code placed after a Cypress command (like `console.log("here")`) will execute immediately before the Cypress command is actually run. Chain using `.then()` if execution must occur after a Cypress command finishes.

## 4. Selecting Elements and Asserting
*   **Resilient Selectors**: Find elements using characteristics integral to what the element is (e.g., placeholders, button text, explicit `data-testid`). Do NOT use brittle CSS hierarchies (e.g., `body > div > ul > li:nth-child(2)`).
*   **Implicit Assertions**: Rely on Cypress's built-in retriability. `cy.get()` and `cy.contains()` automatically assert that elements exist and will retry until the timeout.
*   **Action Log/Multiple Elements**: When finding elements that may exist multiple times (like a history log), use explicit assertions (e.g., `.should("have.length", 2)`) to ensure Cypress correctly waits for the exact number of elements.

## 5. Page Objects Pattern
*   **Centralize Selectors**: Encapsulate DOM interactions inside static methods of a class (e.g., `class InventoryManagement { static addItem(...) }`).
*   **Stateless Page Objects**: Page objects MUST NOT store state. Use static methods only. Stateful page objects introduce flakiness across test executions.
*   **Reuse Internal Methods**: A Page Object method should reuse other methods within the same Page Object to minimize updates if a selector changes (e.g., `static addItem()` calls `InventoryManagement.enterItemName()`).

## 6. Application Actions Pattern
*   **Expose App Methods**: In the application code, expose vital state-altering functions to the `window` object strictly for testing purposes. Wrap this exposure in an `if (window.Cypress)` block to avoid polluting production environments.
*   **Use for Setup**: Invoke Application Actions via `cy.window().then((w) => w.handleAction())` during the Arrange step of a test to quickly bypass UI workflows that are already tested elsewhere (e.g., bypassing a login form or rapidly populating an inventory).
*   **Do Not Replace Core UI Tests**: Do not use Application Actions exclusively. The core interactions a user takes MUST be tested via the UI. Use Application Actions only to reduce test overlap and execution time.

## 7. Eliminating Flakiness
*   **NEVER Use `cy.wait(Number)`**: Do NOT wait for a fixed amount of time (e.g., `cy.wait(2000)`). This is strictly prohibited.
*   **Wait for Conditions/Routes**: Wait for application states (elements appearing in the DOM) or alias HTTP requests using `cy.server()`, `cy.route()`, and `cy.as()`. Use `cy.wait('@aliasName')` to pause test execution precisely until an external condition is met.
*   **Stub Uncontrollable Factors**:
    *   *Time*: Use `cy.clock()` and `cy.tick()` to fast-forward time deterministically instead of waiting for `setTimeout` or `setInterval`.
    *   *External/Third-Party APIs*: Use `cy.route` to intercept requests to external APIs (e.g., Recipe Puppy API) and supply canned responses. Do NOT let tests fail due to third-party network outages.
    *   *Indeterministic Functions*: Use `cy.stub(window.Math, 'random').returns(0.5)` to fix uncontrollable functional outputs.
*   **Retries (Provisional Only)**: Configure test retries (`retries: { runMode: 3, openMode: 0 }`) in `cypress.json` ONLY as a short-term workaround for flakiness when pushing against strict deadlines. It must not be a permanent architectural strategy.

## 8. Visual Regression Testing
*   **Tooling**: Use Percy (`@percy/cypress`) via the `cy.percySnapshot()` command.
*   **Hide Dynamic Data**: When capturing visual snapshots, dynamic uncontrollable data (e.g., timestamps in an action log) will cause false positive failures. MUST use CSS media queries (`@media only percy { ... visibility: hidden; }`) within the application to hide dynamic content strictly from Percy snapshots.

# @Workflow
When developing a UI-based E2E test, the AI must follow this rigid algorithm:
1.  **Preparation**: Identify the specific user workflow to test. Add necessary tasks in `cypress/plugins/index.js` to clear the test database.
2.  **State Initialization (Arrange)**: Start the test block with a `beforeEach()` hook that invokes the database clear task (`cy.task('emptyDatabase')`).
3.  **Setup Bypass (Arrange)**: If the test requires preconditions (like logged-in state or existing items), use Application Actions (via `cy.window()`) or Custom Commands invoking API requests to quickly establish state. Do not use the UI to set up state if that UI is already tested in a dedicated file.
4.  **Stub Uncontrollable Systems (Arrange)**: Call `cy.clock()`, `cy.stub()`, or `cy.route()` to freeze time, fix randomness, and intercept third-party APIs.
5.  **Execution (Act)**: Use stateless, static Page Object methods to perform the core workflow interactions (e.g., `InventoryPage.submitItem(...)`).
6.  **Synchronization (Wait)**: If an asynchronous backend operation occurs, use `cy.wait('@routeAlias')` or `cy.contains()` to let Cypress automatically retry until the application reacts.
7.  **Verification (Assert)**: Use Page Object methods or Cypress assertions (`.should()`) to verify the exact UI change or state reflection.
8.  **Visual Verification**: If visual regression is required, invoke `cy.percySnapshot('Snapshot Name')`.

# @Examples (Do's and Don'ts)

## Waiting for Application State
*   **[DON'T]** Wait for fixed time periods:
    ```javascript
    cy.get('.submit-btn').click();
    cy.wait(3000); // ANTI-PATTERN: Fixed time wait
    cy.get('.success-msg').should('be.visible');
    ```
*   **[DO]** Wait for aliased routes or explicit DOM conditions:
    ```javascript
    cy.server();
    cy.route('POST', '/api/inventory').as('addItemReq');
    cy.get('button').contains('Add to inventory').click();
    cy.wait('@addItemReq'); // Wait exactly for the request to resolve
    cy.contains('p', 'Item successfully added');
    ```

## Page Objects
*   **[DON'T]** Repeat CSS selectors in test files, or store state in a Page Object class:
    ```javascript
    // ANTI-PATTERN: Inline selectors and repetition
    it('adds item', () => {
      cy.get('input[placeholder="Name"]').type('Cake');
      cy.get('.btn-primary').click();
    });
    ```
*   **[DO]** Encapsulate inside stateless static classes using resilient selectors:
    ```javascript
    export class InventoryPage {
      static enterName(name) {
        return cy.get('input[placeholder="Item name"]').clear().type(name);
      }
      static submit() {
        return cy.contains('button', 'Add to inventory').click();
      }
      static addItem(name) {
        InventoryPage.enterName(name);
        InventoryPage.submit();
      }
    }
    ```

## Application Actions
*   **[DON'T]** Use the UI to set up state in a test verifying a different feature (e.g., using the UI to add items just so you can test the "Undo" button).
*   **[DO]** Expose the handler and use it via `cy.window()`:
    ```javascript
    // Application Code
    if (window.Cypress) {
      window.handleAddItem = handleAddItem;
    }

    // Test Code
    it('can undo submitted items', () => {
      InventoryPage.visit();
      cy.window().then((win) => win.handleAddItem('cheesecake', 10)); // App Action
      InventoryPage.undo();
      cy.contains('li', 'cheesecake - Quantity: 10').should('not.exist');
    });
    ```

## Stubbing Third-Party APIs
*   **[DON'T]** Let tests communicate with external APIs (like Recipe Puppy or Stripe) over the network.
*   **[DO]** Intercept external requests and supply deterministic canned responses:
    ```javascript
    beforeEach(() => {
      cy.server();
      cy.route("GET", "https://api.external-service.com/data", {
        results: [{ href: "http://example.com/always-the-same-url" }]
      });
    });
    ```

## Visual Regression with Percy
*   **[DON'T]** Take snapshots of pages with dynamic timestamps. They will fail every Percy build.
*   **[DO]** Hide dynamic data strictly for the Percy capture environment:
    ```html
    <style>
      @media only percy {
        .dynamic-timestamp {
          visibility: hidden;
        }
      }
    </style>
    ```
    ```javascript
    it('validates UI', () => {
      InventoryPage.visit();
      cy.percySnapshot('Inventory Loaded State');
    });
    ```