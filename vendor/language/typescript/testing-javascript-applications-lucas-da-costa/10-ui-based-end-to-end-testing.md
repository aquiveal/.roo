@Domain
These rules are triggered when the AI is tasked with defining a software testing strategy, choosing end-to-end (E2E) testing frameworks, or writing/architecting tests that interact with an application's Graphical User Interface (GUI). This applies specifically when differentiating between UI tests, E2E tests, and UI-based E2E tests, or when evaluating tools like Cypress, Puppeteer, or Selenium.

@Vocabulary
- **End-to-End (E2E) Tests**: Tests that validate an application as a whole, from an engineering perspective, covering the entire software stack.
- **UI Tests**: Tests that validate an application exclusively through its User Interface. They do not necessarily cover the entire stack (e.g., they may use a mocked backend).
- **UI-Based End-to-End Tests**: Tests at the intersection of UI and E2E testing. They cover the entire application stack by interacting with the software strictly through its user-facing GUI.
- **Acceptance Tests**: Tests focused on validating whether the application works from a business/customer perspective (functional requirements). UI-based E2E tests often serve as acceptance tests.
- **Black Box Tests**: Tests that do not know about or rely on an application's internal code or implementation details.
- **JSON Wire Protocol**: A protocol used by Selenium that specifies a set of HTTP routes for handling different actions to be performed within a browser.
- **Webdriver**: A program (e.g., ChromeDriver, Geckodriver) that receives Selenium's commands and performs the necessary actions within a real browser using remote-control APIs.
- **Chrome DevTools Protocol**: The protocol used by Puppeteer to directly control Chrome and Chromium browsers.
- **Time-Travel**: A debugging feature in Cypress that takes snapshots of the application state as it carries out test actions, allowing developers to visually step through the test.

@Objectives
- Accurately categorize and scope tests into Pure UI, Pure E2E, and UI-based E2E based on the software boundaries.
- Position UI-based E2E tests at the very top of the testing pyramid, prioritizing them for critical, labor-intensive features.
- Select the optimal testing tool based on architectural needs, defaulting to Cypress for its built-in testing utilities and debugging features, while reserving Selenium/Puppeteer for specific edge cases.
- Maximize test reliability by avoiding flaky patterns and leveraging the native architectures of modern testing tools (e.g., event-driven architectures and built-in retriability).

@Guidelines
- **Test Classification & Scoping**:
  - The AI MUST NOT conflate UI tests with E2E tests. 
  - When writing "UI-based E2E tests", the AI MUST ensure the test covers BOTH the frontend and the real backend. The AI MUST NOT mock backend responses or use stubbed APIs for this specific category of tests.
  - When writing "Pure E2E tests" for a backend, the AI MUST interact with the application via its provided interfaces (e.g., RESTful HTTP API) without involving the GUI.
  - When writing "Pure UI tests", the AI MUST use testing frameworks (like Jest/JSDOM) to run tests quickly, reserving real-browser execution only for cases requiring browser-specific features or visual regression testing.
- **Timing of Test Implementation**:
  - The AI MUST NOT write UI-based E2E tests during the iterative, early development phases of a feature.
  - The AI MUST write UI-based E2E tests ONLY AFTER implementing complete pieces of functionality to avoid constant maintenance overhead.
- **Prioritization**:
  - The AI MUST justify the creation of a UI-based E2E test based on three factors: how critical the feature is, how labor-intensive manual validation would be, and the cost of automation. Non-essential features MUST be tested lower in the pyramid (e.g., Pure UI tests).
- **Tool Selection Strategy**:
  - **Cypress (Default)**: The AI MUST default to recommending and using Cypress for UI-based E2E testing. The AI MUST leverage its built-in test runner, assertion libraries, and automatic retriability.
  - **Selenium/WebdriverIO/Nightwatch**: The AI MUST recommend Selenium-based tools ONLY if the project strictly requires cross-browser support outside of Edge, Chrome, and Firefox (e.g., Internet Explorer), or if the primary goal is generalized browser automation rather than just testing.
  - **Puppeteer**: The AI MUST recommend Puppeteer ONLY when the project exclusively targets Chrome/Chromium and requires deep browser automation, and MUST pair it with a framework like Jest-Puppeteer if testing is required.
- **Anti-Flakiness**:
  - The AI MUST NOT use fixed-time delays (explicit sleeps) to wait for elements or actions. Instead, the AI MUST rely on the event-driven architecture of Puppeteer or the built-in retriability of Cypress.

@Workflow
1. **Analyze the Request**: Determine if the user is asking for a Pure UI test (component/interface only), a Pure E2E test (backend API), or a UI-based E2E test (full stack via browser).
2. **Evaluate Feature Readiness**: Ensure the feature being tested is fully implemented before drafting UI-based E2E tests.
3. **Assess Value vs. Cost**: Verify that the feature's criticality warrants a top-of-pyramid UI-based E2E test. If it is a trivial UI component, step down to a JSDOM/React-Testing-Library test.
4. **Select the Tool**: 
   - Choose Cypress unless the user explicitly requires Internet Explorer support (use Selenium) or non-testing Chrome automation (use Puppeteer).
5. **Architect the Test**:
   - Treat the application as a Black Box.
   - Do not inject mocks for the backend or database unless requested for a strictly "Pure UI" test.
   - Rely on the tool's native polling/retriability instead of hardcoded timeouts.

@Examples (Do's and Don'ts)

- **[DO]** Write UI-based E2E tests that interact with the real backend stack through the GUI.
```javascript
// Cypress (UI-based E2E)
describe('Checkout Flow', () => {
  it('successfully processes an order through the full stack', () => {
    // Interacts with the real UI, which hits the real backend database
    cy.visit('/checkout');
    cy.get('input[name="cardNumber"]').type('4000000000000000');
    cy.get('button[type="submit"]').click();
    // Relies on built-in retriability, no explicit waits
    cy.contains('Order Successful').should('be.visible'); 
  });
});
```

- **[DON'T]** Mock the backend when the explicit goal is a UI-based End-to-End test.
```javascript
// ANTI-PATTERN for UI-based E2E (This degrades into a Pure UI test)
describe('Checkout Flow', () => {
  it('successfully processes an order', () => {
    // MOCKING the backend violates the "End-to-End" full-stack requirement
    cy.intercept('POST', '/api/checkout', { statusCode: 200, body: { success: true } });
    cy.visit('/checkout');
    cy.get('button[type="submit"]').click();
    cy.contains('Order Successful').should('be.visible'); 
  });
});
```

- **[DO]** Choose the right tool for the required browser matrix.
```markdown
*Recommendation*: Since your application requires strict support for legacy Internet Explorer 11 alongside modern browsers, we MUST use a Webdriver-based tool such as WebdriverIO or Selenium rather than Cypress.
```

- **[DON'T]** Use Selenium manually without a test runner for testing purposes.
```javascript
// ANTI-PATTERN: Using raw selenium-webdriver without a testing framework like Jest/Mocha
const {Builder, By} = require('selenium-webdriver');
(async function test() {
  let driver = await new Builder().forBrowser('chrome').build();
  await driver.get('http://localhost:8080');
  await driver.findElement(By.id('submit')).click();
  // No assertions, no test runner, manual management of the driver
})();
```