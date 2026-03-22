# @Domain
These rules trigger when the AI is tasked with creating, modifying, or debugging Next.js pages, specifically concerning data fetching, page rendering strategies, performance optimization, SEO indexing, or fixing server-side execution crashes related to browser-specific APIs (e.g., `window`, `document`).

# @Vocabulary
- **Server-Side Rendering (SSR):** A strategy where the HTML is dynamically rendered on the server for each incoming request before being sent to the browser.
- **Client-Side Rendering (CSR):** A strategy where the server serves an empty HTML shell, and the browser downloads the JavaScript bundle to render the application dynamically.
- **Static Site Generation (SSG):** A strategy where pages are pre-rendered into static HTML at build time and served globally via CDNs.
- **Incremental Static Regeneration (ISR):** A hybrid Next.js feature that allows static pages to be re-rendered in the background at runtime after a specified timeout, without requiring a full site rebuild.
- **Hydration:** The process where Next.js injects scripts into a server-rendered or statically generated HTML page to make the DOM interactive on the client side.
- **Spider/Bot:** Search engine crawlers that index web pages. They heavily favor SSR and SSG due to immediate HTML availability.
- **`getServerSideProps`:** The reserved Next.js function exported to trigger SSR on a page.
- **`getStaticProps`:** The reserved Next.js function exported to trigger SSG (and ISR) on a page.
- **`next/dynamic`:** A built-in Next.js module used to dynamically load components, allowing developers to disable SSR for specific components.
- **`process.browser`:** A Next.js-specific global boolean variable appended to the Node.js `process` object, returning `true` on the client side and `false` on the server side.

# @Objectives
- The AI MUST select the strictly optimal rendering strategy (SSR, SSG, ISR, or CSR) based on the page's specific requirements for SEO, data security, data freshness, and server workload.
- The AI MUST rigorously prevent Node.js server crashes caused by executing browser-specific APIs or HTML elements (`window`, `document`, `<canvas>`) during the server rendering phase.
- The AI MUST implement data fetching safely, ensuring private APIs and tokens are never exposed to the client unless explicitly required.
- The AI MUST leverage ISR to minimize build times and server workload while maintaining dynamic data freshness.

# @Guidelines

### Server-Side Rendering (SSR) Rules
- When building pages requiring highly secure interactions (managing cookies, calling private APIs), maximum browser compatibility, and strong SEO for highly dynamic per-request data, the AI MUST use SSR.
- The AI MUST implement SSR by exporting an `async function getServerSideProps()`.
- The AI MUST return an object containing a `props` key from `getServerSideProps`. Next.js will inject these props into the page component.
- The AI MUST NOT manually polyfill the `fetch` API inside `getServerSideProps`, as Next.js automatically provides this polyfill on the server.
- The AI MUST account for the latency overhead of SSR. Do not use SSR for pages that can be statically cached unless per-request dynamic rendering is strictly mandated by business logic.

### Client-Side Rendering (CSR) Rules
- When building highly dynamic pages where SEO is irrelevant (e.g., admin dashboards, private profile pages), the AI MUST use CSR to lighten the server workload.
- The AI MUST explicitly isolate third-party libraries and code that rely on browser-specific APIs (like `window`, `document`, or DOM manipulation) to the client side.
- **CSR Implementation Method 1 (useEffect):** To execute logic only on the client, the AI MUST wrap the logic inside a `React.useEffect` hook, which only runs after React hydration.
- **CSR Implementation Method 2 (useState + useEffect):** To entirely prevent a component's markup from rendering on the server, the AI MUST use a boolean state (e.g., `const [isClient, setIsClient] = useState(false)`), set it to `true` inside `useEffect`, and conditionally render the component (`{isClient && <Component />}`).
- **CSR Implementation Method 3 (next/dynamic):** When importing heavy external components or components relying on browser APIs, the AI MUST use `dynamic()` with the `{ ssr: false }` configuration object.
- **CSR Implementation Method 4 (process.browser):** For simple conditional rendering or inline script execution branching, the AI MUST use the `process.browser` boolean check.

### Static Site Generation (SSG) and Incremental Static Regeneration (ISR) Rules
- When building highly scalable, secure, and performant public pages that do not change on every single request, the AI MUST prioritize SSG via `getStaticProps`.
- If an SSG page relies on dynamic data that updates periodically, the AI MUST NOT rely on full site rebuilds. Instead, the AI MUST implement ISR.
- The AI MUST implement ISR by adding a `revalidate` property (specifying the time in seconds) to the object returned by `getStaticProps`.
- The AI MUST understand and respect the lazy nature of ISR: Next.js will only rebuild the page in the background if a request occurs *after* the `revalidate` window has expired. There is no forced API revalidation.
- The AI MUST NOT attempt to use `getServerSideProps` and `getStaticProps` in the same page file. They are mutually exclusive.

# @Workflow
When tasked with creating or modifying a Next.js page or component, the AI MUST execute the following algorithmic decision process:

1. **Analyze SEO and Security Requirements:**
   - Does the page need to be indexed by search engines? 
   - Does the page fetch data using private API keys or direct database queries?
   - *If YES to either:* Eliminate CSR as the primary rendering strategy for the page shell. Move to Step 2.
   - *If NO to both (e.g., an internal Admin panel):* Prioritize CSR.

2. **Analyze Data Freshness vs. Performance (Choosing between SSG/ISR and SSR):**
   - Must the data be uniquely generated for *every single incoming request* (e.g., personalized user greetings, reading cookies)?
   - *If YES:* Implement `getServerSideProps` (SSR).
   - *If NO (data is shared among users and changes periodically):* Implement `getStaticProps` (SSG). Move to Step 3.

3. **Configure Static Regeneration:**
   - Does the static data ever change after build time?
   - *If YES:* Add the `revalidate: X` property to the `getStaticProps` return object, calculating `X` (in seconds) based on acceptable data staleness.

4. **Audit for Browser APIs:**
   - Does the component or its dependencies use `window`, `document`, DOM manipulations, or canvas elements?
   - *If YES:* Wrap the usage in `useEffect`, use a conditional `isClient` state, or import the component using `next/dynamic` with `{ ssr: false }`.

# @Examples (Do's and Don'ts)

### Server-Side Rendering Implementation
**[DO]** Use `getServerSideProps` correctly, returning the nested `props` object without manual fetch polyfills.
```javascript
export async function getServerSideProps() {
  const userRequest = await fetch('https://example.com/api/user');
  const userData = await userRequest.json();
  
  return {
    props: {
      user: userData
    }
  };
}

export default function IndexPage(props) {
  return <div>Welcome, {props.user.name}!</div>;
}
```

**[DON'T]** Forget the `props` wrapper or try to use DOM APIs in SSR.
```javascript
export async function getServerSideProps() {
  const data = await fetch('https://example.com/api/data').then(r => r.json());
  // Anti-pattern: Missing 'props' key wrapper. Next.js will throw an error.
  return { data }; 
}
```

### Handling Browser-Specific APIs
**[DO]** Use `next/dynamic` with `{ ssr: false }` to safely load components reliant on browser APIs.
```javascript
import dynamic from 'next/dynamic';
import styles from '../styles/Home.module.css';

const Highlight = dynamic(
  () => import('../components/Highlight'),
  { ssr: false }
);

export default function DynamicPage() {
  return (
    <div className={styles.main}>
      <Highlight code={"console.log('Hello, world!')"} language='js' />
    </div>
  );
}
```

**[DON'T]** Execute browser APIs directly in the component body, which will crash the Node.js SSR process.
```javascript
import hljs from 'highlight.js'; // Relies on 'document'

export default function Highlight({ code }) {
  // Anti-pattern: This will crash during SSR/Build because 'document' is undefined in Node.js
  hljs.initHighlighting(); 
  return <pre><code className='js'>{code}</code></pre>;
}
```

**[DO]** Use `useState` and `useEffect` to defer rendering of browser-dependent components until hydration is complete.
```javascript
import { useEffect, useState } from 'react';
import Highlight from '../components/Highlight';

export default function UseEffectPage() {
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <div>
      {isClient && <Highlight code={"console.log('Hello, world!')"} language='js' />}
    </div>
  );
}
```

### Implementing Incremental Static Regeneration (ISR)
**[DO]** Use `getStaticProps` with the `revalidate` property to cache slow API responses but allow background updates.
```javascript
export async function getStaticProps() {
  const dashboardReq = await fetch('https://example.com/api/dashboard');
  const dashboardData = await dashboardReq.json();
  
  return {
    props: {
      data: dashboardData,
    },
    revalidate: 600 // Regenerate page in background after 10 minutes
  };
}

export default function IndexPage(props) {
  return <Dashboard data={props.data} />;
}
```

**[DON'T]** Rebuild the whole app for minor data changes when ISR can solve the issue. (Avoid omitting `revalidate` if the data source is expected to change).