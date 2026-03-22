@Domain
Trigger these rules when tasks involve React Refs, direct DOM manipulation, the `useRef` hook, passing references between components (including `forwardRef`), managing non-rendering persistent component data, or implementing imperative component APIs (using `useImperativeHandle` or manual Ref assignment).

@Vocabulary
- **Ref**: A mutable object in React that persists between re-renders. Stored values are kept in the `.current` property.
- **useRef**: The React hook used to create a Ref.
- **forwardRef**: A React function used to wrap functional components so they can accept a `ref` attribute and pass it down to a child element.
- **useImperativeHandle**: A React hook used to expose a custom, encapsulated imperative API to a parent component instead of exposing the raw DOM node.
- **Imperative API**: A set of specific methods (e.g., `.focus()`, `.shake()`) exposed by a child component to its parent, allowing the parent to trigger actions directly without relying on declarative state/prop changes.
- **Mounting/Render Phase**: The synchronous process where React calls the component function. DOM elements do not exist in `ref.current` during this phase.

@Objectives
- Accurately determine whether to use state or Refs for persistent data based on rendering requirements.
- Safely access and manipulate actual DOM elements without violating React's lifecycle.
- Correctly propagate Refs between parent and child components using custom props or `forwardRef`.
- Encapsulate component internals by implementing clean imperative APIs using `useImperativeHandle` or manual Ref mutation.

@Guidelines
- **State vs. Ref Decision Matrix**: 
  - Ask: "Is this value used for rendering components, now or in the future?" 
  - Ask: "Is this value passed as props to other components in any way, now or in the future?" 
  - If the answer to BOTH is "no," you MUST use a Ref. If "yes" to either, use state.
- **No Re-Renders on Mutation**: You MUST NOT rely on Ref updates to trigger a component re-render. Updating `ref.current` is a silent background operation.
- **Synchronous Updates**: Treat Ref updates as synchronous and immediately mutable operations. Unlike state (which operates on asynchronous snapshots), mutating `ref.current` makes the new value available on the very next line of code.
- **DOM Access Timing Constraints**: You MUST ONLY read or write `ref.current` when it contains a DOM element inside a `useEffect` hook or an event handler (e.g., `onClick`). NEVER attempt to read the DOM node directly during the render phase (the component body), as `ref.current` will be null before the element is painted.
- **Propagating Refs**: Functional components cannot inherently accept a `ref` attribute. To pass a Ref to a child, you MUST either pass it via a custom prop name (e.g., `inputRef`, `apiRef`) or wrap the child component in `React.forwardRef()`.
- **Encapsulating DOM via Imperative APIs**: When a parent needs to trigger a visual change or native DOM action in a child (e.g., focusing an input, triggering a CSS animation), DO NOT leak the raw DOM node to the parent. Instead, expose an Imperative API exposing specific methods using either `useImperativeHandle` or by manually mutating the passed Ref in `useEffect`.

@Workflow
1. **Assess the Data Requirement**: Determine the nature of the data being stored. If the data will be drawn to the screen or passed as a prop, initialize `useState`. If it tracks background developer data (e.g., render count, previous state value) or DOM references, initialize `useRef`.
2. **DOM Action Identification**: Identify if a native JavaScript DOM API is required (e.g., `.focus()`, `.scrollIntoView()`, measuring element sizes with `getBoundingClientRect`, or intercepting outside clicks).
3. **Ref Initialization and Attachment**: Create the Ref using `const myRef = useRef(null)`. Attach it to the target JSX element using the `ref={myRef}` attribute.
4. **Safe DOM Interaction**: Place any logic that calls native methods on `myRef.current` strictly inside a `useEffect` hook or an interaction callback (e.g., `onSubmitClick`).
5. **Component Boundary Crossing (If applicable)**:
   - If the DOM node is inside a child component, pass the parent's Ref down using a custom prop (e.g., `<InputField apiRef={myRef} />`).
   - Alternatively, wrap the child in `forwardRef((props, ref) => ...)` and pass it using the standard `ref` attribute.
6. **Implement Imperative Abstraction (If applicable)**: 
   - Create an internal Ref inside the child component and attach it to the raw DOM node.
   - Use `useImperativeHandle(parentRef, () => ({ customMethod: () => { ... } }), [])` to attach specific functions to the parent's Ref.
   - Alternatively, manually assign the API to the parent's Ref: `useEffect(() => { parentRef.current = { customMethod: () => { ... } } }, [parentRef])`.

@Examples (Do's and Don'ts)

**Example 1: State vs. Ref for Rendered Data**
- [DO]: Use state for data that affects the visual output.
```javascript
const Form = () => {
  const [text, setText] = useState("");
  return (
    <>
      <input type="text" onChange={(e) => setText(e.target.value)} />
      Characters count: {text.length}
    </>
  );
};
```
- [DON'T]: Use Ref for data that needs to dynamically update on the screen.
```javascript
const Form = () => {
  const ref = useRef("");
  // ERROR: The character count will not update on the screen when typing.
  return (
    <>
      <input type="text" onChange={(e) => { ref.current = e.target.value; }} />
      Characters count: {ref.current.length}
    </>
  );
};
```

**Example 2: Safe DOM Access Timing**
- [DO]: Access the DOM element inside an effect or callback.
```javascript
const Component = () => {
  const ref = useRef(null);
  
  useEffect(() => {
    console.log(ref.current); // Safe: DOM element exists
  }, []);

  return <input ref={ref} />;
};
```
- [DON'T]: Access the DOM element directly in the render body.
```javascript
const Component = () => {
  const ref = useRef(null);
  
  // ERROR: ref.current will be null here during the initial render.
  if (!ref.current) return null;

  return <input ref={ref} />;
};
```

**Example 3: Passing Refs to Functional Components**
- [DO]: Use `forwardRef` or a uniquely named prop.
```javascript
// Using forwardRef
const InputField = forwardRef((props, ref) => {
  return <input ref={ref} />;
});

// Using custom prop
const InputFieldCustom = ({ innerRef }) => {
  return <input ref={innerRef} />;
}
```
- [DON'T]: Pass the `ref` attribute directly to a standard functional component.
```javascript
const InputField = () => {
  return <input />;
};

const Form = () => {
  const myRef = useRef(null);
  // ERROR: Will throw a warning and fail to attach.
  return <InputField ref={myRef} />;
};
```

**Example 4: Exposing an Imperative API**
- [DO]: Use `useImperativeHandle` to hide the raw DOM element and expose safe actions.
```javascript
const InputField = ({ apiRef }) => {
  const internalRef = useRef(null);

  useImperativeHandle(apiRef, () => ({
    focus: () => {
      internalRef.current.focus();
    },
    shake: () => {
      // trigger CSS animation logic
    }
  }), []);

  return <input ref={internalRef} />;
};

const Form = () => {
  const inputApi = useRef(null);
  return (
    <>
      <InputField apiRef={inputApi} />
      <button onClick={() => inputApi.current.focus()}>Focus Input</button>
    </>
  );
};
```
- [DON'T]: Force the parent to manage internal child implementations via complex props if an imperative trigger is simpler and cleaner, and don't leak the raw DOM node if abstraction is required.
```javascript
// AVOID: Using complex state toggles for one-off actions like focusing
const InputField = ({ focusItself }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (focusItself) ref.current.focus();
  }, [focusItself]); // Will only work once when toggled to true
  return <input ref={ref} />;
};
```