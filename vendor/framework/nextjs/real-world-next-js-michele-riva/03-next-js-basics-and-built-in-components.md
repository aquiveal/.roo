@Domain
These rules MUST be triggered whenever the AI is requested to create, modify, or debug Next.js routing, client-side navigation, static asset serving, image optimization, HTML metadata, or the global `_app.js` and `_document.js` configuration files.

@Vocabulary
- **Page Component**: A React component exported from a file inside the `pages/` directory. Next.js maps these directly to application routes.
- **Dynamic Route**: A route containing a variable, defined by enclosing the filename or folder name in brackets (e.g., `[slug].js`).
- **Query Parameter**: Data extracted from the URL, accessible via the `useRouter` hook or server-side context props, containing both route variables and parsed query strings.
- **Cumulative Layout Shift (CLS)**: A performance and UX penalty occurring when images or elements load late and push layout down. Mitigated via Next.js Automatic Image Optimization.
- **Automatic Image Optimization**: A Next.js feature (via `next/image`) that resizes, optimizes, and serves images in modern formats (like WebP) on-demand to prevent CLS.
- **Hydration**: The process by which React attaches event listeners and state to the server-rendered HTML on the client-side.
- **Open Graph**: A metadata protocol used to generate rich preview cards when links are shared on social media platforms.
- **_app.js**: A reserved Next.js file used to control page initialization, wrap components with providers, and manage global state/layouts.
- **_document.js**: A reserved Next.js file used to customize the fundamental HTML structure (`<html>`, `<body>`) of the server-rendered output.

@Objectives
- Guarantee that all routing relies on the Next.js file-based routing system.
- Maximize performance and prevent CLS by exclusively using the built-in `next/image` component for rendering images.
- Ensure optimal client-side navigation by utilizing the `next/link` component to leverage automatic route prefetching.
- Optimize SEO and social media sharing capabilities by dynamically and modularly managing metadata with the `next/head` component.
- Keep the application interface consistent by appropriately utilizing `_app.js` for layouts and global state, and `_document.js` for fundamental HTML structure.

@Guidelines

# Routing & Variables
- The AI MUST use the `pages/` directory for defining application routes. Nested folders create nested routes.
- The AI MUST use bracket syntax (`[variable_name].js` or `[variable_name]/`) to define dynamic routes.
- When retrieving dynamic route variables inside a **Page Component**, the AI MUST extract `params` from the `getServerSideProps` or `getStaticProps` context and pass them to the component via the returning `props` object.
- When retrieving dynamic route variables inside a **Standard React Component** (non-page), the AI MUST import `{ useRouter }` from `next/router` and extract the variable from `useRouter().query`.
- The AI MUST treat the `useRouter().query` object as the source of truth for both dynamic route parameters and standard URL query string parameters. If a query string parameter shares a key with a route variable, Next.js gives precedence to the route variable.

# Client-Side Navigation
- The AI MUST use the `Link` component from `next/link` for static user-triggered navigation.
- The AI MUST NOT use the legacy `as` prop for dynamic routing inside the `Link` component (Next.js >= 10 uses the `href` prop to automatically resolve both the rendering page and the address bar display).
- If building complex URLs, the AI MUST pass an object to the `href` prop containing `pathname` and `query` properties.
- The AI MUST use `router.push()` (via `useRouter`) ONLY for programmatic redirects (e.g., redirecting an unauthenticated user inside a `useEffect` hook). Programmatic routing bypasses the automatic prefetching provided by the `Link` component.
- To disable default prefetching on a `Link`, the AI MUST explicitly set the `preload={false}` prop.

# Static Assets & Images
- The AI MUST place all static assets (fonts, icons, compiled CSS/JS) inside the `public/` directory and reference them using absolute paths starting with `/`.
- The AI MUST completely avoid using the standard HTML `<img>` tag to prevent Cumulative Layout Shift (CLS). The AI MUST use the `Image` component from `next/image`.
- When utilizing external image sources with the `Image` component, the AI MUST configure the external domains inside the `images.domains` array in the `next.config.js` file.
- The AI MUST provide either explicit `width` and `height` props OR use the `layout='fill'` prop when rendering an `Image` component.
- When using `layout='fill'`, the AI MUST wrap the `Image` component in a parent `div` that has `position: 'relative'` and explicitly defined dimensions. It MUST also use the `objectFit='cover'` prop to crop the image appropriately.
- If automatic image optimization impacts server performance or requires custom routing, the AI MUST delegate optimization to an external service by setting a `loader` property in `next.config.js` (e.g., `akamai`, `imgix`) or passing a custom `loader` function prop directly to the `Image` component.

# Metadata Management
- The AI MUST use the `Head` component from `next/head` to inject HTML metadata (`<title>`, `<meta>`).
- To prevent Next.js from duplicating metadata tags when multiple components attempt to modify the same tag, the AI MUST add a unique `key` prop to the HTML elements inside the `<Head>` component (e.g., `<title key='htmlTitle'>`).
- For content-heavy pages (like blogs), the AI MUST group common metadata (e.g., Open Graph and Twitter card tags) into reusable React components (e.g., `<PostHead>`).

# Customizing _app.js and _document.js
- The AI MUST use `pages/_app.js` to initialize global styles, apply consistent layouts (like a global Navbar), and manage cross-page state (like themes or shopping cart items) via React Context Providers.
- The AI MUST NOT use the `getInitialProps` lifecycle method inside `_app.js` unless absolutely strictly required, as doing so disables Next.js's automatic static optimization for the entire application, forcing all pages to be server-side rendered.
- The AI MUST use `pages/_document.js` exclusively to customize the root `<html>` and `<body>` tags.
- When overriding `_document.js`, the AI MUST extend the `Document` class and MUST render the `<Html>`, `<Head>`, `<Main>`, and `<NextScript>` components exactly. Omitting any of these four components will break the Next.js application.
- The AI MUST NOT put application logic, shared UI components (like navbars), or data fetching inside `_document.js`.

@Workflow
1. **Routing Setup**: Create structural files/folders in the `pages/` directory. Use brackets for dynamic entities.
2. **Data Extraction**: For dynamic pages, extract `params` via `getServerSideProps`/`getStaticProps`. Pass to the page via `props`. For child components, extract via `useRouter().query`.
3. **Navigation Implementation**: Connect pages using `next/link` via the `href` prop. For programmatic forced routing based on state or auth, use `router.push()`.
4. **Asset & Image Integration**: Serve simple files from `/public`. For images, construct `next/image` components, assign layout dimensions (`fixed`, `intrinsic`, `responsive`, or `fill`), and update `next.config.js` domains if the image source is external.
5. **SEO Configuration**: Add `next/head` inside the page component. Include deduplication `key` props on critical tags. Create a grouped Open Graph metadata component if requested.
6. **Global Wrappers**: If cross-page persistence or global wrappers are needed, modify `_app.js`. If `<html lang="en">` or core body structure changes are needed, modify `_document.js`.

@Examples

[DO] Fetch dynamic route variables inside a standard component using useRouter:
```javascript
import { useRouter } from 'next/router';

function Greet() {
  const { query } = useRouter();
  return <h1>Hello {query.name}!</h1>;
}
export default Greet;
```

[DON'T] Attempt to use `getServerSideProps` in a non-page component to extract route variables.

[DO] Implement dynamic routing using Next.js 10+ standard inside a Link:
```javascript
import Link from 'next/link';

// Using a string
<Link href='/blog/2021-01-01/happy-new-year'> Read post </Link>

// Using a URL object
<Link href={{ pathname: '/blog/[date]/[slug]', query: { date: '2021-01-01', slug: 'happy-new-year' } }}>
  Read post
</Link>
```

[DON'T] Use the legacy `as` prop for dynamic routes in Next.js >= 10:
```javascript
// Anti-pattern
<Link href='/blog/[date]/[slug]' as='/blog/2021-01-01/happy-new-year'>
  Read post
</Link>
```

[DO] Use programmatic routing for auth guards or specific event handlers:
```javascript
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import useAuth from '../hooks/auth';

function MyPage() {
  const router = useRouter();
  const { loggedIn } = useAuth();
  
  useEffect(() => {
    if (!loggedIn) {
      router.push('/login');
    }
  }, [loggedIn]);
  
  return loggedIn ? <div>Private Content</div> : null;
}
```

[DON'T] Use `router.push()` as the default method for building standard site navigation menus.

[DO] Implement external, responsive images properly to prevent CLS:
```javascript
import Image from 'next/image';

function Cover() {
  return (
    <div style={{ width: 500, height: 200, position: 'relative' }}>
      <Image
        src='https://images.unsplash.com/photo-12345'
        layout='fill'
        objectFit='cover'
        alt='Cover Image'
      />
    </div>
  );
}
```

[DON'T] Use the standard `<img>` tag which causes Cumulative Layout Shift.

[DO] Prevent duplicate metadata tags using the `key` prop:
```javascript
import Head from 'next/head';

function Widget({ pageName }) {
  return (
    <Head>
      <title key='htmlTitle'>You are browsing {pageName}</title>
    </Head>
  );
}
```

[DON'T] Add metadata in nested components without the `key` prop, which results in duplicate tags in the document head.

[DO] Customize `_document.js` with all mandatory structural components:
```javascript
import Document, { Html, Head, Main, NextScript } from 'next/document';

class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
export default MyDocument;
```

[DON'T] Place layout components (like Navbars), application logic, or data-fetching functions inside `_document.js`. Use `_app.js` for those concerns.