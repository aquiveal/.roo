# @Domain
Trigger these rules when the user requests tasks, code generation, or architectural advice related to integrating a React + TypeScript frontend with a GraphQL API. This includes setting up GraphQL clients, constructing GraphQL queries and mutations, fetching data via native `fetch` or `Apollo Client`, managing server state caching, and strongly typing GraphQL responses.

# @Vocabulary
- **GraphQL**: A query language for APIs that allows clients to request exactly the data they need, enabling flat or hierarchical data retrieval in a single request.
- **Query**: A GraphQL operation used strictly to fetch data. Denoted by the `query` keyword.
- **Mutation**: A GraphQL operation used to change or update underlying data. Denoted by the `mutation` keyword.
- **Query Variables**: Strongly typed parameters passed into a GraphQL operation to make it reusable. Always prefixed with a `$` (e.g., `$owner: String!`).
- **PAT (Personal Access Token)**: A secure string used for authorization against protected GraphQL APIs (e.g., GitHub GraphQL API).
- **Type Assertion Function**: A TypeScript function using an `asserts` signature to narrow an unknown/any API response into a strictly typed data structure.
- **React Query**: A server-state management library used in conjunction with the native `fetch` API to cache and manage GraphQL responses.
- **Apollo Client**: A specialized GraphQL client library (`@apollo/client`) that interacts directly with GraphQL APIs, eliminating the need for manual `fetch` calls.
- **gql**: A tagged template literal function provided by Apollo Client used to parse GraphQL query strings into GraphQL AST (Abstract Syntax Tree) objects.

# @Objectives
- Ensure all GraphQL operations (queries and mutations) strictly declare required fields to prevent over-fetching.
- Guarantee type safety for all GraphQL variables and API responses using TypeScript types and Type Assertion Functions.
- Securely manage API URLs and authentication tokens using standard environment variable separation (`.env` vs `.env.local`).
- Implement efficient caching and re-rendering strategies using either React Query (with `fetch`) or Apollo Client.
- Accurately trigger queries either on component mount or deferred via user interaction (`useLazyQuery` or React Query's `enabled` option).

# @Guidelines

### 1. GraphQL Syntax & Construction
- The AI MUST always explicitly use the `query` or `mutation` keywords when defining GraphQL operations, even though `query` is technically optional.
- The AI MUST define operation parameters using the exact GraphQL type definitions, prefixing variables with a dollar sign `$` and appending `!` if the parameter is required (e.g., `query GetRepo($org: String!, $repo: String!)`).
- The AI MUST structure mutations to pass variables inside an `input` object if the API schema dictates it (e.g., `addStar(input: { starrableId: $repoId })`).
- The AI MUST explicitly select the return fields required after a mutation completes to update the UI efficiently.

### 2. Environment Variables & Security
- The AI MUST NEVER hardcode API URLs or Personal Access Tokens (PAT) in the source code.
- The AI MUST instruct the placement of the GraphQL API URL in a standard `.env` file (e.g., `REACT_APP_GITHUB_URL`).
- The AI MUST instruct the placement of the PAT in a `.env.local` file (e.g., `REACT_APP_GITHUB_PAT`) and ensure `.env.local` is listed in `.gitignore`.
- When accessing these variables in TypeScript code, the AI MUST append the non-null assertion operator `!` (e.g., `process.env.REACT_APP_GITHUB_URL!`) since Create React App injects them at build time.

### 3. Native Fetch + React Query Approach
- When using `fetch` to call a GraphQL API, the AI MUST ALWAYS use the HTTP `POST` method.
- The AI MUST stringify the request body and structure it with a `query` property containing the GraphQL string, and a `variables` property containing the parameter object.
- The AI MUST include `'Content-Type': 'application/json'` and `Authorization: bearer <token>` in the fetch headers.
- To strongly type the response, the AI MUST initially cast the parsed JSON to `unknown` or `any`, and then pass it through a Type Assertion Function.
  - *Exception Handling:* Due to a known TypeScript limitation with narrowing `unknown` objects, the AI MAY use the `any` type for the parameter in the Type Assertion Function (e.g., `function assertIsGetViewerResponse(body: any): asserts body is ...`).
- When a query should only run upon a user interaction (not on mount), the AI MUST use the `enabled` option in `useQuery` (e.g., `enabled: searchCriteria !== undefined`).
- Upon successful mutation, the AI MUST use `queryClient.setQueryData` inside the `onSuccess` callback of `useMutation` to manually update the local cache without requiring a network refetch.

### 4. Apollo Client Approach
- The AI MUST initialize the Apollo Client using `new ApolloClient({ uri, cache: new InMemoryCache(), headers })` and provide it to the app via `<ApolloProvider client={queryClient}>`.
- The AI MUST wrap all GraphQL query and mutation string constants inside the `gql` tagged template literal (e.g., `export const GET_REPO = gql\` query {...} \`;`).
- The AI MUST use `useQuery` for data fetched on component mount, and `useLazyQuery` for data fetched via user interaction (e.g., form submissions).
- `useLazyQuery` MUST be destructured as a tuple: `const [triggerFunction, { data, loading }] = useLazyQuery(...)`.
- To update the cache after an Apollo mutation, the AI MUST use `queryClient.cache.writeQuery` inside the `onCompleted` callback of `useMutation`.

# @Workflow
When tasked with implementing a GraphQL API interaction, the AI MUST adhere to the following algorithmic process:

1. **Environment Setup:** Define the required environment variables (`.env` for URI, `.env.local` for Secrets).
2. **Type Definition:** Create a `types.ts` file. Define exact TypeScript types for the expected Query Variables and the expected JSON Response Data.
3. **Query/Mutation Declaration:** Define the GraphQL strings. If using Apollo Client, wrap them immediately in the `gql` function. Ensure variable definitions match the GraphQL schema exactly.
4. **Data Fetching Implementation:**
   - *If Apollo Client:* Implement `useQuery` or `useLazyQuery` inside the React component.
   - *If fetch + React Query:* Implement a separate async function using `fetch` (Method: POST, Body: JSON stringified `query` and `variables`). Implement a Type Assertion Function. Call this function inside `useQuery` in the component.
5. **Mutation Implementation:** Implement the mutation logic using `useMutation`.
6. **Cache Synchronization:** Inside the mutation hook (`onSuccess` for React Query, `onCompleted` for Apollo), write logic to read the current cached data, merge the mutated result, and write it back to the cache to update the UI instantly.

# @Examples (Do's and Don'ts)

### Defining GraphQL Queries for Apollo Client
**[DO]**
```typescript
import { gql } from '@apollo/client';

export const GET_VIEWER_QUERY = gql`
  query {
    viewer {
      name
      avatarUrl
    }
  }
`;
```

**[DON'T]** (Do not use raw strings for Apollo Client, do not omit formatting)
```typescript
export const GET_VIEWER_QUERY = `query { viewer { name avatarUrl } }`;
```

### Fetching GraphQL Data using Native Fetch
**[DO]**
```typescript
export async function getRepo(searchCriteria: SearchCriteria) {
  const response = await fetch(process.env.REACT_APP_GITHUB_URL!, {
    method: 'POST',
    body: JSON.stringify({
      query: GET_REPO,
      variables: {
        org: searchCriteria.org,
        repo: searchCriteria.repo,
      },
    }),
    headers: {
      'Content-Type': 'application/json',
      Authorization: `bearer ${process.env.REACT_APP_GITHUB_PAT}`,
    },
  });
  
  const body = (await response.json()) as any;
  assertIsGetRepoResponse(body);
  return body.data;
}
```

**[DON'T]** (Do not use GET, do not omit the query property in the body, do not forget the token)
```typescript
export async function getRepo(searchCriteria: SearchCriteria) {
  const response = await fetch(process.env.REACT_APP_GITHUB_URL!, {
    method: 'GET',
    body: JSON.stringify(searchCriteria)
  });
  return await response.json();
}
```

### Type Assertion Function Parameter Typing
**[DO]**
```typescript
function assertIsGetViewerResponse(body: any): asserts body is GetViewerResponse {
  if (!('data' in body)) throw new Error("no data");
}
```

**[DON'T]** (Do not fight TypeScript's `unknown` object narrowing limitations without explicit logic, use `any` as an accepted bypass for the input parameter of the assertion function as per the author's note)
```typescript
// Avoid struggling with TS errors on `in` checks against `unknown`
function assertIsGetViewerResponse(body: unknown): asserts body is GetViewerResponse {
  if (!('data' in body)) throw new Error("no data"); // TS Error
}
```

### Apollo Client Cache Updating
**[DO]**
```typescript
const [starRepo] = useMutation(STAR_REPO, {
  onCompleted: () => {
    queryClient.cache.writeQuery({
      query: GET_REPO,
      data: {
        repository: {
          ...data.repository,
          viewerHasStarred: true,
        },
      },
      variables: searchCriteria,
    });
  },
});
```

**[DON'T]** (Do not force a full network refetch if a simple cache update is possible)
```typescript
const [starRepo] = useMutation(STAR_REPO, {
  onCompleted: () => {
    window.location.reload(); // Anti-pattern
  },
});
```