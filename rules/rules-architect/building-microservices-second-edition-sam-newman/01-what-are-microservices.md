# @Domain
Trigger these rules when the user requests architectural system design, analysis of monolithic versus microservice approaches, system boundary mapping, service decomposition, or foundational microservice patterns and technology selection.

# @Vocabulary
- **Microservice**: An independently releasable service modeled around a business domain, treated as a black box that hides its internal implementation.
- **Information Hiding**: A software design principle (originated by David Parnas) dictating that internal implementation details must be concealed behind stable, external networked interfaces.
- **Hexagonal Architecture**: A pattern (by Alistair Cockburn) separating internal implementation from external interfaces, allowing a service to be driven by various interaction mechanisms.
- **Independent Deployability**: The ability to deploy a change to a single microservice and release it to users without deploying or altering any other services.
- **Cohesion of Business Functionality**: Grouping code and data based on end-to-end business capabilities rather than technical function (e.g., UI vs. database).
- **Conway's Law**: The principle that organizations design systems mirroring their internal communication structures.
- **Stream-Aligned Team**: A poly-skilled team aligned to a single, valuable stream of work with end-to-end responsibility (from UI to data).
- **Single-Process Monolith**: An architecture where all code is packaged and deployed as a single operating system process.
- **Modular Monolith**: A single-process monolith internally divided into strict, independent modules.
- **Distributed Monolith**: An anti-pattern consisting of multiple services that are highly coupled and must be deployed together in lockstep.
- **Delivery Contention**: The bottleneck that occurs when multiple developers or teams get in each other's way working on the same highly coupled codebase.
- **Bulkhead**: An architectural safety mechanism where service boundaries act to isolate failures and prevent them from cascading across the system.
- **Correlation ID**: A unique identifier passed across distributed service calls to aggregate logs and trace the flow of a single user action.

# @Objectives
- Prioritize independent deployability as the ultimate forcing function for microservice design.
- Map service boundaries exclusively to business domains rather than technical layers.
- Enforce strict state encapsulation; services must own their respective data stores.
- Align technical architecture with organizational structure (stream-aligned teams) to reduce coordination overhead.
- Mitigate distributed system complexity (latency, data consistency, monitoring) proactively in the design phase.
- Treat monolithic architectures as sensible defaults; justify the transition to microservices strictly through solving scaling or delivery contention issues.

# @Guidelines
- **Deployability Constraint**: The AI MUST design services so they can be changed, deployed, and released entirely in isolation. 
- **Database Encapsulation**: The AI MUST NEVER design a system where multiple microservices share the same database. Data sharing MUST occur strictly via network calls (e.g., REST API, message queues).
- **Boundary Definition**: The AI MUST define boundaries using Domain-Driven Design (end-to-end slices of business functionality) and MUST AVOID horizontal layered architectures (e.g., Presentation Layer, Logic Layer, Data Layer).
- **Size Agnosticism**: The AI MUST NOT define microservice boundaries based on lines of code. Size MUST be dictated by cognitive load ("as big as your head") and minimizing the external interface surface area.
- **Incremental Adoption**: When migrating from a monolith, the AI MUST propose an incremental dial-up approach rather than a big-bang rewrite.
- **Organizational Alignment**: The AI MUST design architectures that assume or encourage stream-aligned teams who own UI, application logic, and data for their specific business domain.
- **Technology Heterogeneity**: The AI MAY suggest different technology stacks for different microservices if it solves a specific domain problem (e.g., Graph DB for social connections, Document DB for posts), but MUST warn against the operational cost of "technology overload".
- **Observability Prerequisites**: The AI MUST mandate log aggregation and distributed tracing (using correlation IDs) as prerequisites for any microservice architecture.
- **Data Consistency Constraints**: The AI MUST NOT use distributed transactions. To manage state across services, the AI MUST use sagas and eventual consistency.
- **Startup and Greenfield Constraints**: The AI MUST advise AGAINST microservices for startups, brand-new unproven products, or software deployed directly by customers on their own infrastructure. In these cases, the AI MUST recommend a Single-Process or Modular Monolith.
- **Testing Constraints**: The AI MUST warn against massive end-to-end tests across multiple distributed services and recommend localized contract-driven testing.

# @Workflow
1. **Context Evaluation**: Analyze the user's system requirements, team size, and domain stability. If the domain is highly volatile or the team is very small, output a strong recommendation for a Modular Monolith before proceeding.
2. **Business Domain Mapping**: Identify the core business domains (e.g., Shipping, Inventory, Customer Profile) instead of technical tiers.
3. **Vertical Slicing**: Define the microservice boundaries so that each encapsulates its own UI (where applicable), business logic, and database.
4. **Interface Definition**: Define the external networked endpoints (REST, RPC, streams) using the principle of information hiding. Ensure the interface is as small as possible.
5. **State Isolation Check**: Audit the proposed architecture to ensure absolutely no databases are shared between the defined services.
6. **Observability Integration**: Inject log aggregation sinks and correlation ID passing into the architecture's communication pathways.
7. **Failure Mitigation**: Introduce bulkheads and asynchronous communication patterns where temporal coupling could cause cascading failures.
8. **Team Alignment Mapping**: Explicitly state how stream-aligned teams would map to the proposed service boundaries.

# @Examples (Do's and Don'ts)

## State and Data Ownership
- **[DO]**: Service A (Order Management) needs inventory data. It makes a networked HTTP REST call to Service B (Inventory) to request the current stock levels. Service B queries its own isolated database and returns the result.
- **[DON'T]**: Service A (Order Management) and Service B (Inventory) both establish a direct SQL connection to a shared monolithic relational database to read and write to the `Stock` table.

## Architectural Layering
- **[DO]**: Create a "Customer Profile" microservice that owns the profile UI components, the profile validation logic, and the profile document database.
- **[DON'T]**: Create a "Frontend Service" for all UIs, a "Backend Middleware Service" for all business logic, and a "Database Service" for all storage.

## Deployment Coupling
- **[DO]**: Deploy a new feature to the Shipping microservice on a Tuesday afternoon without coordinating with the Inventory or Order teams, because the API contract remains backward-compatible.
- **[DON'T]**: Require the Shipping, Inventory, and Order services to be deployed simultaneously over the weekend because a shared database schema was modified (Distributed Monolith).

## Observability and Troubleshooting
- **[DO]**: Generate an `X-Correlation-ID` at the initial API Gateway and pass it through the Order, Payment, and Shipping services. Aggregate all logs using this ID to trace the exact lifecycle of the user's request.
- **[DON'T]**: Let each microservice log errors locally with only timestamp information, requiring engineers to manually cross-reference timestamps across four different servers to debug a failed transaction.

## Organizational Alignment
- **[DO]**: Assign a single poly-skilled, stream-aligned team to own the "Customer Recommendations" microservice end-to-end.
- **[DON'T]**: Have a dedicated "Database Admin Team" that must approve and execute all schema changes for all microservices across the entire company.