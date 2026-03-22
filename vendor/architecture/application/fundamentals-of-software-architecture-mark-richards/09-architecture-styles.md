# @Domain

This rule file is activated whenever the AI is tasked with software architecture design, system topology analysis, evaluating the transition from monolithic to distributed systems, or addressing integration, networking, and structural trade-offs in software development. It specifically applies when users request structural choices, architecture styles, network communication designs between services, distributed data management, or troubleshooting structural decay in existing systems.

# @Vocabulary

*   **Architecture Style**: The overarching structure of how the user interface and backend source code are organized (e.g., monolithic layers or separately deployed services) and how that source code interacts with a datastore.
*   **Architecture Pattern**: A lower-level design structure that helps form specific solutions within an architecture style (e.g., how to achieve high scalability within a set of services).
*   **Big Ball of Mud**: An architecture anti-pattern characterized by a haphazardly structured, sprawling, sloppy, spaghetti-code jungle with unregulated growth and promiscuous information sharing.
*   **Unitary Architecture**: A historical software structure where software and hardware ran as a single entity (common in embedded systems, rare in modern enterprise software).
*   **Client/Server (Two-Tier)**: An architecture separating presentation logic (desktop or browser) from a separate database or web server.
*   **Three-Tier Architecture**: A distributed structure separating the database tier, application tier, and frontend, historically tied to protocols like CORBA or DCOM.
*   **Monolithic Architecture**: An architecture style defined by a single deployment unit containing all code.
*   **Distributed Architecture**: An architecture style defined by multiple deployment units connected through remote access protocols.
*   **Fallacy of Distributed Computing**: An assumption about distributed systems that is believed to be true but is false, leading to architectural failure.
*   **Stamp Coupling**: A form of coupling where a service returns far more data than the calling service requires, consuming massive bandwidth.
*   **Long Tail Latency**: The 95th to 99th percentile of network response times, which drastically impacts the performance of chained distributed services.
*   **Eventual Consistency**: A data synchronization model used in distributed systems where data processed by separate deployment units will, at some unspecified point, become consistent.
*   **Transactional Sagas**: A method for managing distributed transactions utilizing event sourcing for compensation or finite state machines to manage transaction state.
*   **BASE Transactions**: Basic Availability, Soft state, and Eventual consistency. A technique for distributed transactions, opposing traditional monolithic ACID transactions.

# @Objectives

*   The AI MUST clearly differentiate between high-level Architecture Styles and lower-level Architecture Patterns during system design.
*   The AI MUST prevent the degradation of systems into the "Big Ball of Mud" anti-pattern by enforcing rigid structural boundaries and communication rules.
*   The AI MUST force a rigorous trade-off analysis before recommending a distributed architecture over a monolithic architecture.
*   The AI MUST systematically identify and mitigate all 8 Fallacies of Distributed Computing whenever a distributed architecture style is proposed or analyzed.
*   The AI MUST fundamentally shift transactional strategies from ACID to BASE/Sagas when moving from monolithic to distributed designs.

# @Guidelines

*   **Categorization of Architecture**: The AI MUST classify the proposed architecture as either Monolithic (Layered, Pipeline, Microkernel) or Distributed (Service-Based, Event-Driven, Space-Based, Service-Oriented, Microservices).
*   **Big Ball of Mud Prevention**: The AI MUST reject designs that feature haphazard, duct-tape-and-baling-wire connections without discernible structural boundaries.
*   **Mitigation of Fallacy #1 (Network is Reliable)**: The AI MUST specify the implementation of timeouts and circuit breakers for all inter-service and remote network communications.
*   **Mitigation of Fallacy #2 (Latency is Zero)**: The AI MUST NOT base performance estimates on average latency. The AI MUST calculate or request the 95th to 99th percentile (long tail) latency and evaluate the impact of chaining multiple service calls.
*   **Mitigation of Fallacy #3 (Bandwidth is Infinite)**: The AI MUST aggressively eliminate Stamp Coupling. The AI MUST enforce techniques to pass only minimal required data between services (e.g., using private RESTful API endpoints, field selectors in contracts, GraphQL, value-driven contracts, or consumer-driven contracts).
*   **Mitigation of Fallacy #4 (Network is Secure)**: The AI MUST mandate that every individual endpoint in a distributed deployment unit is secured against unknown or bad requests. The AI MUST NOT rely solely on VPNs or trusted firewalls.
*   **Mitigation of Fallacy #5 & #6 (Topology Never Changes & One Administrator)**: The AI MUST recommend architectural liaisons with operations and network administrators to account for dynamic network upgrades and multiple heterogeneous administrative domains.
*   **Mitigation of Fallacy #7 (Transport Cost is Zero)**: The AI MUST explicitly flag the hidden financial costs of distributed architectures, specifically noting the need for additional hardware, servers, gateways, firewalls, subnets, and proxies.
*   **Mitigation of Fallacy #8 (Network is Homogeneous)**: The AI MUST assume heterogeneous hardware vendors in the network and design for packet loss and interoperability friction.
*   **Distributed Logging Requirements**: When proposing distributed architectures, the AI MUST explicitly dictate the use of log consolidation tools (e.g., Splunk) to prevent the loss of trace-ability across multiple logs.
*   **Distributed Transaction Constraints**: The AI MUST explicitly forbid traditional ACID commits/rollbacks across distributed deployment units. The AI MUST dictate the use of Sagas or BASE transaction techniques for distributed data state.
*   **Contract Management**: The AI MUST establish strict communication models for contract creation, maintenance, and version deprecation between decoupled services.
*   **Historical Tooling Traps**: The AI MUST warn against baking architectural topology assumptions deeply into application code or language features (e.g., avoiding the mistake of Java Serialization which assumed Three-Tier architecture would last forever).

# @Workflow

1.  **Architecture Classification**: Upon receiving a design request, determine if the optimal style is Monolithic or Distributed based on the user's constraints.
2.  **Anti-Pattern Check**: Scan the proposed relationships for unregulated growth, global data sharing, or lack of defined components. If found, explicitly flag as a "Big Ball of Mud" and halt further design until structural boundaries are enforced.
3.  **Distributed Fallacy Application**: If a Distributed Architecture is selected, sequentially process the design through the 8 Fallacies of Distributed Computing:
    *   *Step 3a*: Inject circuit breakers/timeouts (Reliability).
    *   *Step 3b*: Calculate cumulative long-tail latency for chained requests (Latency).
    *   *Step 3c*: Audit data payloads for Stamp Coupling; restrict to essential fields only (Bandwidth).
    *   *Step 3d*: Apply endpoint-level security (Security).
    *   *Step 3e*: Document physical infrastructure cost increases (Transport Cost).
4.  **Operational Mechanisms Definition**: Define the distributed logging consolidation strategy.
5.  **Data Consistency Modeling**: Map out any transactions spanning multiple deployment units and replace any assumed ACID transactions with Sagas or BASE Eventual Consistency patterns.
6.  **Contract Strategy**: Define the exact contract versioning and deprecation strategy for inter-service communication.

# @Examples (Do's and Don'ts)

**Architecture Style vs. Pattern**
*   [DO]: State "We will use a Microservices Architecture Style, and implement the Circuit Breaker Architecture Pattern within inter-service communications."
*   [DON'T]: State "We will use a Circuit Breaker Architecture Style."

**Fallacy #1: Network Reliability**
*   [DO]: "Implement a circuit breaker pattern on Service A so that if Service B is unreachable due to network failure, Service A falls back to a default response rather than hanging."
*   [DON'T]: "Service A will synchronously call Service B to fetch the data." (Assumes network will never fail).

**Fallacy #2: Latency**
*   [DO]: "Service A requires data from B, C, and D. Because the 99th percentile latency is 400ms, chaining these sequentially will take 1200ms. We MUST run these requests in parallel."
*   [DON'T]: "The average latency is 60ms, so chaining 5 services will take a negligible 300ms."

**Fallacy #3: Bandwidth & Stamp Coupling**
*   [DO]: "The Wish List service only requires the customer's name. Use GraphQL or a targeted REST endpoint (`/customer/{id}/name`) to return exactly 200 bytes."
*   [DON'T]: "The Wish List service calls the Customer Profile service, which returns the entire 500kb customer profile object, discarding all but the name."

**Fallacy #4: Security**
*   [DO]: "Even though Service A and Service B are within our internal corporate VPC, the endpoint on Service B MUST require authentication and authorization tokens for the request."
*   [DON'T]: "Service B is behind our firewall, so it can accept unauthenticated HTTP requests from Service A."

**Distributed Transactions**
*   [DO]: "To process the order, the Order Placement service will initiate a Saga. If the remote Payment service fails, the Order Placement service will trigger a compensation event to mark the order as 'Cancelled'."
*   [DON'T]: "The Order Placement service will open a database transaction, call the remote Payment service, and commit the database transaction if the REST call succeeds."