**@Domain**
These rules trigger whenever the AI is tasked with designing a new software architecture, selecting or recommending an architecture style, planning an architectural migration, or performing architectural trade-off analysis for a specified problem domain.

**@Vocabulary**
- **Architecture Style**: The overarching structure defining how the user interface, backend source code, and data stores are organized and partitioned.
- **Domain/Architecture Isomorphism**: The degree to which the topological shape of an architecture naturally maps to the shape of the problem domain (e.g., highly customizable domains naturally map to Microkernel architectures).
- **Architecture Quantum**: An independently deployable artifact with high functional cohesion and synchronous connascence. The scope of a single set of architecture characteristics; dictates whether a system should be a monolith (single quantum) or distributed (multiple quanta).
- **Backends for Frontends (BFF)**: An architecture pattern where an API layer acts as a thin adaptor that translates generic backend information into specific formats, paginations, and latencies expected by specific frontend devices (e.g., iOS, web).
- **Synchronous Communication**: A communication style where the calling service waits for a response from the receiving service.
- **Asynchronous Communication**: A communication style (often utilizing message queues or events) that provides unique benefits in performance and scale but introduces complexities like data synchronization, deadlocks, race conditions, and debugging difficulty.
- **Fitness Functions**: Automated mechanisms designed to protect and verify important architectural principles and operational characteristics over time.

**@Objectives**
- Achieve the "least worst" architectural design by objectively balancing trade-offs rather than attempting to discover a flawless, universal solution.
- Base architectural choices on rigorous criteria including domain characteristics, data architecture, organizational constraints, and team maturity.
- Scope architecture characteristics accurately using Quantum analysis to make informed monolithic versus distributed decisions.
- Produce comprehensive architectural outputs including topology, Architecture Decision Records (ADRs), and fitness functions.

**@Guidelines**
- **Evaluate Shifting Fashions Systematically**: The AI MUST NOT blindly adopt the newest technology trend. Instead, the AI MUST evaluate architecture styles based on observations from past experiences, changes in the ecosystem, new paradigm-shifting capabilities (e.g., containers), domain changes, technology changes, and external factors (e.g., licensing costs).
- **Assess Comprehensive Decision Criteria**: Before selecting a style, the AI MUST analyze:
  - The problem domain (especially aspects impacting operational characteristics).
  - Architecture characteristics required to support the domain.
  - Data architecture impacts (especially when integrating with legacy data).
  - Organizational factors (budget, cloud vendor costs, pending mergers/acquisitions).
  - Team processes, maturity in Agile engineering practices, and operational interaction.
- **Leverage Domain/Architecture Isomorphism**: The AI MUST match the problem domain's natural shape to the architecture's topological shape. (e.g., Use Microkernel for customizability; Use Service-Based for domains with heavy semantic coupling; Avoid Microservices for highly coupled multi-page sequential workflows).
- **Perform Quantum Analysis**: The AI MUST determine if a single set of architecture characteristics suffices for the entire system (yielding a Monolith) or if different parts of the system require differing characteristics (yielding a Distributed architecture).
- **Determine Data Locations**: The AI MUST explicitly decide where data will live. For monoliths, this typically means a single relational database. For distributed architectures, the AI MUST decide which services persist data and how data flows across the system.
- **Apply the Communication Default Rule**: The AI MUST default to synchronous communication between services to minimize design, implementation, and debugging challenges. The AI MUST use asynchronous communication ONLY when explicitly necessary (e.g., to accommodate buffering between services with vastly different operational speeds or elasticity requirements).
- **Design for Differing Operational Characteristics**: If distinct user roles or components require conflicting characteristics (e.g., an Auctioneer needing high reliability vs. Bidders needing high elasticity), the AI MUST isolate them into separate services/quanta using a distributed architecture (e.g., Microservices).
- **Align Data with Domain in Monoliths**: When designing a Modular Monolith, the AI SHOULD recommend separating database tables and assets to match domain components, easing future migration to a distributed architecture if required.
- **Define Output Artifacts**: The final architectural design MUST yield three things: the architecture topology, Architecture Decision Records (ADRs) capturing the hardest trade-offs, and defined architecture fitness functions to govern the structure.

**@Workflow**
1. **Context & Ecosystem Analysis**: Evaluate the business context, budget, existing team maturity, and external organizational constraints. Note any historical pain points or licensing restrictions.
2. **Architecture Characteristics Discovery**: Identify the primary explicit and implicit architecture characteristics required by the domain.
3. **Quantum Mapping**: Group the identified components by their required architecture characteristics. Determine if the system resolves to a single quantum or multiple distinct quanta.
4. **Style Selection**:
   - If Single Quantum + low budget/complexity: Select a Monolithic style (e.g., Modular Monolith or Microkernel).
   - If Multiple Quanta + differing operational characteristics: Select a Distributed style (e.g., Microservices or Event-Driven).
5. **Isomorphism Validation**: Check the selected style against the domain shape. Ensure no excessive semantic coupling spans across highly decoupled service boundaries.
6. **Data & Communication Design**: Map out where databases will reside. Define all inter-service communication as synchronous by default, identifying specific bottlenecks that mandate asynchronous message queues.
7. **Artifact Generation**: Generate the final topology diagram/description. Draft ADRs explaining the "Why" behind the chosen style and communication methods. Formulate fitness functions to protect the design (e.g., restricting cross-domain database access).

**@Examples (Do's and Don'ts)**

- **Choosing Monolith vs. Distributed**
  - [DO]: Design a Modular Monolith for a standard retail sandwich shop application where all operations (ordering, promotions, delivery) share the same basic availability and scale requirements, maintaining a single quantum.
  - [DON'T]: Force a highly decoupled Microservices architecture onto a system that shares a single set of architecture characteristics and has a low budget, merely because Microservices is a current industry trend.

- **Applying Domain/Architecture Isomorphism**
  - [DO]: Select a Microkernel architecture using a core system and specialized plug-ins when the requirements demand extensive local, regional, or client-specific customizations.
  - [DON'T]: Choose a highly decoupled distributed architecture for an insurance application that consists of deeply intertwined, sequential, multi-page data collection forms.

- **Handling Communication Styles**
  - [DO]: Use synchronous communication by default for a standard data retrieval request between a User interface and a Profile service.
  - [DON'T]: Introduce asynchronous communication everywhere. Do not use async for simple operations, thereby unnecessarily introducing data synchronization, race conditions, and debugging nightmares.

- **Handling Conflicting Operational Characteristics**
  - [DO]: Use asynchronous message queues as buffers between a high-volume, highly elastic `BidTracker` service and a slower, heavily constrained third-party `Payment` service to prevent timeouts and dropped requests.
  - [DON'T]: Use synchronous communication to tie a highly scalable web-facing component directly to a slow, rate-limited backend system, which would cause the entire architecture to fail under load.

- **Designing Frontend Integrations**
  - [DO]: Implement the Backends for Frontends (BFF) pattern to adapt a generic backend API into specialized, high-performance payloads tailored for native iOS, Android, and Web interfaces.
  - [DON'T]: Force all varied mobile and web clients to consume a single, massive, generic API payload that wastes bandwidth and requires heavy client-side processing.