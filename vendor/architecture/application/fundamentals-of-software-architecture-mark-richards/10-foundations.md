@Domain
Trigger these rules when analyzing, designing, refactoring, or extending architecture topologies; when extracting components into remote services; when writing inter-service communication logic (APIs, REST, RPC, messaging); when implementing database transactions across multiple domains; or when setting up system observability (logging).

@Vocabulary
- **Architecture Style/Pattern**: A named relationship of components covering a variety of architecture characteristics, acting as a shorthand for specific topologies and trade-offs.
- **Big Ball of Mud**: An architecture anti-pattern characterized by haphazard structure, unregulated growth, spaghetti-code, and promiscuous sharing of information across distant elements.
- **Unitary Architecture**: A historical/constrained architecture where software runs entirely on a single machine with no distributed parts.
- **Client/Server (Two-Tier/Three-Tier)**: An architecture separating technical functionality between frontend (browser/desktop), application/web servers, and a backend database server.
- **Monolithic Architecture**: A system where all source code and components are packaged into a single deployment unit.
- **Distributed Architecture**: A system consisting of multiple independent deployment units connected through remote access protocols.
- **Fallacies of Distributed Computing**: A set of 8 common, dangerous false assumptions developers make about network-based architectures.
- **Stamp Coupling**: A severe bandwidth-wasting anti-pattern in distributed systems where a service returns a large data payload containing far more attributes than the consuming service actually needs.
- **ACID Transactions**: Atomicity, Consistency, Isolation, Durability. The standard transaction model for single/monolithic databases.
- **BASE Transactions**: Basic availability, Soft state, Eventual consistency. The standard distributed transaction model relying on eventual synchronization rather than immediate locking.
- **Transactional Sagas**: A mechanism to manage distributed transactions using event sourcing for compensation (rollbacks) or finite state machines.
- **Contract**: The explicitly agreed-upon behavior and data formats shared between a client and a service.

@Objectives
- Prevent the "Big Ball of Mud" anti-pattern by enforcing rigorous structural boundaries and preventing unregulated code growth.
- Defend all distributed interactions against the 8 Fallacies of Distributed Computing.
- Optimize network bandwidth and eliminate Stamp Coupling in inter-service communications.
- Ensure comprehensive endpoint security, robust distributed logging, and resilient state management via BASE transactions/Sagas.

@Guidelines
- **Prevent Big Ball of Mud**: The AI MUST NEVER implement "duct-tape-and-baling-wire" expedient repairs that bypass established architectural layers. Global state and promiscuous data sharing across unrelated domains are strictly forbidden.
- **Fallacy 1 (The Network Is Reliable)**: The AI MUST NEVER assume a remote call will succeed. All remote inter-service communications MUST be wrapped with timeouts, retries, and circuit breakers.
- **Fallacy 2 (Latency Is Zero)**: The AI MUST NOT treat remote method invocations (RPC/REST/Messaging) like local in-memory method calls. The AI MUST minimize chained synchronous remote calls to prevent compounded latency.
- **Fallacy 3 (Bandwidth Is Infinite) & Stamp Coupling**: The AI MUST explicitly minimize data payloads between services. If a consumer only needs 200 bytes but the provider returns 500kb, the AI MUST resolve this Stamp Coupling by implementing field selectors, GraphQL, value-driven Consumer-Driven Contracts (CDCs), private REST endpoints, or internal messaging endpoints.
- **Fallacy 4 (The Network Is Secure)**: The AI MUST NOT assume internal networks/VPNs are safe. The AI MUST enforce authentication and authorization on EVERY single distributed endpoint, greatly increasing the security surface area.
- **Fallacies 5, 6, & 8 (Topology Changes, Multiple Admins, Heterogeneity)**: The AI MUST decouple application logic from fixed network topologies (e.g., using service discovery instead of hardcoded IPs) and MUST handle packet loss gracefully, anticipating heterogeneous network hardware and unexpected infrastructure upgrades.
- **Fallacy 7 (Transport Cost Is Zero)**: Before extracting code into a new distributed service, the AI MUST explicitly acknowledge the transport and infrastructural cost (gateways, firewalls, proxies, subnets) rather than treating service creation as "free."
- **Distributed Logging**: The AI MUST NOT rely on standard monolithic single-file logs for distributed systems. The AI MUST inject tracking/correlation IDs into all distributed requests to enable root-cause analysis via log consolidation tools (e.g., Splunk).
- **Distributed Transactions**: The AI MUST NEVER attempt to use traditional ACID database commits/rollbacks across multiple distributed services. The AI MUST utilize BASE transactions and implement Sagas to handle distributed state and compensation.
- **Contract Maintenance**: The AI MUST explicitly define, version, and maintain strict data/behavior contracts between distributed components, and MUST include communication models for version deprecation.

@Workflow
1. **Topology Classification**: Determine if the target application is Monolithic (single deployment unit) or Distributed (multiple deployment units).
2. **Structural Audit**: Scan for "Big Ball of Mud" indicators. If the system shares information promiscuously across boundaries, refactor to isolate dependencies into strict tiers or service boundaries.
3. **Remote Access Hardening (If Distributed)**: Locate every instance of inter-service network communication. Ensure every call implements a circuit breaker, a defined timeout, and error fallback logic.
4. **Stamp Coupling Elimination**: Inspect the data returned by remote calls. If the consumer only utilizes a fraction of the returned attributes, immediately refactor the API using field selectors, GraphQL, or a dedicated endpoint to return only the exact bytes needed.
5. **Endpoint Security Audit**: Verify that all endpoints (both public-facing and internal service-to-service) explicitly require authentication/authorization.
6. **Transaction Strategy Implementation**: If an operation modifies data across multiple distributed services, remove local ACID wrappers. Design a Transactional Saga where each service updates its own data and emits events, with defined compensating workflows for failure states.
7. **Observability Integration**: Ensure all incoming requests generate a correlation ID that is passed down through all subsequent inter-service calls and printed in all log statements.

@Examples (Do's and Don'ts)

**Stamp Coupling / Bandwidth**
- [DO]: Implement field selectors in a REST API (`/api/customers/123?fields=name`) so the consuming `WishList` service receives only the 200 bytes it needs.
- [DON'T]: Call a generic `/api/customers/123` endpoint that returns a 500kb payload containing 45 unneeded attributes.

**Distributed Transactions**
- [DO]: Implement a Saga where the `OrderPlacement` service creates an order, emits an event to the `PaymentService`, and listens for a `PaymentFailed` event to execute a compensating action (e.g., marking the order as canceled and freeing inventory).
- [DON'T]: Open an ACID database transaction, make a synchronous REST call to `PaymentService`, and attempt to rollback the local database if the HTTP request times out.

**Network Reliability**
- [DO]: Wrap a remote REST call in a Circuit Breaker that monitors failure rates, enforces a 500ms timeout, and returns a cached response or graceful error if the downstream service is unreachable.
- [DON'T]: Make a raw, blocking HTTP request assuming the network is perfectly reliable and latency is zero.

**Endpoint Security**
- [DO]: Require token validation (e.g., JWT) or mutual TLS (mTLS) for internal traffic between `ServiceA` and `ServiceB`.
- [DON'T]: Leave internal endpoints open to unauthenticated traffic under the false assumption that "the internal network firewall protects us."