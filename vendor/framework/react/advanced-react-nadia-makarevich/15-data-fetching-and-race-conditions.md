# @Domain
- Implementation, modification, or review of data fetching logic inside React components.
- Handling asynchronous operations, Promises, or `async/await` syntax inside `useEffect` hooks.
- Debugging state update issues, flickering UI content, or inconsistent data rendering related to network requests.
- Fixing race conditions in React applications.

# @Vocabulary
- **Promise**: An asynchronous operation in JavaScript that resolves or rejects (e.g., `fetch` or `axios`). Async/await is syntactic sugar over Promises.
- **Race Condition**: A bug occurring when multiple asynchronous requests resolve out of order. In React, this happens when a newer request resolves before an older request, and the older request subsequently overwrites the component state with stale data.
- **Stale Promise/Closure**: A promise initiated from an older render cycle whose `.then` or `await` resolution attempts to update the current component state after a newer dependency change has already occurred.
- **Cleanup Function**: The function returned from a `useEffect` hook, executed by React before the next effect runs or when the component unmounts.
- **AbortController**: A native web API interface used to send an abort signal to a DOM request (like `fetch`), cancelling the network request entirely.
- **State Reset (Forced Re-mounting)**: A technique using the React `key` prop to force React to destroy an existing component instance and mount a completely new one, inadvertently dropping pending promises.

# @Objectives
- The AI MUST completely eliminate data fetching race conditions in React components.
- The AI MUST guarantee that component state accurately reflects only the result of the most recently initiated asynchronous request.
- The AI MUST implement safe promise rejection handling, specifically ignoring errors caused by intentional request cancellations.
- The AI MUST avoid destructive anti-patterns (like forced remounting) for solving async state management unless explicitly required by the user.

# @Guidelines
- **Mandatory Race Condition Prevention**: The AI MUST NEVER write a `fetch` or async call inside a `useEffect` that updates state without implementing a dedicated race-condition prevention strategy. If the `useEffect` has dependencies that can change (e.g., `[id]`, `[url]`), a mitigation strategy is strictly required.
- **Async/Await Equivalence**: The AI MUST treat `async/await` exactly the same as `.then()`. Syntactic sugar does not magically prevent race conditions. All async operations require mitigation.
- **Preferred Mitigation Strategy 1: AbortController (Cancel Requests)**: Use `AbortController` to cancel previous requests. When using this strategy, the AI MUST explicitly catch and ignore the `AbortError` (`error.name === 'AbortError'`) to prevent console warnings or unhandled rejections.
- **Preferred Mitigation Strategy 2: Closure Flag (Drop Results)**: Use a local boolean flag (e.g., `let isActive = true`) inside the `useEffect`. Update state only if the flag is true. Reset the flag to false inside the `useEffect` cleanup function.
- **Preferred Mitigation Strategy 3: Ref Comparison (Drop Incorrect Results)**: If the fetched result includes a unique identifier (like `id` or `url`), store the current identifier in a `useRef`. Update `ref.current` synchronously inside the effect. Compare `ref.current` against the resolved identifier before updating state.
- **Anti-Pattern Constraint**: The AI MUST NOT use the `key` prop on a component (e.g., `<Page id={page} key={page} />`) solely to fix a race condition. This forces complete component unmounting, destroying focus, local state, and causing performance degradation. Treat this as sweeping the problem under the rug.

# @Workflow
1. **Identify Async Operation**: Detect any data fetching or asynchronous operation happening inside a React component (typically within `useEffect`).
2. **Analyze Dependencies**: Check the dependency array of the `useEffect`. If it contains changing variables (like route params, IDs, search queries), proceed to implement a race condition mitigation strategy.
3. **Select Mitigation Strategy**: Default to `AbortController` for network requests (`fetch`). If dealing with non-cancellable promises, default to the Closure Flag (`isActive`) strategy.
4. **Implement Strategy (AbortController)**:
   - Instantiate `const controller = new AbortController();` inside `useEffect`.
   - Pass `{ signal: controller.signal }` to the fetch call.
   - Return a cleanup function calling `controller.abort();`.
   - Add a `.catch` or `try/catch` block explicitly checking `if (error.name === 'AbortError') { return; }`.
5. **Implement Strategy (Closure Flag)**:
   - Declare `let isActive = true;` at the top of the `useEffect` callback.
   - Wrap the state setter in `if (isActive) { setData(result); }`.
   - Return a cleanup function containing `isActive = false;`.
6. **Verify State Integrity**: Ensure that regardless of the order in which promises resolve, the component state will only ever reflect the data of the last requested dependency.

# @Examples (Do's and Don'ts)

### Principle: Fetching data in useEffect requires race condition handling

- **[DON'T]** Execute a fetch without a cleanup or cancellation strategy. This causes the last-resolved request to overwrite state, even if it is stale.
```javascript
const Page = ({ id }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // VULNERABLE TO RACE CONDITIONS
    fetch(`/api/data/${id}`)
      .then(res => res.json())
      .then(res => setData(res));
  }, [id]);

  return <div>{data?.title}</div>;
};
```

- **[DO]** Use `AbortController` to cancel previous requests and explicitly catch the `AbortError`.
```javascript
const Page = ({ id }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch(`/api/data/${id}`, { signal: controller.signal })
      .then(res => res.json())
      .then(res => setData(res))
      .catch(error => {
        if (error.name === 'AbortError') {
          // Ignore cancellation errors
          return;
        }
        // Handle actual errors
        console.error(error);
      });

    return () => {
      controller.abort();
    };
  }, [id]);

  return <div>{data?.title}</div>;
};
```

### Principle: Using async/await with Closure Flags

- **[DON'T]** Assume `async/await` solves race conditions.
```javascript
useEffect(() => {
  const fetchData = async () => {
    // STILL VULNERABLE
    const res = await fetch(`/api/data/${id}`);
    const result = await res.json();
    setData(result);
  };
  fetchData();
}, [id]);
```

- **[DO]** Use an `isActive` flag updated via the cleanup function to drop stale async/await results.
```javascript
useEffect(() => {
  let isActive = true;

  const fetchData = async () => {
    try {
      const res = await fetch(`/api/data/${id}`);
      const result = await res.json();
      if (isActive) {
        setData(result);
      }
    } catch (error) {
      if (isActive) {
        // handle error
      }
    }
  };

  fetchData();

  return () => {
    isActive = false;
  };
}, [id]);
```

### Principle: Dropping incorrect results via Ref Comparison

- **[DO]** Use a `useRef` to track the latest request identifier if cancellation is not viable.
```javascript
const Page = ({ id }) => {
  const [data, setData] = useState(null);
  const latestIdRef = useRef(id);

  useEffect(() => {
    latestIdRef.current = id;

    fetch(`/api/data/${id}`)
      .then(res => res.json())
      .then(result => {
        if (latestIdRef.current === result.id) {
          setData(result);
        }
      });
  }, [id]);
  
  return <div>{data?.title}</div>;
};
```

### Principle: Handling Race Conditions architecturally

- **[DON'T]** Use the `key` prop to intentionally unmount the component just to avoid writing proper Promise cleanup logic.
```javascript
// BAD: Sweeps the race condition under the rug, destroys local state and focus
const App = () => {
  const [page, setPage] = useState('1');
  return <Page id={page} key={page} />; 
};
```