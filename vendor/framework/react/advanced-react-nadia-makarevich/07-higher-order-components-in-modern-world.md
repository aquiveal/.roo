@Domain
This rule file is activated when the AI is tasked with implementing cross-cutting concerns across multiple React components without modifying their internal code. Trigger these rules specifically when dealing with global callback enhancements (e.g., consistent logging on clicks), tracking React lifecycle events across varying components, intercepting/suppressing DOM/keyboard events (e.g., preventing global shortcuts inside modals), or refactoring legacy state-sharing Higher-Order Components (HOCs) into modern React hook patterns. 

@Vocabulary
*   **Higher-Order Component (HOC):** A function that accepts a React component as an argument, executes additional logic, and returns a new React component that renders the original component.
*   **Cross-Cutting Concerns:** Logic or functionality that must be consistently applied across multiple, otherwise unrelated components (e.g., logging, event suppression).
*   **Callback Interception:** The pattern of overriding a prop callback (like `onClick`) inside an HOC to execute side-effects before or after invoking the original callback passed via props.
*   **DOM Event Suppression:** Using an HOC to wrap a component in a DOM element (like a `div`) that calls `event.stopPropagation()` to prevent events from bubbling up to global listeners.
*   **Prop Injection:** The act of passing newly computed or extracted data into a component as props from within an HOC.

@Objectives
*   Restrict the usage of HOCs strictly to modern, valid use cases: enhancing callbacks, tracking lifecycle events, and intercepting DOM events.
*   Actively avoid and refactor the usage of HOCs for sharing stateful logic and Context data, replacing them completely with custom Hooks.
*   Ensure that all generated HOCs properly spread existing props down to the wrapped component to prevent breaking component APIs.
*   Preserve the original behavior of intercepted callbacks by guaranteeing the original prop functions are invoked alongside the injected side-effects.

@Guidelines
*   **Modern HOC Usage Constraints:** The AI MUST NOT generate HOCs to inject Context data or share stateful logic. The AI MUST use custom Hooks for state/Context.
*   **Permitted HOC Use Cases:** The AI MUST ONLY use HOCs for:
    1. Enhancing callbacks without copy-pasting logic into multiple components.
    2. Enhancing React lifecycle events (e.g., firing a logging event `onMount` or on specific prop changes).
    3. Intercepting and suppressing DOM/keyboard events (e.g., blocking global listeners inside dialogs).
*   **HOC Signature Rule:** An HOC MUST be written as a function that takes a `Component` as its first argument and returns a new functional component: `(props) => <Component {...props} />`.
*   **Prop Spreading Rule:** The returned component MUST spread all received `props` onto the wrapped `Component` to ensure the original API remains intact.
*   **Callback Interception Rule:** When intercepting a callback (e.g., `onClick`), the AI MUST check for and invoke the original callback from `props` inside the new callback definition.
*   **Lifecycle Enhancement Rule:** The AI MUST utilize standard React hooks (like `useEffect`) inside the returned functional component to track and react to lifecycle events (e.g., mounting or prop updates).
*   **Parameterizing HOCs:** When an HOC requires external configuration data, the AI MUST pass this data using one of two methods:
    1. As a secondary argument to the HOC function itself (e.g., `withLogic(Component, params)`).
    2. As an extracted prop from the returned component's props (e.g., `return ({ specificProp, ...props }) => ...`).
*   **Event Suppression Structure:** When intercepting DOM events to prevent bubbling, the AI MUST wrap the `Component` inside a native DOM element (e.g., `<div>`) and attach the `stopPropagation` logic to that wrapper.

@Workflow
1.  **Requirement Analysis:** Determine if the requested feature is a cross-cutting concern (logging, event blocking, lifecycle tracking) or a stateful data requirement. If state/data, STOP and use a custom Hook. If a cross-cutting concern, proceed with an HOC.
2.  **HOC Initialization:** Define a factory function prefixed with `with` (e.g., `withLoggingOnClick`) that accepts a `Component` as its primary argument.
3.  **Parameterization (Optional):** If the logic requires static configuration, add a second argument to the factory function. If it requires dynamic runtime configuration, prepare to extract a specific prop in the returned component.
4.  **Component Return:** Inside the factory function, return a functional component that accepts `props`.
5.  **Logic Injection:**
    *   *For Callbacks:* Extract the target callback from `props`, define a new callback that runs the side-effect, and then call the original extracted callback.
    *   *For Lifecycles:* Implement standard React hooks (`useEffect`) inside the returned component.
    *   *For DOM Events:* Define an event handler that calls `event.stopPropagation()`.
6.  **Component Rendering:** Render the passed `Component`.
    *   Ensure all unmodified `props` are spread (`{...props}`).
    *   Inject modified callbacks as explicitly overridden props (e.g., `onClick={interceptedOnClick}`).
    *   If doing DOM event suppression, wrap the `<Component />` in a DOM element (like `div`) and attach the intercepting event handler to the wrapper.

@Examples (Do's and Don'ts)

**Principle: Sharing State and Context**
*   [DO]: Use custom Hooks for injecting state, Context, or theme data.
```javascript
const Button = () => {
  const { theme } = useTheme();
  return <button className={theme}>Button</button>;
};
```
*   [DON'T]: Use an HOC to inject Context or stateful logic in modern React code.
```javascript
const withTheme = (Component) => {
  const theme = isDark ? 'dark' : 'light';
  return (props) => <Component {...props} theme={theme} />;
};
const ButtonWithTheme = withTheme(Button);
```

**Principle: Enhancing Callbacks**
*   [DO]: Use an HOC to intercept a callback, execute a side-effect, and trigger the original callback, ensuring all other props are spread.
```javascript
export const withLoggingOnClick = (Component) => {
  return (props) => {
    const onClick = () => {
      console.log('Log on click something');
      // AI MUST call the original callback
      if (props.onClick) {
        props.onClick();
      }
    };
    // Return original component, spreading props, overriding onClick
    return <Component {...props} onClick={onClick} />;
  };
};
export const ButtonWithLogging = withLoggingOnClick(SimpleButton);
```
*   [DON'T]: Copy-paste side-effect logic into every individual component, or fail to invoke the original prop callback inside the HOC.
```javascript
export const withLoggingOnClick = (Component) => {
  return (props) => {
    const onClick = () => {
      console.log('Log on click something');
      // ERROR: Original props.onClick is never called, breaking the component!
    };
    return <Component {...props} onClick={onClick} />;
  };
};
```

**Principle: Parameterizing the HOC via Props**
*   [DO]: Destructure the required configuration prop to use it in the side-effect, and spread the *rest* of the props to the underlying component.
```javascript
export const withLoggingOnClickWithProps = (Component) => {
  return ({ logText, ...props }) => {
    const onClick = () => {
      console.log('Log on click: ', logText);
      if (props.onClick) props.onClick();
    };
    return <Component {...props} onClick={onClick} />;
  };
};
// Usage: <ButtonWithLoggingOnClickWithProps logText="Page button" onClick={callback} />
```
*   [DON'T]: Pass the configuration prop down to the underlying component if it doesn't natively support it, which pollutes the DOM/React tree.
```javascript
export const withLoggingOnClickWithProps = (Component) => {
  return (props) => { // ERROR: logText is kept in props
    const onClick = () => {
      console.log('Log on click: ', props.logText); 
      if (props.onClick) props.onClick();
    };
    return <Component {...props} onClick={onClick} />; // logText leaks into Component
  };
};
```

**Principle: Intercepting DOM Events**
*   [DO]: Wrap the rendered component in a native DOM element to catch and stop events from bubbling up to the `window`.
```javascript
export const withSuppressKeyPress = (Component) => {
  return (props) => {
    const onKeyPress = (event) => {
      event.stopPropagation();
    };
    return (
      <div onKeyPress={onKeyPress}>
        <Component {...props} />
      </div>
    );
  };
};
const ModalWithSuppressedKeyPress = withSuppressKeyPress(Modal);
```
*   [DON'T]: Apply the `stopPropagation` logic directly to the Component without a DOM wrapper, as custom components do not natively emit DOM events unless explicitly wired to do so via forwarded refs.
```javascript
export const withSuppressKeyPress = (Component) => {
  return (props) => {
    const onKeyPress = (event) => {
      event.stopPropagation();
    };
    // ERROR: Custom components do not handle onKeyPress natively
    return <Component {...props} onKeyPress={onKeyPress} />; 
  };
};
```

**Principle: Enhancing Lifecycle Events**
*   [DO]: Utilize standard React hooks inside the returned functional component to trigger logic based on component mounting or prop changes.
```javascript
export const withLoggingOnReRender = (Component) => {
  return ({ id, ...props }) => {
    useEffect(() => {
      console.log('log on id change');
    }, [id]);

    return <Component id={id} {...props} />;
  };
};
```
*   [DON'T]: Attempt to use legacy class-based lifecycle methods or inject lifecycle logic directly into the component's render execution flow without hooks.