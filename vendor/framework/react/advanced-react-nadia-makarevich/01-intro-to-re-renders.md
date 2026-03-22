@Domain
React development, specifically when writing or refactoring components involving state management (`useState`, `useReducer`, external state libraries), performance optimization, resolving slow UI issues, investigating unnecessary re-renders, and designing or using custom hooks.

@Vocabulary
- **Mounting**: The initial lifecycle stage when React creates a component's instance, initializes its state, runs hooks, and appends elements to the DOM.
- **Unmounting**: The lifecycle stage when React detects a component is no longer needed, destroys the instance and state, and removes the DOM element.
- **Re-rendering**: The lightweight process where React updates an already existing component instance with new data, runs hooks, does calculations, and updates the existing DOM element with new attributes.
- **State Update**: The initial source of all re-renders in React apps. Initiates the re-render of the component holding the state and all its nested children.
- **Render Tree**: The hierarchical chain of components in a React app. Re-renders propagate strictly "down" this tree.
- **The Big Re-renders Myth**: The false belief that "components re-render when their props change." During the normal React cycle, prop changes are ignored unless a state update triggers the render, or the component is wrapped in `React.memo`.
- **Unnecessary Re-render**: When a component is forced to re-render due to a state update in an ancestor, even though it does not depend on that state.
- **Moving State Down**: A primary composition technique for performance optimization where state and its direct UI consumers are extracted into a smaller, isolated sub-component to prevent re-rendering unrelated sibling components.
- **Hooks State Trap**: The hidden danger where a state update inside a custom hook triggers a re-render in the consuming component, regardless of whether the component uses the state or if the hook returns `null`.

@Objectives
- Isolate state updates to the smallest and lightest components possible.
- Prevent unnecessary re-renders of heavy or unrelated components by prioritizing composition over memoization.
- Ensure custom hooks do not inadvertently trigger re-renders in parent components through hidden state updates.
- Eradicate the misconception that mutating props or local variables triggers React lifecycles.

@Guidelines
- **State Location**: The AI MUST place state as close as possible to the UI elements that consume it.
- **Propagation Awareness**: The AI MUST evaluate the entire downward render tree when placing a state variable. Any component rendered below the state holder will re-render when the state updates.
- **No Upward Rendering**: The AI MUST understand that React never goes "up" the render tree. Siblings or parents of a stateful component remain unaffected by its state updates.
- **Local Variables vs. State**: The AI MUST NOT use local variable mutations (e.g., `let isOpen = false; isOpen = true`) to attempt UI updates. The AI MUST strictly use React state mechanisms for interactivity.
- **Props Myth Correction**: The AI MUST NOT assume components re-render solely because props change. If a parent does not re-render via a state update, changed props are swallowed. 
- **Memoization as Secondary**: The AI MUST prioritize the "Moving State Down" technique over wrapping components in `React.memo` to fix performance issues. Memoization should only be applied if composition is impossible.
- **Hook Auditing**: When extracting logic into custom hooks, the AI MUST explicitly check if the hook contains internal state (e.g., a window resize listener). The AI MUST warn or refactor if applying this hook will cause massive unnecessary re-renders in the consuming component.
- **Hook Chains**: The AI MUST trace state updates through hook chains. A state update in a deeply nested hook will strictly re-render the component using the top-level hook.

@Workflow
1. **Identify the Trigger**: Locate the specific user interaction or event that requires a UI update.
2. **Determine Required State**: Define the state variable needed to track this interaction.
3. **Analyze the Render Tree**: Identify all components currently residing in the exact scope where you intend to declare the state.
4. **Isolate Dependents**: Determine exactly which UI elements *actually* depend on this new state.
5. **Move State Down**: If the scope contains heavy components or a "bunch of stuff" that do *not* depend on the state, extract the state and the dependent UI elements into a new, separate component.
6. **Replace Original**: Render the new localized component in the original component tree.
7. **Audit Hooks**: If the state is abstracted into a custom hook, verify that the host component consuming the hook genuinely requires re-rendering when the hook's internal state changes. If not, apply "Moving State Down" to the hook usage itself.

@Examples (Do's and Don'ts)

**Principle: Moving State Down to Prevent Unnecessary Re-renders**

[DON'T]
```javascript
// State is at the top level, causing VerySlowComponent to re-render on every button click.
const App = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="layout">
      <Button onClick={() => setIsOpen(true)}>Open dialog</Button>
      {isOpen ? <ModalDialog onClose={() => setIsOpen(false)} /> : null}
      <VerySlowComponent />
      <BunchOfStuff />
    </div>
  );
};
```

[DO]
```javascript
// State is extracted with its dependent UI into a localized component.
// VerySlowComponent is now safe from re-renders.
const ButtonWithModalDialog = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open dialog</Button>
      {isOpen ? <ModalDialog onClose={() => setIsOpen(false)} /> : null}
    </>
  );
};

const App = () => {
  return (
    <div className="layout">
      <ButtonWithModalDialog />
      <VerySlowComponent />
      <BunchOfStuff />
    </div>
  );
};
```

**Principle: The Big Re-renders Myth (Local Variables vs. State)**

[DON'T]
```javascript
// Mutating a local variable will NOT trigger a re-render. The dialog will never show up.
const App = () => {
  let isOpen = false;

  return (
    <div className="layout">
      <Button onClick={() => (isOpen = true)}>Open dialog</Button>
      {isOpen ? <ModalDialog onClose={() => (isOpen = false)} /> : null}
    </div>
  );
};
```

[DO]
```javascript
// Always use state to trigger the re-render lifecycle.
const App = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="layout">
      <Button onClick={() => setIsOpen(true)}>Open dialog</Button>
      {isOpen ? <ModalDialog onClose={() => setIsOpen(false)} /> : null}
    </div>
  );
};
```

**Principle: The Danger of Custom Hooks**

[DON'T]
```javascript
// The custom hook contains a state update (resize).
// Even though App doesn't use the 'width' value or the hook returns null,
// App and VerySlowComponent will re-render on EVERY window resize.
const useResizeDetector = () => {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const listener = () => setWidth(window.innerWidth);
    window.addEventListener('resize', listener);
    return () => window.removeEventListener('resize', listener);
  }, []);
  return null;
};

const App = () => {
  useResizeDetector(); 
  
  return (
    <div className="layout">
      <VerySlowComponent />
    </div>
  );
};
```

[DO]
```javascript
// Isolate the hook to only the specific component that needs it.
const useResizeDetector = () => {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const listener = () => setWidth(window.innerWidth);
    window.addEventListener('resize', listener);
    return () => window.removeEventListener('resize', listener);
  }, []);
  return width;
};

const ResponsiveElement = () => {
  const width = useResizeDetector();
  return <div>Current width is {width}</div>;
};

const App = () => {
  return (
    <div className="layout">
      <ResponsiveElement />
      <VerySlowComponent />
    </div>
  );
};
```