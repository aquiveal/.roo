# @Domain
These rules apply when the AI is instructed to implement, refactor, or optimize state management in React, specifically dealing with passing state deep into component trees, avoiding props drilling, creating React Contexts, consuming Contexts, or mitigating unnecessary re-renders caused by Context value changes.

# @Vocabulary
- **Props Drilling**: The process of passing state and state-setter functions through multiple layers of intermediate components that do not use the data themselves.
- **Children as Props Pattern**: A composition technique where a component receives UI elements via the `children` prop, ensuring that the parent's state changes do not force the children to re-render.
- **Context Provider**: A component (`Context.Provider`) that supplies a `value` to all descendant components.
- **Context Consumer**: Any component deep in the tree that accesses the Provider's value using the `useContext` hook.
- **Referential Equality Problem**: The issue where recreating an object or function on every render creates a new reference, failing shallow comparison and triggering re-renders in consumers.
- **Split Providers**: The architectural pattern of separating a single Context into two distinct Contexts: one for changing state (`ContextData`) and one for static functions/actions (`ContextApi`).
- **Context Selectors**: A pattern used to extract a specific piece of context data without triggering re-renders on other context changes, achieved in React via Higher-Order Components (HOCs) combined with `React.memo`.

# @Objectives
- The AI MUST utilize Context to prevent bloated APIs and intermediate component re-renders caused by props drilling.
- The AI MUST protect Context consumers from unnecessary re-renders caused by the parent of the Context Provider.
- The AI MUST decouple static API functions (like `open`/`close`) from volatile state data (like `isOpen`) using Split Providers.
- The AI MUST ensure that functions relying on previous state do not break Context API memoization by utilizing `useReducer` instead of `useState`.
- The AI MUST simulate Context selectors using HOCs and `React.memo` when Provider splitting is not feasible or desired for granular performance tuning.

# @Guidelines
- **Context over Props Drilling**: When state needs to be accessed by deeply nested components, the AI MUST extract the state and its modifiers into a Context rather than passing them as props through intermediate components.
- **Provider Composition**: When creating a component that manages Context state, the AI MUST use the "children as props" pattern (`({ children }) => <Context.Provider>{children}</Context.Provider>`) to insulate the rest of the application from the provider's state updates.
- **Mandatory Value Memoization**: The AI MUST NEVER pass inline objects or unmemoized variables directly to the `value` prop of a Context Provider. The AI MUST wrap the `value` object in `useMemo` and any functions passed inside it in `useCallback`.
- **Split Providers Implementation**: If a Context value contains both state variables and functions that modify the state, the AI MUST evaluate if consumers use *only* the functions. If so, the AI MUST split the Context into `ContextData` (for state) and `ContextApi` (for functions) to prevent function-only consumers from re-rendering when the state changes.
- **Reducer over State for API Contexts**: When using Split Providers, if an API function requires access to the current state (e.g., a `toggle` function), the AI MUST NOT use `useState`. Instead, the AI MUST use `useReducer` so that dispatch actions can be passed into the API Context without creating a dependency on the volatile state.
- **Context Selector HOCs**: When a heavy component requires only a single specific value or function from a Context and MUST NOT re-render when other Context values change, the AI MUST implement a Context Selector using a Higher-Order Component.
    - The HOC MUST extract the needed value via `useContext`.
    - The HOC MUST wrap the target component in `React.memo`.
    - The HOC MUST pass the extracted context value to the memoized target component as a prop.

# @Workflow
When tasked with implementing or refactoring shared state using Context, the AI MUST follow this rigid step-by-step algorithm:
1. **Extract State**: Remove the shared state from the high-level application component and place it inside a dedicated Controller/Provider component.
2. **Implement Children Pattern**: Structure the Controller component to accept and return the `children` prop to prevent top-down re-renders.
3. **Analyze Context Shape**: Determine if the Context payload includes both volatile data (state) and static actions (functions).
4. **Determine Splitting**: 
    - If the context is simple, create a single Context. Wrap functions in `useCallback` and the value object in `useMemo`.
    - If the context is complex and consumed by structurally distinct components, create two Contexts (`ContextData` and `ContextApi`).
5. **Resolve Dependencies**: If Split Providers are used and an action in `ContextApi` depends on state data, convert the state management from `useState` to `useReducer`. Pass the `dispatch` actions into the `ContextApi`'s `useMemo` payload with no state dependencies.
6. **Provider Nesting**: Render the Providers in the Controller component (`<ContextData.Provider><ContextApi.Provider>{children}</ContextApi.Provider></ContextData.Provider>`).
7. **Consumer Implementation**: Create custom hooks (e.g., `useData()`, `useApi()`) and implement them in the deep components that explicitly require the data or actions.
8. **Selector Optimization (Optional)**: If a specific heavy component consumes a context that frequently updates, create a selector HOC to isolate the specific prop, wrap the heavy component in `React.memo`, and apply the HOC.

# @Examples (Do's and Don'ts)

### Context Value Memoization
**[DON'T]** Pass unmemoized objects or functions directly to the Context Provider's value prop.
```jsx
const NavigationController = ({ children }) => {
  const [isNavExpanded, setIsNavExpanded] = useState(false);
  const toggle = () => setIsNavExpanded(!isNavExpanded);

  // Anti-pattern: Object and function recreated on every parent re-render
  const value = { isNavExpanded, toggle }; 

  return <Context.Provider value={value}>{children}</Context.Provider>;
};
```

**[DO]** Memoize the functions with `useCallback` and the value payload with `useMemo`.
```jsx
const NavigationController = ({ children }) => {
  const [isNavExpanded, setIsNavExpanded] = useState(false);

  const toggle = useCallback(() => {
    setIsNavExpanded(!isNavExpanded);
  }, [isNavExpanded]);

  const value = useMemo(() => {
    return { isNavExpanded, toggle };
  }, [isNavExpanded, toggle]);

  return <Context.Provider value={value}>{children}</Context.Provider>;
};
```

### Split Providers and Reducers
**[DON'T]** Group state and functions in a single Context if consumers rely solely on the functions, or use `useState` if it forces the API to depend on volatile state.
```jsx
const Context = React.createContext();

const NavigationController = ({ children }) => {
  const [isNavExpanded, setIsNavExpanded] = useState(false);
  
  // Anti-pattern: Toggle forces the API to update on every state change
  const toggle = useCallback(() => setIsNavExpanded(!isNavExpanded), [isNavExpanded]);
  const open = useCallback(() => setIsNavExpanded(true), []);
  const close = useCallback(() => setIsNavExpanded(false), []);

  const value = useMemo(() => ({ isNavExpanded, open, close, toggle }), [isNavExpanded, open, close, toggle]);

  return <Context.Provider value={value}>{children}</Context.Provider>;
}
```

**[DO]** Split the data and API into two providers, and use `useReducer` to remove state dependencies from the API functions.
```jsx
const ContextData = React.createContext({ isNavExpanded: false });
const ContextApi = React.createContext({ open: () => {}, close: () => {}, toggle: () => {} });

const reducer = (state, action) => {
  switch (action.type) {
    case 'open-sidebar': return { ...state, isNavExpanded: true };
    case 'close-sidebar': return { ...state, isNavExpanded: false };
    case 'toggle-sidebar': return { ...state, isNavExpanded: !state.isNavExpanded };
    default: return state;
  }
};

const NavigationController = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, { isNavExpanded: true });

  const data = useMemo(() => ({ isNavExpanded: state.isNavExpanded }), [state.isNavExpanded]);

  const api = useMemo(() => {
    return {
      open: () => dispatch({ type: 'open-sidebar' }),
      close: () => dispatch({ type: 'close-sidebar' }),
      toggle: () => dispatch({ type: 'toggle-sidebar' }),
    };
  }, []); // No dependency on state!

  return (
    <ContextData.Provider value={data}>
      <ContextApi.Provider value={api}>
        {children}
      </ContextApi.Provider>
    </ContextData.Provider>
  );
};
```

### Context Selectors via HOCs
**[DON'T]** Extract a value inside a component if it causes unnecessary re-renders, and do not attempt to solve it by memoizing the extracted value locally.
```jsx
const SomeHeavyComponent = () => {
  // Anti-pattern: If Context changes, this component re-renders even if `open` didn't change
  const { open } = useContext(Context); 
  const memoizedOpen = useMemo(() => open, []); // Useless against context re-renders

  return <button onClick={memoizedOpen} />;
};
```

**[DO]** Create a Higher-Order Component that reads the Context, wraps the inner component in `React.memo`, and passes the targeted Context value as a prop.
```jsx
// 1. Create the HOC
const withNavigationOpen = (AnyComponent) => {
  // 2. Memoize the target component
  const AnyComponentMemo = React.memo(AnyComponent);

  return (props) => {
    // 3. Extract specific context value
    const { open } = useContext(Context);

    // 4. Pass the extracted value as a prop. 
    // The HOC re-renders, but the Memoized component only re-renders if `open` or `props` change.
    return <AnyComponentMemo {...props} openNav={open} />;
  };
};

// 5. Apply the HOC
const SomeHeavyComponent = withNavigationOpen(({ openNav }) => {
  return <button onClick={openNav} />;
});
```