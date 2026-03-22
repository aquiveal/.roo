@Domain
These rules MUST trigger when the AI is tasked with designing React component APIs, refactoring components that possess excessive configuration props (e.g., `iconColor`, `iconSize`, `headerStyle`), building UI primitive components (Buttons, ModalDialogs, Layouts), or implementing conditional rendering involving React elements.

@Vocabulary
- **Component**: A function that accepts an argument (props) and returns Elements.
- **Element**: A lightweight object description of what needs to be rendered (syntax sugar for `React.createElement`). It sits in memory cheaply and does not impact rendering performance until it is actually returned in a component's render output.
- **Elements as Props**: A composition pattern where an entire React Element is passed via a prop (e.g., `icon={<Loading />}`) to delegate configuration concerns to the consumer, rather than passing multiple primitive configuration props.
- **cloneElement**: A React API (`React.cloneElement`) used to copy an existing Element and inject new props into it. Used in this context to apply default values to Elements passed as props.

@Objectives
- Drastically reduce the number of configuration props on components by delegating sub-component configuration to the consumer.
- Maintain flexibility in UI components (like Dialogs and Layouts) while allowing the parent component to enforce safe default behaviors.
- Prevent the AI from performing unnecessary performance optimizations regarding Element creation prior to conditional rendering statements.
- Prevent API destruction when using `cloneElement` by rigidly enforcing prop merging order.

@Guidelines
- **Component API Design**: When a component renders a sub-component (like an icon in a button, or a footer in a dialog), the AI MUST NOT create multiple props to control the sub-component's attributes (e.g., avoid `iconLeftName`, `iconLeftColor`, `iconLeftSize`).
- **Delegation**: The AI MUST replace bloated configuration props with a single prop that accepts a React Element (e.g., `icon={<Icon />}`), forcing the consumer to handle the configuration.
- **Primary Content**: The AI MUST use the `children` prop (and JSX nested syntax) to pass the "main" part of a component (e.g., the content area of a ModalDialog or the middle column of a Layout).
- **Element Creation vs. Rendering**: The AI MUST NOT treat the creation of a React Element (e.g., `const footer = <Footer />;`) as a performance concern. Creating an Element is just creating an object; it is ONLY rendered when the component returning it actually renders.
- **Conditional Rendering**: It is perfectly safe and valid to declare React Elements in variables before conditional `if` or early `return` statements. The AI MUST NOT unnecessarily wrap element declarations in conditions or memoization purely to avoid element creation.
- **Default Values for Passed Elements**: If a parent component needs to control default attributes of an Element passed as a prop (e.g., a primary button forcing its icon to be white), the AI MUST use `React.cloneElement(element, newProps)`.
- **cloneElement Safety Constraint**: The `cloneElement` pattern is highly fragile. When using it, the AI MUST explicitly merge the element's original props into the `newProps` object using the spread operator (`...element.props`). The original props MUST spread LAST to ensure consumer overrides take precedence over the component's defaults.
- **Limitation**: The AI MUST restrict the use of `cloneElement` to very simple cases. If the configuration logic becomes overly complex or requires explicit state sharing, the AI must consider other patterns (like render props).

@Workflow
1. **Analyze Component API**: Review the target component for configuration bloat. Identify props that solely exist to pass data down to a sub-element (e.g., `isLoading`, `iconName`).
2. **Refactor to Elements as Props**: Remove the specific configuration props and replace them with a structural prop (e.g., `icon`, `footer`, `leftColumn`).
3. **Determine Default Requirements**: Assess if the parent component must enforce specific default values on the passed Element (e.g., sizes or colors matching the parent's theme).
4. **Clone and Merge (If Defaults Required)**:
    - Create a `defaultProps` object based on the parent's state/props.
    - Create a `newProps` object that spreads the `defaultProps`, followed immediately by spreading the passed element's existing props (`...passedElement.props`).
    - Pass the original element and `newProps` into `React.cloneElement`.
5. **Render**: Render the prop (or cloned Element) directly in the component's JSX payload.
6. **Consumer Implementation**: Update the consumer/parent component to pass fully configured Elements into the new props.

@Examples (Do's and Don'ts)

**Principle: Elements as Props vs. Configuration Bloat**
- [DON'T]: Add multiple props to control a child element's internal state/styles.
```jsx
const Button = ({ appearance, iconName, iconColor, iconSize }) => {
  return (
    <button className={appearance}>
      Submit <Icon name={iconName} color={iconColor} size={iconSize} />
    </button>
  );
};
```
- [DO]: Pass the pre-configured Element as a single prop.
```jsx
const Button = ({ appearance, icon }) => {
  return (
    <button className={appearance}>
      Submit {icon}
    </button>
  );
};
// Consumer handles configuration:
<Button appearance="primary" icon={<Icon name="alert" color="red" size="large" />} />
```

**Principle: Conditional Rendering and Element Creation**
- [DON'T]: Avoid creating element variables before conditions due to false performance concerns.
```jsx
const App = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  
  // Anti-pattern: Unnecessary inline ternary just to avoid creating the Footer element in memory
  return isDialogOpen ? (
    <ModalDialog footer={<Footer />} />
  ) : null;
};
```
- [DO]: Safely create Elements outside the condition; they are cheap objects and won't render until returned.
```jsx
const App = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  
  // Safe: This is just a lightweight object description. It does not render yet.
  const footer = <Footer />;
  
  return isDialogOpen ? (
    <ModalDialog footer={footer} />
  ) : null;
};
```

**Principle: Setting Default Props via cloneElement**
- [DON'T]: Overwrite the passed element's props by omitting the merge step. This destroys the consumer's ability to override the defaults.
```jsx
const Button = ({ appearance, size, icon }) => {
  const defaultIconProps = {
    size: size === 'large' ? 'large' : 'medium',
    color: appearance === 'primary' ? 'white' : 'black',
  };

  // Anti-pattern: Overwrites consumer's props completely!
  const clonedIcon = React.cloneElement(icon, defaultIconProps);

  return <button>Submit {clonedIcon}</button>;
};
```
- [DO]: Explicitly merge `icon.props` AFTER the default props so consumer overrides are preserved.
```jsx
const Button = ({ appearance, size, icon }) => {
  const defaultIconProps = {
    size: size === 'large' ? 'large' : 'medium',
    color: appearance === 'primary' ? 'white' : 'black',
  };

  const newProps = {
    ...defaultIconProps,
    ...icon.props, // Crucial: preserves consumer's custom props
  };

  const clonedIcon = React.cloneElement(icon, newProps);

  return <button>Submit {clonedIcon}</button>;
};
```