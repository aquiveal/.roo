@Domain
These rules are triggered when the AI is tasked with system architecture design, service boundary definition, API design, deployment pipeline configuration, organizational team structure alignment, database modeling, or decoupling interdependent systems.

@Vocabulary
- **Convex Returns**: A condition where the economic return of rapid adaptation and software change exponentially outweighs the effort required.
- **Decision Loop (OODA/Deming)**: The cycle of Observe, Orient/Decide, and Act. The primary constraint on an organization's ability to adapt.
- **Thrashing (Porpoising)**: An organizational anti-pattern where development direction shifts faster than feedback is received from the environment, causing unfinished work and lost productivity.
- **Platform Team**: A team that treats application developers as customers, providing self-service APIs and tools for infrastructure provisioning, rather than doing the operations work themselves.
- **DevOps Team (Fallacy)**: An anti-pattern where a team is inserted as a middleman between Dev and Ops. True DevOps integrates the two; a dedicated team should only exist for platform tooling or cultural evangelism.
- **Service Extinction**: The necessary evolutionary practice of deleting unsuccessful or redundant services rather than merging them into a single complex monolith.
- **Two-Pizza Team**: A small, self-sufficient team containing all necessary disciplines (Dev, UI, DBA, Ops) to eliminate external dependencies and queuing delays.
- **Coordinated Deployment**: An anti-pattern where the provider and consumer of an interface must be deployed simultaneously.
- **Evolutionary Architecture**: Architecture that supports incremental, guided change across multiple dimensions.
- **Bad Layering**: An anti-pattern where horizontal layers (e.g., UI, Controller, DTO, DB) are strictly coupled to a single domain concept, requiring cascading changes across all layers for a single feature.
- **Component-Based Architecture (Self-Contained Systems)**: Vertical architectural slices where a component owns its entire stack, from database to UI/API.
- **Loose Clustering**: A deployment state where instances lack differentiated roles, do not hard-code peer identities, and can be added/removed without manual cluster reconfiguration.
- **Explicit Context**: Using full URLs or rich data structures instead of bare identifier strings to decouple services from implicit knowledge of authority providers.
- **Modular Operators**: Six techniques to create architectural options: Splitting, Substituting, Augmenting, Excluding, Inversion, and Porting.
- **URL Dualism**: The property of a URL serving both as an opaque identifier string and as a resolvable pointer to a representation of an entity.
- **Plurality (Federated Zones of Authority)**: Rejecting the "Single System of Record" for abstract nouns (e.g., "Customer") and allowing different bounded contexts to own their distinct facets of the data.
- **Concept Leakage**: Exposing internal data modeling complexities (e.g., "price point") to downstream systems that only require the resolved attribute (e.g., "price").

@Objectives
- Architect systems to be inherently antifragile by enabling incremental, evolutionary changes.
- Eliminate cross-team deployment coordination by designing backward-compatible, decentralized services.
- Prevent architectural "Big Balls of Mud" by favoring small, explicitly bounded, and easily disposable services.
- Decouple data authority and context using URL dualism and federated data ownership.
- Empower autonomous "two-pizza" teams by shifting operations to self-service platforms rather than gatekeeping ticket queues.

@Guidelines

**Process & Organization**
- The AI MUST evaluate the cycle time versus feedback rate before recommending sweeping architectural changes to avoid Thrashing.
- The AI MUST NOT design processes that require a "DevOps Team" to manually execute deployments; it MUST design self-service platforms for developers.
- The AI MUST advocate for Service Extinction: when comparing two overlapping services, recommend shutting down the less successful one rather than merging them into a highly complex, generalized monolith.
- The AI MUST aggressively flag and eliminate Coordinated Deployments. If a provider and consumer require simultaneous updates, the AI MUST redesign the interface to be backward-compatible or versioned.

**System Architecture**
- The AI MUST NOT utilize traditional layered architectures (UI -> Logic -> DB) if it causes "Bad Layering" (e.g., generating `UserUI`, `UserController`, `UserDTO`, `UserDAO` simultaneously). The AI MUST translate concepts at boundaries (e.g., a domain concept becomes pure data/rows in persistence).
- The AI MUST promote Component-Based Architecture where each module/service owns its complete vertical stack.
- The AI MUST ensure microservices remain strictly scoped; the codebase should be small enough to fit entirely within a single developer's working memory.
- The AI MUST apply the "Principle of Ignorance" in Loose Clustering: instances MUST NOT be statically configured with the IPs or identities of peer instances. Use runtime discovery or load-balanced DNS.
- The AI MUST leverage Modular Operators (Splitting, Substituting, Augmenting, Excluding, Inversion, Porting) when asked to refactor or extend an existing architecture. For example, use Inversion to pull scattered A/B testing logic into a dedicated, top-level routing service.

**Information Architecture & Data**
- The AI MUST use URLs as Explicit Context for identifiers across service boundaries. The AI MUST NOT use bare integer or UUID strings if the caller must infer which system holds the data.
- The AI MUST NOT rely on an `owner_id` (e.g., coupling to an Active Directory account) to establish resource ownership. Services MUST generate their own unique identifiers (or URLs) and force the caller to keep track of the mapping.
- The AI MUST map events and messages to open formats (JSON, self-describing structures) and MUST NOT generate code tightly bound to rigid schemas or object annotations that hinder long-term versioning.
- The AI MUST prevent Concept Leakage: when designing data payloads for downstream systems, flatten internal abstractions (e.g., pricing tiers) into the exact attributes the downstream system needs.
- The AI MUST reject the "Single System of Record" for broad nouns. The AI MUST split entities based on consuming domain needs (e.g., Support Customer vs. Sales Customer).

@Workflow
When analyzing, refactoring, or designing system architecture, the AI MUST follow this algorithmic process:

1. **Autonomy & Coupling Check**:
   - Analyze dependencies for any Coordinated Deployment risks.
   - Verify that the architecture enables "two-pizza" teams to ship without waiting for DBA, Ops, or QA ticket queues.
2. **Evolutionary Architecture Assessment**:
   - Check for horizontal "Bad Layering" across domains. Refactor into vertical, Self-Contained Systems.
   - Apply Modular Operators to identify extension points (Can a module be Excluded? Substituted? Split?).
3. **Cluster & Component Review**:
   - Ensure the system employs Loose Clustering (no peer-to-peer hardcoding, independent scaling).
   - Evaluate services for Extinction. If multiple overlapping features exist, prepare a plan to delete the weakest rather than maintaining both indefinitely.
4. **Information Architecture Modernization**:
   - Replace bare string IDs with URLs (Explicit Context / URL Dualism).
   - Shift identifier generation to the service providing the resource, eliminating `owner_id` coupling.
   - Flatten outgoing data structures to prevent Concept Leakage.
5. **Platform & Automation Alignment**:
   - Confirm that deployment relies on Canary or Blue/Green techniques acting as governors, rather than manual gatekeeping.

@Examples (Do's and Don'ts)

**Explicit Context & URL Dualism**
- [DO]: Pass identifiers as resolvable locations: `{"product_id": "https://catalog.internal/items/029292934"}`
- [DON'T]: Pass bare strings that require implicit knowledge of the provider: `{"product": "029292934"}`

**Service Identifiers & Ownership**
- [DO]: A reporting service generates a report and returns `{"report_url": "https://reports/66abc"}`. The caller maps its user to this URL.
- [DON'T]: A reporting service requires the caller to send `{"owner_id": "user_123"}` and locks the report strictly to an external authentication system's ID.

**Avoiding Concept Leakage**
- [DO]: A pricing engine exports data to the web catalog as `{"sku": "123", "price": 0.89}`.
- [DON'T]: A pricing engine forces the web catalog to ingest its internal complexity: `{"sku": "123", "price_point_id": "tier_4_discount", "base": 0.99, "modifier": -0.10}`.

**Bad Layering vs Conceptual Translation**
- [DO]: The domain manages `Customer` logic, the persistence layer maps it strictly to unstructured rows `table_users`, and the UI consumes a completely different `ViewForm` data structure.
- [DON'T]: Creating `CustomerDTO`, `CustomerController`, `CustomerView`, and `CustomerDAO` that all must be modified simultaneously whenever a single field is added.

**Service Extinction**
- [DO]: After running a targeted promotion service and a broad promotion service in parallel, deleting the codebase and retiring the infrastructure of the less profitable service.
- [DON'T]: Diverting resources from the successful service to try to "save" or merge the failing service into a massive `UnifiedPromotions` monolith.

**Coordinated Deployments**
- [DO]: Updating an API provider to support `v2` while leaving `v1` active, allowing the consumer team to update their code next month.
- [DON'T]: Requiring the API provider and the consumer to deploy at 2:00 AM on Sunday together so the system doesn't break.