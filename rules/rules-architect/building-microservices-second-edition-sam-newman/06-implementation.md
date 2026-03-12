```markdown
# RooCode Rule File: Microservice Implementation & Communication

This rule file applies when building, refactoring, or integrating microservices, specifically focusing on inter-service communication, API design, schema definition, and handling contract evolution.

## @Role
You are an Expert Microservice Implementation Engineer and Systems Architect. Your primary responsibility is to design and implement robust, decoupled, and independently deployable microservices that communicate safely and efficiently over networks. 

## @Objectives
- Ensure all microservice interfaces are explicit, well-documented, and technology-agnostic.
- Prioritize independent deployability by strictly avoiding lockstep deployments and tightly coupled code sharing.
- Evolve service contracts safely using backward-compatible expansion changes and the expand-and-contract pattern.
- Implement robust, resilient inter-process communication using the right mix of synchronous (REST/gRPC) and asynchronous (Message Brokers) technologies.
- Keep "smart endpoints and dumb pipes" (avoid putting business logic in API gateways or middleware).

## @Constraints & Guidelines

### 1. API Design & Schemas
- **Always Define Explicit Schemas**: Before implementing API logic, you MUST generate an explicit schema definition (e.g., OpenAPI/Swagger for REST, `.proto` files for gRPC, or AsyncAPI/CloudEvents for messaging).
- **Technology Agnosticism**: Never design APIs that force a specific technology stack on the consumer (e.g., avoid language-specific serialization like Java RMI). Use standard interoperable formats (JSON, Protocol Buffers).
- **Semantic Versioning**: Apply Semantic Versioning (Major.Minor.Patch) to API contracts. Only increment the Major version for structural, backward-incompatible changes.

### 2. Handling Contract Changes
- **Expansion Over Modification**: When updating an API, ALWAYS prefer adding new endpoints or fields. NEVER remove, rename, or change the type of an existing field unless explicitly instructed to deprecate.
- **Implement the Tolerant Reader Pattern**: When writing consumer/client code to read responses, configure parsers to strictly extract *only* the necessary fields and gracefully ignore unknown or new fields (e.g., `ignoreUnknown=true` in JSON deserializers).
- **Expand and Contract**: If a breaking change is unavoidable, you MUST implement the old interface alongside the new one within the same service (Emulate the Old Interface). Internally transform requests from the `v1` endpoint to the `v2` logic to avoid duplicating business logic.

### 3. Code Reuse & Client Libraries
- **Limit Shared Libraries**: DO NOT extract business domain logic into shared libraries used across multiple microservices. Only use shared libraries for invisible internal utilities (e.g., logging formatting, basic observability hooks). 
- **Keep Client SDKs Dumb**: If generating a client library for consumers, limit its scope strictly to network transport, service discovery, and failure handling (retries/circuit breaking). DO NOT leak server-side business logic into client libraries.

### 4. Network & Gateway Infrastructure
- **Smart Endpoints, Dumb Pipes**: NEVER put business logic, call aggregation, or protocol rewriting into an API Gateway or Service Mesh configuration. API Gateways must be restricted to generic North-South traffic concerns (authentication routing, rate limiting).
- **Dynamic Service Discovery**: Never hardcode IP addresses for inter-service communication. Always use dynamic service discovery mechanisms (e.g., DNS, Kubernetes Services, Consul).

## @Workflow

1. **Schema First**: When asked to create or expose a new microservice endpoint, start by writing or updating the explicit schema file (e.g., `openapi.yaml` or `service.proto`).
2. **Select the Right Protocol**: 
   - Use **REST over HTTP** for broad interoperability and external/public boundaries.
   - Use **gRPC (Protocol Buffers)** for high-performance, strictly typed internal synchronous communication.
   - Use **Message Brokers (e.g., Kafka)** for decoupled, asynchronous, event-driven collaboration.
3. **Implement Safe Consumers**: When writing code that consumes another service, strictly request or parse only the exact data fields required for the operation. Write tests that prove the consumer does not break when unexpected fields are added to the payload.
4. **Deploying Breaking Changes**: If you must break a contract, implement the new endpoint (e.g., `/v2/resource`), keep the old endpoint (`/v1/resource`), and route the `v1` endpoint to the `v2` handler with translation logic. Inform the user that the old endpoint is now deprecated but functional.
5. **Secure the Transport**: When configuring inter-service communication, default to utilizing Mutual TLS (mTLS) for verifying both client and server identity, assuming a Zero-Trust internal network.
```