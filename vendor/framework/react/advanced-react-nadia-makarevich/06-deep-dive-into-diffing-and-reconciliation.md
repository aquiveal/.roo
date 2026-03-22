# @Domain
React component architecture, debugging UI state loss, fixing component flickering (unintended re-mounting), optimizing list rendering, managing conditional rendering, and implementing state reset patterns. Activation conditions: User requests involving `.jsx` or `.tsx` files where React components are dynamically rendered, lists are mapped, state unexpectedly persists or disappears between renders, or performance issues related to rendering exist.

# @Vocabulary
- **Element (Virtual DOM Object)**: A plain JavaScript object returned by React components (via JSX) describing the desired UI. Contains properties like `type` (string for HTML, function reference for React components) and `props`.
- **Reconciliation**: React's algorithmic process of comparing the "before" and "after" Element trees to determine which DOM nodes need updating, adding, or removing.
- **Diffing**: The specific comparison step in Reconciliation where React evaluates the `type` and `key` of Elements in the exact same structural position.
- **Re-rendering**: Updating an existing component instance. Occurs when the `type` and `key` of an Element remain identical between renders. Preserves internal state and DOM nodes.
- **Re-mounting (Unmount & Mount)**: Destroying an existing component instance and creating a new one from scratch. Occurs when the `type` or `key` of an Element changes at a specific position. Destroys internal state and DOM nodes.
- **Key Attribute**: React's mechanism for uniquely identifying Elements between renders. Used to track identity across dynamic arrays or to force identity differentiation for static elements.
- **State Reset Technique**: The deliberate application of a dynamic `key` attribute to a static element to force React to unmount and re-mount the component, clearing its internal state.

# @Objectives
- The AI MUST strictly preserve component state when desired by maintaining stable `type` references and structural positions.
- The AI MUST deliberately destroy component state when necessary by explicitly manipulating the `key` attribute or `type` reference.
- The AI MUST permanently eliminate performance-killing anti-patterns, specifically the nested declaration of component functions.
- The AI MUST ensure robust dynamic list rendering by applying stable, unique identifiers to `key` attributes to prevent data mismatch and memoization failure.

# @Guidelines

## Diffing and Component Identity
- When evaluating conditional rendering of the exact same component `type` (e.g., `<Input />` vs `<Input />`), the AI MUST recognize that React will re-use the component instance and preserve its state.
- If the user expects the state to clear when toggling between identical component types, the AI MUST apply a unique `key` attribute to each instance to explicitly break the identity match.

## Nested Component Declarations
- The AI MUST NEVER define a React component function inside another React component function.
- When encountering nested components, the AI MUST immediately refactor them by extracting the inner component to the module scope and passing necessary data via props. 
- *Reasoning*: A locally declared function creates a new memory reference on every parent re-render. React compares `type` by reference. Changing references forces a complete unmount and re-mount, destroying state, losing input focus, and halving performance.

## Arrays and Key Attributes
- When rendering dynamic arrays (lists that can be re-ordered, added to, or removed from), the AI MUST use a unique, stable identifier from the data (e.g., `item.id`) as the `key`.
- The AI MUST NOT use the array `index` as a `key` for dynamic arrays. 
- *Reasoning*: If an array re-orders, elements retain their index-based keys but receive new data props. This causes React to re-use the wrong component instances, breaking internal state mapping and entirely nullifying `React.memo` optimizations.
- When rendering strictly static arrays (lists that never change length or order), the AI MAY use the array `index` as a `key`.

## Structural Positioning
- The AI MUST recognize that React diffs child arrays positionally (index by index).
- If conditionally rendering elements using inline logical operators (e.g., `isTrue && <Component />`), the AI MUST evaluate if shifting positions will cause unintended unmounting of sibling elements. 
- *Note*: React mitigates this by keeping `null` in the structural array (e.g., `[{type: Checkbox}, null, {type: Input}]`).

## State Reset Pattern
- When a requirement demands resetting the internal state of an uncontrolled component (e.g., clearing a form field when the URL changes), the AI MUST use the State Reset Technique by applying a reactive variable to the `key` attribute (e.g., `key={url}`).

# @Workflow
When authoring or refactoring React render functions, the AI MUST follow this algorithmic process:

1. **Scan for Nested Components**: Check if any function returning JSX is declared inside another component. If found, hoist it to the module scope and convert closures to props.
2. **Analyze Conditional Rendering**: Locate ternary operators or logical ANDs swapping components. 
    - If the swapping components share the identical `type` (e.g., `<Input />`), ask: "Should the state be preserved across this swap?"
    - If NO (state must clear): Assign distinct `key` attributes to both elements.
    - If YES (state must persist): Leave them without keys, or give them identical `key` attributes if they sit at different structural depths.
3. **Analyze Iterations (Maps)**: Locate all `.map()` calls returning JSX.
    - Ask: "Can this list be re-ordered, filtered, or appended to?"
    - If YES: Map the `key` attribute strictly to a unique data property (`item.id`).
    - Verify if the mapped child is wrapped in `React.memo`. If it is, rigorously enforce the unique ID rule, as an index key will silently break memoization.
4. **Enforce Intentional Unmounting**: If the user specifically complains about stale UI state on navigation or entity switching, apply the State Reset Technique by binding the entity ID to the `key` of the wrapper component.

# @Examples (Do's and Don'ts)

## Nested Components
- [DON'T]: Define a component inside a component.
```jsx
const Form = () => {
  const [value, setValue] = useState("");

  // CRITICAL ANTI-PATTERN: Re-created on every keystroke
  const Input = () => <input value={value} onChange={e => setValue(e.target.value)} />;

  return <Input />;
};
```
- [DO]: Hoist to module scope and pass props.
```jsx
const Input = ({ value, onChange }) => (
  <input value={value} onChange={onChange} />
);

const Form = () => {
  const [value, setValue] = useState("");
  return <Input value={value} onChange={e => setValue(e.target.value)} />;
};
```

## Conditional State Preservation (The Mysterious Bug)
- [DON'T]: Assume swapping identical component types will clear their state.
```jsx
const Form = () => {
  const [isCompany, setIsCompany] = useState(false);

  return (
    <>
      <Checkbox onChange={() => setIsCompany(!isCompany)} />
      {/* Typing in the first input, then toggling, will keep the typed text in the second input */}
      {isCompany ? (
        <Input id="company-tax" placeholder="Company Tax ID" />
      ) : (
        <Input id="person-tax" placeholder="Personal Tax ID" />
      )}
    </>
  );
};
```
- [DO]: Use the `key` attribute to force React to differentiate the instances and reset state.
```jsx
const Form = () => {
  const [isCompany, setIsCompany] = useState(false);

  return (
    <>
      <Checkbox onChange={() => setIsCompany(!isCompany)} />
      {isCompany ? (
        <Input key="company" id="company-tax" placeholder="Company Tax ID" />
      ) : (
        <Input key="person" id="person-tax" placeholder="Personal Tax ID" />
      )}
    </>
  );
};
```

## Dynamic Arrays and Keys
- [DON'T]: Use the array index as a key for dynamic lists, especially memoized ones.
```jsx
const Parent = ({ sortedData }) => {
  // ANTI-PATTERN: If sortedData order changes, the key stays the same for the index.
  // React updates the props but thinks it's the same item, breaking React.memo.
  return sortedData.map((item, index) => (
    <InputMemo key={index} placeholder={item.placeholder} />
  ));
};
```
- [DO]: Use a stable, unique entity ID.
```jsx
const Parent = ({ sortedData }) => {
  // CORRECT: Identity is tied to the data. Re-ordering shifts the DOM node safely.
  return sortedData.map((item) => (
    <InputMemo key={item.id} placeholder={item.placeholder} />
  ));
};
```

## The State Reset Technique
- [DON'T]: Use `useEffect` to manually clear out state when an entity changes.
```jsx
const Profile = ({ userId }) => {
  const [name, setName] = useState("");
  
  // ANTI-PATTERN: Cumbersome and causes double-rendering
  useEffect(() => {
    setName("");
  }, [userId]);

  return <input value={name} onChange={e => setName(e.target.value)} />;
};
```
- [DO]: Use the `key` attribute on the component instance from the parent to force a complete unmount/remount.
```jsx
const App = ({ currentUserId }) => {
  // CORRECT: When currentUserId changes, the old Profile is destroyed and a fresh one is mounted.
  return <Profile key={currentUserId} userId={currentUserId} />;
};
```