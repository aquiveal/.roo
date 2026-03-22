@Domain
Trigger these rules when tasked with interacting with RESTful APIs in a React application. This includes creating data-fetching functions using the browser's `fetch` API, typing HTTP responses with type assertion functions, managing asynchronous state via `useEffect`, implementing route-level data loading using React Router (`loader`, `defer`, `Await`), and managing server state/caching with React Query (`useQuery`, `useMutation`, `QueryClient`).

@Vocabulary
- **JSON Server**: A development tool used to mock a REST API backend by serving data from a `db.json` file.
- **Type Assertion Function**: A TypeScript function using the `asserts data is Type` signature that rigorously validates an `unknown` payload at runtime and throws an explicit `Error` if the structure is invalid.
- **React Router Loader**: A function defined on a React Router route that executes and fetches data *before* the route's component renders.
- **Defer**: A React Router utility function used within a loader to return a promise rather than awaiting it, unblocking the initial render of the route component.
- **Suspense & Await**: React and React Router components used in tandem to display a fallback UI while a deferred promise resolves.
- **React Query (TanStack Query)**: A library used to manage, cache, and synchronize asynchronous server state in React.
- **useQuery**: A React Query hook used to fetch and cache data using a unique key array.
- **useMutation**: A React Query hook used to execute data-modifying requests (POST, PUT, DELETE) and handle success/error side effects.

@Objectives
- Execute standard HTTP GET and POST requests using the native `fetch` API.
- Guarantee type safety of REST API responses by casting JSON to `unknown` and applying robust runtime type assertion functions.
- Prevent memory leaks and React state errors in `useEffect` fetching by implementing cleanup functions with boolean cancellation flags.
- Optimize user experience during data fetching by utilizing React Router's `loader` and `defer` functionality.
- Manage server state, caching, and cache invalidation efficiently using React Query.
- Integrate React Router loaders with React Query to achieve optimal performance, preventing unnecessary component re-renders while utilizing a robust client-side cache.

@Guidelines
- **Environment Variables**: Always store API URLs in environment files (e.g., `.env`) using the `REACT_APP_` prefix. When accessing these variables in code, use the TypeScript non-null assertion operator (`!`) if their existence is guaranteed (e.g., `process.env.REACT_APP_API_URL!`).
- **Fetching and Parsing**: When using `fetch`, await the response, call `.json()`, and cast the result to `unknown`. Do not cast directly to the target type.
- **Type Assertion Logic**: Type assertion functions MUST validate the data thoroughly. Check if the payload is an array (if applicable), loop through items, use the `in` operator to check for required keys, use `typeof` to check value types, and throw a specific `Error` if any check fails.
- **Effect Hook Fetching**: If forced to use `useEffect` for data fetching (instead of React Router or React Query), DO NOT make the effect callback `async`. Instead, use `.then()` or define a nested `async` function. You MUST define a `let cancel = false` flag, check `if (!cancel)` before setting state, and return a cleanup function that sets `cancel = true`.
- **Posting Data**: For POST requests, configure the `fetch` options with `method: 'POST'`, serialize the body using `JSON.stringify(data)`, and explicitly set the `Content-Type: application/json` header.
- **React Router Loaders**: Prefer React Router's route `loader` property over `useEffect` for initial data fetching. Access the fetched data inside the component using the `useLoaderData` hook.
- **Deferred Loading**: If an API request is slow, use React Router's `defer` function in the loader. In the component, wrap the data rendering logic in React's `<Suspense>` (providing a fallback) and React Router's `<Await>` component.
- **React Query Setup**: Initialize a `QueryClient` outside the App component tree and wrap the application in a `<QueryClientProvider>`.
- **Cache Mutations**: When modifying data using React Query's `useMutation`, use the `onSuccess` callback to manually update the local cache via `queryClient.setQueryData`, ensuring the UI reflects the change immediately.
- **Combining React Router and React Query**: To get the best of both tools, define a React Router `loader` that checks the React Query cache using `queryClient.getQueryData()`. If data exists, return it via `defer()`. If it does not exist, fetch it using `queryClient.fetchQuery()` and wrap it in `defer()`. To refresh this data after a mutation, use React Router's `navigate('/')` to re-trigger the loader.

@Workflow
1. **Define Types**: Create TypeScript types/interfaces representing the expected structure of the REST API response.
2. **Create Fetch Functions**: Implement standalone asynchronous functions that execute `fetch` requests using environment variables for the URL.
3. **Implement Runtime Type Safety**: Write a `asserts data is TargetType` function. Inside the fetch function, cast the JSON response to `unknown`, pass it to the assertion function, and then return the strongly typed data.
4. **Select a Data-Fetching Strategy**:
   - *Strategy A (Basic/Legacy)*: Use `useState` and `useEffect` with a cancellation flag.
   - *Strategy B (React Router)*: Export the fetch function and assign it to a route's `loader`. Retrieve data using `useLoaderData()`.
   - *Strategy C (React Query)*: Use the `useQuery` hook with a query key array and the fetch function.
   - *Strategy D (Optimal Combined)*: Inside a route `loader`, check `queryClient.getQueryData()`. Fallback to `queryClient.fetchQuery()`. Return the promise wrapped in `defer()`. In the component, use `<Suspense>` and `<Await>`.
5. **Implement Mutations**: Write a POST fetch function. Execute it using React Query's `useMutation`.
6. **Update Cache**: In the `useMutation`'s `onSuccess` block, call `queryClient.setQueryData` to immutably update the cached data array with the newly returned object.
7. **Trigger Sync (If using Strategy D)**: Call `navigate(currentPath)` inside the `onSuccess` block to force the React Router loader to pull the freshly updated cache.

@Examples (Do's and Don'ts)

- [DO] Use a cancellation flag when fetching inside `useEffect` to prevent state updates on unmounted components.
```typescript
useEffect(() => {
  let cancel = false;
  getPosts().then((data) => {
    if (!cancel) {
      setPosts(data);
      setIsLoading(false);
    }
  });
  return () => {
    cancel = true;
  };
}, []);
```

- [DON'T] Pass an async function directly to `useEffect` or fail to handle unmounting.
```typescript
// Anti-pattern: Async useEffect callback, no cleanup flag
useEffect(async () => {
  const data = await getPosts();
  setPosts(data); // Can cause memory leaks if component unmounts
}, []);
```

- [DO] Validate unknown JSON responses using a strict type assertion function.
```typescript
export function assertIsPosts(postsData: unknown): asserts postsData is PostData[] {
  if (!Array.isArray(postsData)) {
    throw new Error("posts isn't an array");
  }
  postsData.forEach((post) => {
    if (!('id' in post)) {
      throw new Error("post doesn't contain id");
    }
    if (typeof post.id !== 'number') {
      throw new Error('id is not a number');
    }
  });
}

export async function getPosts() {
  const response = await fetch(process.env.REACT_APP_API_URL!);
  const body = (await response.json()) as unknown;
  assertIsPosts(body);
  return body;
}
```

- [DON'T] Blindly cast API responses using `as any` or `as TargetType` without runtime validation.
```typescript
// Anti-pattern: Bypassing type safety
export async function getPosts() {
  const response = await fetch(process.env.REACT_APP_API_URL!);
  const body = await response.json();
  return body as PostData[]; // Dangerous!
}
```

- [DO] Combine React Query and React Router loaders using `defer` for optimal performance.
```typescript
const router = createBrowserRouter([
  {
    path: "/",
    element: <PostsPage />,
    loader: async () => {
      const existingData = queryClient.getQueryData(['postsData']);
      if (existingData) {
        return defer({ posts: existingData });
      }
      return defer({
        posts: queryClient.fetchQuery(['postsData'], getPosts)
      });
    }
  }
]);
```

- [DO] Update the React Query cache manually on successful mutation.
```typescript
const { mutate } = useMutation(savePost, {
  onSuccess: (savedPost) => {
    queryClient.setQueryData<PostData[]>(
      ['postsData'],
      (oldPosts) => {
        if (oldPosts === undefined) {
          return [savedPost];
        } else {
          return [savedPost, ...oldPosts];
        }
      }
    );
    navigate('/'); // Re-trigger router loader
  },
});
```

- [DON'T] Use `fetch` for a POST request without setting the correct method, headers, and stringified body.
```typescript
// Anti-pattern: Missing headers and stringification
const response = await fetch(url, {
  method: 'POST',
  body: newPostData // Will fail to process correctly
});
```