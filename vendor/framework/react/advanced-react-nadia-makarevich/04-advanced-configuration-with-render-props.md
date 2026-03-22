@Domain
React component architecture and stateful logic sharing. Triggered when configuring highly flexible components, injecting state or dynamic props into child components passed from the outside, abstracting stateful logic, or refactoring legacy component APIs.

@Vocabulary
- **Element as Prop**: Passing a pre-instantiated React Element to a component (e.g., `icon={<Icon />}`).
- **Render Prop**: A function passed as a prop to a React component that returns a React Element, enabling the component to explicitly pass state or props back up to the consumer.
- **Children as Render Prop**: Using the standard React `children` prop as a function that returns an Element, commonly used for sharing stateful logic.
- **Stateful Logic**: Logic involving React state and side effects that needs to be abstracted and reused across multiple components.

@Objectives
- Replace fragile magic (like `React.cloneElement`) with explicit, traceable data flows when parents need to influence injected child components.
- Expose a component's internal state to its consumers for advanced UI configurations without lifting state up.
- Correctly identify when to use Custom Hooks versus Render Props for sharing stateful logic.

@Guidelines
- The AI MUST NOT use `React.cloneElement` to inject state, dynamic values, or override props on Elements passed as props. 
- When a parent component needs to pass its own state to an injected child component, the AI MUST use the Render Prop pattern.
- When invoking a Render Prop, the AI MUST pass data via standard function arguments. The AI SHOULD separate configuration props and state into distinct arguments (e.g., `renderIcon(defaultProps, { isHovered })`) to maintain a clean API.
- The AI MUST use Custom Hooks to abstract and share stateful logic that does NOT depend on a specific DOM wrapper (e.g., tracking window dimensions, geolocation, global event listeners).
- The AI MUST NOT use Render Props to share DOM-independent stateful logic in modern React codebases.
- The AI MUST use Render Props (often via the `children` prop) when abstracting stateful logic that intrinsically depends on attaching events to a specific DOM element (e.g., an `onScroll` listener attached to a wrapping `div`).
- When implementing a Render Prop as `children`, the AI MUST support JSX nesting syntax on the consumer side (e.g., `<Parent>{(data) => <Child data={data} />}</Parent>`).

@Workflow
1. Analyze the component API requirements: Does the component accept a UI element from the outside?
2. Determine State/Prop injection needs: Does the component need to provide its own state (like `isHovered`) or computed default props to this external UI element?
3. If no state/prop injection is needed, use standard Elements as Props. 
4. If state/prop injection is needed, implement a Render Prop:
   - Define the prop as a function (e.g., `renderIcon`).
   - Inside the component, invoke the function where the element should render, passing the required state/props as arguments: `{renderIcon(defaultProps, state)}`.
5. For stateful logic abstraction, analyze DOM dependence:
   - If the logic requires attaching listeners to a window/document, create a Custom Hook.
   - If the logic requires attaching listeners to a generated DOM node (like a `div`), create a component that renders the DOM node and uses the `children` Render Prop to pass the state down to consumers.

@Examples

**Example 1: Passing State and Props to an Injected Component**

[DO]
```javascript
// Component Definition
const Button = ({ appearance, size, renderIcon }) => {
  const [isHovered, setIsHovered] = useState(false);

  const iconParams = {
    size: size === 'large' ? 'large' : 'medium',
    color: appearance === 'primary' ? 'white' : 'black',
  };

  return (
    <button 
      onMouseOver={() => setIsHovered(true)} 
      onMouseOut={() => setIsHovered(false)}
    >
      Submit {renderIcon(iconParams, { isHovered })}
    </button>
  );
};

// Consumer Side
<Button 
  appearance="primary" 
  renderIcon={(props, state) => (
    <HomeIcon {...props} className={state.isHovered ? 'icon-hovered' : ''} />
  )} 
/>
```

[DON'T]
```javascript
// Anti-pattern: Using cloneElement to magically inject state
const Button = ({ appearance, size, icon }) => {
  const [isHovered, setIsHovered] = useState(false);

  const newProps = {
    size: size === 'large' ? 'large' : 'medium',
    color: appearance === 'primary' ? 'white' : 'black',
    isHovered, // Magically injected, overrides explicit consumer props
    ...icon.props,
  };

  const clonedIcon = React.cloneElement(icon, newProps);

  return (
    <button 
      onMouseOver={() => setIsHovered(true)} 
      onMouseOut={() => setIsHovered(false)}
    >
      Submit {clonedIcon}
    </button>
  );
};
```

**Example 2: Abstracting DOM-Independent Stateful Logic**

[DO]
```javascript
// Extracting DOM-independent logic into a custom hook
const useResizeDetector = () => {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const listener = () => setWidth(window.innerWidth);
    window.addEventListener("resize", listener);
    return () => window.removeEventListener("resize", listener);
  }, []);

  return width;
};

const Layout = () => {
  const windowWidth = useResizeDetector();
  return windowWidth > 600 ? <WideLayout /> : <NarrowLayout />;
};
```

[DON'T]
```javascript
// Anti-pattern: Using Render Props for DOM-independent logic in the Hooks era
const ResizeDetector = ({ children }) => {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const listener = () => setWidth(window.innerWidth);
    window.addEventListener("resize", listener);
    return () => window.removeEventListener("resize", listener);
  }, []);

  return children(width);
};

const Layout = () => {
  return (
    <ResizeDetector>
      {(windowWidth) => (windowWidth > 600 ? <WideLayout /> : <NarrowLayout />)}
    </ResizeDetector>
  );
};
```

**Example 3: Abstracting DOM-Dependent Stateful Logic**

[DO]
```javascript
// Using children as a Render Prop because the logic requires attaching to a specific DOM node
const ScrollDetector = ({ children }) => {
  const [scroll, setScroll] = useState(0);

  return (
    <div onScroll={(e) => setScroll(e.currentTarget.scrollTop)}>
      {children(scroll)}
    </div>
  );
};

const Layout = () => {
  return (
    <ScrollDetector>
      {(scroll) => (
        <>{scroll > 30 ? <SomeBlock /> : null}</>
      )}
    </ScrollDetector>
  );
};
```

[DON'T]
```javascript
// Anti-pattern: Trying to use a hook for DOM-dependent logic without managing Refs properly
// (While possible with Refs, the Render Prop is much cleaner for encapsulating the DOM wrapper).
const Layout = () => {
  const [scroll, setScroll] = useState(0);
  
  // Consumer has to manually wire up the onScroll event to their own div
  // breaking the encapsulation of the scroll detection logic.
  return (
    <div onScroll={(e) => setScroll(e.currentTarget.scrollTop)}>
      {scroll > 30 ? <SomeBlock /> : null}
    </div>
  );
}
```