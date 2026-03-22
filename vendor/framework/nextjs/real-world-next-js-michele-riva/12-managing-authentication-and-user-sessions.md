# @Domain
These rules apply to Next.js applications implementing user authentication, session management, API route security, and protected content. They MUST be activated whenever the AI encounters or generates tasks involving login/registration flows, JSON Web Tokens (JWT), session cookies, authentication hooks, Next.js API routes handling user credentials, or integration with Identity-as-a-Service providers (such as Auth0, NextAuth.js, or Firebase).

# @Vocabulary
- **Authentication:** The process of identifying a specific user, granting them appropriate read/write/delete permissions based on authorization level (e.g., Credentials-based, Social login, Passwordless/Magic link, SSO).
- **Session:** The mechanism used to remember an authenticated user across page changes so they do not have to re-authenticate.
- **Stateful Session:** A session where the user state is kept on the server-side and linked to the client via a session cookie (e.g., PHP `$_SESSION`). Unsuitable for serverless Next.js deployments.
- **Stateless Session:** A session where user state is kept on the client (typically via a JWT) and sent to the server on every request. Ideal for serverless Next.js deployments.
- **JWT (JSON Web Token):** An RFC 7519 open standard for representing claims securely between two parties. Composed of a Header, Payload, and Signature.
- **Payload:** The second chunk of a JWT containing non-sensitive user data and claims (e.g., `sub`, `aud`, `exp`).
- **Signature:** The third chunk of a JWT that ensures the token has not been tampered with. It is generated using a secret key strictly kept on the server.
- **httpOnly Cookie:** A cookie flag that prevents client-side JavaScript from accessing the cookie, mitigating Cross-Site Scripting (XSS) attacks.

# @Objectives
- ALWAYS prioritize managed, industry-standard authentication providers (e.g., Auth0) over custom-built authentication systems to ensure maximum security.
- ENFORCE stateless session management (JWTs) to ensure compatibility with serverless hosting environments like Vercel.
- PREVENT sensitive data exposure by strictly forbidding the storage of JWTs or authentication tokens in vulnerable client-side storage mechanisms.
- SECURE Next.js API routes by explicitly validating HTTP methods and user input payloads.
- IMPLEMENT seamless client-side protected routes that handle loading states, authenticated redirects, and unauthenticated fallbacks without exposing private content to search engine spiders.

# @Guidelines

## Architecture and Provider Selection
- The AI MUST default to recommending and implementing established Identity-as-a-Service (IDaaS) providers (e.g., Auth0) for production applications. Custom authentication SHOULD ONLY be implemented for learning purposes or when explicitly mandated by the user.
- The AI MUST utilize stateless sessions (JWTs) for Next.js applications. Stateful server-side sessions MUST NOT be used due to serverless function lifecycle limitations.
- When generating private routes (user settings, dashboards), the AI MUST prioritize security over SEO. Server-side rendering (SSR) via `getServerSideProps` is preferred for private routes to validate authentication before rendering, hiding the API call from the frontend.
- When rendering partially public pages (e.g., a blog post where only authenticated users can comment), the AI MUST use Static Site Generation (SSG) for SEO and render the authenticated components dynamically on the client side.

## Security Constraints and Anti-Patterns
- **JWT Payload Constraint:** The AI MUST NEVER place passwords, bank details, or highly sensitive private information inside a JWT payload. The payload is easily decodable by anyone.
- **Client-Side Storage Anti-Pattern:** The AI MUST NEVER store JWTs, session tokens, or authentication credentials in `localStorage`, `sessionStorage`, or `indexedDB`. Doing so exposes the application to XSS attacks.
- **Cookie Constraint:** The AI MUST ALWAYS store JWTs in cookies utilizing the `httpOnly: true` and `path: '/'` flags to ensure the token is inaccessible to client-side scripts.
- **Environment Variable Constraint:** The AI MUST NEVER hardcode authentication secrets, API keys, or provider configurations in the source code. They MUST be placed in a `.env.local` file. The AI MUST ensure `.env.local` is added to `.gitignore`.

## Custom Authentication Implementation Rules
- **API Method Filtering:** Every Next.js API route handling authentication MUST explicitly check and restrict the `req.method` (e.g., enforcing `POST` for logins). If the method does not match, the AI MUST return a `404` status code.
- **Input Validation:** API routes MUST validate the presence of required fields (e.g., `email`, `password`). If missing, the AI MUST return a `400` status code with an error message.
- **Credential Failure:** If authentication fails, the AI MUST return a `401` status code (Unauthorized).
- **Token Generation:** The AI MUST use the `jsonwebtoken` package to sign tokens and the `cookie` package (specifically the `serialize` function) to set the `Set-Cookie` header.

## Auth0 Implementation Rules
- The AI MUST use the official `@auth0/nextjs-auth0` SDK.
- The AI MUST create the catch-all API route exactly at `pages/api/auth/[...auth0].js` and export `handleAuth()`.
- The AI MUST wrap the application in `<UserProvider>` within `pages/_app.js`.
- The AI MUST utilize the `useUser()` hook in client components to extract `user`, `error`, and `isLoading` states.

# @Workflow

## Workflow: Implementing Auth0 Authentication
1. **Dependency Installation:** Ensure `@auth0/nextjs-auth0` is installed.
2. **Environment Configuration:** Create a `.env.local` file generating/defining `AUTH0_SECRET`, `AUTH0_BASE_URL`, `AUTH0_ISSUER_BASE_URL`, `AUTH0_CLIENT_ID`, and `AUTH0_CLIENT_SECRET`.
3. **API Route Setup:** Create `pages/api/auth/[...auth0].js` and export `handleAuth()` to automatically generate `/api/auth/login`, `/api/auth/callback`, `/api/auth/logout`, and `/api/auth/me`.
4. **App Wrapping:** Open `pages/_app.js` and wrap the `<Component />` in `<UserProvider>`.
5. **Component Consumption:** In target pages, import `useUser` from `@auth0/nextjs-auth0`.
6. **State Handling:** Handle `isLoading` (render loading state), `error` (render error), and conditionally render content based on the presence of the `user` object. Provide links to `/api/auth/login` and `/api/auth/logout`.

## Workflow: Implementing Custom JWT Authentication
1. **Dependency Installation:** Ensure `jsonwebtoken` and `cookie` are installed.
2. **JWT Utility Creation:** Create a `lib/jwt.js` file with `encode` and `decode` functions using `jwt.sign` and `jwt.verify`.
3. **Login API Route:** Create `pages/api/login.js`.
   - Restrict to `POST` method.
   - Validate `email` and `password` presence.
   - Authenticate user against data source.
   - Generate JWT via `encode`.
   - Use `serialize` from `cookie` to set `httpOnly: true` cookie.
   - Return `200` success JSON.
4. **Session Retrieval API Route:** Create `pages/api/get-session.js`.
   - Restrict to `GET` method.
   - Parse incoming cookies using `parse` from `cookie`.
   - Decode JWT and return user session data.
5. **Custom Auth Hook:** Create `lib/hooks/auth.js` exporting `useAuth()`.
   - Use `useState` for `loggedIn`, `user`, `loading`, and `error`.
   - Use `useEffect` to fetch `/api/get-session` and update state.
6. **Client-Side Protection:** In protected pages, call `useAuth()`.
   - Render loading indicator while `loading` is true.
   - If `!loading && !loggedIn`, use `next/router` to `router.push('/login')`.
   - Render protected content if `loggedIn` is true.

# @Examples

## Token Storage
- [DO] Store JWTs securely in an HTTP-only cookie during API responses.
```javascript
import { serialize } from 'cookie';
import { encode } from '../../lib/jwt';

export default function handler(req, res) {
  // ... authentication logic ...
  const token = encode({ id: user.id, email: user.email });
  
  res.setHeader('Set-Cookie', serialize('my_auth', token, { 
    path: '/', 
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production'
  }));
  return res.status(200).json({ success: true });
}
```

- [DON'T] Return the token to the client to be stored in localStorage.
```javascript
// ANTI-PATTERN: Exposes token to XSS attacks
export default function handler(req, res) {
  // ... authentication logic ...
  const token = encode({ id: user.id, email: user.email });
  
  // NEVER send the raw token to be saved in localStorage on the frontend
  return res.status(200).json({ success: true, token: token }); 
}
```

## API Route Filtering and Validation
- [DO] Filter HTTP methods and validate required parameters.
```javascript
export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(404).end();
  }

  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Missing required params' });
  }

  // ... proceed with authentication
}
```

- [DON'T] Process requests without checking the method or validating the payload.
```javascript
// ANTI-PATTERN: Accepts GET requests and crashes if body is missing
export default function handler(req, res) {
  const { email, password } = req.body;
  const user = authenticateUser(email, password);
  // ...
}
```

## Client-Side Protected Route Logic
- [DO] Wait for the loading state to finish before checking auth and redirecting.
```javascript
import { useRouter } from 'next/router';
import { useAuth } from '../lib/hooks/auth';

export default function ProtectedRoute() {
  const router = useRouter();
  const { loading, error, loggedIn } = useAuth();

  // Wait for loading to finish before making redirect decisions
  if (!loading && !loggedIn) {
    router.push('/login');
    return null; // Prevent rendering anything while redirecting
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p>An error occurred.</p>;

  return (
    <div>
      <h1>Protected Route</h1>
      <p>Only visible to authenticated users.</p>
    </div>
  );
}
```

- [DON'T] Redirect immediately without accounting for the asynchronous loading state.
```javascript
// ANTI-PATTERN: Will redirect the user to login immediately because loggedIn is initially false
export default function ProtectedRoute() {
  const router = useRouter();
  const { loggedIn } = useAuth();

  if (!loggedIn) {
    router.push('/login');
  }

  return <div><h1>Protected Route</h1></div>;
}
```