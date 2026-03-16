# @Domain
Trigger these rules when the user requests assistance with testing React applications, specifically focusing on component integration, snapshot testing, styling tests (including CSS-in-JS), or creating component stories and documentation using Storybook.

# @Vocabulary
- **Transitive Guarantee**: Centralizing a dependency (like text formatting) into a separate, unit-tested function, then relying on that function within higher-level integration tests to reduce test overlap and maintenance overhead.
- **Snapshot Testing**: A technique where a target's output (markup, text, or data) is saved on the first run and compared against future runs to detect unexpected changes.
- **Serializer**: A tool used by Jest to cleanly format data (like React components or CSS-in-JS rules) before writing them to a snapshot file, ensuring snapshots remain readable and reviewable.
- **Component Stubbing**: Replacing a child component (often from a third-party library) with a test double to prevent undesirable side effects (like animations) from interfering with tests.
- **Component Story**: A code module demonstrating the visual states and functionalities of an individual component in isolation, typically using Storybook.
- **Knobs**: Storybook addons that allow viewers to dynamically manipulate a component's props through a UI panel.
- **Actions**: Storybook addons that log event handler calls (e.g., form submissions) to a UI panel instead of triggering disruptive browser alerts.
- **MDX**: A file format combining Markdown and JSX used to document components and render live interactive instances alongside the documentation.
- **Component-Level Acceptance Testing**: The practice of using Storybook stories to allow QA, designers, or product managers to validate UI components interactively without running the entire application stack.

# @Objectives
- Write integration tests as high up the component tree as necessary to generate reliable, run-time-resembling guarantees.
- Reduce test maintenance costs by utilizing transitive guarantees and avoiding brittle assertions on deep component trees.
- Avoid testing third-party libraries; use stubs exclusively for uncontrollable or disruptive component side effects.
- Leverage snapshot testing strictly for complex, static markup or large texts, ensuring they remain deterministic, small, and human-readable.
- Test component styles by asserting on applied dynamic classes or inline styles, utilizing custom serializers for CSS-in-JS.
- Foster component-level acceptance testing and documentation by writing comprehensive, interactive Storybook stories and MDX documentation.

# @Guidelines

## Component Integration & Stubbing
- The AI MUST write integration tests high in the component tree to closely resemble the user's run-time environment. 
- The AI MUST NOT use Enzyme's `shallow` rendering to isolate components; favor `react-testing-library` and render components fully to maintain reliable guarantees.
- When an integration test becomes too brittle because a child component's text/markup format changes frequently, the AI MUST extract the formatting logic into a separate function, unit test it individually, and use it in the integration test to establish a "transitive guarantee".
- The AI MUST NOT test third-party components (e.g., `react-spring` animations). Instead, create a test double (stub) using `jest.mock()` and a dummy React component that renders the children without the side effects.
- The AI MUST limit component stubbing to situations where a component triggers uncontrollable side effects. Over-stubbing decreases test reliability.

## Snapshot Testing
- The AI MUST use snapshot testing (`toMatchSnapshot()`) for components with extensive markup, large quantities of text, or complex configurations (like generated reports).
- The AI MUST ensure the assertion target for a snapshot is completely deterministic. Time-dependent data (e.g., `Date.prototype.toISOString`), random numbers, or generated UUIDs MUST be stubbed or mocked before taking the snapshot.
- The AI MUST NOT generate massive, whole-page snapshots. Scope the snapshot to the smallest relevant DOM node (e.g., `expect(container.firstChild).toMatchSnapshot()` or `expect(document.querySelector('ul')).toMatchSnapshot()`) to keep code reviews manageable.
- The AI MUST explicitly instruct the user to carefully verify the component's output before generating or updating snapshots (using `--updateSnapshot` or `-u`), and to run updates on a single test file at a time to prevent masking bugs.

## Testing Styles
- The AI MUST NOT write assertions to check static class names that never change (e.g., `expect(element).toHaveClass('item-list')`), as this provides no reliable guarantee of appearance and creates brittle tests.
- When asserting on dynamic styles applied conditionally, the AI MUST use `toHaveClass()` (for external stylesheets) or `toHaveStyle()` (for inline styles).
- When using CSS-in-JS (e.g., `emotion`), the AI MUST configure Jest with the appropriate custom serializer (e.g., `jest-emotion`) so that snapshots output readable CSS rules instead of cryptic, autogenerated class hashes.
- To assert on CSS-in-JS rules programmatically, the AI MUST use library-specific matchers like `toHaveStyleRule`.

## Stories & Documentation (Storybook)
- The AI MUST create stories (`*.stories.jsx`) to showcase individual components in multiple visual states.
- The AI MUST NOT use Node.js-specific mocking libraries (like `nock`) within Storybook stories. Use browser-compatible mocking tools (like `fetch-mock`) to intercept HTTP requests.
- The AI MUST clean up any network interceptors or stubs when a Storybook component unmounts (e.g., returning a cleanup function from `useEffect`) to prevent interference between stories.
- The AI MUST NOT use `alert()` in stories to demonstrate event handling. Use `@storybook/addon-actions` to log interactions gracefully.
- The AI MUST prioritize `@storybook/addon-knobs` over custom stateful wrapper components to allow users to manipulate component props dynamically.
- The AI MUST document components using MDX (`*.docs.mdx`), combining markdown explanations of component intent with `<Preview><Story>...</Story></Preview>` blocks for live examples.

# @Workflow
1. **Integration Setup**: Import components, mock API calls using `nock` (for Jest) or `fetch-mock` (for Storybook), and render using `react-testing-library`.
2. **Interaction Execution**: Use `fireEvent` to type into inputs or click buttons. Wrap async assertions in `waitFor` or use `findBy*` queries to allow the React component to process state changes.
3. **Deterministic Snapshotting**: If utilizing `toMatchSnapshot()`, identify and mock any dynamic data (dates, IDs). Target the specific nested DOM node rather than the entire document body.
4. **Style Verification**: For dynamically applied styles, query the specific element and assert using `toHaveStyle`, `toHaveClass`, or `toHaveStyleRule` (if using CSS-in-JS).
5. **Storybook Extraction**: Replicate the component states in a `*.stories.jsx` file. Inject `knobs` for prop manipulation and `actions` for event logging. Clean up browser-level mocks on unmount.

# @Examples (Do's and Don'ts)

## Transitive Guarantees for Integration Tests
[DO] Extract volatile string formatting into a separate function to reduce maintenance overhead in integration tests.
```javascript
// ItemList.jsx
export const generateItemText = (name, quantity) => `${name} - Quantity: ${quantity}`;

// App.test.jsx
import { generateItemText } from "./ItemList.jsx";

test("updates list when item added", async () => {
  // ... render and fireEvent setup
  await waitFor(() => {
    expect(getByText(generateItemText("cheesecake", 8))).toBeInTheDocument();
  });
});
```

[DON'T] Hardcode brittle string formats in high-level integration tests that will break if the presentation format changes.
```javascript
// App.test.jsx
test("updates list when item added", async () => {
  // If we change "Quantity: 8" to "Qty: 8", this test and ALL other integration tests break
  await waitFor(() => {
    expect(getByText("cheesecake - Quantity: 8")).toBeInTheDocument();
  });
});
```

## Snapshot Testing
[DO] Make dynamic data deterministic before taking a snapshot, and target a specific container.
```javascript
test("action log snapshot", () => {
  // Mock the date so the snapshot doesn't fail on every run
  jest.spyOn(Date.prototype, "toISOString").mockReturnValue("2020-06-20T13:37:00.000Z");
  
  const { getByTestId } = render(<ActionLog actions={actions} />);
  const actionLog = getByTestId("action-log");
  
  expect(actionLog).toMatchSnapshot();
});
```

[DON'T] Snapshot components containing unpredictable timestamps or random generation without mocking.
```javascript
test("action log snapshot", () => {
  // FAILS on next run because `new Date().toISOString()` changes
  const { container } = render(<ActionLog actions={actions} />);
  expect(container).toMatchSnapshot(); 
});
```

## Testing CSS-in-JS Styles
[DO] Use custom serializers (`jest-emotion`) to generate readable snapshots, and test specific logic-driven CSS rules.
```javascript
import { matchers } from "jest-emotion";
expect.extend(matchers);

test("highlights items almost out of stock", () => {
  const { getByText } = render(<ItemList itemList={{ cheesecake: 2 }} />);
  const item = getByText(/cheesecake/);
  
  // Validates the specific rule applied by the CSS-in-JS library
  expect(item).toHaveStyleRule("color", "red");
});
```

[DON'T] Assert on static classes that never change, as they provide no reliable quality guarantee.
```javascript
test("has list class", () => {
  const { container } = render(<ItemList itemList={{}} />);
  const ul = container.querySelector("ul");
  
  // Meaningless test: Doesn't prove the list looks correct, just checks a static string
  expect(ul).toHaveClass("item-list");
});
```

## Writing Stories
[DO] Use browser-compatible mocks (`fetch-mock`), clean up on unmount, and log events with `@storybook/addon-actions`.
```javascript
import React, { useEffect } from "react";
import fetchMock from "fetch-mock";
import { action } from "@storybook/addon-actions";
import { ItemForm } from "./ItemForm";

export const itemForm = () => {
  const ItemFormStory = () => {
    useEffect(() => {
      fetchMock.post(`glob:http://localhost:3000/inventory/*`, 200);
      return () => fetchMock.restore(); // Cleanup is critical
    }, []);

    return <ItemForm onItemAdded={action("form-submission")} />;
  };
  return <ItemFormStory />;
};
```

[DON'T] Use Node.js specific libraries (`nock`) in Storybook, or use disruptive browser alerts for logging.
```javascript
import nock from "nock"; // WILL CRASH IN BROWSER
import { ItemForm } from "./ItemForm";

export const itemForm = () => {
  nock("http://localhost:3000").post("/inventory/cheesecake").reply(200);
  
  // Disruptive to the user experience in Storybook
  return <ItemForm onItemAdded={(...data) => alert(JSON.stringify(data))} />; 
};
```