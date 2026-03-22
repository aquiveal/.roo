# @Domain
Architecture design, configuration management, session state management, load testing, and production readiness for public-facing web applications and distributed systems. Trigger these rules when reviewing system architecture, configuring environment variables, designing load tests, managing user sessions, or troubleshooting high-load/capacity failures.

# @Vocabulary
- **Conway's Law**: The principle that organizations design systems whose structures are copies of the communication structures of those organizations.
- **Active Sessions**: A server-side abstraction representing the state of a user's connection over time, which always lasts longer than the user's actual interaction due to timeouts.
- **Concurrent Users**: The actual number of humans interacting with the system at an exact moment. (Do not confuse with Active Sessions).
- **Session Bloat**: The dangerous accumulation of large datasets (e.g., search results, entire shopping carts) inside in-memory session objects.
- **Session Replication**: The process of serializing and transmitting user sessions to backup servers after every request to allow failover.
- **Polite Traffic**: Traffic that follows expected paths, honors cookies, and respects application flow (typically seen in QA or standard load testing).
- **Hostile Traffic / Noise**: Traffic from scrapers, shopbots, and spiders that ignores `robots.txt`, drops cookies, cloaks IPs/User-Agents, and rapidly polls deep links.
- **Edge Shielding**: Using a Content Delivery Network (CDN) or edge server to enforce cookie policies, throttle requests, and blacklist IPs before they hit application servers.

# @Objectives
- Ensure the application is designed to survive the chaotic, noisy, and hostile environment of production, not just the sanitized environment of Quality Assurance (QA).
- Protect server memory and CPU from session exhaustion caused by bots, search engines, and malicious scrapers.
- Decouple environment-specific configuration from the application codebase to prevent topology mismatches and security leaks.
- Design load tests that simulate real-world chaos, including dropped cookies, random page access, and extreme noise.
- Implement proactive safety devices (throttles, circuit breakers) to prevent thread pile-ups during partial failures.

# @Guidelines

## Configuration & Environment Management
- **Environment Overrides**: The AI MUST isolate environment-specific properties (hostnames, ports, DB passwords) into an override structure separate from the application codebase. 
- **Topology Awareness**: The AI MUST NOT assume production topology matches QA topology. Production configurations must account for clustered instances, load balancers, and internal firewalls.
- **Credential Protection**: The AI MUST explicitly prevent production database passwords from being committed to standard source control or accessible within QA environments.

## Session Management & Memory Protection
- **No Query Parameter Sessions**: The AI MUST strictly forbid the use of URL query parameters for tracking Session IDs. Session tracking MUST rely exclusively on cookies to prevent spidering bots from creating infinite sessions.
- **Require Cookies for State**: The AI MUST route users/bots that drop cookies to a static error page or discard their requests rather than creating infinite unassociated sessions.
- **Never Session 404s**: The AI MUST ensure that requests for missing assets or invalid URLs (404s) DO NOT generate or allocate server-side sessions.
- **Session Size Limits**: The AI MUST store only lightweight identifiers (e.g., User ID, Cart ID) in the session. It MUST NOT store large object graphs, full shopping carts, or search result sets in session state.
- **Disable Replication for Large State**: If the framework forces large object graphs into sessions, the AI MUST disable session replication/serialization to prevent saturating network bandwidth and CPU.

## Load Testing & QA Deficiencies
- **Simulate Hostile Traffic**: The AI MUST generate load testing scripts that simulate hostile behavior: dropping cookies, hitting deep links randomly, ignoring flow, and masking User-Agents.
- **Do Not Trust "Polite" Tests**: The AI MUST NOT rely solely on "happy path" load scripts that follow links sequentially.
- **Test Safety Devices**: The AI MUST test how the system reacts when downstream services slow down. It must verify that safety devices cut off bad situations rather than allowing request threads to pile up and crash the server.

## Performance & Edge Routing
- **Static Defaults for Unauthenticated Users**: The AI MUST generate static, cached versions of expensive landing pages for anonymous users. Do not perform heavy DB transactions (e.g., loading 80+ categories) for users without an identification cookie.
- **Leverage Edge Servers**: The AI MUST design the architecture to push IP blacklisting, traffic throttling, and cookie-enforcement to the CDN or Edge router.

# @Workflow
When tasked with reviewing system readiness, configuring environments, or diagnosing load failures, the AI MUST execute the following algorithmic process:

1. **Topology & Configuration Audit**:
   - Extract all environment variables and configuration files.
   - Verify that configuration uses a level of indirection (overrides) rather than hardcoded QA values.
   - Confirm production secrets are vaulted and excluded from source control.
2. **Session Architecture Review**:
   - Trace the session lifecycle. 
   - Verify that 404 errors and static assets bypass session creation.
   - Audit the session payload: flag any instance where domain objects, lists, or large datasets are written to the session.
   - Verify that session IDs are passed via cookies ONLY, explicitly rejecting URL-rewriting fallbacks.
3. **Edge & Traffic Defense Setup**:
   - Define edge routing rules (CDN/Load Balancer) to drop or redirect requests missing required cookies.
   - Implement rate limiters and throttles at the infrastructure edge to shed load before it reaches application instances.
4. **Chaos Load Test Design**:
   - Design standard user journey scripts (searchers, grazers, buyers).
   - Inject "Noise" scripts: randomized deep-link hitting without cookies.
   - Inject "Failure" scenarios: simulate slow downstream DBs to ensure application request threads time out rather than piling up.
5. **Dynamic Content Mitigation**:
   - Identify the most heavily trafficked unauthenticated routes (e.g., Home Page).
   - Convert dynamic DB-driven renders into static or heavily cached endpoints for anonymous traffic.

# @Examples (Do's and Don'ts)

## Session Payload Management
- **[DO]** Store only reference keys in the session, relying on fast secondary caches for the data.
  ```java
  // Correct Session Usage
  session.setAttribute("cartId", userCart.getId());
  session.setAttribute("userId", user.getId());
  ```
- **[DON'T]** Store large data structures or collections in the session, which will crash the server during serialization/failover.
  ```java
  // Anti-pattern: Session Bloat
  session.setAttribute("shoppingCartItems", fullCartObjectGraph);
  session.setAttribute("lastSearchResults", listOf500ProductObjects);
  ```

## Session ID Transmission
- **[DO]** Enforce cookie-only session tracking at the framework level.
  ```xml
  <!-- Correct Configuration (Java Servlet Example) -->
  <session-config>
      <tracking-mode>COOKIE</tracking-mode>
  </session-config>
  ```
- **[DON'T]** Allow URLs to carry session state, which allows search engine spiders to generate thousands of duplicate sessions.
  ```html
  <!-- Anti-pattern: URL Session Rewriting -->
  <a href="/checkout?jsessionid=3498573498573495834">Checkout</a>
  ```

## Edge Defense against Noise
- **[DO]** Block or redirect clients at the CDN/Edge if they refuse to accept cookies, protecting app server RAM.
  ```nginx
  # Correct Edge Configuration (Nginx snippet)
  if ($cookie_sessionid = "") {
      return 302 /enable-cookies.html;
  }
  ```
- **[DON'T]** Route all raw traffic directly to the application server and allow it to blindly allocate memory for every single HTTP request from scraping bots.

## Dynamic Page Generation
- **[DO]** Serve pre-rendered static HTML for the homepage when the user is not authenticated.
  ```javascript
  // Correct Routing
  app.get('/', (req, res) => {
      if (!req.cookies.auth) {
          return res.sendFile('/static/home.html');
      }
      return renderPersonalizedHome(req, res);
  });
  ```
- **[DON'T]** Execute 1000+ database queries to build navigation trees and unpersonalized content for every anonymous scraper hitting the root URL.