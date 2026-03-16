@Domain
Frontend JavaScript Application Testing. These rules MUST trigger when the AI is tasked with writing, modifying, or configuring automated tests for client-side JavaScript applications, specifically those utilizing Jest, DOM interactions, browser APIs (History, Web Storage), HTTP requests, or WebSockets.

@Vocabulary
- **JSDOM**: A pure JavaScript implementation of web standards for Node.js, used to emulate a browser's `window` and `document` within Jest tests.
- **dom-testing-library (`@testing-library/dom`)**: A library that provides queries to find DOM nodes based on user-centric characteristics (e.g., text, role, label) rather than arbitrary markup.
- **jest-dom (`@testing-library/jest-dom`)**: A companion library that extends Jest with custom DOM-specific matchers (e.g., `toBeInTheDocument()`, `toHaveStyle()`).
- **fireEvent**: A utility from `@testing-library/dom` used to programmatically trigger events (clicks, inputs) accurately, handling internal event intricacies like bubbling.
- **Event Bubbling**: The propagation of an event from a child element up through its ancestors. Essential for testing delegated event listeners.
- **nock**: A library used to intercept and mock HTTP requests at the network layer to prevent frontend tests from depending on a real backend.
- **isomorphic-fetch**: A Node.js compatible implementation of the `fetch` API, required because native Node.js (and thus Jest) lacks the browser's `fetch`.

@Objectives
- Accurately replicate browser environments within Node.js to enable execution of frontend tests without a real browser.
- Create resilient, decouple DOM assertions that do not break when non-functional markup/structural changes occur.
- Precisely simulate user behaviors by dispatching events that reflect actual runtime conditions (including proper event bubbling).
- Eliminate cross-test pollution by rigorously resetting DOM state, module caches, and browser APIs (`localStorage`, `History`) between tests.
- Isolate the frontend from the backend by intercepting HTTP requests and spinning up local, test-specific WebSocket servers.

@Guidelines

**Environment Setup & Configuration**
- The AI MUST set `testEnvironment: "jsdom"` in `jest.config.js` to ensure the global `window` and `document` objects are available.
- The AI MUST configure `setupFilesAfterEnv` in `jest.config.js` to load configuration scripts for DOM assertions and global polyfills.
- The AI MUST polyfill `fetch` for Node.js by assigning `require("isomorphic-fetch")` to `global.window.fetch` in a setup file.

**DOM Manipulation and Querying**
- The AI MUST reset the document state before each test by assigning the original HTML string to `document.body.innerHTML` inside a `beforeEach` hook.
- The AI MUST NOT use CSS structural hierarchy selectors (e.g., `body > ul`, `div > span`) to query elements.
- The AI MUST NOT query elements by arbitrary HTML `id` attributes unless the element lacks semantic meaning or text.
- The AI MUST query elements by their textual content (e.g., `getByText`, `screen.getByText`) or semantic attributes (e.g., `getByRole`, `getByLabelText`, `data-testid`).

**DOM Assertions**
- The AI MUST use `@testing-library/jest-dom` matchers (e.g., `toBeInTheDocument()`, `toHaveClass()`, `toHaveStyle()`) instead of manually inspecting DOM properties (e.g., checking `.innerHTML` or `.style.color`).
- The AI MUST extend Jest with DOM matchers in a setup script using `expect.extend(jestDom)`.

**Event Handling & Simulation**
- The AI MUST NOT test event handler functions by manually invoking them with hand-crafted, mocked event objects (e.g., `handleAddItem({ preventDefault: ... })`).
- The AI MUST trigger events through the DOM using `element.dispatchEvent(new Event('...'))` or `fireEvent` from `@testing-library/dom`.
- When manually dispatching native events (e.g., `input`), the AI MUST pass `{ bubbles: true }` in the Event constructor if the application relies on event delegation/bubbling.
- The AI MUST use `jest.resetModules()` followed by re-`require("./main")` in a `beforeEach` hook to ensure event listeners are freshly bound to the new DOM in each test.

**Browser APIs (LocalStorage & History)**
- The AI MUST use JSDOM's native implementations of browser APIs (`localStorage`, `history`) in tests. The AI SHALL NOT replace these with test doubles/stubs.
- The AI MUST clear `localStorage` using `localStorage.clear()` in a `beforeEach` hook.
- The AI MUST reset the `History` API between tests by recursively calling `history.back()` until `history.state === null`, listening to the `popstate` event.
- The AI MUST spy on `window.addEventListener` to capture and manually remove all `popstate` listeners in an `afterEach` hook to prevent assertions from bleeding into subsequent tests.

**HTTP Requests & WebSockets**
- The AI MUST mock backend HTTP boundaries using `nock`. Do not spin up an actual backend server for pure frontend unit/integration tests.
- The AI MUST clear interceptors in an `afterEach` hook using `nock.cleanAll()`.
- The AI MUST assert that all expected HTTP requests were made using `nock.isDone()`. If it returns false, throw an error in the `afterEach` hook.
- For WebSocket testing, the AI MUST NOT stub the client socket. Instead, the AI MUST spin up a local fake `socket.io` server using `http.createServer()` within the test file, connect the client to it in `beforeAll`, dispatch messages via `io.sockets.emit`, and shut it down in `afterAll`.

@Workflow
1. **Environment Initialization**: Define the JSDOM environment in `jest.config.js`. Create setup files for `jest-dom` and `isomorphic-fetch`.
2. **Test Block Setup**:
    - Add `beforeEach` hooks to: Reset `document.body.innerHTML`, call `jest.resetModules()`, re-require the main application entry point, clear `localStorage`, reset `history` state, and initialize `nock` endpoints.
3. **Execution (Act)**: Find elements using `@testing-library/dom` (`screen.getByText`, `screen.getByPlaceholderText`). Interact using `fireEvent` (e.g., `fireEvent.input`, `fireEvent.click`).
4. **Assertion (Assert)**: Verify DOM mutations using `toBeInTheDocument()` or `toHaveStyle()`. Verify network calls using `nock.isDone()`.
5. **Teardown**: Add `afterEach` hooks to clean up `nock`, remove dangling event listeners (specifically `popstate`), and reset mocks using `jest.restoreAllMocks()`.

@Examples (Do's and Don'ts)

**DOM Selectors**
- [DO]: `const submitBtn = screen.getByText("Add to inventory");`
- [DON'T]: `const submitBtn = document.querySelector("body > form > button");`

**Assertions**
- [DO]: `expect(screen.getByText("cheesecake - Quantity: 6")).toBeInTheDocument();`
- [DON'T]: `expect(document.getElementById("item-list").innerHTML).includes("cheesecake - Quantity: 6");`

**Event Simulation**
- [DO]:
```javascript
const itemField = screen.getByPlaceholderText("Item name");
fireEvent.input(itemField, { target: { value: "cheesecake" } });
// Or using native events:
const inputEvent = new Event("input", { bubbles: true });
itemField.dispatchEvent(inputEvent);
```
- [DON'T]:
```javascript
const fakeEvent = { target: { value: "cheesecake" }, preventDefault: jest.fn() };
handleItemName(fakeEvent); // Bypasses the DOM entirely
```

**HTTP Mocking**
- [DO]:
```javascript
beforeEach(() => {
  nock("http://localhost:3000")
    .post("/inventory/cheesecake")
    .reply(200);
});
afterEach(() => {
  if (!nock.isDone()) {
    nock.cleanAll();
    throw new Error("Not all mocked endpoints received requests.");
  }
});
```
- [DON'T]:
```javascript
// Do not stub fetch directly for integration behaviors unless specifically necessary
jest.spyOn(window, "fetch").mockResolvedValue({ json: () => ({}) });
```

**History API Cleanup**
- [DO]:
```javascript
beforeEach(done => {
  const clearHistory = () => {
    if (history.state === null) {
      window.removeEventListener("popstate", clearHistory);
      return done();
    }
    history.back();
  };
  window.addEventListener("popstate", clearHistory);
  clearHistory();
});
```
- [DON'T]:
```javascript
beforeEach(() => {
  // Direct reassignment doesn't clear the stack or trigger popstate correctly in JSDOM
  history.state = null; 
});
```