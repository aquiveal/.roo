@Domain
These rules are activated when the user requests to create, modify, or debug a custom backend server (e.g., Express.js, Fastify) for a Next.js application, implements server-side routing overrides, migrates an existing Node.js application to Next.js, or discusses deployment configurations involving custom backend servers.

@Vocabulary
- **Custom Server**: A programmatic Node.js backend (like Express.js or Fastify) that wraps and serves a Next.js application, overriding the default Next.js server.
- **Multi-tenancy**: A software architecture where a single instance of the software serves multiple tenants (e.g., domains). A primary use case for utilizing a custom server in Next.js.
- **`next({ dev })`**: The Next.js factory function used to instantiate a Next.js application programmatically within a custom Node.js server.
- **`app.prepare()`**: An asynchronous method that must be awaited before binding any custom server routes, ensuring the Next.js engine is ready to handle requests.
- **`getRequestHandler()`**: A Next.js method that returns a default routing handler function, routing Node.js HTTP requests/responses directly into the Next.js ecosystem.
- **`app.render()`**: A Next.js method used to explicitly map a specific server route to a specific Next.js page component.
- **`_next/` Assets**: The internal static asset path used by Next.js to serve JavaScript bundles, hydration scripts, and client-side logic.
- **`fastify-nextjs`**: The official Fastify plugin used to seamlessly register and serve Next.js pages within a Fastify server.

@Objectives
- Evaluate and validate the necessity of a custom server before implementation, favoring the default Next.js server whenever possible.
- Ensure that custom Express.js servers correctly identify and route `/_next/` static assets to prevent blank pages and hydration failures.
- Implement efficient, programmatic Next.js instantiations using `app.prepare()`.
- Ensure correct usage of custom framework adapters (e.g., `fastify-nextjs` for Fastify).
- Prevent deployment mismatches by actively avoiding Vercel-centric configurations when a custom server is implemented.

@Guidelines

**1. Architectural Evaluation & Use Cases**
- The AI MUST question or warn the user if a custom server is requested without a valid architectural need. Most Next.js applications do not require a custom server.
- The AI MUST ONLY proceed with custom server implementations if the project meets one of these valid use cases:
  - **Progressive Migration**: Integrating Next.js into an existing Express/Fastify application.
  - **Multi-tenancy**: Complex domain routing and handling thousands of custom domains programmatically.
  - **Strict MVC Control**: The user requires a strict MVC architecture where Next.js acts strictly as the "View" layer behind a custom Node.js controller.
- The AI MUST warn the user that implementing a custom server removes the ability to deploy the application to Vercel and requires standard Node.js hosting environments (e.g., AWS EC2, DigitalOcean, Heroku, Docker).

**2. Express.js Custom Server Implementation Rules**
- When setting up Express.js, the AI MUST add the following specific dependencies: `express`, `react`, `react-dom`, and `next`.
- The AI MUST import `parse` from the native `url` module to parse incoming request URLs.
- The AI MUST instantiate the Next.js app using `const app = next({ dev: process.env.NODE_ENV !== 'production' })`.
- The AI MUST await `app.prepare()` inside an `async` function before creating the Express server instance.
- **CRITICAL ASSET ROUTING**: If custom routes are defined, the AI MUST explicitly define a route using a regular expression to catch Next.js static assets (`server.get(/_next\/.+/, ...)`). If this is omitted, Express will drop the Next.js frontend scripts, resulting in a blank HTML page.
- When explicitly mapping an Express route to a Next.js page, the AI MUST use `app.render(req, res, '/page-path', query)`.
- The AI MUST define a catch-all route (`*`) at the very end of the routing block to pass all unhandled requests to `app.getRequestHandler()`.

**3. Fastify Custom Server Implementation Rules**
- When setting up Fastify, the AI MUST add the following specific dependencies: `fastify`, `fastify-nextjs`, `react`, `react-dom`, and `next`.
- The AI MUST register the `fastify-nextjs` plugin using `fastify.register(require('fastify-nextjs'))`.
- The AI MUST define Next.js routes inside an `.after()` block following the plugin registration.
- The AI MUST map routes using `fastify.next('/route-path')`.
- The AI MUST NOT manually configure a `/_next/` static asset route in Fastify; the `fastify-nextjs` plugin handles Next.js static assets automatically.

@Workflow

When tasked with creating or modifying a custom Next.js server, the AI must execute the following step-by-step process:

1. **Verify Use Case**: Check if the custom server is necessary (Migration, Multi-tenancy, MVC). If not explicitly stated by the user, briefly advise that standard Next.js routing is preferred unless these conditions are met.
2. **Install Required Packages**: Execute package installation for the target framework (`express` or `fastify` along with `next`, `react`, `react-dom`, and `fastify-nextjs` if applicable).
3. **Initialize App**: Setup the `const dev = process.env.NODE_ENV !== 'production'; const app = next({ dev });` boilerplate.
4. **Prepare Environment**: Wrap the server initialization in an async function and execute `await app.prepare()`.
5. **Configure Framework-Specific Routes**:
   - **For Express**: Implement custom `.get()` routes utilizing `app.render()`. 
   - **For Fastify**: Register the plugin and use `fastify.next()`.
6. **Implement Hydration Failsafe (Express Only)**: Add `server.get(/_next\/.+/, (req, res) => { handle(req, res, parse(req.url, true)); })` to ensure frontend scripts load.
7. **Implement Catch-All**: Route all remaining traffic to the default Next.js handler (`handle(req, res, parsedUrl)`).
8. **Start Listening**: Bind the server to the target port (default `3000`).

@Examples (Do's and Don'ts)

**Express Asset Routing**
- [DO] Explicitly route `_next/` assets so React hydration works perfectly.
```javascript
const { parse } = require('url');
const express = require('express');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });

async function main() {
  await app.prepare();
  const handle = app.getRequestHandler();
  const server = express();

  // Custom route mapping
  server.get('/about', (req, res) => {
    const { query } = parse(req.url, true);
    app.render(req, res, '/about', query);
  });

  // CRITICAL: Handle Next.js static assets
  server.get(/_next\/.+/, (req, res) => {
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  });

  // Catch-all
  server.get('*', (req, res) => {
    const url = parse(req.url, true);
    handle(req, res, url);
  });

  server.listen(3000, () => console.log('server ready'));
}
main();
```

- [DON'T] Define custom routes without protecting the `_next/` path, which causes a blank page.
```javascript
// ANTIPATTERN: Missing _next/ asset handler
async function main() {
  await app.prepare();
  const handle = app.getRequestHandler();
  const server = express();

  server.get('/about', (req, res) => {
    app.render(req, res, '/about', req.query);
  });

  // Requests to /_next/main.js will fail or fall through incorrectly here
  server.get('*', (req, res) => {
    handle(req, res, parse(req.url, true));
  });
}
```

**Fastify Implementation**
- [DO] Use the official `fastify-nextjs` plugin to simplify custom server logic.
```javascript
const fastify = require('fastify')();

fastify
  .register(require('fastify-nextjs'))
  .after(() => {
    // Maps standard Next.js pages seamlessly
    fastify.next('/');
    fastify.next('/about');
    fastify.next('/greet/:user');

    // Define custom Fastify routes alongside Next.js
    fastify.get('/api/custom', (req, reply) => {
      reply.send({ hello: 'world' });
    });
  });

fastify.listen(3000, () => {
  console.log('Server listening on http://localhost:3000');
});
```

- [DON'T] Manually try to implement the Next.js request handler inside Fastify routes using Express-like syntax.
```javascript
// ANTIPATTERN: Treating Fastify like Express
const fastify = require('fastify')();
const next = require('next');
const app = next({ dev: true });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  fastify.get('*', (request, reply) => {
    // This will cause compatibility and performance issues in Fastify
    handle(request.raw, reply.raw); 
  });
});
```