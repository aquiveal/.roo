# @Domain
Frontend React development tasks involving client-side routing, multi-page application navigation, URL state management (search and route parameters), routing error handling, and component code-splitting. These rules activate whenever the AI uses React Router (specifically version 6+ using `react-router-dom`).

# @Vocabulary
- **React Router**: A declarative client-side routing library for React applications.
- **createBrowserRouter**: The recommended function to create a browser router instance for web applications.
- **RouterProvider**: The component used to provide the router instance to the React component tree.
- **Route Object**: An object containing a `path` and an `element` to render when the browser URL matches the path.
- **Link**: A React Router component used for declarative navigation, preventing default full-page reloads.
- **NavLink**: A specialized version of `<Link>` that provides an `isActive` state to style active navigation items.
- **Nested Routes**: Routes defined within a `children` array of a parent route, allowing for shared layouts.
- **Outlet**: A React Router component used inside a parent route component to determine where child route components should be rendered.
- **Route Parameter**: A dynamic segment in a URL path (prefixed with `:`), extracted as a string via `useParams`.
- **Error Page (`errorElement`)**: A custom React component rendered when a routing error occurs or no matching route is found.
- **useRouteError**: A hook used inside an `errorElement` to retrieve the thrown error payload (which is of type `unknown`).
- **Type Predicate**: A TypeScript function used to narrow down the `unknown` type of `useRouteError` payloads (e.g., `error is { statusText: string }`).
- **Index Route**: A default child route (defined with `index: true`) that renders when the parent path is matched exactly, but no child path is appended.
- **Search Parameter (Query Parameter)**: Key-value pairs in the URL after a `?`, managed via the `useSearchParams` hook and the `URLSearchParams` API.
- **Programmatic Navigation**: Imperative navigation using the `navigate` function returned by the `useNavigate` hook.
- **Form Navigation**: Using React Router's `<Form>` component to handle form submissions client-side, syncing form data into the URL search parameters or triggering route actions.
- **Lazy Loading**: The practice of splitting code into separate bundles and loading them on demand using `React.lazy` and `React.Suspense`.

# @Objectives
- Implement highly performant, declarative client-side routing without triggering full page reloads.
- Isolate page layouts from page content using nested routes and the `<Outlet />` component.
- Strictly type and handle URL parameters (both route parameters and search parameters).
- Provide robust, user-friendly error boundaries to catch invalid paths or routing failures gracefully.
- Optimize application load times by lazily loading distinct route components.
- Minimize imperative navigation (`useNavigate`) by favoring declarative links (`<Link>`) and client-side form submissions (`<Form>`).

# @Guidelines
- The AI MUST define web app routes using `createBrowserRouter` and pass the returned router instance to `<RouterProvider>`.
- The AI MUST place the `<RouterProvider>` at the very top of the React component tree (e.g., in `index.tsx`).
- The AI MUST NOT use native HTML anchor tags (`<a href="...">`) for internal navigation. Use `<Link to="...">` instead.
- The AI MUST use `<NavLink>` instead of `<Link>` for navigation menus where the active state must be visually differentiated. `className` on `<NavLink>` MUST receive a function `({ isActive }) => string`.
- The AI MUST use nested routes (the `children` array in the route object) to share layout components (like Headers or sidebars).
- The AI MUST use the `<Outlet />` component inside the parent layout component to render the matching child route's element.
- The AI MUST treat all route parameters extracted via `useParams()` as strings. If a number is required, the AI MUST parse it explicitly (e.g., `parseInt(params.id)`).
- The AI MUST define custom error boundaries using the `errorElement` property on the root route or specific child routes.
- The AI MUST use `useRouteError()` to display error information. Because the error is of type `unknown`, the AI MUST implement a TypeScript type predicate function to safely narrow the error type before accessing properties like `statusText` or `message`.
- The AI MUST use `index: true` (instead of `path: ""`) to define default child components for parent layouts.
- The AI MUST manage URL query strings using `useSearchParams()`.
- When reading from `searchParams.get('param')`, the AI MUST handle the possibility of `null` returns using nullish coalescing (`??`) or explicit `null` checks.
- The AI MUST prefer React Router's `<Form>` component over native HTML `<form>` elements to leverage client-side URL synchronization.
- When using `<Form>`, the AI MUST NOT call `e.preventDefault()`; React Router handles this automatically.
- The AI MUST use `React.lazy()` to dynamically import large or isolated route components (e.g., Admin pages).
- Lazy-loaded components MUST use `export default`. `React.lazy` does not support named exports directly.
- Any lazy-loaded element within the router MUST be wrapped in a `<Suspense>` component with a defined `fallback` prop (e.g., `<Suspense fallback={<div>Loading...</div>}>`).

# @Workflow
1. **Router Initialization**: Instantiate the router using `createBrowserRouter([...])` containing all root paths. Wrap the application root in `<RouterProvider router={router} />`.
2. **Layout Segregation**: Create a root layout component (e.g., `App`) containing shared UI (Header, Navigation) and an `<Outlet />`. Add it to the router as the root `element`.
3. **Route Declaration**: Define child route objects within the `children` array of the root layout. Use `index: true` for the home page.
4. **Error Handling**: Create an `ErrorPage` component using `useRouteError()`. Implement a type predicate to narrow the error. Assign it to the `errorElement` property of the root route.
5. **Navigation Construction**: Build navigation menus using `<NavLink>` to dynamically highlight active states. Use `<Link>` for standard inter-page navigation.
6. **Stateful URLs**: Use `useParams()` for unique identifiers (e.g., resource IDs). Use `useSearchParams()` for filters, search terms, or optional state.
7. **Form Transitions**: Replace `<form onSubmit={...}>` with `<Form action="/path" method="get|post">` to synchronize inputs with route state.
8. **Performance Optimization**: Identify distinct features (e.g., isolated settings pages). Export them as defaults, import them via `lazy(() => import('...'))`, and wrap their routing declaration in `<Suspense>`.

# @Examples (Do's and Don'ts)

## 1. Initializing Routes
**[DO]** Use `createBrowserRouter` and nested layout structures.
```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';
import { HomePage } from './HomePage';
import { ProductsPage } from './ProductsPage';
import { ErrorPage } from './ErrorPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'products', element: <ProductsPage /> },
    ],
  },
]);

export function Routes() {
  return <RouterProvider router={router} />;
}
```

**[DON'T]** Manually render individual route components without a unified layout outlet or using older router syntaxes (like `<BrowserRouter>` wrapping individual `<Route>` components arbitrarily).

## 2. Shared Layouts with Outlet
**[DO]** Use `<Outlet />` to render nested child components.
```tsx
import { Outlet } from 'react-router-dom';
import { Header } from './Header';

export default function App() {
  return (
    <>
      <Header />
      <main className="container mx-auto">
        <Outlet />
      </main>
    </>
  );
}
```

**[DON'T]** Attempt to pass child routes as `children` props to the App component manually.

## 3. Declarative Navigation
**[DO]** Use `NavLink` for active styling and `Link` for standard links.
```tsx
import { NavLink, Link } from 'react-router-dom';

export function Header() {
  return (
    <nav>
      {/* Active state styling */}
      <NavLink
        to="products"
        className={({ isActive }) =>
          `p-2 border-b-2 ${isActive ? "border-white" : "border-transparent"}`
        }
      >
        Products
      </NavLink>

      {/* Standard link */}
      <Link to={`/products/123`} className="text-blue-500 hover:underline">
        View Product
      </Link>
    </nav>
  );
}
```

**[DON'T]** Use `<a href="/products">` or rely solely on `useNavigate` for standard link clicks.

## 4. Error Handling and Type Predicates
**[DO]** Use `useRouteError` combined with a type predicate to extract and display error information safely.
```tsx
import { useRouteError } from 'react-router-dom';
import { Header } from './Header';

// Type predicate function
function isError(error: any): error is { statusText: string } {
  return "statusText" in error;
}

export function ErrorPage() {
  const error = useRouteError();

  return (
    <>
      <Header />
      <div className="text-center p-5">
        <h1>Sorry, an error has occurred</h1>
        {isError(error) && <p>{error.statusText}</p>}
      </div>
    </>
  );
}
```

**[DON'T]** Assume `error` is a specific type or attempt to render `error.statusText` without type-checking, as `useRouteError` returns `unknown`.

## 5. Route Parameters
**[DO]** Extract and explicitly parse route parameters.
```tsx
import { useParams } from 'react-router-dom';

type Params = {
  id: string;
};

export function ProductPage() {
  const params = useParams<Params>();
  const id = params.id ? parseInt(params.id, 10) : undefined;

  return <div>Product ID: {id}</div>;
}
```

**[DON'T]** Assume `params.id` is a number directly from the hook.

## 6. Form Navigation
**[DO]** Use React Router's `<Form>` for client-side search submissions.
```tsx
import { Form, useSearchParams } from 'react-router-dom';

export function SearchHeader() {
  const [searchParams] = useSearchParams();

  return (
    <Form action="/products" method="get">
      <input
        type="search"
        name="search"
        defaultValue={searchParams.get('search') ?? ''}
      />
      <button type="submit">Search</button>
    </Form>
  );
}
```

**[DON'T]** Use native HTML `<form onSubmit={(e) => e.preventDefault(); navigate(...) }>` for basic routing when `<Form>` can handle it automatically.

## 7. Lazy Loading
**[DO]** Lazily load isolated chunks, ensuring the component is a default export and wrapped in Suspense.
```tsx
import { lazy, Suspense } from 'react';
import { createBrowserRouter } from 'react-router-dom';

// Must be a default export in AdminPage.tsx
const AdminPage = lazy(() => import('./pages/AdminPage'));

const router = createBrowserRouter([
  {
    path: 'admin',
    element: (
      <Suspense fallback={<div>Loading Admin Panel...</div>}>
        <AdminPage />
      </Suspense>
    ),
  },
]);
```

**[DON'T]** Lazily import named exports or forget to wrap the lazy element in `<Suspense>`, which will cause React to suspend indefinitely or crash the tree.