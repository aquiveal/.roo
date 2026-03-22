# @Domain
React and TypeScript component development, specifically triggered when creating, refactoring, or optimizing reusable UI components, lists, or custom hooks. These rules apply when tasks involve making components API-flexible, strongly typed with varying data, customizable in rendering, or capable of having their internal state controlled by a consumer.

# @Vocabulary
- **Generics**: Type parameters defined in angled brackets (`<T>`) that allow functions, types, and React components to be reusable with different data types while remaining strongly typed.
- **keyof Operator**: A TypeScript operator used to query a type for its property names and construct a union type from them.
- **Props Spreading**: A pattern utilizing rest parameters to collect standard HTML element props and spreading them (`{...props}`) onto an internal JSX element.
- **ComponentPropsWithoutRef**: A generic React type (e.g., `ComponentPropsWithoutRef<'ul'>`) that allows a custom component's prop type to inherit all standard props of a specific HTML element.
- **Rest Parameters**: JavaScript syntax (`...props`) used in function parameters to collect multiple remaining arguments/props into a single object or array.
- **Render Props**: A pattern where a component takes a function as a prop (often returning a `ReactNode`) allowing the consumer to override and control the internal rendering of specific elements (e.g., list items).
- **Currying**: A pattern where a function returns another handler function, used to pass specific arguments (like an item ID) into an event handler that doesn't natively provide them.
- **Custom Hooks**: Reusable logic extracted into a function whose name starts with `use` and which calls at least one standard React hook.
- **Controllable Internal State**: A pattern allowing a component to manage its own state internally while also providing optional props (`value` and `onChange`) that allow a parent component to override and control that state.

# @Objectives
- Make components highly reusable without sacrificing TypeScript type safety by leveraging generic types.
- Provide maximum flexibility to component consumers by allowing them to spread standard HTML props onto underlying elements.
- Enable consumers to override internal component rendering using the render props pattern.
- Isolate complex component logic into custom hooks to keep component code clean and promote logic reuse.
- Build flexible components that can operate completely autonomously or have their internal state strictly controlled by parent components.

# @Guidelines
- **Generic Components**: You MUST use generic parameters (e.g., `export function Checklist<Data>({...}: Props<Data>)`) when building components that handle arrays of varying or unknown data types.
- **Strongly Typed Property Selectors**: When a component needs to reference a specific property of a generic data object, you MUST type that prop using the `keyof` operator (e.g., `id: keyof Data`) to ensure the consumer provides a valid property name.
- **HTML Prop Inheritance**: To allow consumers to style or modify underlying HTML wrappers, you MUST intersect the component's `Props` type with `ComponentPropsWithoutRef<'element'>`.
- **Prop Extraction**: You MUST use rest parameters (e.g., `...ulProps`) at the end of the component's destructuring signature to collect inherited HTML props, and then spread them onto the target JSX element.
- **Render Props Pattern**: If a component renders a list or complex internal structure, you MUST provide an optional render prop (e.g., `renderItem?: (item: Data) => ReactNode`) that allows the consumer to completely override the default rendering.
- **Currying for Handlers**: If an event handler requires specific data (like an ID) but the React event does not natively supply it, you MUST use currying to generate the handler (e.g., `(id) => () => { ... }`).
- **Custom Hook Creation**: 
  - You MUST prefix custom hook names with `use`.
  - The custom hook MUST call at least one standard React hook (e.g., `useState`, `useEffect`).
  - You MUST return an object structure (not a tuple) from the hook when returning more than two items, utilizing object keys for clarity.
  - If the hook accepts multiple parameters, you MUST group them into an object parameter.
- **Controllable State Implementation**:
  - To make an internal state controllable, you MUST expose two optional props: one for the state value itself, and one for the change handler function.
  - You MUST initialize the internal state to the controlled prop if it is provided (`useState(controlledProp || defaultValue)`).
  - You MUST synchronize the internal state with the external controlled prop using a `useEffect` hook that triggers when the controlled prop changes.
  - In your update handlers, you MUST check if the consumer provided a change handler. If they did, invoke the consumer's handler; otherwise, update the internal state.

# @Workflow
1. **Define the Generic API**: Define the generic `Props<T>` type. Add strictly typed property selector props using `keyof T`. 
2. **Implement HTML Spreading**: Add `& ComponentPropsWithoutRef<'htmlElement'>` to the `Props` type. Destructure the specific component props and use a rest parameter to gather the remaining HTML props. Spread these onto the primary container element in the JSX.
3. **Add Render Props**: Define an optional `renderItem` prop returning a `ReactNode`. Inside your map or render logic, add a conditional check: if `renderItem` is defined, return its result; otherwise, fall back to the default JSX.
4. **Isolate State Logic**: If the component handles complex state (e.g., keeping track of checked items), extract this into a custom hook. Move `useState` and handler logic into the hook, and return an object with the state and handlers.
5. **Add Controllable State Capabilities**: Inside the custom hook (or component), add optional parameters for the state value and the `onChange` event. Implement a `useEffect` to sync the internal state with the external prop. Update the internal update handler to conditionally fire the consumer's `onChange` event if provided.

# @Examples (Do's and Don'ts)

## Generics & Property Selectors
- **[DO]** Use generic parameters and `keyof` to enforce strict typing on data structures.
  ```typescript
  type Props<Data> = {
    data: Data[];
    id: keyof Data;
    primary: keyof Data;
  };
  export function Checklist<Data>({ data, id, primary }: Props<Data>) { ... }
  ```
- **[DON'T]** Use `any` or standard `string` types for property selectors, which defeats type safety.
  ```typescript
  type Props = {
    data: any[];
    id: string; // Anti-pattern: No type safety ensuring 'id' exists on data
  };
  ```

## Props Spreading
- **[DO]** Intersect with `ComponentPropsWithoutRef`, use rest parameters, and spread onto the HTML element.
  ```typescript
  import { ComponentPropsWithoutRef } from 'react';
  
  type Props<Data> = {
    data: Data[];
  } & ComponentPropsWithoutRef<'ul'>;
  
  export function Checklist<Data>({ data, ...ulProps }: Props<Data>) {
    return <ul className="bg-gray-300" {...ulProps}>{/* ... */}</ul>;
  }
  ```
- **[DON'T]** Put rest parameters anywhere but the end of the destructuring signature, or manually redefine standard HTML props.
  ```typescript
  // Anti-pattern: Rest parameter must be the last one
  export function Checklist<Data>({ ...ulProps, data }: Props<Data>) { ... }
  ```

## Render Props
- **[DO]** Accept an optional function returning a `ReactNode` and conditionally render it.
  ```typescript
  type Props<Data> = {
    data: Data[];
    renderItem?: (item: Data) => ReactNode;
  };
  
  // Usage inside map:
  {data.map((item) => {
    if (renderItem) {
      return renderItem(item);
    }
    return <li key={item.id}>{/* Default rendering */}</li>;
  })}
  ```
- **[DON'T]** Force consumers to use strict internal elements without override capabilities when building highly reusable lists.

## Custom Hooks
- **[DO]** Start with `use`, call React hooks, and return an object structure for clarity.
  ```typescript
  export function useChecked() {
    const [checkedIds, setCheckedIds] = useState<IdValue[]>([]);
    const handleCheckChange = (checkedId: IdValue) => () => { ... };
    
    return { checkedIds, handleCheckChange };
  }
  ```
- **[DON'T]** Return tuples (arrays) when your custom hook returns more than two items, or omit internal React hooks.

## Controllable Internal State
- **[DO]** Accept optional external state props, synchronize via `useEffect`, and branch the update handler.
  ```typescript
  type Params = {
    checkedIds?: IdValue[];
    onCheckedIdsChange?: (checkedIds: IdValue[]) => void;
  };

  export function useChecked({ checkedIds, onCheckedIdsChange }: Params) {
    const [resolvedCheckedIds, setResolvedCheckedIds] = useState<IdValue[]>(checkedIds || []);

    useEffect(() => {
      const isControlled = checkedIds !== undefined;
      if (isControlled) {
        setResolvedCheckedIds(checkedIds);
      }
    }, [checkedIds]);

    const handleCheckChange = (checkedId: IdValue) => () => {
      // ... calculate newCheckedIds
      if (onCheckedIdsChange) {
        onCheckedIdsChange(newCheckedIds);
      } else {
        setResolvedCheckedIds(newCheckedIds);
      }
    };

    return { resolvedCheckedIds, handleCheckChange };
  }
  ```
- **[DON'T]** Ignore the external prop changes after the initial render. Failing to add the `useEffect` synchronization will cause the component to ignore updates sent from the parent.