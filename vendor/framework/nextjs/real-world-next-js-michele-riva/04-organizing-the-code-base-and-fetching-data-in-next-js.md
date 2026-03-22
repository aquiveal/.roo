# @Domain
Trigger these rules when the user requests Next.js project scaffolding, folder structure reorganization, component creation, or implementation of data fetching architectures (REST or GraphQL) on either the client or server side within a Next.js environment.

# @Vocabulary
- **Atomic Design**: A methodology for organizing components into hierarchical categories: `atoms` (basic HTML wrappers/UI elements), `molecules` (groups of atoms), `organisms` (complex structures of molecules/atoms), and `templates` (page skeletons).
- **Utility Scripts (`utilities/`)**: Modular, generic scripts used across different components that do not export React components (e.g., time formatters, localStorage handlers).
- **Lib Files (`lib/`)**: Scripts that explicitly configure and wrap third-party libraries (e.g., GraphQL clients, Redis connectors).
- **Static Assets**: Non-dynamic files (images, compiled CSS/JS, manifests) strictly served from the `public/` directory.
- **Client-Side Proxy / API Routes**: Next.js serverless functions placed in the `pages/api/` directory, used to proxy browser requests to external APIs to hide credentials and bypass CORS.
- **Environment Variables**: Sensitive tokens and endpoints stored in `.env` or `.env.local` files, accessed via `process.env`, and explicitly excluded from version control.

# @Objectives
- Establish a highly scalable, maintainable, and predictable folder structure using Atomic Design and colocation.
- Prevent security vulnerabilities by rigorously isolating database connections and hiding private API keys from the client-side bundle.
- Implement robust server-side data fetching (SSR/SSG) using HTTP clients like Axios, securely passing environment variables.
- Safely execute client-side data fetching by proxying authenticated requests through Next.js API routes to prevent CORS errors and token leakage.
- Standardize GraphQL integration using Apollo Client with a unified singleton instance that seamlessly hydrates cache between the server and the browser.

# @Guidelines

## Folder and Architecture Constraints
- The AI MUST allow placing directories (except `public/` and `node_modules/`) inside a `src/` folder for root tidiness. 
- The AI MUST NEVER create both `pages/` and `src/pages/`. If both exist, Next.js ignores `src/pages/`.
- The AI MUST organize components strictly following Atomic Design principles: `components/atoms/`, `components/molecules/`, `components/organisms/`, and `components/templates/`.
- The AI MUST colocate component files. Every component MUST have its own folder containing its logic (`index.js`), tests (`[name].test.js`), and styles (`[name].styled.js` or `style.module.css`).
- The AI MUST place generic, reusable logic in a `utilities/` folder (grouped by scope, e.g., `time.js`, `jwt.js`) along with their respective test files.
- The AI MUST place third-party configuration wrappers (like Apollo, Axios instances) in a `lib/` directory.
- The AI MUST place static assets in `public/assets/` organized into subdirectories: `js/`, `css/`, `icons/`, `images/`.

## Data Fetching and Security Constraints
- The AI MUST NEVER establish direct database connections (e.g., MySQL, PostgreSQL) directly inside Next.js pages or components. Database access MUST be delegated to external APIs, Headless CMSs, or backend frameworks.
- The AI MUST NEVER hardcode API tokens, keys, or endpoints in the source code. All credentials MUST be accessed via `process.env.VARIABLE_NAME`.
- The AI MUST enforce that `.env` files are added to `.gitignore` and `.dockerignore`.
- When fetching data in `getServerSideProps`, the AI MUST handle 404 responses from APIs by returning `{ notFound: true }` to trigger the Next.js default 404 page.
- When performing client-side data fetching that requires Authorization tokens, the AI MUST NEVER send the token directly from the browser. Instead, the AI MUST create a Next.js API Route (`pages/api/[name].js`) to act as a proxy, attaching the secure token on the server side and returning the result to the client.
- Client-side API calls MUST ONLY be made to trusted sources and strictly over HTTPS.

## GraphQL and Apollo Constraints
- When integrating GraphQL, the AI MUST configure Apollo Client to work universally (client and server) by setting `ssrMode: typeof window === 'undefined'`.
- The AI MUST implement a cache restoration mechanism (`client.cache.restore`) to merge the server-fetched state with the client-side state.
- The AI MUST use the `useMemo` React hook to memoize the Apollo Client initialization to prevent expensive re-initializations during re-renders.
- The AI MUST separate GraphQL queries and mutations into their own colocated files inside `lib/graphql/queries/` and `lib/graphql/mutations/`.
- The AI MUST wrap the root application in `pages/_app.js` with `<ApolloProvider client={apolloClient}>`.

# @Workflow
1. **Repository Setup**: Initialize folders `components/` (with atomic subfolders), `utilities/`, `lib/`, and `public/assets/`. If `src/` is requested, move everything except `public` and `node_modules` into it.
2. **Component Creation**: When asked to create a component, determine its atomic level. Create a specific directory for it (e.g., `components/atoms/Button/`) and generate the `index.js`, `.test.js`, and style files together.
3. **Server-Side Fetching Setup**: Implement `getServerSideProps`. Extract route parameters from the context, fetch data using Axios utilizing `process.env` for headers/tokens, handle 404s, and return data in the `props` object.
4. **Client-Side Fetching Setup**: 
    - Identify if the endpoint requires an Authorization token.
    - If yes, create a proxy route in `pages/api/` that reads the `process.env` token and performs the actual fetch.
    - Implement `useEffect` or an event handler in the React component to call the proxy `/api/` route.
5. **GraphQL Configuration**:
    - Create `lib/apollo/index.js`.
    - Implement `createApolloClient()` utilizing `isomorphic-unfetch` and `InMemoryCache`.
    - Implement `initApollo(initialState)` for state hydration.
    - Create the `useApollo` hook utilizing `useMemo`.
    - Wrap the `_app.js` export in `ApolloProvider`.

# @Examples (Do's and Don'ts)

## Folder and Architecture
**[DO]**
```text
src/
  components/
    atoms/
      Button/
        index.js
        button.test.js
        button.module.css
  utilities/
    time.js
    time.test.js
  lib/
    graphql/
      index.js
pages/
public/
  assets/
    images/
```
**[DON'T]**
```text
src/
  pages/
pages/
components/
  Button.js
  Button.css
  Button.test.js
```
*(Reason: Never duplicate `pages/` and `src/pages/`. Never leave components un-grouped without their own folders and outside the Atomic Design structure.)*

## Direct Database Connections
**[DO]**
```javascript
export async function getServerSideProps() {
  const req = await axios.get(`${process.env.API_ENDPOINT}/users`);
  return { props: { users: req.data } };
}
```
**[DON'T]**
```javascript
import mysql from 'mysql';
export async function getServerSideProps() {
  const connection = mysql.createConnection({ ... });
  const users = await connection.query('SELECT * FROM users');
  return { props: { users } };
}
```
*(Reason: Next.js should only care about the frontend. Direct database connections inside Next.js expose the app to security vulnerabilities. Always use an API or Headless CMS.)*

## Authenticated Client-Side Fetching
**[DO]**
```javascript
// pages/api/singleUser.js (Proxy)
import axios from 'axios';
export default async function handler(req, res) {
  const { username } = req.query;
  const userReq = await axios.get(`${process.env.API_ENDPOINT}/users/${username}`, {
    headers: { authorization: process.env.API_TOKEN }
  });
  res.status(200).json(userReq.data);
}

// components/UserPage.js (Client Component)
useEffect(() => {
  const req = await fetch(`/api/singleUser?username=${username}`);
  const data = await req.json();
  setData(data);
}, []);
```
**[DON'T]**
```javascript
// components/UserPage.js (Client Component)
useEffect(() => {
  const req = await fetch(`https://external-api.com/users/${username}`, {
    headers: { authorization: 'my_super_secret_token' }
  });
  const data = await req.json();
  setData(data);
}, []);
```
*(Reason: Fetching directly from the client with secure tokens exposes the token to the browser's Network tab and risks CORS errors. Always proxy authenticated client requests through Next.js API routes.)*

## Handling 404 in SSR
**[DO]**
```javascript
export async function getServerSideProps(ctx) {
  const userReq = await axios.get(`${process.env.API_ENDPOINT}/users/${ctx.query.username}`);
  if (userReq.status === 404) {
    return { notFound: true };
  }
  return { props: { user: userReq.data } };
}
```
**[DON'T]**
```javascript
export async function getServerSideProps(ctx) {
  const userReq = await axios.get(`${process.env.API_ENDPOINT}/users/${ctx.query.username}`);
  if (userReq.status === 404) {
    return { props: { user: null, error: 'Not found' } };
  }
  return { props: { user: userReq.data } };
}
```
*(Reason: Do not manually pass error props to render a custom empty state for 404s in SSR; use Next.js's built-in `{ notFound: true }` to natively trigger the 404 page.)*