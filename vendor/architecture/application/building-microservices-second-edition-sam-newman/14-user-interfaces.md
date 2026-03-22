@Domain
These rules MUST trigger when the AI is executing tasks related to designing, structuring, refactoring, or integrating User Interfaces (UIs) in a microservice architecture. This includes frontend-to-backend communication, frontend decomposition, Single-Page Application (SPA) modularization, API Gateway configuration, Backend for Frontend (BFF) implementation, and GraphQL schema design for client consumption.

@Vocabulary
- **Stream-Aligned Team**: A cross-functional team with end-to-end responsibility for the delivery of a single, valuable stream of user-facing functionality (spanning UI, backend, and data).
- **Enabling Team**: A specialized team (e.g., UI design, architecture) that supports stream-aligned teams without acting as a bottleneck or gatekeeper.
- **Monolithic Frontend**: A UI architecture where all state and behavior are defined in a single deployable unit, making calls to backing microservices.
- **Micro Frontend**: An architectural style where independently deliverable frontend applications are composed into a greater whole.
- **Self-Contained System (SCS)**: An autonomous web application with no shared UI, owned by one team, communicating asynchronously.
- **Page-Based Decomposition**: Decomposing a UI by splitting it into independent web pages served by different microservices.
- **Widget-Based Decomposition**: Splicing independently changeable widgets (components) from different microservices into a single screen.
- **Central Aggregating Gateway**: A single server-side proxy that performs call aggregation and filtering for all types of external UIs.
- **Backend for Frontend (BFF)**: A single-purpose aggregating gateway developed and maintained for a specific user interface/client type (e.g., one for Web, one for iOS).
- **GraphQL**: A query language allowing clients to dynamically define, aggregate, and filter exactly what information they need from multiple downstream microservices.

@Objectives
- Eradicate horizontal, siloed architectural layers (e.g., separate "frontend" and "backend" teams) in favor of vertical, business-domain-aligned streams.
- Ensure the UI architecture preserves the independent deployability of underlying microservices.
- Protect client devices (especially mobile) from bandwidth drain, battery drain, and over-fetching by aggregating and filtering data on the server side.
- Prevent integration layers (like API Gateways or BFFs) from becoming bloated, monolithic bottlenecks.
- Maintain cohesion of business capabilities, ensuring logic is not smeared across intermediate gateway layers.

@Guidelines

**1. Ownership and Organizational Alignment**
- The AI MUST align UI components with the backend microservices that support them, grouping them under a single logical domain (Stream-Aligned Team model).
- The AI MUST NOT design horizontal architectures where a single monolithic UI layer sits on top of all microservices unless explicitly constrained to a single-team environment.
- The AI MUST delegate cross-cutting UI consistency concerns (like CSS style guides or shared components) to shared libraries or Enabling Teams, rather than centralizing UI ownership.

**2. Frontend Decomposition Strategies**
- When working with traditional websites, the AI MUST prioritize **Page-Based Decomposition**, routing different URL paths (e.g., `/albums`, `/artists`) to their respective domain microservices.
- When working with Single-Page Applications (SPAs), the AI MUST implement **Widget-Based Decomposition** (Micro Frontends) to prevent SPA framework monoliths.
- The AI MUST implement communication between in-page widgets using decoupled custom browser events. Widgets MUST NOT directly invoke methods on one another.
- The AI MUST strictly monitor and minimize dependency bloat when composing widgets (e.g., preventing the inclusion of multiple versions of React or large duplicated vendor bundles).

**3. Call Aggregation and Filtering**
- The AI MUST implement server-side call aggregation to support client devices with specific constraints (e.g., mobile networks, screen sizes).
- The AI MUST NOT put business logic, call aggregation, or protocol rewriting inside generic, third-party API Gateway products. Keep the pipes dumb and the endpoints smart.
- The AI MUST NOT use a **Central Aggregating Gateway** for multiple disparate client types (e.g., combining Web and Native Mobile aggregations into one gateway).

**4. Backend for Frontend (BFF) Implementation**
- The AI MUST follow the "One experience, one BFF" rule. Create a dedicated BFF for each distinct client experience (e.g., separate BFFs for iOS, Android, and Desktop Web).
- The AI MUST align the deployment and codebase of a BFF with the UI it serves.
- If duplication occurs across multiple BFFs, the AI MUST NOT merge the BFFs. Instead, extract the common business logic into a new, downstream microservice (e.g., a shared `Wishlist` microservice).

**5. GraphQL Usage**
- When using GraphQL to replace BFFs, the AI MUST use it specifically as a call aggregation and filtering mechanism at the perimeter.
- The AI MUST ensure the GraphQL schema is not tightly coupled to the underlying database schemas of the microservices.
- The AI MUST address GraphQL's lack of native HTTP request-level caching by implementing appropriate client-side ID-based caching or specific edge-caching mechanisms.

@Workflow
When tasked with designing, implementing, or refactoring a UI and its integration with microservices, the AI MUST follow this exact sequence:

1. **Analyze Client Constraints**: Identify the devices and users accessing the system (e.g., Web, iOS, third-party API). Identify their specific constraints (screen size, bandwidth, accessibility).
2. **Select UI Decomposition Strategy**:
   - If the application is a standard website: Apply *Page-Based Decomposition*.
   - If the application is an SPA: Apply *Widget-Based Decomposition* (Micro Frontends).
   - If the application is a Native Mobile App: Proceed to backend integration design.
3. **Establish Widget Integration (If SPA)**:
   - Define custom DOM events for inter-widget communication.
   - Audit and deduplicate frontend framework dependencies to prevent page bloat.
4. **Design the Aggregation Layer**:
   - If multiple distinct user experiences exist: Define a dedicated *BFF* for each experience.
   - If the client requires highly dynamic, user-specified payloads: Define a *GraphQL* perimeter.
5. **Enforce Dumb Pipes**: Review all Gateway/BFF configurations. Strip out any domain business logic and push it down to the appropriate backing microservices.
6. **Resolve Duplication**: If multiple BFFs perform the same aggregate downstream calls, generate a specification for a new downstream microservice to encapsulate that specific capability.

@Examples (Do's and Don'ts)

**Principle: Inter-Widget Communication**
- [DO] Use custom browser events to maintain loose coupling between widgets.
  ```javascript
  // Chart Widget
  const event = new CustomEvent('albumSelected', { detail: { albumId: 123 } });
  window.dispatchEvent(event);

  // Recommendation Widget
  window.addEventListener('albumSelected', (e) => {
      fetchRecommendations(e.detail.albumId);
  });
  ```
- [DON'T] Tightly couple widgets by directly importing and invoking their internal methods.
  ```javascript
  // Chart Widget
  import { fetchRecommendations } from '../recommendationWidget';
  function onSelect(albumId) {
      fetchRecommendations(albumId); // VIOLATION: Tight coupling
  }
  ```

**Principle: Backend for Frontend (BFF) Separation**
- [DO] Create distinct, focused BFFs for different client constraints.
  ```text
  /src
    /bff-ios
      package.json (tailored for iOS endpoints)
    /bff-android
      package.json (tailored for Android endpoints)
    /bff-web
      package.json (tailored for Desktop Web)
  ```
- [DON'T] Create a single Central Aggregating Gateway bloated with conditional logic for different clients.
  ```javascript
  function getCustomerDashboard(req) {
      if (req.headers['device'] === 'ios') {
          return buildIosDashboard();
      } else if (req.headers['device'] === 'android') {
          return buildAndroidDashboard();
      } else {
          return buildWebDashboard(); // VIOLATION: Bloated central gateway
      }
  }
  ```

**Principle: Extracting Shared BFF Logic**
- [DO] Extract shared aggregation logic into a domain microservice.
  ```text
  iOS BFF -> calls `Wishlist Microservice`
  Android BFF -> calls `Wishlist Microservice`
  ```
- [DON'T] Share binary libraries containing business logic across BFFs or merge BFFs to DRY up code.
  ```text
  iOS BFF -> uses `shared-wishlist-lib` -> calls Catalog, Customer, Inventory
  Android BFF -> uses `shared-wishlist-lib` -> calls Catalog, Customer, Inventory
  // VIOLATION: Leaks business process into client libraries
  ```

**Principle: Dumb Pipes / Smart Endpoints**
- [DO] Use an API Gateway purely for generic cross-cutting concerns (e.g., SSL termination, rate limiting, authentication).
- [DON'T] Configure an API Gateway (like AWS API Gateway, Kong, or Apigee) to perform protocol translation (SOAP to REST) or complex JSON payload merging for business processes.