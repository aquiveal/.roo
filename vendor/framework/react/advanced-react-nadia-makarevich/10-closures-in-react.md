@Domain
When modifying, creating, analyzing, or debugging React functional components that utilize state, callbacks, memoization (`React.memo`, `useCallback`, `useMemo`), refs for storing functions (`useRef`), or effects (`useEffect`), specifically when dealing with frequently updating state, callback props, and the prevention of unnecessary re-renders.

@Vocabulary
- **Closure**: A function that "closes over" and freezes the variables from its surrounding scope at the exact moment of its creation. Every function declared inside a React component is a closure.
- **Stale Closure**: A performance bug where a cached closure (stored via `useCallback`, `useMemo`, `useRef`, or an external cache) retains outdated, "frozen" state or props because the closure was not re-created or refreshed when the underlying data changed.
- **Mutable Ref**: A reference object created by `useRef` that persists across re-renders. While closures freeze the state of variables, they only freeze the *reference* to the ref object, allowing `ref.current` to be mutated and accessed dynamically inside a frozen closure.
- **Closure Trap Escape Pattern**: A specific architectural pattern combining a mutable `useRef`, a dependency-less `useEffect`, and a dependency-less `useCallback` to provide a stable function reference that always has access to the latest component state.

@Objectives
- The AI MUST actively identify and prevent stale closures when caching functions using React hooks or Refs.
- The AI MUST ensure that performance optimizations (like `React.memo`) do not compromise the accuracy of state accessed within callbacks.
- The AI MUST apply the "Closure Trap Escape Pattern" when a component requires a stable callback reference (to prevent child re-renders) but that callback simultaneously requires access to frequently changing state.
- The AI MUST evaluate custom comparison functions in `React.memo` to ensure they do not inadvertently cache stale callback references.

@Guidelines
- **Closure Awareness**: The AI MUST treat every inline function, `useEffect`, and `useCallback` inside a React component as a static snapshot of the component's state at the time of the render.
- **Dependency Arrays**: The AI MUST include all referenced local state and props in the dependency arrays of `useCallback` and `useEffect`. Omitting dependencies explicitly causes the stale closure problem.
- **Function Refs Updating**: When using `useRef` to store a callback function to avoid dependency changes, the AI MUST NOT rely solely on the initial value passed to `useRef(callback)`. The AI MUST update `ref.current` inside a `useEffect` whenever the referenced state or props change.
- **React.memo Custom Comparisons**: The AI MUST NOT omit callback functions from `React.memo` custom comparison functions (e.g., `(before, after) => before.title === after.title`) to force memoization, unless the passed callback is explicitly designed to handle state updates via the Closure Trap Escape Pattern. Doing so blindly caches the first render's closure, making it infinitely stale.
- **The Object Mutability Exception**: The AI MUST understand that closures do not deep-clone objects. If a closure captures a `ref` object, it captures the reference to the object, not the properties inside it. The AI MUST leverage this by updating `ref.current` to access fresh data inside an otherwise stale closure.
- **Implementing the Closure Trap Escape Pattern**: When required to pass a callback to a heavily memoized child component without triggering re-renders, while accessing the latest state, the AI MUST strictly follow this pattern:
  1. Declare a ref: `const callbackRef = useRef();`
  2. Update the ref with the latest closure on every render using an empty-dependency effect: `useEffect(() => { callbackRef.current = () => { /* use latest state */ } });`
  3. Create a stable callback that invokes the ref: `const stableCallback = useCallback(() => { callbackRef.current?.(); }, []);`
  4. Pass `stableCallback` to the child component.

@Workflow
1. **Analyze Callback Dependencies**: When defining a callback function inside a component, identify all state variables and props accessed within it.
2. **Evaluate Memoization Requirements**: Determine if the callback is passed to a child component wrapped in `React.memo` or used as a dependency in downstream hooks.
3. **Check for Stale Closure Risks**: If the callback is wrapped in `useCallback`, verify the dependency array. If adding dependencies causes excessive re-renders of memoized child components, proceed to step 4.
4. **Inspect Custom Memoization**: If `React.memo` uses a custom comparison function, check if it ignores callback props. If it ignores them, the callback passed MUST be stable and immune to stale closures.
5. **Apply the Closure Trap Escape Pattern**: If a callback must be referentially stable (no dependencies) but must access volatile state (like text input value), implement the mutable ref + `useEffect` + `useCallback` architecture exactly as defined in the guidelines.
6. **Verify Ref Updates**: If using `useRef` to hold a function, verify there is a corresponding `useEffect` updating `ref.current` with the latest function closure.

@Examples (Do's and Don'ts)

**Principle: Using useCallback without creating Stale Closures**
- [DO] Include all state variables used inside the callback in the dependency array.
```javascript
const Component = () => {
  const [state, setState] = useState();

  const onClick = useCallback(() => {
    console.log(state);
  }, [state]); 
}
```
- [DON'T] Omit dependencies to artificially keep the reference stable, which creates a stale closure logging the initial state forever.
```javascript
const Component = () => {
  const [state, setState] = useState();

  const onClick = useCallback(() => {
    // state will ALWAYS be undefined (initial value)
    console.log(state);
  }, []); 
}
```

**Principle: Storing functions in Refs safely**
- [DO] Update the ref containing the function inside a `useEffect` to capture the latest closure.
```javascript
const Component = ({ someProp }) => {
  const [state, setState] = useState();
  const ref = useRef();

  useEffect(() => {
    // Updates on state/prop change, keeping the closure fresh
    ref.current = () => {
      console.log(someProp);
      console.log(state);
    };
  }, [state, someProp]);
}
```
- [DON'T] Initialize the ref with a function and never update it, freezing the closure at the initial mount.
```javascript
const Component = ({ someProp }) => {
  const [state, setState] = useState();

  // Initializes once. The closure is stale immediately after the first state change.
  const ref = useRef(() => {
    console.log(someProp);
    console.log(state);
  });
}
```

**Principle: Escaping the Closure Trap for Memoized Components**
- [DO] Use the mutable ref trick to provide a completely stable callback that always executes the latest closure.
```javascript
const HeavyComponentMemo = React.memo(HeavyComponent);

const Form = () => {
  const [value, setValue] = useState('');
  const ref = useRef();

  // 1. Update ref on every render (no dependency array)
  useEffect(() => {
    ref.current = () => {
      console.log(value); // Always has latest value
    };
  });

  // 2. Stable callback (empty dependency array)
  const onClick = useCallback(() => {
    ref.current?.();
  }, []);

  return (
    <>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      {/* HeavyComponentMemo will NOT re-render on keystrokes, but onClick works perfectly */}
      <HeavyComponentMemo title="Welcome" onClick={onClick} />
    </>
  );
};
```
- [DON'T] Use a custom comparison function to ignore the callback while passing a continuously updating unmemoized callback, which creates a permanently stale closure inside the memoized component.
```javascript
// DANGEROUS: Ignores onClick, causing the child to hold onto the first render's onClick closure.
const HeavyComponentMemo = React.memo(HeavyComponent, (before, after) => {
  return before.title === after.title; 
});

const Form = () => {
  const [value, setValue] = useState('');

  // This closure is re-created on every render, but HeavyComponentMemo 
  // ignores the update and holds the very first one where value is ''
  const onClick = () => {
    console.log(value); 
  };

  return (
    <>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <HeavyComponentMemo title="Welcome" onClick={onClick} />
    </>
  );
};
```