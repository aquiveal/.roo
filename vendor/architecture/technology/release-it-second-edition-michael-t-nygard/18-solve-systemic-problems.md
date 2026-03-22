@Domain
These rules activate when designing system architectures, defining microservice boundaries, creating APIs and data contracts, setting up load testing protocols, configuring deployment pipelines (CI/CD), implementing state/session management, and integrating reliability, resilience, and chaos engineering practices into distributed systems.

@Vocabulary
- **Conway's Law**: The principle that systems are constrained to produce designs that are copies of the communication structures of the organizations that build them.
- **OODA Loop / Deming Cycle**: Decision loops (Observe, Orient, Decide, Act) governing the speed of adaptation.
- **Thrashing (Porpoising)**: Changing organizational or system direction faster than feedback can be received from the environment, leading to lost productivity.
- **Platform Team**: A team that treats application developers as its customers, providing self-service APIs and command-line provisioning for infrastructure, as opposed to a siloed "DevOps Team" that executes deployments.
- **Canary Deploy**: Releasing new code to a single or small subset of instances to evaluate health before full rollout.
- **Blue/Green Deploy**: Releasing to an inactive pool of machines, then shifting traffic over via load balancers.
- **Service Extinction**: The deliberate deletion and shutdown of less successful services to free up capacity and eliminate dependencies.
- **Two-Pizza Team**: A cross-functional, autonomous team small enough to be fed by two pizzas, designed to minimize external dependencies and eliminate coordinated deployments.
- **Evolutionary Architecture**: Architectures that support incremental, guided change across multiple dimensions (e.g., component-based, self-contained systems, event-based).
- **Loose Clustering**: A principle where clustered instances share no specific dependencies on or knowledge of peer identities, relying instead on virtual IPs, DNS, and runtime discovery.
- **Explicit Context (URL Dualism)**: Using full URLs as identifiers that carry both opaque token value and resolvable context, replacing bare database IDs.
- **Modular Operators**: Six techniques to create architectural options: Splitting, Substituting, Augmenting, Excluding, Inversion, and Porting.
- **Event Sourcing & CQRS**: Treating events as the primary, persistent source of truth, and separating command structures from read-optimized views (CQRS).
- **Concept Leakage**: Forcing consumers to understand internal system optimizations or constructs (e.g., an internal "price point" ID) rather than providing flattened, consumer-focused data.
- **Chaos Engineering**: The empirical discipline of experimenting on a distributed system to build confidence in its capability to withstand turbulent conditions.
- **Drift into Failure**: The tendency of systems to be optimized for throughput and efficiency until they drift too close to safety boundaries and fail catastrophically.
- **FIT (Failure Injection Testing)**: Tagging requests to automatically fail downstream (e.g., simulating latency or HTTP 500s) to validate fallbacks.
- **Blast Radius**: The magnitude of bad experiences and number of customers affected by a failure or a chaos experiment.

@Objectives
- Optimize systems for adaptation, evolutionary change, and survivability over raw efficiency or throughput.
- Eliminate horizontal coupling across architectural layers; favor vertical, self-contained components that isolate failure domains.
- Achieve team-scale autonomy by decoupling services so that coordinated, simultaneous deployments across teams are never required.
- Maintain production-level SLAs for development, QA, and build pipeline infrastructure.
- Validate system resilience empirically by continuously injecting realistic turbulence (noise, bad bots, latency, instance death) rather than testing only the "happy path."
- Architect data and integration points to prevent internal concept leakage and to embrace federated zones of authority instead of single "Systems of Record."

@Guidelines

# Architecture and Adaptation
- **Minimize Horizontal Coupling**: Do not build applications where a single change requires modifying the UI, Controller, DTO, Domain, and Database layers simultaneously. Rotate boundaries to create vertical, self-contained components.
- **Enforce Loose Clustering**: Ensure instances do not require static IP configuration of peers. Use load balancers, DNS, or runtime service discovery. Ensure instances can start and stop in any sequence.
- **Design for Extinction**: Isolate experimental business logic in separate, disposable services rather than adding conditional bloat to a monolith. When an experiment fails, delete the service completely.
- **Apply Modular Operators**: When refactoring, explicitly consider Splitting (breaking apart), Substituting (swapping implementations), Augmenting (adding), Excluding (removing), Inversion (extracting common logic up a level), and Porting.
- **Avoid Over-Efficiency**: Do not optimize systems or teams to 100% utilization. Highly efficient, tightly coupled pipelines (like physical conveyor belts) break adaptability. Leave slack in the system for change.

# Data and Integration
- **Implement URL Dualism**: Always use full URLs instead of bare string/numeric IDs for resources in JSON payloads. Treat URLs as both opaque tokens to pass forward and addresses to resolve.
- **Services Control Identifiers**: Do not require a caller to pass an "owner ID" to create a resource. The service must issue its own identifier for the resource. Use Policy Proxies to handle authorization mapping externally.
- **Prevent Concept Leakage**: Flatten data on outbound boundaries. Do not export internal modeling hacks (e.g., abstract hierarchies or grouping constructs) to downstream consumers.
- **Embrace Plurality**: Reject the "Single System of Record" fallacy. Accept that "Customer" means different things to Support, Billing, and Sales. Use federated data models connected by common formats.
- **Use Open Formats for Events**: When implementing Event Sourcing, use open, schema-less formats (like JSON). Avoid rigid, code-generated formats that break when replaying historical data.

# Load Testing and State Management
- **Simulate Real-World Turbulence**: Load tests MUST include malformed inputs, missing cookies, SEO bot scraping, session hijack attempts, and erratic user flows. Do not only script the "happy path."
- **Minimize Session State**: Never serialize large data structures (like full search result sets or shopping carts) into session memory. Sessions must be lightweight keys.
- **Implement Boundary Defenses**: Provide static fallback pages and CDN-level throttles to protect application servers when session limits are breached.
- **Assume Unpredictable Scaling**: Design the system to handle spikes by aggressively throttling or rejecting requests at the edge (API Gateway/CDN) before they consume application threads.

# Deployment and Operations
- **Development is Production**: Treat version control, CI/CD, and QA environments as production systems with strict SLAs. If developers cannot deploy, the system is down.
- **No Coordinated Deployments**: If a deployment requires updating a consumer and a provider simultaneously, the architecture is broken. Always implement backward/forward compatibility.
- **Platform over Silo**: Build self-service APIs and deployment pipelines (Platform) for developers. Do not use a human "DevOps Team" as a gatekeeper for running deployment scripts.
- **Govern Deployments**: Use Canary and Blue/Green deployment patterns to limit the blast radius of bad code. Automatically rollback if metrics degrade.

# Chaos Engineering
- **Define Steady State**: Before injecting chaos, ensure you have accurate metrics defining the normal, healthy state of the system (e.g., successful requests per second, baseline latency).
- **Hypothesize and Contain**: Formulate a specific hypothesis (e.g., "If service A fails, service B will return cached data"). Scope the blast radius to a subset of users or traffic.
- **Inject Latency and Failure**: Do not just kill instances. Use Failure Injection Testing (FIT) to simulate slow network calls, dropped packets, and HTTP 500 errors between internal services.
- **Plan the Revert**: Always have an automated or documented abort switch to immediately stop a chaos experiment and return the system to normal operations.
- **Simulate Human Disaster**: Conduct "zombie apocalypse" simulations where key personnel are unavailable to expose single points of human failure and undocumented operational knowledge.

@Workflow
1. **Architectural Review**: 
   - Analyze dependencies. Are we requiring coordinated deployments? If yes, refactor boundaries to decouple.
   - Check data payloads for bare IDs. Convert bare IDs to full, resolvable URLs.
   - Check outbound payloads for internal concept leakage. Flatten DTOs.
2. **State and Session Audit**:
   - Inspect session object structures. Strip out any large collections. Ensure session tracking relies on cookies/headers, not URL parameters.
3. **Deployment Pipeline Setup**:
   - Validate that infrastructure configurations (dev, QA, production) are codified.
   - Implement Canary or Blue/Green routing logic.
4. **Chaos and Turbulence Testing Planning**:
   - Write load test scripts that intentionally break session rules and hammer deep-links without cookies.
   - Define a Chaos Engineering hypothesis, establish baseline steady-state metrics, define the blast radius, and execute a targeted Failure Injection (FIT) or instance termination.
5. **Observation and Extinction**:
   - Review active microservices or modules. Identify those providing negative convex returns.
   - Execute the "Extinction" protocol: redirect traffic, delete the codebase, and reassign the team.

@Examples (Do's and Don'ts)

# Explicit Context (URL Dualism)
- **[DO]** Return fully qualified URLs that provide context and addressability:
  `{"item": "https://api.example.com/products/849201"}`
- **[DON'T]** Return bare, ambiguous identifiers that force the consumer to guess the provider:
  `{"item": "849201"}`

# Concept Leakage
- **[DO]** Flatten outbound events to reflect business reality for the consumer:
  `{"track_id": "123", "title": "Song", "price": 0.99}`
- **[DON'T]** Force consumers to understand internal optimization schemas:
  `{"track_id": "123", "title": "Song", "price_point_id": "PP-Tier4"}`

# Session Management under Load
- **[DO]** Store only identifiers in the session to minimize memory footprint:
  `Session.set("cart_id", "cart_77382");`
- **[DON'T]** Store large, serialized data structures in the session which will cause memory exhaustion and failover crashes:
  `Session.set("search_results", [...500 items...]);`

# Chaos Engineering
- **[DO]** Run a scoped chaos experiment with FIT headers:
  "Inject a 400ms delay into 5% of requests from the Web API to the Recommendation Service, and verify the Web API returns the default recommendations without timing out."
- **[DON'T]** Randomly reboot database clusters in production without measuring steady-state metrics, defining a hypothesis, or establishing a rollback plan.

# Team and Deployment Structure
- **[DO]** Build an API that allows the Billing Team to automatically provision their own database and CI pipeline.
- **[DON'T]** Create a "DevOps Team" that receives Jira tickets from the Billing Team requesting database schema changes and deployment script execution.