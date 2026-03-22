# @Domain

Next.js React state management implementation, encompassing both component-scoped local states and application-wide global states using React Context APIs and Redux, particularly handling Next.js server-side rendering (SSR) and client-side hydration constraints.

# @Vocabulary

- **Local State**: State that is scoped to a single component (e.g., loading states, atom component toggles) managed via `useState` or `useReducer`.
- **Global State**: State shared across multiple components and pages (e.g., shopping cart, UI themes, user sessions) managed via React Context, Redux, Recoil, MobX, or Apollo Client.
- **Unidirectional Data Flow**: React's architectural pattern where data is passed downwards from parent to child via props. State updates flow upwards only via explicitly passed callback functions or global dispatchers.
- **Context API**: React's built-in APIs (`createContext`, `Context.Provider`, `useContext`) for sharing data across the component tree without prop drilling.
- **Store**: The centralized object in Redux that holds the complete state tree of the application.
- **Reducer**: A pure function in Redux that takes the previous state and an action, and returns the next state.
- **Dispatch**: A function used to trigger state changes in Redux by dispatching actions.
- **Selector**: A function (often used with `useSelector` in Redux) to extract specific pieces of data from the global store.
- **Store Memoization**: The technique of caching the Redux store initialization using `useMemo` to prevent expensive re-parsing and re-initialization of complex initial states during re-renders.

# @Objectives

- Distinguish correctly between scenarios requiring local state management versus global state management.
- Implement React Context API for lightweight, built-in global state management that persists across Next.js page transitions.
- Implement Redux for complex global state management with strict adherence to Next.js SSR constraints, ensuring the store is conditionally initialized on the server and client.
- Maintain persistent global state across page navigations by anchoring Providers at the `_app.js` level.
- Prevent anti-patterns such as duplicating global state into local component state.

# @Guidelines

## Local State Management Constraints
- MUST use `useState` or `useReducer` for Atom components (the most basic UI building blocks).
- MUST use local state to manage temporary UI statuses, specifically loading states during client-side data fetching before the data resolves.
- MUST NOT use local state for data that dictates the rendering of separate, unlinked components (e.g., a Navbar and a Product Card).

## React Context API Implementation Rules
- MUST define the Context using `createContext()` with a default structure matching the expected state shape (e.g., `{ items: {}, setItems: () => null }`).
- MUST anchor the Context state using `useState` inside the Next.js `_app.js` custom component to ensure the state persists across page navigations.
- MUST wrap the `<Component {...pageProps} />` inside `_app.js` with the `<Context.Provider>` and pass the state and setter as the `value`.
- Components requiring global state MUST access it strictly using the `useContext(MyContext)` hook.
- MUST NOT keep a redundant local state copy of data that already exists in the Context. Derive computed values directly from the Context state instead.

## Redux Setup and SSR Compatibility Rules
- MUST initialize the Redux store dynamically to handle Next.js's dual execution environment (Node.js server and browser).
- MUST declare a global `let store;` variable outside the initialization function to cache the store on the client-side.
- MUST implement an `initializeStore(preloadedState)` function that:
  1. Creates a new store if one doesn't exist.
  2. Merges `preloadedState` with the existing store state if both exist.
  3. Returns a fresh store without overriding the global variable if running on the server (`typeof window === 'undefined'`).
  4. Assigns the newly created store to the global `store` variable ONLY if running on the client.
- MUST memoize the store instance using a custom hook (e.g., `useStore`) utilizing React's `useMemo` to avoid re-initializing the store on every render.
- MUST wrap the application in `_app.js` with `react-redux`'s `<Provider store={store}>`.
- MUST abstract state retrieval into custom hooks (e.g., `useGlobalItems() { return useSelector((state) => state, shallowEqual); }`) to ensure clean component logic and optimized re-rendering using `shallowEqual`.

# @Workflow

1. **Scope Identification**: Determine if the required state dictates the behavior of a single component (Local) or multiple distinct components across the app (Global).
2. **Local State Path**: 
   - If Local: Implement `useState` directly inside the component.
3. **Global State Path Definition**: 
   - Choose **Context API** for simpler, lightweight shared state.
   - Choose **Redux** for complex, highly scalable state logic requiring dev-tools or middleware.
4. **Context API Execution**:
   - Create `[name]Context.js` exporting `createContext(default)`.
   - In `_app.js`, instantiate state with `useState` and wrap the app in `<[name]Context.Provider value={{ state, setState }}>`.
   - In target components, call `useContext([name]Context)`.
5. **Redux Execution**:
   - Create `store.js` with the reducer, `initStore`, and `initializeStore` (handling `typeof window === 'undefined'`).
   - Create a `useStore` hook wrapping `initializeStore` in `useMemo`.
   - In `_app.js`, call `useStore(pageProps.initialReduxState)` and wrap the app in `<Provider store={store}>`.
   - In target components, build custom hooks using `useSelector` and `shallowEqual` for data, and `useDispatch` for actions.
6. **State Mutation**: Ensure all child components update global state strictly via the context setter or Redux dispatch actions. Do not mutate the state objects directly.

# @Examples (Do's and Don'ts)

## Context API Setup

**[DO]** Anchor global context state properly inside `_app.js`:
```javascript
import { useState } from 'react';
import CartContext from '../components/context/cartContext';

function MyApp({ Component, pageProps }) {
  const [items, setItems] = useState({});

  return (
    <CartContext.Provider value={{ items, setItems }}>
      <Component {...pageProps} />
    </CartContext.Provider>
  );
}
export default MyApp;
```

**[DON'T]** Duplicate global context state into a component's local state:
```javascript
import { useContext, useState, useEffect } from 'react';
import cartContext from '../components/context/cartContext';

function ProductCard({ id }) {
  const { items } = useContext(cartContext);
  // INCORRECT: Creating local state for data that already lives in the global context
  const [localAmount, setLocalAmount] = useState(0); 

  useEffect(() => {
    setLocalAmount(items[id] || 0);
  }, [items, id]);

  return <div>{localAmount}</div>;
}
```
*Correction*: Simply derive the value: `const productAmount = items?.[id] ?? 0;`

## Redux Next.js Initialization

**[DO]** Handle Next.js SSR constraints and client-side caching when initializing the Redux store:
```javascript
import { useMemo } from 'react';
import { createStore, applyMiddleware } from 'redux';

let store;
const initialState = {};

const reducer = (state = initialState, action) => { /* ... */ };

function initStore(preloadedState = initialState) {
  return createStore(reducer, preloadedState, applyMiddleware());
}

export const initializeStore = (preloadedState) => {
  let _store = store ?? initStore(preloadedState);

  if (preloadedState && store) {
    _store = initStore({
      ...store.getState(),
      ...preloadedState,
    });
    store = undefined;
  }

  // Return _store explicitly when on the server-side to prevent state leaking across requests
  if (typeof window === 'undefined') return _store;
  
  if (!store) store = _store;
  return _store;
};

export function useStore(initialState) {
  return useMemo(() => initializeStore(initialState), [initialState]);
}
```

**[DON'T]** Initialize Redux unconditionally outside the component tree or omit memoization, which causes hydration mismatches or memory leaks on the server:
```javascript
import { createStore } from 'redux';

// INCORRECT: This will be shared across all users on the server, causing a massive security/data leak!
const store = createStore(reducer, {}); 

export default function MyApp({ Component, pageProps }) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
```

## Abstracting Redux Selectors

**[DO]** Create custom hooks with `shallowEqual` to cleanly consume Redux state inside components:
```javascript
import { useDispatch, useSelector, shallowEqual } from 'react-redux';

function useGlobalItems() {
  return useSelector((state) => state, shallowEqual);
}

function ProductCard({ id }) {
  const dispatch = useDispatch();
  const items = useGlobalItems();
  const productAmount = items?.[id] ?? 0;

  return (
    <button onClick={() => dispatch({ type: 'INCREMENT', id })}>
      +
    </button>
  );
}
```