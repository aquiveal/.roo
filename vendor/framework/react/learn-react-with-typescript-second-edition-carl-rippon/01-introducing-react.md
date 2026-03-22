# @Domain
These rules apply when the AI is tasked with creating, modifying, refactoring, or debugging React applications, specifically focusing on React components, JSX syntax, component module structures, props, local state (`useState`), and event handling.

# @Vocabulary
*   **Component**: A reusable piece of the UI composed of HTML and JavaScript logic, implemented as a JavaScript function starting with a capital letter.
*   **JSX (JavaScript XML)**: A syntax extension that mixes HTML and JavaScript to specify the output of a React component. Requires transpilation (via Babel) into `React.createElement` calls.
*   **Virtual DOM**: An in-memory representation of the real DOM used by React to calculate the minimum required changes to the actual DOM, ensuring performant updates.
*   **Rendering**: The process of displaying React components on the page. Triggered initially via `createRoot` and subsequently upon state changes.
*   **Props (Properties)**: Optional, read-only object parameters passed into a component as JSX attributes to configure its output or behavior.
*   **Children**: A special prop used to pass nested content directly between the opening and closing tags of a component's JSX.
*   **State**: A special variable tied to a component that holds information about its current situation. Changes to state trigger component re-rendering.
*   **Hook**: Special React functions (like `useState`) that give functional components powerful capabilities like state management.
*   **Tuple**: An array with a fixed number of elements, returned by `useState` containing the state variable and its setter function.
*   **Event Handler (Event Listener)**: A function registered to an element's event (e.g., `onClick`) containing logic to execute when the user interacts with it.
*   **Short-Circuit Expression**: A JavaScript logical AND (`&&`) used in JSX to conditionally render an element only if a specific condition is truthy.
*   **Strict Mode**: An environment mode that checks content for potential problems and reports them in the console, ensuring code quality (used in both JS natively and via React's `<StrictMode>`).

# @Objectives
*   The AI MUST build modular, isolated, and highly reusable React components.
*   The AI MUST ensure type-safe and idiomatic JSX, strictly adhering to React's attribute naming conventions (e.g., `className` instead of `class`).
*   The AI MUST guarantee predictable component output by utilizing proper prop destructuring, default values, and safe event invocations.
*   The AI MUST optimize component structures by placing logic, state, and event handlers securely inside the component function to maintain scope isolation.
*   The AI MUST prioritize web accessibility (a11y) inside JSX elements, particularly for non-text visual representations.

# @Guidelines

### Component Architecture & Modules
*   When creating a component, the AI MUST name the function starting with a Capital Letter (PascalCase). Lowercase names are strictly prohibited as they are treated as generic DOM elements by transpilers.
*   When placing components in files, the AI MUST allocate exactly one React component per file/module to prevent bloated codebases and improve readability.
*   When exporting components, the AI MUST use **named exports** (e.g., `export function Alert() {...}`) rather than default exports, making it immediately apparent which functions are public.
*   When importing components, the AI MUST use exact name matching in named import statements (e.g., `import { Alert } from './Alert';`).
*   When defining the entry point of the React app (typically `index.js`), the AI MUST use `createRoot` from `react-dom/client` and wrap the root component inside React's `<StrictMode>`.

### JSX Syntax & Composition
*   When defining CSS classes in JSX, the AI MUST use the `className` attribute. Never use the `class` attribute.
*   When embedding JavaScript variables or expressions inside JSX, the AI MUST wrap them entirely in curly braces `{}`.
*   When applying conditional rendering based on boolean values, the AI MUST use the logical AND short-circuit expression (`{condition && <Element />}`) or ternary operators for inline branching (`{condition ? <TrueElement /> : <FalseElement />}`).
*   When utilizing emoji or icon-based `<span>` elements, the AI MUST provide accessibility attributes, specifically `role="img"` and `aria-label="[Description]"`.
*   When rendering standard interactive elements (like `<button>`), the AI MUST provide an `aria-label` attribute if the element lacks descriptive text content.

### Props Handling
*   When receiving props in a component function, the AI MUST destructure the props object directly in the function signature instead of referencing `props.[propertyName]`.
*   When a prop is optional, the AI MUST assign default values directly inside the destructured function signature (e.g., `({ type = "information" })`).
*   When nesting content inside a component, the AI MUST use the special `children` prop rather than defining a custom prop for the main body content.
*   When passing boolean props to a component, the AI MUST pass the attribute without an explicit value to imply `true` (e.g., `<Alert closable />` instead of `<Alert closable={true} />`).

### State & Interactivity
*   When implementing state, the AI MUST import and use the `useState` hook from `react`.
*   When naming state variables and setters, the AI MUST use standard tuple destructuring with the pattern: `[variableName, setVariableName]`.
*   When a component needs to be entirely hidden based on state, the AI MUST implement an early return of `null` before the main `return` statement (e.g., `if (!visible) return null;`).

### Event Handling
*   When attaching native events in JSX, the AI MUST use camelCase attributes (e.g., `onClick`, `onChange`).
*   When defining an event handler function, the AI MUST place it inside the component function scope to ensure access to component state and props.
*   When exposing custom events to consumer components, the AI MUST name the prop starting with `on` (e.g., `onClose`, `onConfirm`).
*   When invoking a custom event prop inside an event handler, the AI MUST verify the prop exists before calling it to prevent execution errors (e.g., `if (onClose) { onClose(); }`).

# @Workflow
1.  **Module Setup**: Create the file. Use a named export for the function component. Capitalize the component name.
2.  **State Initialization**: Import `useState`. Define all required interactive states, providing sensible initial values.
3.  **Prop Definition**: Destructure props in the parameter list. Assign default parameters for optional presentation configurations. Pull in `children` if wrapping content. Include custom event callbacks prefixed with `on`.
4.  **Handler Creation**: Define event listener functions (e.g., `handleCloseClick`) inside the component scope. Within these handlers, execute state setter functions, and safely invoke any passed-in custom event props.
5.  **Early Returns**: Evaluate state or props that completely hide the component. Return `null` immediately if the component should not be visible.
6.  **JSX Construction**: Return the UI structure. Apply `className` for styling. Use `{}` for variables. Implement `&&` short-circuiting for conditional elements. Ensure all visual elements (buttons, emojis) have `aria-label` and `role` attributes where required.

# @Examples (Do's and Don'ts)

### Component Declaration
*   [DO]: `export function ImportantAlert() { ... }`
*   [DON'T]: `export function importantAlert() { ... }` (Lowercase fails transpilation as a component).

### Embedding Variables in JSX
*   [DO]: `<span>{heading}</span>`
*   [DON'T]: `<span>heading</span>` (Renders the literal string "heading").

### Passing Props
*   [DO]: `<ContactDetails firstName="Fred" email="fred@example.com" closable />`
*   [DON'T]: `<ContactDetails name="Fred" email="fred@example.com" closable={true} />` (Avoid non-specific prop names like `name` if `firstName` is expected. Avoid explicit `{true}` for booleans).

### Destructuring Props
*   [DO]: 
```javascript
export function ContactDetails({ firstName, email, type = "standard" }) {
  return <div>{firstName} - {email}</div>;
}
```
*   [DON'T]:
```javascript
export function ContactDetails(props) {
  return <div>{props.firstName} - {props.email}</div>;
}
```

### Event Attribute Naming
*   [DO]: `<button onClick={() => console.log("clicked")}>`
*   [DON'T]: `<button click={() => console.log("clicked")}>` (Invalid React event attribute).

### State Updates
*   [DO]: 
```javascript
const [agree, setAgree] = useState(false);
return <button onClick={() => setAgree(true)}>Agree</button>;
```
*   [DON'T]: 
```javascript
const [agree, setAgree] = useState(false);
return <button onClick={() => agree = true}>Agree</button>;
``` (State mutations bypassing the setter do not trigger re-renders).

### Custom Event Invocation
*   [DO]: 
```javascript
export function Agree({ onAgree }) {
  function handleClick() {
    if (onAgree) {
      onAgree();
    }
  }
  return <button onClick={handleClick}>Click to agree</button>;
}
```
*   [DON'T]: 
```javascript
export function Agree({ onAgree }) {
  function handleClick() {
    onAgree(); // Errors if onAgree is undefined
  }
  return <button onClick={handleClick}>Click to agree</button>;
}
```

### Accessibility
*   [DO]: `<span role="img" aria-label="Warning">⚠</span>`
*   [DON'T]: `<span>⚠</span>` (Inaccessible to screen readers).