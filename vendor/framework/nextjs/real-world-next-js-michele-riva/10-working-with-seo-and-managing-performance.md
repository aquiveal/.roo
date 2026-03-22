@Domain
- **Activation Conditions:** Trigger these rules when working within a Next.js project and the user requests tasks related to page creation, architectural routing, rendering strategy selection (CSR, SSR, SSG, ISR), Search Engine Optimization (SEO), Web Vitals tracking, or general frontend performance tuning.

@Vocabulary
- **CSR (Client-Side Rendering):** Rendering methodology where the application is bundled into a JS file and dynamic content is generated in the browser. High performance/interactivity, but poor SEO and security.
- **SSR (Server-Side Rendering):** Rendering methodology where HTML is generated on the server per request. Excellent for security and SEO, but can degrade performance under high load and requires server maintenance.
- **SSG (Static Site Generation):** Rendering methodology where HTML is generated at build time. Best possible performance and SEO, but lacks dynamic security and requires long build times for massive amounts of pages.
- **ISR (Incremental Static Regeneration):** Next.js feature allowing static pages to be updated in the background at runtime without requiring a full rebuild.
- **Web Spiders (Bots):** Automated scripts used by search engines to crawl and index websites. They struggle with heavy JS-dependent client-side rendering.
- **LCP (Largest Contentful Paint):** Web Vital measuring loading performance. Must occur within 2.5 seconds of the initial page load.
- **FID (First Input Delay):** Web Vital measuring page interactivity latency. Must be under 100 milliseconds.
- **CLS (Cumulative Layout Shift):** Web Vital measuring visual stability (e.g., elements moving as heavy images load). Prevented using the Next.js Image component.
- **Fallback (`fallback: true`):** A Next.js configuration in `getStaticPaths` that allows ungenerated static pages to be rendered dynamically on the first request and cached for subsequent ones.
- **reportWebVitals:** A Next.js built-in function exported from `_app.js` used to capture and log/send frontend performance metrics.

@Objectives
- **Optimal Rendering Selection:** The AI must ruthlessly evaluate the purpose of every single page to select the exact right combination of SSG, SSR, or CSR, avoiding uniform global rendering strategies.
- **Maximum SEO Indexability:** The AI must architect public-facing pages to be immediately readable by web spiders using semantic HTML, structured metadata, and SEO-friendly URLs.
- **Frontend Performance Dominance:** The AI must enforce architectures that guarantee passing Web Vitals (LCP < 2.5s, FID < 100ms, minimal CLS).
- **Data Security:** The AI must completely hide sensitive API calls and user session validation on the server side using SSR for private routes.

@Guidelines

**1. Rendering Strategy Constraints:**
- **User-Specific/Highly Dynamic Feeds (e.g., Logged-in Homepages):** The AI MUST use a combination of SSG (for the page shell/skeleton) and CSR (to fetch the user-specific data after React hydration). Do NOT use SSR for user-specific feeds unless SEO is specifically required (which it typically is not for authenticated feeds).
- **Public Detail Pages (e.g., Articles, Products, Image details):** The AI MUST evaluate the expected scale of the application:
  - If the site has thousands/millions of pages (e.g., e-commerce, large social media), the AI MUST use SSR to prevent crippling build times, OR use SSG strictly for a subset of the top/most popular pages with `fallback: true` to generate the rest at request time.
  - If the site has a manageable amount of pages (e.g., a standard blog), the AI MUST use SSG combined with ISR (Incremental Static Regeneration) to allow authors to update content without triggering a full site rebuild.
- **Private/Protected Routes (e.g., Account Settings):** The AI MUST use SSR (`getServerSideProps`). The AI MUST validate the user session on the server and redirect unauthenticated users *before* rendering the page. The AI MUST preload all private user data on the backend to prevent exposing sensitive API endpoints to the client browser.

**2. SEO Architecture Rules:**
- **URL Structure:** The AI MUST construct human-readable, descriptive URLs (slugs). Example: `/posts/how-to-deal-with-seo` instead of `/posts/1`.
- **Metadata Management:** The AI MUST include structured `<head>` tags for every public page. The AI SHOULD recommend and utilize the `next-seo` library to manage Open Graph, Twitter cards, and standard metadata efficiently.
- **Sitemap Generation:** For production deployments, the AI MUST generate an XML sitemap to assist web spiders. The AI SHOULD utilize tools like `nextjs-sitemap-generator`.
- **Semantic HTML:** The AI MUST use appropriate HTML semantic tags to signal priority to web spiders. The AI MUST NOT use `<h1>` tags for all text content; `<h1>` MUST be reserved strictly for the main page title.

**3. Performance and Web Vitals Rules:**
- **Image Optimization:** To prevent CLS (Cumulative Layout Shift) and improve LCP (Largest Contentful Paint), the AI MUST NEVER use standard `<img>` tags for content images. The AI MUST enforce the use of the `next/image` (`<Image />`) component.
- **Tracking Web Vitals:** The AI MUST implement frontend performance tracking. If the user is deploying to Vercel, the AI must note that Vercel Analytics handles this. If deploying elsewhere, the AI MUST export the `reportWebVitals` function in `_app.js` and configure it to log metrics or send them to an external analytics provider (e.g., Google Analytics, Plausible).
- **Deployment Awareness:** The AI MUST recognize that SSG pages achieve maximum performance when deployed to a CDN, while SSR applications require scalable server infrastructure to prevent performance degradation under load.

@Workflow

When tasked with creating a new Next.js page or optimizing an existing one, the AI MUST follow this exact sequence:

1. **Requirement Analysis:**
   - Ask or determine: Does this page require SEO? (Yes/No)
   - Ask or determine: Is this page private/authenticated? (Yes/No)
   - Ask or determine: How often does the data change? (Real-time, frequently, rarely).
   - Ask or determine: How many total pages of this type will exist? (Tens, thousands, millions).

2. **Rendering Strategy Selection:**
   - IF Private/Authenticated -> Select SSR. Implement session check and redirect inside `getServerSideProps`.
   - IF Public + Millions of pages -> Select SSR OR SSG with `fallback: true`.
   - IF Public + Manageable pages + Frequent updates -> Select SSG with ISR (`revalidate`).
   - IF User-specific feed (No SEO needed) -> Select SSG (Skeleton) + CSR (Data Fetch).

3. **SEO Implementation (If Public):**
   - Implement descriptive URL slug logic.
   - Inject the `next-seo` component with dynamic title and description props.
   - Ensure the layout uses strict semantic HTML (one `<h1>`, proper `<article>`, `<section>` tags).

4. **Performance Hardening:**
   - Audit all media. Replace any standard `<img>` tags with `next/image`.
   - Verify `_app.js` contains the `reportWebVitals` export.

@Examples (Do's and Don'ts)

**Routing & URL Structure**
- [DO]: Implement human-readable routes: `https://myblog.com/posts/how-to-deal-with-seo`
- [DON'T]: Implement database-ID-based opaque routes for content: `https://myblog.com/posts/1`

**Private Route Protection**
- [DO]: Use SSR to protect data and redirect before the browser renders anything.
```javascript
export async function getServerSideProps(context) {
  const session = await getSession(context.req);
  if (!session) {
    return { redirect: { destination: '/login', permanent: false } };
  }
  const privateData = await fetchPrivateUserData(session.userId);
  return { props: { user: privateData } };
}
```
- [DON'T]: Rely entirely on CSR for private routes, which downloads the protected JS bundle and exposes the private API endpoint to the client's network tab before redirecting.

**Semantic HTML for SEO**
- [DO]: Use hierarchical, meaningful tags.
```javascript
<article>
  <h1>Working with SEO in Next.js</h1>
  <h2>Understanding Web Vitals</h2>
  <p>Content goes here...</p>
</article>
```
- [DON'T]: Use `<h1>` tags just to make text large, confusing web spiders.
```javascript
<div>
  <h1>Working with SEO in Next.js</h1>
  <h1>Understanding Web Vitals</h1>
  <h1>Content goes here...</h1>
</div>
```

**Web Vitals Tracking**
- [DO]: Export `reportWebVitals` from `_app.js` to monitor LCP, FID, and CLS.
```javascript
// pages/_app.js
export function reportWebVitals(metric) {
  if (metric.label === 'web-vital') {
    sendToAnalytics(metric);
  }
}
export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
```
- [DON'T]: Ignore frontend performance metrics, assuming server-side speed guarantees a good user experience. Ensure CLS and FID are actively monitored.