@Domain
Trigger these rules when the user requests assistance with error handling, application stability, preventing app crashes, catching fetch/async errors, implementing Error Boundaries, or debugging blank screens/unmounts in React applications.

@Vocabulary
- **React Lifecycle Errors:** Errors that occur during the rendering phase, inside React lifecycle methods, or inside hooks (but outside of asynchronous callbacks).
- **Async/Event Errors:** Errors that occur outside the React lifecycle, such as inside Promises, `setTimeout`, `fetch` requests, or event handler callbacks (e.g., `onClick`).
- **Component Element Definition:** The object created when writing JSX (e.g., `<Child />`). It is a description of an element, not the synchronous execution of the component's render function.
- **Error Boundary:** A React class component that implements `static getDerivedStateFromError(error)` and optionally `componentDidCatch(error, errorInfo)` to catch React Lifecycle Errors anywhere in its child component tree.
- **Async Error Thrower Hack:** A pattern used to catch an Async/Event Error and re-throw it inside a React state updater function (e.g., `setState(() => { throw error; })`), forcing the error into the React lifecycle so an Error Boundary can catch it.

@Objectives
- Prevent the entire React application from unmounting and displaying a blank screen by strategically implementing Error Boundaries.
- Ensure `try/catch` blocks are placed correctly, accounting for asynchronous execution and the React component lifecycle.
- Prevent infinite re-render loops caused by improper state updates inside render-phase `try/catch` blocks.
- Unify error handling by delegating Async/Event Errors to Error Boundaries using the Async Error Thrower Hack or the `react-error-boundary` library.

@Guidelines
- The AI MUST NOT rely on `try/catch` blocks wrapping JSX elements (e.g., `try { return <Child /> } catch(e) {}`) because JSX evaluation does not synchronously trigger the child's render function.
- The AI MUST NOT wrap a `useEffect` hook from the outside with a `try/catch` block. Because `useEffect` runs asynchronously after the render, the `try/catch` will have already finished executing and will fail to catch the error.
- The AI MUST place `try/catch` blocks *inside* the `useEffect` callback if it intends to catch errors originating from the effect.
- The AI MUST NOT call state setter functions inside a `catch` block that executes during the main render phase. Doing so triggers an infinite re-render loop. If catching an error during render, the AI MUST return a fallback JSX directly from the `catch` block.
- The AI MUST use Error Boundaries to catch React Lifecycle Errors originating from nested child components.
- The AI MUST implement Error Boundaries using class components with `static getDerivedStateFromError` to update the fallback UI state, and `componentDidCatch` to log the error.
- The AI MUST recognize that Error Boundaries DO NOT catch Async/Event Errors natively.
- To catch Async/Event Errors using an Error Boundary, the AI MUST use the Async Error Thrower Hack: catch the error using a standard `try/catch`, trigger a state update, and re-throw the error from within the state updater function.
- The AI MAY abstract the Async Error Thrower Hack into custom hooks (e.g., `useThrowAsyncError`) or higher-order function wrappers (e.g., `useCallbackWithErrorHandling`).
- The AI MAY recommend or use the `react-error-boundary` library as a valid, community-standard alternative to manually implementing class-based Error Boundaries and async thrower hooks.

@Workflow
1. **Identify the Error Source:** Determine if the potential error is a React Lifecycle Error (during render/effects) or an Async/Event Error (callbacks, fetches, promises).
2. **Implement Error Boundaries:** For React Lifecycle Errors, wrap the vulnerable component tree in an `<ErrorBoundary>` component.
3. **Handle Effect Errors:** For errors inside `useEffect`, place the `try/catch` block *inside* the effect's callback.
4. **Handle Render Phase Errors (Non-Boundary):** If using `try/catch` inside a component's render body directly, immediately return fallback JSX in the `catch` block. NEVER use `setState` in this specific block.
5. **Bridge Async Errors to Boundaries:** For event handlers or async code, implement a `try/catch` block. In the `catch` block, use `setState(() => { throw error })` to push the error into the React lifecycle, allowing the nearest Error Boundary to handle it.
6. **Abstract for Reusability:** If the component has multiple async handlers, extract the Async Error Thrower Hack into a custom hook to maintain clean component code.

@Examples (Do's and Don'ts)

**Principle: Catching errors inside `useEffect`**
- [DO]
```javascript
useEffect(() => {
  try {
    throw new Error('Hulk smash!');
  } catch (e) {
    // Handle error locally or push to boundary
  }
}, []);
```
- [DON'T]
```javascript
try {
  useEffect(() => {
    throw new Error('Hulk smash!');
  }, []);
} catch (e) {
  // WILL NEVER BE CALLED. useEffect runs asynchronously.
}
```

**Principle: Catching errors from nested child components**
- [DO]
```javascript
const Component = () => {
  return (
    <ErrorBoundary fallback={<SomeErrorScreen />}>
      <Child />
    </ErrorBoundary>
  );
};
```
- [DON'T]
```javascript
const Component = () => {
  try {
    return <Child />;
  } catch (e) {
    // WILL NEVER BE CALLED. <Child /> is just an object definition.
  }
};
```

**Principle: Handling errors directly during the render phase**
- [DO]
```javascript
const Component = () => {
  try {
    doSomethingComplicated();
  } catch (e) {
    return <SomeErrorScreen />; // Safely returning fallback UI
  }
  return <SomeComponentContent />;
};
```
- [DON'T]
```javascript
const Component = () => {
  const [hasError, setHasError] = useState(false);
  try {
    doSomethingComplicated();
  } catch (e) {
    setHasError(true); // CAUSES INFINITE RE-RENDER LOOP!
  }
  if (hasError) return <SomeErrorScreen />;
  return <SomeComponentContent />;
};
```

**Principle: Catching Async/Event Errors with Error Boundaries (Async Error Thrower Hack)**
- [DO]
```javascript
const Component = () => {
  const [state, setState] = useState();

  const onClick = () => {
    try {
      // Async or event code that throws
      throw new Error('Something bad happened');
    } catch (e) {
      // Re-throw into React's lifecycle to be caught by ErrorBoundary
      setState(() => {
        throw e;
      });
    }
  };

  return <button onClick={onClick}>Click me</button>;
};
```
- [DON'T]
```javascript
const Component = () => {
  const onClick = () => {
    // ErrorBoundary WILL NOT catch this error natively! It will disappear into the void.
    throw new Error('Something bad happened');
  };

  return <button onClick={onClick}>Click me</button>;
};
```