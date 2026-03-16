# @Domain
These rules MUST be triggered whenever the AI is tasked with setting up, configuring, writing, refactoring, or debugging automated tests for React applications. This includes interactions with React components (`.jsx`, `.tsx`), Jest configuration files (`jest.config.js`), Babel configuration files (`babel.config.js`), and any test files (`*.test.jsx`, `*.spec.jsx`, `*.test.tsx`, `*.spec.tsx`) within a web-based React project.

# @Vocabulary
- **JSX**: A syntax extension for JavaScript used to write React components. It is syntactic sugar that compiles to `React.createElement` calls. Browsers and Node.js cannot execute JSX natively.
- **Babel**: A JavaScript compiler used to transform JSX and modern ES modules into plain JavaScript that Node.js and Jest can execute.
- **JSDOM**: A pure JavaScript implementation of web standards used to replicate a browser's environment (like `window` and `document`) within Node.js.
- **act**: A utility from `react-dom/test-utils` that ensures all component updates, rendering, and interactions are processed and applied to the DOM before assertions are made.
- **React Testing Library (RTL)**: A testing tool (`@testing-library/react`) built on top of DOM Testing Library that automatically handles React-specific concerns like unmounting, scoping queries, and wrapping interactions in `act`. 
- **Enzyme**: An older testing library that allows fine-grained control over a component's internals (state, props) and supports "shallow rendering." This tool is heavily discouraged in this ecosystem.
- **Shallow Rendering**: A testing technique (commonly used in Enzyme) that renders only the top-level component and stubs all child components. It is considered an anti-pattern as it weakens reliability guarantees.
- **React Test Renderer**: A tool that renders React components to plain JavaScript objects instead of the DOM. Suitable for React Native, but discouraged for web applications.
- **nock**: An HTTP mocking library used to intercept HTTP requests and provide deterministic, canned responses in tests.

# @Objectives
- Accurately replicate a browser's environment within Node.js using JSDOM so tests can interact with components as users do.
- Transform test files properly using Babel so that Jest can understand JSX and modern ES module syntax.
- Test React components as atomic units in the DOM using `@testing-library/react`, completely avoiding the testing of internal implementation details (e.g., state, internal methods).
- Ensure all asynchronous state updates and API calls are deterministically mocked and appropriately waited for using RTL's built-in async utilities.

# @Guidelines

## Environment & Setup
- The AI MUST configure Jest to use JSDOM by setting `testEnvironment: "jsdom"` in `jest.config.js`.
- The AI MUST configure Babel to transform JSX into plain JavaScript using `@babel/preset-react`.
- The AI MUST configure Babel to transform ES modules for Node.js using `@babel/preset-env` with the target set to `{ node: "current" }`.
- When dealing with `fetch` in tests, the AI MUST polyfill the global `fetch` API using a setup file (e.g., importing `isomorphic-fetch` and assigning it to `global.window.fetch`) and register it in Jest's `setupFilesAfterEnv`.

## Rendering Components
- The AI MUST render React components to the DOM using `@testing-library/react` (`render(<Component />)`).
- The AI MUST NOT isolate components from React (e.g., calling component functions directly as pure JS functions). 
- The AI MUST NOT use Enzyme.
- The AI MUST NOT use shallow rendering. All components must be deeply rendered to resemble the run-time environment.
- The AI MUST NOT use React Test Renderer (`react-test-renderer`) for web applications. JSDOM is strictly required for web.

## Interacting with Components
- The AI MUST use RTL's `fireEvent` to simulate user interactions.
- The AI MUST rely on RTL's automatic `act` wrapping. Manual `act()` wrappers should only be used if performing custom DOM updates outside the scope of RTL's provided utilities.
- The AI MUST NOT test a component's internal state or implementation details. Testing must occur strictly through DOM interactions and visual output.

## Asynchronous Handling & Mocking
- The AI MUST mock third-party API dependencies using `nock` to ensure deterministic tests and avoid firing actual HTTP requests in component tests.
- When waiting for asynchronous updates (like API resolutions), the AI MUST use RTL's `findBy*` queries or `waitFor()`.
- The AI MUST keep `waitFor` callbacks lean. Only wrap the minimal necessary assertions inside `waitFor` (ideally a single assertion). Do not wrap multiple, unrelated assertions in a single `waitFor` block, as it slows down tests and causes misleading timeout failures.

## Assertions
- The AI MUST use `@testing-library/jest-dom` extensions (e.g., `toBeInTheDocument`, `toHaveStyle`) to write clear, DOM-specific assertions.
- The AI MUST ensure `jest-dom` is globally imported via a setup file listed in Jest's `setupFilesAfterEnv`.

# @Workflow
When tasked with creating or modifying a test for a React component, the AI MUST follow this rigid step-by-step process:

1. **Verify Environment Setup**: Ensure `jest.config.js` specifies `testEnvironment: "jsdom"` and `setupFilesAfterEnv` points to necessary polyfills (e.g., `jest-dom`, global fetch). Ensure `babel.config.js` contains `@babel/preset-env` and `@babel/preset-react`.
2. **Mock External Dependencies**: If the component makes HTTP requests, use `nock` in a `beforeEach` hook to define expected endpoints and return canned JSON responses. Add an `afterEach` hook to call `nock.cleanAll()` and verify all interceptors were hit using `nock.isDone()`.
3. **Render the Component**: Import `render` from `@testing-library/react` and invoke it with the target component. Extract the necessary scoped queries (e.g., `getByText`, `getByPlaceholderText`) from the `render` result, or use the global `screen` object.
4. **Simulate User Interaction**: Import `fireEvent` from `@testing-library/react`. Simulate the sequence of user actions (e.g., `fireEvent.change`, `fireEvent.click`).
5. **Handle Asynchronous State**: If the interaction triggers an async update (like a fetch resolution), use `await findBy*` to wait for the specific UI change, or use `await waitFor(() => expect(...))` strictly for the specific element change.
6. **Assert on the DOM**: Use `jest-dom` matchers to assert the final state of the UI (e.g., `.toBeInTheDocument()`). 

# @Examples (Do's and Don'ts)

## Example 1: Test Environment Compilation Setup
- **[DO]** Configure Babel to handle both Node.js execution and JSX transpilation for Jest:
```javascript
// babel.config.js
module.exports = {
  presets: [
    [
      "@babel/preset-env",
      { targets: { node: "current" } }
    ],
    "@babel/preset-react"
  ]
};
```
- **[DON'T]** Run Jest on raw JSX without a Babel configuration, or configure it exclusively for the browser, which causes syntax errors in Node.js.

## Example 2: Rendering and Interacting with Components
- **[DO]** Use React Testing Library to render and interact with components automatically wrapped in `act`:
```jsx
import { render, fireEvent } from "@testing-library/react";
import { App } from "./App.jsx";

test("increments the number of cheesecakes", () => {
  const { getByText } = render(<App />);
  
  expect(getByText("Cheesecakes: 0")).toBeInTheDocument();
  
  fireEvent.click(getByText("Add cheesecake"));
  
  expect(getByText("Cheesecakes: 1")).toBeInTheDocument();
});
```
- **[DON'T]** Use `react-dom/test-utils` to manually attach elements to the DOM and manually wrap interactions in `act`:
```jsx
// ANTI-PATTERN
import { render } from "react-dom";
import { act } from "react-dom/test-utils";

const root = document.createElement("div");
document.body.appendChild(root);

act(() => {
  render(<App />, root);
});
// Manual querying and manual act wrappers are verbose and error-prone.
```

## Example 3: Waiting for Asynchronous Events
- **[DO]** Use `findBy*` queries to wait for an asynchronous element to appear, keeping assertions minimal:
```jsx
import { render } from "@testing-library/react";
import { App } from "./App.jsx";

test("rendering the server's list of items", async () => {
  const { findByText } = render(<App />);
  
  expect(await findByText("cheesecake - Quantity: 2")).toBeInTheDocument();
  
  const listElement = document.querySelector("ul");
  expect(listElement.childElementCount).toBe(1);
});
```
- **[DON'T]** Bloat a `waitFor` callback with multiple assertions. If the list content is incorrect, RTL will blindly retry all assertions until timeout, causing slow tests and poor failure messages:
```jsx
// ANTI-PATTERN
await waitFor(() => {
  const listElement = document.querySelector("ul");
  expect(listElement.childElementCount).toBe(3); // Might pass
  expect(getByText("cheesecake - Quantity: 2")).toBeInTheDocument(); // Might fail, causing the whole block to unnecessarily retry
  expect(getByText("croissant - Quantity: 5")).toBeInTheDocument();
});
```

## Example 4: Testing Component Implementations
- **[DO]** Test components deeply through their rendered DOM output, exactly as a user perceives them using RTL.
- **[DON'T]** Use Enzyme to perform shallow rendering or inspect internal state.
```jsx
// ANTI-PATTERN: DO NOT DO THIS
import { shallow } from "enzyme";
import { App } from "./App";

test("updates state", () => {
  const wrapper = shallow(<App />);
  wrapper.instance().setCheesecake(1); // Modifying internal state directly
  expect(wrapper.state('cheesecakes')).toBe(1); // Asserting on internal state
});
```