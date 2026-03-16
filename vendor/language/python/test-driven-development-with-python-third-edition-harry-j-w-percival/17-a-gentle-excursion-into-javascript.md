# @Domain
These rules MUST be activated when the AI is tasked with implementing, refactoring, debugging, or testing client-side JavaScript behavior within a web application, specifically tasks involving DOM manipulation, event handling, client-side validation UI updates, integrating JavaScript with CSS frameworks (like Bootstrap), and writing JavaScript unit tests using browser-based test runners (like Jasmine).

# @Vocabulary
- **Spiking**: A phase of exploratory coding without tests to learn a new API, tool, or to build a throwaway proof-of-concept.
- **De-spiking**: The process of throwing away spiked code and rewriting it from scratch using rigorous Test-Driven Development (TDD).
- **Jasmine**: A standalone JavaScript behavior-driven development testing framework using `describe`, `it`, and `expect` blocks.
- **SpecRunner**: An HTML file serving as the entry point and test harness for browser-based Jasmine unit tests.
- **DOM Fixture**: HTML elements dynamically created and injected into the test document during test setup (`beforeEach`) to give JavaScript code a sandbox to interact with.
- **Global State Contamination**: The anti-pattern in JavaScript testing where DOM modifications from one test persist and affect the execution of subsequent tests.
- **Initialize Pattern**: An architectural pattern where JavaScript logic is wrapped inside a callable function (e.g., `initialize()`) rather than executing immediately upon script load, ensuring control over execution order.
- **Magic Constants/Hardcoded Selectors**: CSS selectors hardcoded directly into application logic rather than being passed as parameters.
- **Event Dispatching**: Programmatically simulating user actions in tests (e.g., `dispatchEvent(new InputEvent("input"))`).

# @Objectives
- The AI MUST test-drive all JavaScript DOM manipulation and UI state changes.
- The AI MUST rigidly control JavaScript execution order to prevent script execution before the DOM is fully loaded.
- The AI MUST guarantee absolute test isolation in JavaScript test suites by meticulously managing DOM fixtures.
- The AI MUST decouple JavaScript logic from specific HTML structures by parameterizing CSS selectors.
- The AI MUST leverage existing CSS framework methodologies (e.g., class toggling) rather than manually overriding inline styles.

# @Guidelines

### Test Strategy & Spiking
- The AI MAY use "Spiking" (coding without tests) ONLY when explicitly asked to explore a new API.
- If a Spike is performed, the AI MUST explicitly inform the user that this is a Spike and MUST subsequently perform "De-spiking" (removing the code and rebuilding it via TDD).
- Functional Tests (FTs) validating UI visibility MUST use Selenium's `.is_displayed()` method rather than just checking for element presence in the DOM.
- The AI MUST refactor redundant CSS selectors in Selenium FTs into helper methods (e.g., `def get_error_element(self): return self.browser.find_element(...)`).

### JavaScript Testing (Jasmine)
- The AI MUST organize JavaScript tests using `describe("Description", () => { ... })` and `it("should ...", () => { ... })`.
- The AI MUST manage DOM Fixtures safely using `beforeEach` to create/append elements (`document.createElement`, `innerHTML`, `document.body.appendChild`) and `afterEach` to destroy them (`element.remove()`).
- The AI MUST declare fixture variables in the outer `describe` scope using `let` so they can be accessed inside `beforeEach`, `it`, and `afterEach` blocks.
- The AI MUST simulate user input in tests by utilizing `element.dispatchEvent(new InputEvent("input"))`.
- The AI MUST use `checkVisibility()` to assert whether DOM elements are visible (`expect(el.checkVisibility()).toBe(false)`).
- The AI MUST keep each `it` block highly focused, ideally containing a single assertion or testing a single behavior.

### JavaScript Architecture & Execution Order
- The AI MUST NOT place executable DOM manipulation logic directly in the global scope of a `.js` file.
- The AI MUST wrap all setup and event-binding logic in an `initialize` function (e.g., `const initialize = () => { ... };`).
- The AI MUST load JavaScript files at the end of the HTML `<body>` to optimize page load times.
- The AI MUST wrap the call to the `initialize` function inside a `window.onload` callback (e.g., `window.onload = () => { initialize(...); };`) to guarantee the DOM is fully rendered before execution.

### Refactoring & Decoupling
- The AI MUST NOT hardcode CSS selectors (magic constants) inside the `initialize` function.
- The AI MUST pass CSS selectors as arguments to the `initialize` function (e.g., `const initialize = (inputSelector, errorSelector) => { ... }`).
- The AI MUST use template literals / string interpolation (`` `#${inputId}` ``) in tests to share base constants between fixture generation and selector assertions.
- When working with CSS frameworks like Bootstrap, the AI MUST manipulate classes using `classList.remove("classname")` or `classList.add("classname")` instead of manually hacking inline styles (e.g., `style.display = "none"`).

### Debugging
- When facing execution order or global state issues in JavaScript, the AI MUST strategically inject `console.log()` statements in both the source code and the test files to trace the sequence of module loading, fixture creation, and function execution.

# @Workflow
When tasked with adding new client-side behavior:
1. **Write the Functional Test**: Start with a Selenium FT that interacts with the browser and asserts the expected UI state change (e.g., asserting an element `.is_displayed()` is false). See it fail.
2. **Setup JS Test Harness**: If not present, configure the Jasmine `SpecRunner.html` to load the target `.js` file, the testing framework, and required CSS frameworks (like Bootstrap).
3. **Write the JS Smoke Test**: Create a `describe` block. Implement `beforeEach` to build the exact HTML DOM fixture required by the feature, and `afterEach` to remove it. Write a basic `it` test to assert the initial state of the fixture.
4. **Write the Failing JS Unit Test**: Write an `it` block describing the target behavior. Call `initialize()`, dispatch the required event (e.g., `InputEvent`), and `expect()` the new UI state. See it fail.
5. **Implement the Logic**: Write the code inside an exported/accessible `initialize` function. Prefer modifying `classList` over manual style overrides.
6. **Debug Execution Order**: If tests fail unexpectedly (e.g., "element is null"), use `console.log` to verify that fixtures are appended *before* logic executes.
7. **Refactor**: Parameterize hardcoded CSS selectors in the `initialize` function. Update the unit tests to pass these selectors.
8. **Integrate**: Add the `<script>` tags to the bottom of the main HTML template and invoke `initialize()` inside `window.onload`.
9. **Verify**: Run the FT to confirm end-to-end integration passes.

# @Examples (Do's and Don'ts)

### Test Isolation & Fixtures
- **[DO]**
  ```javascript
  describe("UI Behavior", () => {
    let testDiv;
    beforeEach(() => {
      testDiv = document.createElement("div");
      testDiv.innerHTML = `<input id="id_text" /><div class="error">Error</div>`;
      document.body.appendChild(testDiv);
    });
    afterEach(() => {
      testDiv.remove();
    });
    it("should hide error on input", () => {
      // test logic
    });
  });
  ```
- **[DON'T]** Inject fixtures directly into the global DOM without cleaning them up, causing subsequent tests to read stale HTML state.
  ```javascript
  // Anti-pattern: Missing afterEach cleanup
  beforeEach(() => {
    document.body.innerHTML += `<div id="test-fixture">...</div>`; 
  });
  ```

### Execution Order & Architecture
- **[DO]**
  ```javascript
  // my_script.js
  const initialize = (inputSelector, errorSelector) => {
    const textInput = document.querySelector(inputSelector);
    textInput.oninput = () => {
      document.querySelector(errorSelector).classList.remove("is-invalid");
    };
  };

  // HTML Template
  <script src="my_script.js"></script>
  <script>
    window.onload = () => {
      initialize("#id_text", ".error-feedback");
    };
  </script>
  ```
- **[DON'T]** Execute logic globally on load and hardcode selectors.
  ```javascript
  // Anti-pattern: Executes immediately, will crash if DOM isn't ready. Hardcoded selectors.
  document.querySelector("#id_text").oninput = () => {
    document.querySelector(".invalid-feedback").style.display = "none";
  };
  ```

### Functional Test Helper Extraction
- **[DO]**
  ```python
  def get_error_element(self):
      return self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback")

  def test_error_clears(self):
      self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))
  ```
- **[DON'T]** Duplicate long selectors across multiple assertions in the FT.
  ```python
  # Anti-pattern: Duplication
  self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").is_displayed())
  # ... later ...
  self.assertFalse(self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").is_displayed())
  ```