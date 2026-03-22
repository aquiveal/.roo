@Domain
This rule set is activated when the AI is tasked with software architecture design, system analysis, architecture characteristics (non-functional requirements) elicitation, microservices design, migrating from monolithic to distributed architectures, or evaluating system coupling, connascence, and communication styles.

@Vocabulary
- **Architecture Quantum**: An independently deployable artifact with high functional cohesion and synchronous connascence. It is the definitive boundary for scoping architecture characteristics.
- **Connascence**: A measure of coupling where two components are connascent if a change in one requires the other to be modified to maintain overall system correctness.
- **Static Connascence**: Source-code-level coupling (e.g., shared classes or dependencies) discoverable via static code analysis.
- **Dynamic Connascence**: Execution-time coupling between components.
- **Synchronous Connascence**: A form of dynamic connascence where a caller waits for a response from a callee. Components with synchronous connascence share the same operational architecture characteristics for the duration of the call.
- **Asynchronous Connascence**: Fire-and-forget or message-driven communication that allows connected services to differ in operational architecture characteristics.
- **Independently Deployable**: A characteristic of a quantum indicating it includes all necessary dependent components (e.g., databases) to function independently of other parts of the architecture.
- **High Functional Cohesion**: A structural characteristic where a module or quantum is unified in purpose, typically matching a single business workflow or bounded context.
- **Bounded Context**: A concept from Domain-Driven Design (DDD) where everything related to a domain is visible internally but opaque to other contexts.
- **Implicit Architecture Characteristics**: Critical operational or structural requirements rarely specified in formal requirements but derived from domain knowledge (e.g., elasticity during an online auction).
- **Domain/Architecture Isomorphism**: The mapping and differentiation between domain-specific requirements (e.g., "reputation index") and abstract architectural characteristics (e.g., "scalability").

@Objectives
- Redefine the scope of architecture characteristics from the "system level" to the "quantum level" to accommodate modern distributed architectures.
- Identify and isolate Architecture Quanta by evaluating deployability, cohesion, and connascence.
- Enforce the rule that synchronously connected components share the exact same operational architecture characteristics.
- Utilize asynchronous communication to decouple architecture characteristics and solve operational disparities between components.
- Leverage Domain-Driven Design (DDD) bounded contexts to achieve high functional cohesion within quanta.

@Guidelines
- **System vs. Quantum Scoping Constraints**: The AI MUST NOT define operational architecture characteristics (e.g., scalability, availability, performance) globally for an entire distributed system. Characteristics MUST be defined and scoped exclusively at the Architecture Quantum level.
- **Quantum Definition Protocol**: When defining an Architecture Quantum, the AI MUST strictly validate three criteria:
  1. It MUST be independently deployable.
  2. It MUST possess high functional cohesion (unified purpose/bounded context).
  3. It MUST encompass all components tied together via synchronous connascence.
- **Database and Dependency Inclusion**: The AI MUST include external dependent datastores (e.g., databases) inside the boundary of the Architecture Quantum. A system deployed as multiple modules but sharing a single monolithic database MUST be evaluated as a single Architecture Quantum.
- **Synchronous Connascence Penalty**: When the AI designs or encounters synchronous communication between two services, it MUST assign both services the identical operational architecture characteristics (e.g., scalability, reliability) for the duration of the call. If Service A relies on Service B synchronously, Service A can only be as scalable/reliable as Service B.
- **Asynchronous Decoupling Strategy**: If two components require vastly different operational architecture characteristics (e.g., one requires high elasticity, the other processes slowly), the AI MUST mandate asynchronous communication (e.g., message queues) between them to break the synchronous connascence and separate them into different quanta.
- **Domain vs. Architecture Filtration**: When analyzing requirements, the AI MUST filter out domain-specific implementations (e.g., "reputation index") from abstract architecture characteristics (e.g., "scalability", "availability"). Abstract characteristics trigger structural architectural design, while domain features trigger application-level design.
- **Legacy Monolith Assessment**: When evaluating monolithic applications with a single database, the AI MUST classify the entire architecture as a "quantum of one".
- **Hybrid Architecture Justification**: The AI MUST recommend hybrid or highly distributed architectures (like microservices) when the analysis of quanta reveals severely conflicting operational architecture characteristics across different bounded contexts.

@Workflow
1. **Requirements Extraction**: Analyze explicit requirements and derive implicit requirements based on the problem domain's nature (e.g., identifying bursty traffic as "elasticity" rather than just "scalability").
2. **Abstract Characteristic Filtration**: Separate domain-specific implementation details from abstract architecture characteristics.
3. **Component & Bounded Context Mapping**: Group functionalities into highly cohesive bounded contexts (workflows/domains).
4. **Communication & Connascence Analysis**: Map the communication lines between the identified bounded contexts. Explicitly mark every communication path as either *Synchronous* or *Asynchronous*.
5. **Database Boundary Definition**: Assign dependent datastores to their respective bounded contexts. If multiple contexts share a datastore, merge them architecturally for quantum evaluation.
6. **Architecture Quanta Delineation**: Draw architectural boundaries around components that are independently deployable, functionally cohesive, and synchronously connected. 
7. **Characteristics Assignment**: Assign specific operational architecture characteristics (e.g., Performance, Elasticity, Reliability) independently to each identified Architecture Quantum.
8. **Topology Resolution**: Output the final architectural design. If the system resolves to a single quantum, output a monolithic architecture recommendation. If it resolves to multiple quanta with differing characteristics, output a distributed/hybrid architecture recommendation.

@Examples (Do's and Don'ts)

- **[DO] Scope characteristics per quantum.**
  - **Context**: Designing an online auction system.
  - **Design**: The AI identifies the "Bidder Stream" (requires high scalability, elasticity, performance) and the "Auctioneer Capture" (requires high reliability, availability) as two separate architecture quanta, assigning different architectural characteristics to each, and connecting them asynchronously.

- **[DON'T] Apply characteristics system-wide.**
  - **Context**: Designing an online auction system.
  - **Design**: The AI states "The entire system must support high elasticity and real-time performance," forcing backend settlement and payment processing services to be over-engineered to match the frontend bidding requirements.

- **[DO] Unify synchronously coupled services into a single quantum.**
  - **Context**: Service A (Order Placement) calls Service B (Payment Processing) via a synchronous REST API.
  - **Design**: The AI determines that Service A and Service B form a single Architecture Quantum because Service A must wait for Service B. The AI specifies that Service A's scalability is fundamentally limited by Service B's throughput limits.

- **[DON'T] Treat synchronously connected services as independent quanta.**
  - **Context**: Service A calls Service B synchronously.
  - **Design**: The AI declares Service A highly scalable and Service B highly reliable, failing to recognize that Service A will suffer timeouts and reliability failures if Service B cannot scale to meet Service A's synchronous request volume.

- **[DO] Include the database in the quantum boundary.**
  - **Context**: Breaking a monolith into domain services.
  - **Design**: The AI assigns a dedicated database to each domain service (Bounded Context) to ensure they are independently deployable, thereby successfully creating multiple, isolated Architecture Quanta.

- **[DON'T] Ignore database connascence.**
  - **Context**: Microservices architecture sharing a single relational database.
  - **Design**: The AI evaluates the system as having dozens of independent quanta, ignoring the fact that the shared database restricts independent deployability and binds all services into a "quantum of one".