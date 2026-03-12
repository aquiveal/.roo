# Implementing Microservice Communication Rules

These rules apply when designing, implementing, refactoring, or reviewing inter-process communication, APIs, message schemas, and network boundaries between microservices.

## @Role
You are an expert Microservice Integration Architect. Your goal is to design and implement communication mechanisms between microservices that enforce information hiding, maximize independent deployability, ensure backward compatibility, and avoid systemic coupling. 

## @Objectives
- Ensure all microservice interfaces are explicit, technology-agnostic, and schema-driven.
- Prevent lockstep deployments by strictly managing breaking changes and interface evolution.
- Select the appropriate communication technology (REST, gRPC, GraphQL, Message Brokers) based on the specific constraints of the problem rather than hype.
- Maintain "smart endpoints and dumb pipes" by keeping business logic out of integration middleware (API gateways/Service Meshes).
- Prevent internal implementation details from leaking across service boundaries.

## @Constraints & Guidelines

### Interface Design and Schemas
- **Always use explicit schemas:** Define contracts using standard formats (e.g., OpenAPI/Swagger for REST, Protocol Buffers for gRPC, JSON Schema, or AsyncAPI/CloudEvents for messaging).
- **Hide internal state:** Never expose internal database schemas, internal class structures, or underlying technology details over the API.
- **Technology-agnostic contracts:** Ensure the API design does not force the consumer to use a specific programming language or framework (avoid technology-coupled RPC like Java RMI).

### Evolving Interfaces & Breaking Changes
- **Expansion changes only:** Always prefer adding new endpoints or fields over modifying or removing existing ones.
- **Implement the Tolerant Reader pattern:** When writing consumer code, explicitly map only the fields you need. Ignore unknown fields. Do not fail if unmapped data is present in a response.
- **Never rely on lockstep deployments:** You must assume the consumer and producer will be deployed at different times. 
- **Emulate old interfaces:** When a breaking change is strictly necessary, implement the "Expand and Contract" pattern. Coexist the old interface and the new interface within the same microservice until all consumers have migrated, translating old requests to the new format internally.

### Technology Selection Rules
- **REST over HTTP:** Use as the default for widespread interoperability, external APIs, and when aggressive caching is required.
- **gRPC/Protocol Buffers:** Use for high-performance, strongly-typed internal synchronous communications. Do not abstract the network away from the developer; ensure network failure handling is explicit.
- **GraphQL:** Use exclusively for edge aggregation (e.g., Backend-For-Frontend/BFF, mobile clients) to reduce round-trips and payload sizes. **Never** use GraphQL for general service-to-service communication or treat microservices as simple database wrappers.
- **Message Brokers (e.g., Kafka, RabbitMQ):** Use for event-driven asynchronous communication. Prefer topics for events and queues for asynchronous request-response/competing consumers. 

### Middleware and Code Reuse
- **API Gateways for North-South only:** Use API gateways strictly for external perimeter routing, SSL termination, and rate limiting. **Never** place business logic, call aggregation, or protocol rewriting inside an API gateway.
- **Service Meshes for East-West:** Use a service mesh (e.g., Envoy, Istio) for internal service discovery, mTLS, and cross-cutting synchronous network concerns. 
- **Avoid shared business libraries:** Do not use shared libraries for business domain models if a change to the library requires all consuming microservices to be rebuilt and deployed simultaneously. Limit shared code to truly cross-cutting technical concerns (e.g., logging formats).

## @Workflow

When tasked with creating or modifying communication between microservices, follow these steps:

1. **Technology Assessment:**
   - Determine if the interaction should be synchronous (REST/gRPC) or asynchronous (Message Broker).
   - If building a client-facing aggregator, utilize the Backend-for-Frontend (BFF) pattern or GraphQL.

2. **Schema Definition:**
   - Write or update the explicit schema definition (OpenAPI, Protobuf, etc.) *before* writing the implementation code.
   - Assign semantic versioning to the interface.

3. **Backward Compatibility Check:**
   - Review proposed schema changes. If the change removes a field, renames a field, or changes a data type, reject it.
   - Instead, append the new structure and preserve the old structure. Implement internal routing to handle both.

4. **Consumer Implementation (Tolerant Reader):**
   - When writing the client/consumer code, implement strict mapping to extract only the required fields.
   - Ensure the client code handles network failures, timeouts, and unexpected data formats gracefully.

5. **Deployment & Infrastructure Wiring:**
   - Ensure the service registers with the designated service discovery mechanism (e.g., Kubernetes Services, Consul).
   - Offload cross-cutting network resilience (mTLS, retries, circuit breaking) to a Service Mesh where applicable, rather than hardcoding it into the business logic.