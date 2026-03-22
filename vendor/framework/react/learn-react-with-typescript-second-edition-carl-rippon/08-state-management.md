@Domain
These rules apply when the AI is tasked with implementing, refactoring, or managing shared state across multiple React components in a TypeScript application. This includes user requests involving prop drilling, React Context API, or Redux (specifically Redux Toolkit).

@Vocabulary
- **Shared State**: State that is used and accessed by several different components within an application.
- **Prop Drilling**: The simplest state solution where state is defined in a parent component and passed down the component tree to child components using props.
- **React Context**: An object created via `createContext` that can be accessed by components to share state, eliminating the need for prop drilling.
- **Provider Wrapper**: A custom component that stores the shared state (typically using `useState` or `useReducer`) and passes it to the React Context's `<Provider>` component.
- **Redux**: A mature state management library where state lives in a centralized, immutable object.
- **Store**: The centralized object in Redux containing the state for the whole app. Created using Redux Toolkit's `configureStore` function.
- **Slices**: Different, feature-specific areas of state within a Redux store. Created using Redux Toolkit's `createSlice` function.
- **Action**: An object containing the type of change and any data required to make the change. Handled by reducer functions.
- **Reducer**: A function that takes the current state and an action, and updates the state accordingly.
- **Immer**: A library utilized under the hood by Redux Toolkit that allows developers to write code that appears to directly mutate state, while actually keeping it immutable.

@Objectives
- Choose the most appropriate state management approach (Prop Drilling, React Context, or Redux) based on the specific needs, scale, and complexity of the application.
- Eliminate unnecessary prop drilling by implementing Context or Redux when deeply nested components or many disparate components require access to the same state.
- Ensure all state management implementations are strictly typed using TypeScript, leveraging generic types, utility types, and type assertions where required.
- Structure state management code cleanly, isolating contexts, slices, and stores into dedicated files and exporting easy-to-use custom hooks for consumption.

@Guidelines
- **Evaluating State Approaches**: 
  - The AI MUST use Prop Drilling for simple state shared only across a few adjacent components.
  - The AI MUST NOT use Prop Drilling if it forces components that do not need the state to declare it in their props just to pass it down to their children.
  - The AI MUST use React Context when state needs to be shared across many components, but the scale does not justify a full third-party library.
  - The AI MUST use Redux (via Redux Toolkit) when there is a large amount of shared application-level state.
- **Implementing React Context**:
  - The AI MUST use `createContext<ContextType>(defaultValue)` and ALWAYS pass a default value to satisfy TypeScript constraints.
  - The AI MUST create a dedicated Provider Wrapper component that utilizes `useReducer` or `useState` to manage the actual state values, and pass those values to the `Context.Provider` via the `value` prop.
  - The AI MUST export a custom hook (e.g., `export const useAppContext = () => useContext(AppContext);`) to streamline context consumption in child components.
  - The AI MUST place the Provider component appropriately in the component tree, high enough to wrap all components requiring the state, but no higher than necessary.
- **Implementing Redux Toolkit**:
  - The AI MUST define the slice state type and an `initialState` variable explicitly.
  - The AI MUST use `createSlice` from `@reduxjs/toolkit` to define the slice name, initial state, and reducer action handlers.
  - The AI MUST use the `PayloadAction<T>` generic type from `@reduxjs/toolkit` to strongly type the `action` parameter within slice reducers.
  - The AI MUST directly mutate state properties within `createSlice` reducers, relying on the underlying `immer` library to handle immutability.
  - The AI MUST export the slice's action creators (e.g., `export const { myAction } = mySlice.actions;`) and use a default export for the slice reducer.
  - The AI MUST create the store using `configureStore` and combine the slice reducers into the `reducer` object property.
  - The AI MUST infer and export the `RootState` type using TypeScript's `ReturnType` utility: `export type RootState = ReturnType<typeof store.getState>;`.
  - The AI MUST wrap the application or necessary component tree with the `<Provider store={store}>` component imported from `react-redux`.
  - The AI MUST use the `useSelector` hook from `react-redux` combined with the `RootState` type to access specific state values in components.
  - The AI MUST use the `useDispatch` hook to obtain the dispatch function, and NEVER call `useDispatch` directly inside an event handler inline.

@Workflow
1. **Analyze State Sharing Requirements**: Identify which components need access to the state and determine their positions in the React component tree.
2. **Select the Strategy**: 
   - Choose Prop Drilling if the state is localized.
   - Choose React Context if the state is shared across multiple, nested components.
   - Choose Redux if managing complex, app-wide state.
3. **If Executing React Context Strategy**:
   - Define the `State` type, `Action` type, and `initialState` object.
   - Define a `reducer` function handling state transitions.
   - Define a `ContextType` combining the `State` and `dispatch` signature.
   - Initialize the context using `createContext<ContextType>` with a complete default value.
   - Implement an `<AppProvider>` component using `useReducer(reducer, initialState)` and return `<AppContext.Provider value={{...state, dispatch}}>`.
   - Export a `useAppContext` custom hook.
   - Wrap the required component tree in `<AppProvider>` and use `useAppContext` in child components.
4. **If Executing Redux Toolkit Strategy**:
   - Define the `State` type and `initialState` object.
   - Create a slice using `createSlice`, defining `name`, `initialState`, and `reducers`.
   - Use `PayloadAction<Type>` for typing action payloads within the reducers.
   - Export destructured actions and the default reducer from the slice.
   - Create a `store.ts` file, use `configureStore`, and assign the slice reducer.
   - Export `RootState` using `ReturnType<typeof store.getState>`.
   - Wrap the React tree in `<Provider store={store}>`.
   - In consuming components, import `useSelector`, `useDispatch`, and `RootState`.
   - Instantiate `const dispatch = useDispatch()` and extract state via `const value = useSelector((state: RootState) => state.feature.value)`.

@Examples (Do's and Don'ts)

- **Context Creation**
  - [DO]: Provide a complete default value matching the generic type when creating a context in TypeScript.
    ```typescript
    type ThemeContextType = Theme & {
      changeTheme: (name: string, color: 'dark' | 'light') => void;
    };
    const ThemeContext = createContext<ThemeContextType>({
      name: 'standard',
      color: 'light',
      changeTheme: () => {},
    });
    ```
  - [DON'T]: Leave the default value empty or undefined, which will cause a TypeScript compiler error.
    ```typescript
    // TypeScript Error: Expected 1 arguments, but got 0.
    const ThemeContext = createContext<ThemeContextType>();
    ```

- **Redux Dispatching**
  - [DO]: Assign the `useDispatch` hook to a variable and use that variable to dispatch actions.
    ```typescript
    import { useDispatch } from 'react-redux';
    
    export function ThemeChanger() {
      const dispatch = useDispatch();
      
      function handleChangeTheme({ name, color }: Theme) {
        dispatch(changeThemeAction(name, color));
      }
      return <button onClick={handleChangeTheme}>Change Theme</button>;
    }
    ```
  - [DON'T]: Call `useDispatch` directly inside an event handler or nested function. (Violates the Rules of Hooks).
    ```typescript
    function handleChangeTheme({ name, color }: Theme) {
      useDispatch(changeThemeAction(name, color)); // Error!
    }
    ```

- **Redux Slice State Updates**
  - [DO]: Mutate the state directly inside Redux Toolkit `createSlice` reducers (thanks to the underlying Immer library).
    ```typescript
    import { createSlice, PayloadAction } from '@reduxjs/toolkit';

    export const userSlice = createSlice({
      name: 'user',
      initialState,
      reducers: {
        authorizedAction: (state, action: PayloadAction<string[]>) => {
          state.permissions = action.payload;
          state.loading = false;
        }
      }
    });
    ```
  - [DON'T]: Attempt to manually spread and return state inside `createSlice` unnecessarily, confusing standard `useReducer` patterns with Redux Toolkit patterns.

- **Redux Selectors**
  - [DO]: Explicitly type the state parameter in `useSelector` with the exported `RootState` type.
    ```typescript
    const permissions = useSelector((state: RootState) => state.user.permissions);
    ```
  - [DON'T]: Leave the state parameter implicitly typed as `any`.
    ```typescript
    const permissions = useSelector((state) => state.user.permissions);
    ```