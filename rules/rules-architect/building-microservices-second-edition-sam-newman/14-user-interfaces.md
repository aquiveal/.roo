# @Domain
These rules MUST be activated when the AI is presented with tasks, architectural discussions, or code generation requests related to:
- Designing or implementing User Interfaces (UIs) in a microservices environment.
- Integrating frontend applications (web, mobile, desktop, SPAs) with backend microservices.
- Structuring frontend codebases and deployment artifacts (e.g., micro frontends).
- Designing API gateways, call aggregation, filtering, or routing layers for clients.
- Restructuring teams or code ownership models spanning frontend and backend domains.
- Evaluating GraphQL, Backend for Frontend (BFF), or single-page application (SPA) architectures in distributed systems.

# @Vocabulary
- **Monolithic Frontend**: An architecture where all UI state and behavior is defined in a single deployable unit, making calls to backing microservices. Prone to causing organizational silos.
- **Micro Frontends**: An architectural style where independently deliverable frontend applications are composed into a greater whole, allowing different teams to work on and deploy different parts of the frontend independently.
- **Page-Based Decomposition**: Decomposing a web UI by serving different sets of independent web pages from different microservices, relying on native browser navigation.
- **Widget-Based Decomposition**: Decomposing a single screen or SPA into independent widgets provided by different teams, spliced together via client-side or server-side templating.
- **Self-Contained System (SCS)**: An architectural style requiring an autonomous web application with no shared UI, owned by one team, using async communication, and sharing no business code.
- **Stream-Aligned Team**: A cross-functional team with end-to-end responsibility for delivering a slice of user-facing functionality (including both backend services and the UI).
- **Enabling Team**: A cross-cutting specialist team (e.g., UI/UX, accessibility) acting as an internal consultancy to help stream-aligned teams upskill or maintain consistency, rather than hoarding the work in a silo.
- **Central Aggregating Gateway**: A single server-side proxy that performs call filtering and aggregation for all external user interfaces. Highly prone to becoming a delivery bottleneck.
- **Backend for Frontend (BFF)**: A single-purpose aggregating gateway developed for and tightly coupled to a specific user interface (e.g., one for Web, one for iOS), maintained by the same team that builds that UI.
- **GraphQL**: A query language allowing clients to dynamically define exactly what information they want to retrieve, reducing round trips. Acts as an alternative to or implementation of a BFF.
- **Progressive Enhancement / Graceful Degradation**: Web design techniques ensuring pages adapt to device constraints.

# @Objectives
- The AI MUST advocate for UI architectures that preserve and enhance independent deployability and team autonomy.
- The AI MUST actively discourage layered architectures (e.g., dedicated "Frontend" teams separated from "Backend" teams) in favor of vertical, stream-aligned teams.
- The AI MUST optimize client-server network interactions to handle the unique constraints of different devices (mobile vs. web) without polluting backend microservices with client-specific logic.
- The AI MUST decompose frontend monolithic applications using patterns that match backend microservice boundaries.
- The AI MUST ensure that business logic remains inside cohesive microservices and does NOT leak into intermediate aggregation layers (Gateways or BFFs).

# @Guidelines

## Organizational and Team Alignment
- **Enforce Stream-Aligned Ownership**: The AI MUST recommend that the team owning a backend microservice also owns the UI components (micro frontends) that surface its functionality.
- **Avoid Dedicated Frontend Teams**: When users propose a dedicated frontend team to manage an SPA, the AI MUST warn that this causes delivery bottlenecks, handoffs, and silos.
- **Deploy Enabling Teams for Consistency**: To solve UI consistency or specialist scarcity, the AI MUST suggest using Enabling Teams to build shared UI components (e.g., living style guides, Web Components) or act as consultants, rather than taking over feature delivery.

## Frontend Decomposition Patterns
- **Select the Right Decomposition**: 
  - For standard websites, the AI MUST recommend **Page-Based Decomposition** as the default, simplest approach.
  - For rich Single-Page Applications (SPAs), the AI MUST recommend **Widget-Based Decomposition**.
- **Widget Communication**: When widgets within the same UI need to communicate, the AI MUST implement custom browser/DOM events (e.g., `Album Selected` event). The AI MUST NOT use iFrames or tight coupling between widget codebases.
- **Prevent Dependency Bloat**: When using Widget-Based Decomposition, the AI MUST warn about and implement checks for page load size bloat caused by loading multiple versions of frontend frameworks (e.g., multiple React versions).

## Call Aggregation and Gateways
- **Reject Central Aggregating Gateways**: The AI MUST advise against using a single Central Aggregating Gateway for multiple different UI types (e.g., mobile, web, third-party API) to prevent it from becoming a bloated, cross-team bottleneck.
- **Implement Backend for Frontend (BFF)**: The AI MUST recommend the BFF pattern to aggregate calls and tailor payloads for specific client constraints.
- **Enforce "One Experience, One BFF"**: The AI MUST map one BFF to one specific UI experience. If iOS and Android experiences diverge, they MUST have separate BFFs. If they are identical and owned by the same team, they MAY share a BFF.
- **Handle BFF Duplication via Microservices**: If multiple BFFs duplicate the same aggregation logic, the AI MUST NOT extract a shared client library (which causes lockstep deployment coupling). Instead, the AI MUST recommend extracting the shared business logic into a new, downstream microservice (e.g., a dedicated `Wishlist` microservice).

## GraphQL Implementation
- **Use GraphQL for Client-Driven Aggregation**: The AI MAY recommend GraphQL as a BFF implementation to reduce round trips and payload size for constrained devices (like mobile).
- **Address GraphQL Risks**: When proposing GraphQL, the AI MUST explicitly warn about and architect solutions for:
  - Caching difficulties (HTTP caching/CDNs are hard to leverage).
  - Server-side load and rate-limiting complexities due to dynamic, deep queries.
  - The danger of treating microservices merely as CRUD database wrappers.

## Business Logic Placement
- **Keep Pipes Dumb, Endpoints Smart**: The AI MUST ensure that API Gateways and BFFs are used STRICTLY for routing, call aggregation, and payload filtering. The AI MUST NOT place domain/business logic into these layers.

# @Workflow
When tasked with designing or modifying a User Interface architecture connected to microservices, the AI MUST follow this algorithmic process:

1. **Analyze Client Constraints**: Identify the specific devices (web desktop, native mobile app, third-party API) and their constraints (bandwidth, battery, screen real estate, interaction models).
2. **Determine Organizational Mapping**: Assess the team structure. Map end-to-end functionality to stream-aligned teams. If a monolithic frontend team is proposed, challenge it and pivot the design to micro frontends.
3. **Select UI Decomposition Pattern**:
   - If building a document-centric website: Select **Page-Based Decomposition**. Route URLs to respective microservices.
   - If building a highly interactive SPA: Select **Widget-Based Decomposition**. Design a container app and isolated widgets.
   - If legacy or single-team constraint applies: Select **Monolithic Frontend** but isolate backend calls cleanly.
4. **Design the Aggregation Layer**:
   - If multiple distinct clients exist (e.g., Web and Mobile): Instantiate a **Backend for Frontend (BFF)** for each client type.
   - If dynamic client querying is highly prioritized over HTTP caching: Implement **GraphQL** as the BFF layer.
5. **Establish Widget Interaction (If Applicable)**: Define standard custom DOM events for loosely coupled widget-to-widget communication within the browser.
6. **Audit for Logic Leaks**: Review the BFF/Gateway layers. Strip out any domain/business logic and push it down into the respective backend microservices.
7. **Address Consistency**: Define shared assets (Web Components, CSS style guides) to be provided by Enabling Teams to maintain UX consistency across micro frontends.

# @Examples (Do's and Don'ts)

### UI Team Organization
- **[DO]**: Assign a "Customer Profile Team" to own the backend Customer microservice, the database, AND the UI widget/page where the user updates their profile.
- **[DON'T]**: Create a "Frontend Team" that owns the React application and requires tickets to be submitted to a "Backend Team" to add new fields to the API.

### Call Aggregation
- **[DO]**: Create a `Web_BFF` for the browser application and a `Mobile_iOS_BFF` for the iPhone application. Allow the Web team to maintain the Web BFF and the iOS team to maintain the iOS BFF.
- **[DON'T]**: Use a commercial API Gateway product to write custom JSON transformations and business logic scripts to serve both web and mobile from a single layer.

### Frontend Decomposition (Widgets)
- **[DO]**: Build a Shopping Cart widget that independently fetches data from the Cart Microservice. When a user adds an item via the Catalog widget, the Catalog widget emits a `ItemAddedToCart` DOM event, which the Cart widget listens to so it can refresh its state.
- **[DON'T]**: Write a monolithic React state manager (like a global Redux store) that tightly couples the Catalog component's code directly to the Cart component's codebase across team boundaries.

### Handling BFF Duplication
- **[DO]**: Notice that both the `iOS_BFF` and `Android_BFF` are executing the exact same complex logic to aggregate User, Catalog, and Inventory data to create a Wishlist. Extract this logic into a newly deployed `Wishlist_Microservice` that both BFFs simply query.
- **[DON'T]**: Publish a shared `wishlist-aggregator-lib.jar` (or `.npm`) and force both the iOS and Android BFFs to import it, requiring synchronized lockstep deployments when the library updates.

### Using GraphQL
- **[DO]**: Deploy a GraphQL server as a BFF to allow a constrained mobile application to fetch Order, User, and Shipping status in a single query.
- **[DON'T]**: Treat GraphQL as a direct pass-through to databases, bypassing the behavioral logic encapsulated inside the microservices.