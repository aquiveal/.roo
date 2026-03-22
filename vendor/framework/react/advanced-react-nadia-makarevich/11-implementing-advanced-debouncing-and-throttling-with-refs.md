@Domain
Trigger these rules when tasked with implementing debouncing or throttling for event handlers (e.g., input `onChange`, window `onScroll`, auto-save features) in React components, particularly when the debounced/throttled callback requires access to the component's internal state or props.

@Vocabulary
- **Debouncing**: A technique that skips function execution until a specified wait time has elapsed *after* the last time the function was invoked. (Resets the timer on continuous calls).
- **Throttling**: A technique that guarantees a function is executed regularly at specific intervals, regardless of how many times it is triggered.
- **Delay Anti-pattern**: A failure mode in React where a debounced function is re-created on every render (due to state changes). Instead of dropping previous calls, multiple new timers are created, turning the debounce into a simple delay that fires multiple times.
- **Stale Closure**: A scenario where a function (often inside a hook or a Ref) captures the initial state or props of a component and never updates, continuously operating on outdated data.
- **Closure Trap Escape Trick**: An advanced architectural pattern that leverages the mutability of `useRef` to store the latest callback. It allows a stable, memoized debounced function to access the latest state without being re-created.

@Objectives
- Implement reliable debouncing and throttling without falling into the "Delay Anti-pattern" caused by React's rendering lifecycle.
- Ensure debounced and throttled callbacks always execute with the most up-to-date state and props.
- Prevent infinite recreation of timers and callbacks during state updates.
- Encapsulate complex closure and ref-based orchestration into clean, reusable custom hooks (e.g., `useDebounce`).

@Guidelines
- **NEVER** declare a `debounce` or `throttle` function directly inside the component body if the component has state. Re-rendering will recreate the debounced function, resetting the internal timer and causing the Delay Anti-pattern.
- **AVOID** relying solely on `useMemo` and `useCallback` for debouncing when the callback depends on component state. Adding state to the dependency array will force the debounced function to be recreated on every keystroke/update, breaking the debounce mechanism.
- **NEVER** initialize a `useRef` with a debounced callback that reads state directly without updating it. This results in a Stale Closure where the callback only ever sees the initial state.
- **AVOID** using `useEffect` cleanup functions (e.g., `return () => ref.current.cancel()`) to reset debounced functions when state changes if you intend to build a universal hook. While it works for debouncing, it fundamentally breaks throttling behavior by cancelling executions before the interval completes.
- **MUST** use the "Closure Trap Escape Trick" for all advanced debouncing/throttling requirements where the callback needs access to internal state.
- **MUST** utilize a mutable `useRef` to store the latest callback function and update it continuously via `useEffect`.
- **MUST** initialize the actual `debounce` or `throttle` wrapper exactly once using `useMemo` with an empty dependency array `[]`.
- **MUST** invoke `ref.current?.()` inside the stable memoized function rather than passing the callback to the debounce wrapper directly.

@Workflow
1. **Identify the Data Flow**: Determine if the debounced/throttled function needs to read component state (e.g., an auto-save reading an input value).
2. **Abstract into a Custom Hook**: Create a `useDebounce` (or `useThrottle`) hook to hide the closure management complexity.
3. **Setup the Mutable Ref**: Inside the hook, instantiate `const ref = useRef()`.
4. **Sync Latest Callback**: Add a `useEffect` that updates `ref.current = callback` whenever the passed `callback` changes.
5. **Memoize the Debouncer**: Use `useMemo` with an empty dependency array `[]` to create the debounced function only once upon mount.
6. **Implement the Escape Trick**: Inside the `useMemo` factory, pass an anonymous function to your external `debounce` utility. This anonymous function must execute `ref.current?.()`.
7. **Return the Function**: Return the memoized debounced callback from the custom hook.
8. **Consume the Hook**: In the target component, pass the state-dependent function to `useDebounce` and attach the returned function to the event handler.

@Examples (Do's and Don'ts)

[DON'T] Call debounce directly in the component body (Causes Delay Anti-pattern)
```javascript
const Input = () => {
  const [value, setValue] = useState('');

  const sendRequest = (val) => console.log(val);
  
  // WRONG: Recreated on every render. Timer is lost.
  const debouncedSendRequest = debounce(sendRequest, 500);

  const onChange = (e) => {
    setValue(e.target.value);
    debouncedSendRequest(e.target.value); // Will fire multiple times (just delayed)
  };

  return <input onChange={onChange} value={value} />;
};
```

[DON'T] Use useMemo with state dependencies for debouncing (Breaks debounce)
```javascript
const Input = () => {
  const [value, setValue] = useState('');

  const sendRequest = useCallback(() => {
    console.log(value);
  }, [value]);

  // WRONG: Dependency changes on every keystroke, recreating the debounce.
  const debouncedSendRequest = useMemo(() => {
    return debounce(sendRequest, 1000);
  }, [sendRequest]);

  // ...
};
```

[DON'T] Store debounce in a Ref without updating the closure (Causes Stale Closure)
```javascript
const Input = () => {
  const [value, setValue] = useState('');

  // WRONG: Closure is frozen. It will only ever log the initial state ('').
  const ref = useRef(debounce(() => {
    console.log(value); 
  }, 500));

  // ...
};
```

[DO] Use the Closure Trap Escape Trick via a custom hook
```javascript
import { useState, useRef, useEffect, useMemo } from 'react';
import debounce from 'lodash/debounce';

// 1. Abstract into a custom hook
const useDebounce = (callback) => {
  const ref = useRef();

  // 2. Keep the ref updated with the latest callback (and its fresh closure)
  useEffect(() => {
    ref.current = callback;
  }, [callback]);

  // 3. Create the debounced function exactly once
  const debouncedCallback = useMemo(() => {
    const func = () => {
      // 4. Access the latest callback via the mutable ref
      ref.current?.();
    };

    return debounce(func, 1000);
  }, []); // Empty dependency array!

  return debouncedCallback;
};

// Usage in Component
const Input = () => {
  const [value, setValue] = useState('');

  const debouncedRequest = useDebounce(() => {
    // Has access to the latest state seamlessly!
    console.log('Sending to backend:', value);
  });

  const onChange = (e) => {
    setValue(e.target.value);
    debouncedRequest();
  };

  return <input onChange={onChange} value={value} />;
};
```