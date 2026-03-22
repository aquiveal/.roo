# @Domain
Trigger these rules when writing, refactoring, or optimizing React components, specifically when the user requests performance improvements, addresses unnecessary re-renders, or when the AI detects the usage or potential usage of `useMemo`, `useCallback`, or `React.memo`.

# @Vocabulary
*   **Primitive Values**: Values compared by actual value (e.g., strings, booleans, numbers). `a === b` evaluates to true if values match.
*   **Non-Primitive Values**: Objects, arrays, and functions. Compared by reference in memory, not by shape. Two identically shaped objects evaluate to false unless they point to the exact same reference.
*   **Reference Equality / Referential Stability**: Ensuring a non-primitive value maintains the exact same memory reference across component re-renders so that shallow comparisons return true.
*   **Re-render**: The process where React calls the component's function again, inherently re-creating all locally defined variables and inline functions.
*   **Shallow Comparison**: The exact method (`Object.is`) React uses in hooks' dependencies and `React.memo` to compare previous and current values.
*   **React.memo**: A higher-order component that halts the natural re-render chain by performing a shallow comparison of all incoming props. If no props change reference/value, the component skips re-rendering.
*   **Element Object**: The underlying Javascript object returned by JSX syntax (e.g., `<Child />` translates to `{ type: Child, props: {} }`). It is recreated on every render.

# @Objectives
*   Prevent the misuse and overuse of `useMemo` and `useCallback` on standard, non-memoized components.
*   Ensure that when `React.memo` is used, its implementation is flawless, meaning absolutely no props (including `children` and spread props) break referential equality.
*   Bust the "props change causes re-renders" myth: enforce the understanding that components re-render because their parent re-renders, regardless of props, unless wrapped in `React.memo`.
*   Prevent unnecessary memory and initialization overhead from premature memoization of cheap Javascript calculations.

# @Guidelines
*   **Rule of Referential Equality**: The AI MUST treat all inline objects, arrays, and functions defined inside a React component as unstable references that will fail dependency arrays and `React.memo` checks on every re-render.
*   **useCallback Execution Reality**: The AI MUST understand that `useCallback` does *not* prevent the recreation of the inline function passed as its first argument. The function is recreated on every render; React simply discards the new one and returns the cached one if dependencies haven't changed. Therefore, the AI MUST NOT place expensive executions inline inside the first argument of `useCallback` (e.g., `useCallback(expensiveCalc(), [])`).
*   **Anti-Pattern: Useless Prop Memoization**: The AI MUST NOT wrap functions in `useCallback` or objects in `useMemo` solely to pass them as props to a standard, unmemoized child component. This does nothing to prevent the child from re-rendering and only adds cognitive and processing overhead.
*   **Valid Use Cases for useCallback/useMemo**: The AI MUST restrict the use of `useCallback` and `useMemo` to only three scenarios:
    1. The value/function is passed as a prop to a component wrapped in `React.memo`.
    2. The value/function is used as a dependency in a downstream hook (like `useEffect`).
    3. The value/function is being passed down to other components that meet conditions 1 or 2.
*   **React.memo Strict Prop Auditing**: If the AI implements `React.memo`, it MUST audit every single prop passed to that component. If even one prop breaks referential equality, the AI MUST flag the `React.memo` wrapper as completely useless and fix the offending prop.
*   **No Prop Spreading on Memoized Components**: The AI MUST NOT use the spread operator for props (`<ChildMemo {...props} />`) on components wrapped in `React.memo`, as it is impossible to guarantee referential stability of unknown upstream props. Props MUST be passed explicitly.
*   **Opaque Custom Hook Returns**: The AI MUST NOT pass non-primitive returns from custom hooks (e.g., `const { submit } = useForm();`) directly into a `React.memo` component unless the AI can definitively prove the custom hook memoizes that return value.
*   **The Children Prop Trap**: The AI MUST recognize that JSX children (e.g., `<ChildMemo><div>Text</div></ChildMemo>`) are non-primitive objects (`props.children`). If passing children to a `React.memo` component, the AI MUST wrap the JSX children in `useMemo`.
*   **The Render Prop Trap**: The AI MUST recognize that children passed as functions (`<ChildMemo>{() => <div/>}</ChildMemo>`) are recreated on every render. They MUST be wrapped in `useCallback` or `useMemo` when passed to a memoized component.
*   **Memoized Components as Children**: The AI MUST recognize that wrapping a child component in `React.memo` does NOT make the Element object itself stable. `<ParentMemo><ChildMemo /></ParentMemo>` still breaks `ParentMemo`'s props check. The element `<ChildMemo />` must be wrapped in `useMemo` before being passed to `ParentMemo`.
*   **Expensive Calculation Verification**: The AI MUST NOT proactively wrap standard array operations (e.g., sorting 300 items), string concatenations, or basic regex in `useMemo` under the guise of "expensive calculations". The AI must prioritize preventing component re-renders (DOM updates) over memoizing cheap JS operations.

# @Workflow
1.  **Analyze Re-render Goal**: Determine if the task is to prevent a specific component from re-rendering.
2.  **Check Child Memoization Requirement**: If preventing a child re-render, verify if the child is wrapped in `React.memo`. If it is not, wrapping its props in `useCallback` or `useMemo` in the parent is forbidden.
3.  **Implement React.memo**: Wrap the target child in `React.memo`.
4.  **Audit All Incoming Props**:
    *   Trace every prop passed to the memoized child.
    *   If a prop is a primitive (string, boolean, number), pass it directly.
    *   If a prop is an object or array, wrap it in `useMemo`.
    *   If a prop is a function, wrap it in `useCallback`.
    *   If a prop is a JSX element or a render function (including `children`), wrap it in `useMemo` or `useCallback`.
5.  **Remove Prop Spreading**: Identify any `<Component {...props} />` on the memoized child and replace it with explicit prop declarations.
6.  **Verify Hook Dependencies**: For all newly created `useMemo` and `useCallback` hooks, strictly populate the dependency array.

# @Examples (Do's and Don'ts)

### 1. Memoizing Props on Standard Components
**[DON'T]**
```javascript
// Anti-pattern: Memoizing props when the child is NOT wrapped in React.memo.
// React will re-render <Button> anyway when <Component> re-renders.
const Component = () => {
  const onClick = useCallback(() => {
    console.log("clicked");
  }, []);

  return <Button onClick={onClick}>Click me</Button>;
};
```

**[DO]**
```javascript
// Correct: Do not use useCallback if the child is not memoized and the function isn't a dependency elsewhere.
const Component = () => {
  const onClick = () => {
    console.log("clicked");
  };

  return <Button onClick={onClick}>Click me</Button>;
};
```

### 2. Passing Props to React.memo Components
**[DON'T]**
```javascript
const ChildMemo = React.memo(Child);

const Component = (props) => {
  // Anti-pattern: Spreading unknown props breaks React.memo guarantees.
  // Anti-pattern: Passing an inline function breaks React.memo immediately.
  return <ChildMemo {...props} onChange={() => {}} />;
};
```

**[DO]**
```javascript
const ChildMemo = React.memo(Child);

const Component = (props) => {
  const onChange = useCallback(() => {
    console.log("changed");
  }, []);

  // Correct: Explicitly defining props and ensuring referential stability for functions.
  return <ChildMemo someProp={props.some} onChange={onChange} />;
};
```

### 3. Passing Children to React.memo Components
**[DON'T]**
```javascript
const ChildMemo = React.memo(Child);

const Component = () => {
  // Anti-pattern: The <div> is an Element object recreated on every render.
  // This breaks ChildMemo's prop check (props.children changes reference).
  return (
    <ChildMemo>
      <div>Some text here</div>
    </ChildMemo>
  );
};
```

**[DO]**
```javascript
const ChildMemo = React.memo(Child);

const Component = () => {
  // Correct: The Element object is referentially stabilized using useMemo.
  const content = useMemo(() => <div>Some text here</div>, []);

  return (
    <ChildMemo>
      {content}
    </ChildMemo>
  );
};
```

### 4. Nested Memoized Components
**[DON'T]**
```javascript
const ChildMemo = React.memo(Child);
const ParentMemo = React.memo(Parent);

const Component = () => {
  // Anti-pattern: <ChildMemo /> creates a NEW Element object on every render.
  // ParentMemo will re-render because its `children` prop reference changed.
  return (
    <ParentMemo>
      <ChildMemo />
    </ParentMemo>
  );
};
```

**[DO]**
```javascript
const ParentMemo = React.memo(Parent);

const Component = () => {
  // Correct: The Element object itself is memoized.
  // Note: Because the Element is memoized, Child doesn't even need React.memo here
  // if the goal is only to prevent ParentMemo from re-rendering.
  const child = useMemo(() => <Child />, []);

  return (
    <ParentMemo>
      {child}
    </ParentMemo>
  );
};
```