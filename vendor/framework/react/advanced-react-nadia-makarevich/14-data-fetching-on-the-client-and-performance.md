@Domain
React data fetching, component lifecycle performance, network request orchestration, and client-side application architecture. Triggered when implementing API calls, `useEffect` fetching, custom data hooks, or analyzing application load performance.

@Vocabulary
- **Initial Data Fetching**: Data required before a component ends up on the screen, typically fetched inside `useEffect` or on component mount.
- **On-Demand Data Fetching**: Data fetched in response to a user interaction (e.g., autocompletes, dynamic forms), triggered inside callbacks.
- **Request Waterfall**: A performance anti-pattern where data fetching requests are executed in sequence because child components do not mount (and thus do not trigger their own fetches) until parent components finish loading.
- **Data Provider**: A Context-based abstraction wrapping data fetching logic, allowing fetch initialization at the top of the app tree while providing data to nested components without prop drilling.
- **Browser Connection Limit**: The maximum number of parallel HTTP1 requests a browser can make to the same host (typically 6 in Chrome).
- **Out-of-Lifecycle Fetching**: Triggering a `fetch` Promise at the file/module scope (outside of a React component) to initiate a request before React even parses the component tree.

@Objectives
- Eliminate sequential "Request Waterfalls" to minimize total application load time.
- Orchestrate data loading strictly based on the designated user experience "story" (e.g., wait-for-all vs. progressive rendering).
- Prevent connection slot saturation caused by uncontrolled parallel requests.
- Avoid architectural pollution (like severe prop drilling) while implementing performance optimizations.

@Guidelines
- The AI MUST determine the desired loading UX (wait for all data vs. progressive rendering) before implementing data fetching optimizations.
- The AI MUST NOT implement data fetching inside nested child components if the parent component conditionally renders those children behind a loading state (this inherently causes a Request Waterfall).
- The AI MUST hoist data requests as high up the render tree as possible to execute them in parallel.
- When hoisting requests to achieve a "wait for all" experience, the AI MUST use `Promise.all` to resolve all parallel fetches together before triggering a state update.
- When hoisting requests to achieve a "progressive rendering" experience, the AI MUST resolve parallel Promises independently using individual `.then()` chains to trigger isolated state updates.
- The AI MUST be cautious with independent top-level state updates, as triggering multiple independent state changes in the root component will cause multiple full-tree re-renders.
- To avoid massive prop drilling from hoisted fetch requests, the AI MUST utilize Context-based "Data Providers" to initiate fetches globally while exposing data locally.
- The AI MUST NEVER initialize a `fetch` request at the file scope (outside a React component) UNLESS it is strictly for router-level critical pre-fetching or pre-fetching inside a lazy-loaded component. This is to avoid saturating the browser's 6-request connection limit with non-critical background data.
- The AI MUST respect that assigning a component to a variable (e.g., `const child = <Child />`) does NOT trigger its `useEffect` or data fetching; it only runs when the component is explicitly returned in the render tree.
- The AI MUST evaluate whether a simple `fetch` within `useEffect` suffices for "fetch once and forget" scenarios before introducing heavy external state management or fetching libraries.

@Workflow
1. **Analyze Component Hierarchy**: Review the component tree to identify all components that require Initial Data Fetching.
2. **Detect Waterfalls**: Check if any parent components return a loading state (e.g., `if (!data) return 'loading';`) while wrapping children that also require data fetching.
3. **Determine UX Strategy**: Decide whether the UI should render all at once (wait-for-all) or piece-by-piece (progressive rendering).
4. **Hoist Fetching Logic**: Move the `fetch` calls from nested children up to a common parent component or into Context Data Providers.
5. **Implement Parallelism**:
   - For *wait-for-all*: Group the `fetch` calls inside a `Promise.all` block. Save the combined result to state.
   - For *progressive rendering*: Execute the `fetch` calls sequentially in the code block but resolve them via independent `.then()` handlers.
6. **Abstract with Providers (If Needed)**: If hoisting creates excessive prop drilling, encapsulate the independent fetch logic inside distinct Context Provider components and wrap the application root. Use `useContext` in the deeply nested components to retrieve the resolved data.

@Examples (Do's and Don'ts)

[DO] Use `Promise.all` to fetch data in parallel when you want to wait for all data before rendering the application.
```javascript
const useAllData = () => {
  const [sidebar, setSidebar] = useState();
  const [issue, setIssue] = useState();

  useEffect(() => {
    const dataFetch = async () => {
      // Trigger all fetches in parallel
      const [sidebarRes, issueRes] = await Promise.all([
        fetch('/get-sidebar'),
        fetch('/get-issue')
      ]);
      
      const sidebarData = await sidebarRes.json();
      const issueData = await issueRes.json();

      setSidebar(sidebarData);
      setIssue(issueData);
    };
    dataFetch();
  }, []);

  return { sidebar, issue };
};

const App = () => {
  const { sidebar, issue } = useAllData();

  if (!sidebar || !issue) return 'loading';

  return (
    <>
      <Sidebar data={sidebar} />
      <Issue issue={issue} />
    </>
  );
};
```

[DON'T] Create a Request Waterfall by co-locating fetching in nested components that are conditionally blocked by parent loading states.
```javascript
// ANTIPATTERN: The child will not fetch until the parent finishes fetching.
const Issue = () => {
  const { data } = useData('/get-issue');
  
  if (!data) return 'loading'; // Blocks Comments from mounting!
  
  return (
    <div>
      <h3>{data.title}</h3>
      <Comments /> 
    </div>
  );
};

const Comments = () => {
  // This fetch won't start until Issue's fetch is 100% complete
  const { data } = useData('/get-comments'); 
  if (!data) return 'loading';
  return <div>Comments loaded</div>;
};
```

[DO] Use Context Data Providers to execute fetches in parallel at the root level without causing prop drilling.
```javascript
const CommentsContext = React.createContext();

export const CommentsDataProvider = ({ children }) => {
  const [comments, setComments] = useState();

  useEffect(() => {
    fetch('/get-comments')
      .then((res) => res.json())
      .then((data) => setComments(data));
  }, []);

  return (
    <CommentsContext.Provider value={comments}>
      {children}
    </CommentsContext.Provider>
  );
};

export const useComments = () => useContext(CommentsContext);

// At the root level:
// <IssueDataProvider><CommentsDataProvider><App /></CommentsDataProvider></IssueDataProvider>

const Comments = () => {
  const comments = useComments(); // No prop drilling required!
  if (!comments) return 'loading';
  return <div>Comments loaded</div>;
};
```

[DON'T] Place `fetch` Promises at the file scope indiscriminately, as it circumvents the React lifecycle and can easily consume the browser's maximum connection limit, blocking critical requests.
```javascript
// ANTIPATTERN: This fetch fires immediately upon file parsing, potentially saturating browser connection slots.
const commentsPromise = fetch('/get-comments');

const Comments = () => {
  const [data, setData] = useState();

  useEffect(() => {
    const dataFetch = async () => {
      const result = await (await commentsPromise).json();
      setData(result);
    };
    dataFetch();
  }, []);
  
  if (!data) return 'loading';
  return <div>{data.title}</div>;
};
```