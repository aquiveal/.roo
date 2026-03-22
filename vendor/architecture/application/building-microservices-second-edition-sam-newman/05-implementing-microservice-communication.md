@Domain
Trigger these rules when tasks involve designing, implementing, refactoring, or documenting communication between microservices, defining API contracts (REST, gRPC, GraphQL), configuring asynchronous message brokers, managing API versioning/schemas, implementing service discovery, or configuring API gateways and service meshes.

@Vocabulary
*   **Information Hiding**: Concealing internal implementation details and data representations behind an explicit, minimal external interface to reduce coupling.
*   **RPC (Remote Procedure Call)**: A technique making a remote network call look like a local method call (e.g., gRPC, SOAP).
*   **REST (Representational State Transfer)**: An architectural style based on resources, utilizing standard HTTP verbs (GET, POST, PUT) and hypermedia controls.
*   **HATEOAS**: Hypermedia As The Engine Of Application State; decoupling client and server by using hypermedia links for application state transitions.
*   **Message Broker**: Middleware managing asynchronous communication via queues (point-to-point/competing consumers) or topics (publish/subscribe).
*   **Structural Breakage**: A backward-incompatible change to the structure of an endpoint (e.g., removing a field, adding a required field).
*   **Semantic Breakage**: A change in the behavior or logic of an endpoint while the structure remains the same.
*   **Tolerant Reader**: A client implementation pattern (Postel's Law) that extracts only the needed data and ignores unrecognized fields, preventing breakage when new fields are added.
*   **Lockstep Deployment**: An anti-pattern where an upstream service and its downstream consumers must be deployed simultaneously to handle a breaking change.
*   **Expand and Contract Pattern**: Phasing in breaking changes by temporarily emulating and supporting both the old and new interfaces within the same running microservice until consumers migrate.
*   **North-South Traffic**: Network traffic crossing the system perimeter (e.g., from external clients to internal services).
*   **East-West Traffic**: Internal network traffic between microservices within the system perimeter.
*   **API Gateway**: A perimeter proxy primarily for North-South traffic handling cross-cutting concerns (rate limiting, auth).
*   **Service Mesh**: A decentralized infrastructure layer handling East-West traffic reliability and observability via sidecar proxies (e.g., Envoy).
*   **Humane Registry**: A centralized, programmatic catalog providing human-readable information, schemas, and health status for all microservices in an organization.

@Objectives
*   Ensure independent deployability of microservices by designing stable, explicit, and backward-compatible communication contracts.
*   Select communication protocols strictly based on interaction requirements, avoiding premature optimization and technology fetishism.
*   Prevent organizational and architectural coupling caused by shared code, monolithic client libraries, or centralized "smart" middleware.
*   Safeguard system integrity by strictly isolating internal databases from external consumers and using explicit schemas to catch structural breakages before deployment.
*   Establish seamless service discovery and routing mechanisms that accommodate dynamic, highly ephemeral infrastructure without polluting microservice business logic.

@Guidelines

### 1. Protocol and Technology Selection
*   The AI MUST select gRPC when high-performance, strongly typed, synchronous request-response communication is required between internal microservices.
*   The AI MUST NOT use Java RMI or any RPC technology that heavily couples the client and server to a specific platform or forces the exposure of internal binary types ("expand-only" types).
*   The AI MUST use REST over HTTP when ensuring broad interoperability, maximizing caching capabilities, or exposing APIs to external parties.
*   When using REST, the AI MUST correctly implement standard HTTP verbs (GET, POST, PUT) and reserve HTTP 400-series codes for client errors and 500-series codes for server errors.
*   The AI MUST utilize GraphQL ONLY at the system perimeter (North-South traffic) for mobile/UI clients to perform call aggregation and filtering. The AI MUST NOT use GraphQL for general microservice-to-microservice (East-West) communication.
*   The AI MUST NOT treat microservices running behind a GraphQL endpoint simply as wrappers over databases; the microservice must retain its own internal business logic.
*   The AI MUST use Message Brokers (e.g., Kafka, RabbitMQ) for asynchronous, event-driven communication or competing-consumer workload distribution.

### 2. Interface Design and Schemas
*   The AI MUST define explicit schemas for all microservice interfaces (e.g., Protocol Buffers for gRPC, OpenAPI for REST, AsyncAPI/CloudEvents for messaging).
*   The AI MUST NOT expose internal implementation details (e.g., database schemas, internal models) in the external schema.
*   The AI MUST automate schema compatibility validation (e.g., using `openapi-diff`, `json-schema-diff-validator`, or Schema Registries) to fail CI builds if a structural breakage is detected.

### 3. Managing Interface Evolution
*   The AI MUST prioritize "Expansion Changes" (adding optional fields/endpoints) over modifications or deletions to maintain backward compatibility.
*   The AI MUST implement the Tolerant Reader pattern on all client consumers, extracting only explicitly required fields and ignoring unrecognized data (e.g., using XPath or JSONPath).
*   When a breaking change is completely unavoidable, the AI MUST NOT plan or execute a Lockstep Deployment.
*   To manage a breaking change, the AI MUST implement the Expand and Contract pattern: coexist the old interface (emulated) and the new interface within the *same* microservice codebase until all clients migrate.
*   The AI MUST NOT deploy old and new versions of a microservice as separate physical instances to handle versioning, except for short-lived canary releases.
*   The AI MUST implement tracking (e.g., logging `User-Agent` or client API keys) on deprecated endpoints to monitor client migration progress.

### 4. Code Reuse and Client Libraries
*   The AI MUST NOT share domain logic or domain entity models across microservices using shared libraries. If business logic reuse is necessary, the AI MUST extract it into a dedicated microservice.
*   When providing client libraries (SDKs) to consumers, the AI MUST restrict the library scope to transport-level concerns (service discovery, failure modes, logging, retries).
*   The AI MUST NOT put business logic inside client SDKs.
*   The AI MUST ensure that the consumer team dictates when the client library is upgraded, preventing forced lockstep upgrades by the server team.

### 5. API Gateways and Service Meshes
*   The AI MUST keep intermediate networking layers ("pipes") dumb and push business logic ("smarts") into the microservice endpoints.
*   The AI MUST NOT configure business logic, protocol rewriting (e.g., SOAP to REST transformations), or complex call aggregation inside an API Gateway.
*   The AI MUST use API Gateways strictly for North-South traffic to handle generic concerns (API keys, rate limiting, external routing).
*   The AI MUST use a Service Mesh (via sidecar proxies like Envoy) for East-West traffic to implement cross-cutting inter-service reliability (mTLS, service discovery, retries).

### 6. Service Discovery
*   The AI MUST NOT rely on raw DNS entries pointing directly to highly volatile microservice IPs due to TTL caching issues. DNS MUST point to a load balancer that manages the dynamic node pool.
*   For highly dynamic environments, the AI MUST implement a dynamic service registry (e.g., Consul, etcd, Kubernetes native services).

@Workflow
When designing or modifying a communication pathway between microservices, the AI MUST execute the following algorithm:

1.  **Interaction Analysis**: Determine if the interaction requires Synchronous Request-Response, Asynchronous Request-Response, or Event-Driven publish/subscribe.
2.  **Protocol Selection**: Select the transport mechanism (gRPC, REST, Kafka) based on the interaction type, required latency, and client constraints.
3.  **Schema Definition**: Author an explicit, technology-agnostic schema (OpenAPI, Protobuf, CloudEvents) defining *only* the data necessary for the consumer.
4.  **Compatibility Check**: Validate the proposed schema against the previous version using a schema diff tool to ensure no structural breakages.
5.  **Client Implementation**: Write the client-side consumption code utilizing the Tolerant Reader pattern.
6.  **Deprecation Strategy (If Breaking)**: If the new schema requires a breaking change, implement the new endpoint alongside the old endpoint in the same codebase. Translate old requests to the new internal model.
7.  **Infrastructure Configuration**: Configure East-West routing through the Service Mesh definition, and if applicable to external clients, configure the API Gateway strictly for routing and access control.

@Examples (Do's and Don'ts)

### Interface Evolution & Tolerant Reader
*   [DO] Add a new, optional field to a REST response payload.
```json
// Old Response
{ "id": 123, "name": "MusicCorp" }
// New Response
{ "id": 123, "name": "MusicCorp", "established": 1999 }
```
*   [DON'T] Rename a field or change its data type, which causes a structural breakage for existing consumers.
```json
// BAD: Renaming 'name' to 'companyName' breaks clients expecting 'name'
{ "id": 123, "companyName": "MusicCorp" }
```

### Tolerant Reader Implementation
*   [DO] Extract only what is needed, ignoring the rest.
```javascript
// Good Client Implementation
function getCustomerName(responsePayload) {
    // Ignores all other fields, won't break if new fields are added
    return responsePayload.name; 
}
```
*   [DON'T] Strictly bind the entire response to a rigid, fully mapped class where unmapped fields cause deserialization exceptions.

### Emulating Old Interfaces (Expand and Contract)
*   [DO] Expose both v1 and v2 endpoints in the same service router, mapping v1 requests to the new v2 internal logic.
```python
@app.route('/v1/customer')
def get_customer_v1():
    # Emulate v1 response using v2 internal logic
    internal_data = get_internal_customer_v2()
    return map_v2_to_v1_response(internal_data)

@app.route('/v2/customer')
def get_customer_v2():
    return get_internal_customer_v2()
```
*   [DON'T] Shut down the v1 endpoint simultaneously while launching v2, forcing all consumers to update their code exactly when the server deploys (Lockstep Deployment).

### Gateways and Middleware
*   [DO] Configure the API Gateway to validate OAuth tokens and apply rate limiting.
*   [DON'T] Configure the API Gateway to fetch user data, transform it into XML, fetch order data, stitch them together, and return a composite object to the client. (Use a BFF or GraphQL endpoint managed by the frontend team instead).

### Code Reuse
*   [DO] Create a shared library for logging formatting or distributed tracing instrumentation.
*   [DON'T] Create a shared library containing the "Order" and "Customer" domain object models and force all microservices to import it.