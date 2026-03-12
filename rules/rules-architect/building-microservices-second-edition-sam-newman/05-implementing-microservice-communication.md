# @Domain
Triggered when the user requests tasks related to designing, implementing, refactoring, configuring, or documenting communication between microservices. This includes selecting inter-process communication (IPC) protocols (REST, gRPC, GraphQL, Message Brokers), defining API schemas, handling API versioning and backward compatibility, structuring code reuse, implementing service discovery, or configuring API Gateways and Service Meshes.

# @Vocabulary
*   **Information Hiding**: Hiding internal implementation details (code and data) behind a defined module boundary, exposing only the bare minimum required to satisfy external consumers.
*   **Interface Definition Language (IDL)**: A schema format used to define remote procedure call (RPC) interfaces (e.g., WSDL for SOAP, Protocol Buffers for gRPC).
*   **HATEOAS (Hypermedia as the Engine of Application State)**: A REST architectural constraint where clients interact with a network application entirely through hypermedia links provided dynamically by the application servers.
*   **Competing Consumer Pattern**: A message broker pattern where multiple worker instances (consumers) pull from the same queue to distribute load.
*   **Structural Breakage**: A backward-incompatible change where the physical structure of an endpoint changes (e.g., fields removed, new required fields added).
*   **Semantic Breakage**: A backward-incompatible change where the physical structure of the endpoint remains the same, but the internal behavioral logic changes, breaking consumer expectations.
*   **Tolerant Reader**: A consumer-side coding pattern where the client strictly extracts only the data it needs and ignores any unrecognized or newly added fields to prevent brittle breakages.
*   **Semantic Versioning**: A versioning scheme (MAJOR.MINOR.PATCH) where MAJOR indicates backward-incompatible changes, MINOR indicates backward-compatible additions, and PATCH indicates backward-compatible bug fixes.
*   **Lockstep Deployment**: An anti-pattern where a microservice and all its consumers must be updated and deployed at the exact same time due to a tightly coupled breaking change.
*   **Expand and Contract Pattern**: A migration pattern where a microservice exposes both the old and new interfaces simultaneously (Expand) and translates old requests to the new logic, allowing consumers time to migrate before the old interface is retired (Contract).
*   **North-South Traffic**: Network traffic entering or leaving the system perimeter (from external clients to internal services).
*   **East-West Traffic**: Network traffic flowing internally between microservices within the system perimeter.
*   **API Gateway**: An infrastructural component sitting at the system perimeter managing North-South traffic.
*   **Service Mesh**: An infrastructural component managing East-West traffic, typically using local sidecar proxies to handle cross-cutting communication concerns without altering microservice code.
*   **Humane Registry**: A lightweight, human-readable catalog (e.g., a wiki or auto-generated portal) documenting running services, aggregated from live system metadata.

# @Objectives
*   Ensure microservices maintain **Independent Deployability** by establishing stable, backward-compatible network contracts.
*   Enforce the rule of keeping "pipes dumb and endpoints smart" by prohibiting business logic in middleware, gateways, and service meshes.
*   Mitigate the inherent unreliability of networks by treating all remote inter-process calls differently from local in-process calls.
*   Prevent the accidental coupling of microservices caused by shared code libraries, monolithic frontends, or implicit contracts.

# @Guidelines

## Technology Selection & Protocol Design
*   When selecting IPC technologies, the AI MUST prioritize options that easily support backward compatibility, explicit schemas, technology-agnostic APIs, and information hiding.
*   When implementing RPC (e.g., gRPC), the AI MUST NOT abstract the network layer so heavily that developers treat remote calls as local in-process calls. The AI MUST account for network unreliability, latency, and serialization costs.
*   When designing REST APIs, the AI MUST leverage standard HTTP capabilities (e.g., verbs, status codes, Cache-Control, ETags). The AI MUST NOT implement HATEOAS unless the user explicitly dictates the creation of a distributed hypermedia system.
*   When implementing GraphQL, the AI MUST strictly restrict its use to the external perimeter (e.g., as a Backend-For-Frontend/BFF aggregating calls for mobile/web clients). The AI MUST NOT use GraphQL as the generic communication protocol between internal microservices.
*   When utilizing GraphQL, the AI MUST NOT treat the backing microservices as thin CRUD wrappers over databases; microservices must retain their own encapsulated business logic.
*   When implementing asynchronous communication, the AI MUST use queues for point-to-point load distribution and topics for event broadcasting.
*   When designing message consumers, the AI MUST assume messages may be delivered more than once and MUST implement idempotent processing logic.

## Schemas & Contracts
*   When creating a microservice endpoint, the AI MUST define an explicit schema (e.g., OpenAPI for REST, Protobuf for gRPC, CloudEvents/AsyncAPI for messages). The AI MUST NOT create implicit, schemaless APIs.
*   When configuring CI/CD pipelines for microservices, the AI MUST integrate schema validation tools (e.g., openapi-diff, Protolock) to automatically fail builds if a structural breakage is detected.

## Handling Change & Backward Compatibility
*   When modifying an existing microservice contract, the AI MUST utilize "Expansion Changes" (adding new fields or endpoints) and MUST NOT remove, rename, or change the data type of existing fields.
*   When writing code that consumes a microservice, the AI MUST implement the "Tolerant Reader" pattern (e.g., using XPath/JSONPath to extract specific fields while ignoring unknown surrounding data). The AI MUST NOT use strict binary deserialization that breaks when unmapped fields are received.
*   When a breaking change is absolutely unavoidable, the AI MUST NOT orchestrate a Lockstep Deployment. Instead, the AI MUST implement the "Expand and Contract" pattern by deploying a new version of the microservice that coexists both V1 and V2 endpoints, routing V1 requests to V2 logic internally.

## Code Reuse
*   When asked to share code between microservices, the AI MUST NOT extract business/domain logic into shared libraries if updating that library requires coordinated deployments across multiple microservices.
*   When generating client libraries (SDKs) for microservices, the AI MUST restrict the library code strictly to transport, service discovery, and failure-handling mechanisms. The AI MUST NOT leak server-side business logic into the client library.

## Infrastructure & Routing
*   When configuring Service Discovery via DNS, the AI MUST ensure the DNS record points to a load balancer rather than directly to ephemeral microservice host IPs to prevent TTL caching outages.
*   When configuring an API Gateway, the AI MUST restrict its responsibilities to North-South traffic and generic concerns (API keys, rate limiting, external routing). The AI MUST NOT implement business logic, call aggregation, or protocol rewriting (e.g., SOAP to REST translation) within the API Gateway.
*   When configuring a Service Mesh (e.g., Istio, Envoy), the AI MUST restrict its use to East-West traffic for cross-cutting operational concerns (mTLS, correlation IDs, discovery, retries). The AI MUST NOT leak microservice-specific business logic into the control plane or sidecars.

# @Workflow
1.  **Analyze Communication Requirements:** Determine if the interaction requires synchronous blocking (RPC/REST) or asynchronous non-blocking (Message Brokers) behavior based on latency tolerance and temporal coupling constraints.
2.  **Define Explicit Schema:** Author an exact, technology-agnostic schema definition (OpenAPI, Protobuf) representing the contract.
3.  **Implement Server-Side Hiding:** Ensure the microservice implementation perfectly encapsulates its database and internal domain models. Map internal models to the external schema response.
4.  **Implement Client-Side Tolerance:** Write consumer code that selectively extracts only required fields from the response payload, ignoring all other data.
5.  **Evaluate Modification Impact:** If modifying an existing contract, test the schema against the previous version to verify it is strictly an Expansion Change. If it is a breaking change, initiate the Expand and Contract pattern.
6.  **Configure Infrastructure Boundaries:** Ensure Gateway routing is configured only if the endpoint faces external clients (North-South). Configure Service Mesh sidecars for internal-only (East-West) communication.

# @Examples (Do's and Don'ts)

## Contract Evolution (Avoiding Breakages)
*   **[DO]** Add a new `dateOfBirth` field to an existing JSON response while keeping all previous fields perfectly intact.
*   **[DON'T]** Rename a `firstName` field to `givenName` or combine `firstName` and `lastName` into a single `fullName` field on an existing endpoint, as this causes a Structural Breakage for current consumers.

## Breaking Changes (Expand and Contract)
*   **[DO]** Deploy a service exposing both `/v1/customer` and `/v2/customer`. Inside the service, translate `/v1/customer` inbound requests into the new `/v2` internal data structures so both endpoints are served from the same unified backend logic, allowing consumers 6 months to migrate.
*   **[DON'T]** Delete the `/v1/customer` endpoint, deploy the service, and force the frontend team and 3 other backend teams to deploy their updated client code at the exact same minute (Lockstep Deployment).

## API Gateways
*   **[DO]** Configure an API Gateway to validate third-party API keys, enforce a limit of 100 requests per minute, and route `/api/shop` to the Web Shop microservice.
*   **[DON'T]** Configure an API Gateway to receive a single client request, make a call to the Customer service, make a subsequent call to the Order service, merge the JSON responses using custom gateway scripting, and return the aggregated payload. (Use a BFF or GraphQL resolver for this instead).

## Consumer Implementation (Tolerant Reader)
*   **[DO]** Parse an incoming JSON payload by extracting `payload.email` and `payload.id` directly, ignoring the fact that the server just added 15 new profile fields to the response.
*   **[DON'T]** Use a strict Java/C# serialization framework configured to throw a `MappingException` or `UnrecognizedPropertyException` if the JSON payload contains fields not explicitly defined in the consumer's local Data Transfer Object class.

## Code Reuse
*   **[DO]** Create a shared Java library that standardizes how correlation IDs are injected into log files and how mutual TLS handshakes are performed, distributing this to all JVM-based microservices.
*   **[DON'T]** Create a `CommonDomainEntities` library containing the validation logic for what constitutes a valid `UserAccount`, forcing all microservices to update their library version and redeploy simultaneously whenever the user validation rules change.