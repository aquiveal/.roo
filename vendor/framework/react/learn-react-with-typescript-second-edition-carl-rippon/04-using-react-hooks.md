@Domain
Trigger these rules when creating, modifying, or reviewing React functional components, specifically when implementing React Hooks (`useEffect`, `useState`, `useReducer`, `useRef`, `useMemo`, `useCallback`), handling component state, performing data fetching within components, or optimizing React rendering performance.

@Vocabulary
- **Hook**: A special function that lets you "hook into" React state and lifecycle features from function components.
- **Side Effect**: An operation executed outside the scope of the component's predictable rendering process, such as web service requests or manual DOM manipulation.
- **Effect Cleanup**: A function returned by an effect to remove subscriptions, event listeners, or cancel asynchronous tasks, preventing memory leaks when a component unmounts.
- **Strict Mode**: A development-only React feature that intentionally executes effect functions twice to help detect side-effect bugs and prepare for future React features.
- **Tuple**: An array with a fixed number of elements of known types, commonly used as the return type for hooks like `useState` and `useReducer` (e.g., `[state, setter]`).
- **Reducer**: A pure function used in `useReducer` that takes the current state and an action, returning a completely new state object.
- **Action**: An object dispatched to a reducer describing a state change, conventionally containing a `type` property.
- **Ref**: A mutable object created by `useRef` whose `.current` property is persisted across renders without causing a component re-render when changed.
- **Memoization**: A performance optimization technique storing the results of expensive function calls or object references, implemented in React via `useMemo`, `useCallback`, and the `memo` function.

@Objectives
- Enforce the absolute strictness of the "Rules of Hooks".
- Implement safe and memory-leak-free side effects using `useEffect`.
- Choose the correct state management Hook (`useState` vs `useReducer`) based on state complexity.
- Ensure strict immutability when updating state, particularly within reducers.
- Accurately manage DOM element references and persistent variable tracking using `useRef`.
- Apply memoization hooks (`useMemo`, `useCallback`) strategically to prevent unnecessary re-renders without prematurely complicating the codebase.

@Guidelines

**Rules of Hooks:**
- The AI MUST call Hooks ONLY at the top level of a React function component.
- The AI MUST NEVER call Hooks inside loops, conditions, or nested functions (including event handlers).
- The AI MUST call Hooks ONLY from React function components or custom Hooks, NEVER from class components or regular JavaScript functions.

**Effect Hook (`useEffect`):**
- When attaching DOM event listeners or subscriptions inside `useEffect`, the AI MUST return a cleanup function to detach them.
- When performing asynchronous operations (like `fetch`), the AI MUST NOT mark the effect function itself as `async`. Instead, define an internal `async` function and immediately invoke it, or use standard `.then()` promise syntax.
- When updating state based on fetched data, the AI MUST use a local boolean flag (e.g., `let cancel = false;`) inside the effect to ensure state is not set if the component unmounts during the request.
- The AI MUST pass an explicit dependency array (e.g., `[]` for on-mount only) as the second argument to prevent infinite re-render loops.

**State Hooks (`useState`, `useReducer`):**
- The AI MUST use `useState` for primitive values or independent state variables.
- The AI MUST use `useReducer` for complex state objects with interdependent properties or when state changes heavily depend on previous state values.
- When updating state based on its previous value in `useState`, the AI SHOULD use the callback parameter form of the state setter (e.g., `setScore(prev => prev + 1)`).
- The AI MUST recognize that state updates are batched; therefore, the AI MUST NOT attempt to read the newly set state synchronously on the very next line of code.
- Within `useReducer`, the AI MUST NEVER mutate the `state` object directly. The AI MUST return a completely new state object using the spread operator (`...state`).
- When typing `useReducer` in TypeScript, the AI MUST explicitly define the types using the generic parameter: `useReducer<Reducer<State, Action>>(reducer, initialState)`.

**Ref Hook (`useRef`):**
- The AI MUST use `useRef` to store mutable values that do not necessitate a component re-render when changed.
- The AI MUST use `useRef` to imperatively access HTML elements by assigning the ref to the element's `ref` attribute.
- The AI MUST access or modify the ref's value strictly through its `.current` property.
- When invoking DOM methods on a ref (e.g., `focus()`), the AI MUST use the optional chaining operator (`?.`) to safely handle potential `null` values (e.g., `ref.current?.focus()`).

**Memoization Hooks (`useMemo`, `useCallback`, and `memo`):**
- The AI MUST use `useMemo` exclusively to cache the results of computationally expensive functions, passing a precise dependency array.
- The AI MUST use the `memo` function to wrap child components to prevent unnecessary re-renders when parent state changes but child props do not.
- When passing function props to a `memo`-wrapped child component, the AI MUST wrap the parent's handler function in `useCallback` to maintain a stable function reference across renders.
- The AI MUST NOT apply `useMemo` or `useCallback` to cheap operations, as the overhead of memoization can cost more than the operation itself.

@Workflow
1. **Hook Validation**: Before writing any hook, confirm the cursor is at the top level of a React function component, outside of any blocks or conditional statements.
2. **State Selection**: Evaluate the data being stored. If it is primitive or isolated, instantiate `useState`. If it is a complex object with multiple sub-values or transition states, define an `Action` union type, a `State` type, a pure `reducer` function, and instantiate `useReducer`.
3. **Side Effect Implementation**: 
   - Define the `useEffect` block.
   - Inject the exact dependencies into the dependency array.
   - If performing async fetching, implement the `cancel` flag pattern.
   - If setting up listeners, write the `return () => { ... }` cleanup function.
4. **Ref Utilization**: If direct DOM manipulation or persistent non-rendering values are needed, instantiate `useRef`, explicitly type it (e.g., `<HTMLInputElement>(null)`), and use `?.` when calling methods on `.current`.
5. **Performance Audit**: Review the component tree. Only if a child component is rendering unnecessarily and causing proven performance issues, wrap the child in `memo` and wrap the passed event handlers in `useCallback`.

@Examples (Do's and Don'ts)

[DO] Enforce the Rules of Hooks by keeping Hooks at the top level.
```tsx
export function MyComponent({ someProp }) {
  useEffect(() => {
    if (someProp) {
      console.log("Some effect");
    }
  }, [someProp]);

  if (!someProp) {
    return null;
  }
  return <div>{someProp}</div>;
}
```

[DON'T] Call Hooks conditionally or after early returns.
```tsx
export function MyComponent({ someProp }) {
  if (!someProp) {
    return null;
  }
  // VIOLATION: Hook is called after a conditional return
  useEffect(() => {
    console.log("Some effect");
  });
  return <div>{someProp}</div>;
}
```

[DO] Implement safe asynchronous data fetching in `useEffect` with a cancellation flag.
```tsx
useEffect(() => {
  let cancel = false;
  async function fetchPerson() {
    const person = await getPerson();
    if (!cancel) {
      setName(person.name);
    }
  }
  fetchPerson();

  return () => {
    cancel = true;
  };
}, []);
```

[DON'T] Pass an `async` function directly to `useEffect` or omit the unmounted component check.
```tsx
// VIOLATION: useEffect cannot accept an async function directly
useEffect(async () => {
  const person = await getPerson();
  setName(person.name); // Potential memory leak if unmounted
}, []);
```

[DO] Use standard cleanup functions in `useEffect` for event listeners.
```tsx
useEffect(() => {
  function handleClick() {
    onClickAnywhere();
  }
  document.addEventListener("click", handleClick);
  return () => {
    document.removeEventListener("click", handleClick);
  };
}, [onClickAnywhere]);
```

[DON'T] Attach listeners in `useEffect` without a cleanup function.
```tsx
useEffect(() => {
  // VIOLATION: Missing return cleanup function causes memory leaks
  document.addEventListener("click", () => onClickAnywhere());
});
```

[DO] Maintain strict immutability in `useReducer` by using the spread operator.
```tsx
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, score: state.score + 1 };
    default:
      return state;
  }
}
```

[DON'T] Mutate state directly within a reducer.
```tsx
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      // VIOLATION: Direct mutation of state object
      state.score = state.score + 1;
      return state;
    default:
      return state;
  }
}
```

[DO] Use optional chaining when calling methods on a typed `useRef` current value.
```tsx
export function PersonScore() {
  const addButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    addButtonRef.current?.focus();
  }, []);

  return <button ref={addButtonRef}>Add</button>;
}
```

[DON'T] Call methods on a ref without verifying `.current` is not null.
```tsx
export function PersonScore() {
  const addButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    // VIOLATION: Unsafe call, could throw if current is null
    addButtonRef.current.focus();
  }, []);

  return <button ref={addButtonRef}>Add</button>;
}
```