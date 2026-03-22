# @Domain
- React performance optimization and debugging.
- Component architecture refactoring.
- Resolving UI lag caused by frequent state updates (e.g., scroll events, mouse movements, animations).
- Code reviews or implementation tasks involving nested components, state lifting, and component composition.
- React element tree construction and reconciliation analysis tasks.

# @Vocabulary
- **Component**: A function that accepts an argument (`props`) and returns React Elements. Example: `const A = () => <B />`.
- **Element**: A plain JavaScript object that describes what needs to be rendered on the screen. It is created using JSX (which transpiles to `React.createElement`). It contains a `type` (a string for DOM nodes or a reference to a Component function) and `props`. Example: `const b = <B />` evaluates to `{ type: B, props: {} }`.
- **Re-render**: The process where React calls the Component's function, executes its internal logic (including hooks), and returns a new set of Elements to build a new Virtual DOM tree.
- **Reconciliation (Diffing)**: The process React uses to compare the Element object before a re-render with the Element object after a re-render.
- **Element Reference Stability (`Object.is`)**: React evaluates whether an Element requires re-rendering by performing a strict equality check (`Object.is(ElementBefore, ElementAfter)`). If true, React skips re-rendering that component and its children. If false, React proceeds with the re-render.
- **Elements as Props**: A composition pattern where a parent component instantiates a React Element and passes it as a prop to a child component. This preserves the Element's object reference when the child's internal state changes.
- **Children as Props**: A specific application of the "Elements as Props" pattern utilizing JSX nesting syntax (`<Parent><Child /></Parent>`). It is functionally identical to passing a prop named `children` (`<Parent children={<Child />} />`).

# @Objectives
- Improve application performance by isolating state updates and preventing the propagation of unnecessary re-renders.
- Prioritize component composition techniques over caching/memoization (`React.memo`, `useMemo`) to solve re-render bottlenecks.
- Maintain stable object references for expensive or complex components by passing them as props from a higher level in the component tree.
- Leverage the exact mechanics of React's reconciliation algorithm (`Object.is` comparison) to seamlessly bypass rendering phases for static or independent child trees.

# @Guidelines
- **Component vs. Element Distinction**: The AI MUST strictly differentiate between a Component (the function) and an Element (the object returned by the function or JSX).
- **Avoid Premature Memoization**: When facing a performance issue caused by state changes re-rendering slow nested components, the AI MUST NOT immediately suggest `React.memo`. Composition MUST be the primary architectural solution.
- **Isolate Volatile State**: State that updates frequently (e.g., scroll positions, mouse coordinates) MUST be extracted into the smallest possible dedicated wrapper component.
- **Utilize Object Reference Mechanics**: The AI MUST recognize that any JSX declared inside a component creates a *new* Element object on every render. To prevent a component from re-rendering, its Element object MUST be created *outside* the re-rendering component and passed in.
- **Treat `children` as a Prop**: The AI MUST process `children` exactly like any other prop. Nesting JSX inside a component tag creates an Element object that is passed to the `children` prop.
- **Protect Slow Components**: Any slow, heavy, or complicated component that does not directly depend on a volatile state variable MUST be lifted out of the stateful component and passed back down via the `children` prop.
- **Observe the One-Way Render Flow**: The AI MUST remember that React never traverses "up" the render tree. A state update in a child component will never trigger a re-render in its parent, which protects any Elements passed from the parent as props.

# @Workflow
1. **Identify the Bottleneck**: Locate the component containing the volatile state (e.g., `position` tracked via `onScroll`) and the heavy nested components (`<VerySlowComponent />`) being unintentionally re-rendered.
2. **Extract State**: Create a new wrapper component (e.g., `ScrollableWithMovingBlock`).
3. **Migrate Logic**: Move the volatile state (`useState`), the event handlers (`onScroll`), and the specific UI elements that depend strictly on this state (`<MovingBlock position={position} />`) into the new wrapper component.
4. **Define the Injection Point**: Add a `children` prop to the new wrapper component's signature. Place `{children}` in the JSX where the heavy components originally resided.
5. **Implement Composition**: In the original parent component, instantiate the newly created wrapper component.
6. **Pass Elements as Props**: Place the heavy/slow components inside the wrapper component's JSX tags (passing them as `children`).
7. **Verify Reference Stability**: Ensure that the heavy components are instantiated in the parent (which does not re-render) so that when the wrapper updates its state, the `children` prop maintains its strict equality (`Object.is`), successfully bypassing the reconciliation algorithm.

# @Examples (Do's and Don'ts)

**[DON'T]**
Do not place volatile state in a parent component that also directly renders heavy, independent child components. This creates new Element objects for the heavy components on every state update, forcing them to re-render.

```jsx
const MainScrollableArea = () => {
  // Volatile state
  const [position, setPosition] = useState(300);

  const onScroll = (e) => {
    const calculated = getPosition(e.target.scrollTop);
    setPosition(calculated);
  };

  return (
    <div className="scrollable-block" onScroll={onScroll}>
      <MovingBlock position={position} />
      {/* ANTI-PATTERN: These slow components will re-render on every scroll event */}
      <VerySlowComponent />
      <BunchOfStuff />
      <OtherStuffAlsoComplicated />
    </div>
  );
};
```

**[DO]**
Extract the volatile state into a wrapper component and pass the heavy components as `children`. The parent creates the Elements once, and the stateful wrapper receives them as stable object references.

```jsx
// 1. Create a wrapper component for the volatile state
const ScrollableWithMovingBlock = ({ children }) => {
  const [position, setPosition] = useState(300);

  const onScroll = (e) => {
    const calculated = getPosition(e.target.scrollTop);
    setPosition(calculated);
  };

  return (
    <div className="scrollable-block" onScroll={onScroll}>
      <MovingBlock position={position} />
      {/* The reference to 'children' remains identical before and after the state update */}
      {children}
    </div>
  );
};

// 2. Consume the wrapper and pass the slow components as children
const App = () => {
  return (
    <ScrollableWithMovingBlock>
      {/* PERFORMANCE OPTIMIZED: These elements are created in App. 
          When ScrollableWithMovingBlock updates its state, React skips re-rendering these. */}
      <VerySlowComponent />
      <BunchOfStuff />
      <OtherStuffAlsoComplicated />
    </ScrollableWithMovingBlock>
  );
};
```

**[DON'T]**
Do not assume that passing elements via a named prop behaves differently than `children`. Avoid convoluted prop names when the standard JSX nesting is cleaner.

```jsx
// ANTI-PATTERN: While technically functional, this is hard to read and unconventional.
<ScrollableWithMovingBlock 
  content={
    <>
      <VerySlowComponent />
      <BunchOfStuff />
    </>
  } 
/>
```

**[DO]**
Recognize that `children` is just a prop and use JSX nesting to achieve the "elements as props" pattern cleanly.

```jsx
// DO: Use JSX nesting to pass the elements to the 'children' prop.
<ScrollableWithMovingBlock>
  <VerySlowComponent />
  <BunchOfStuff />
</ScrollableWithMovingBlock>
```