@Domain
The AI MUST activate these rules when engaged in tasks involving the design, development, modernization, or architectural planning of RESTful APIs, microservices, cloud-native applications, legacy-to-cloud migrations, cyber-physical systems (CPS), and IoT integration (Device-to-Device [D2D] or Device-to-Cloud [D2C]).

@Vocabulary
*   **CPS (Cyber-Physical Systems):** Environments where physical, mechanical, and electrical systems are digitized and integrated via software.
*   **D2D (Device-to-Device):** Direct integration and communication between networked embedded devices.
*   **D2C (Device-to-Cloud):** Integration between ground-level IoT devices and faraway cloud environments.
*   **ROA (Resource-Oriented Architecture):** The core architectural style of REST where application state and functionality are divided into distributed, web-accessible resources.
*   **Data Elements (REST):** The six elements comprising REST data: Resource, Resource Identifier (URI), Resource metadata, Representation, Representation metadata, and Control data.
*   **ELK Stack:** The log analytics stack comprising Elasticsearch (fuzzy search/storage), Logstash (collection/transformation), and Kibana (GUI for knowledge discovery).
*   **Correlate ID:** A random UUID generated for a client request and passed to every internal service request to enable distributed tracing.
*   **API-First Development:** A strategy where the API is defined and mocked before any backend or frontend development begins, enabling parallel development.
*   **SRE (Site Reliability Engineering):** The discipline of ensuring software systems are designed and deployed with high reliability, resiliency, and elasticity.
*   **EDA (Event-Driven Architecture):** A reactive architecture style where services communicate asynchronously via events and message brokers, avoiding synchronous blocking.
*   **Resiliency:** The ability of an application to proactively detect, contain, and survive internal or external faults without bringing down the whole system.
*   **Elasticity:** The ability of a system to scale up or out dynamically to handle extra user and data loads.
*   **Pipeline Pattern:** An architectural workaround for synchronous point-to-point REST blocking, utilizing a central entity to orchestrate control and data flows.

@Objectives
*   Design APIs adhering strictly to the RESTful paradigm and Resource-Oriented Architecture (ROA) constraints.
*   Facilitate legacy modernization by breaking monolithic applications into fine-grained, independent, stateless microservices.
*   Implement the API-First approach to eliminate development friction and allow parallel frontend, backend, and QA workflows.
*   Ensure microservices are highly observable by mandating proper HTTP headers (Meaningful Names/User-Agent) and distributed tracing (Correlate IDs).
*   Architect systems for high reliability (SRE principles), separating synchronous REST operations from long-running or downstream tasks using event-driven asynchronous messaging or pipeline patterns to prevent blocking.

@Guidelines

**REST Architectural Constraints**
*   **Client-Server Separation:** The AI MUST isolate client and server implementations. The client must only know resource URIs.
*   **Stateless Communication:** The AI MUST NOT design servers to store client session context. Every request must be self-contained. Any authentication state must be managed via tokens (e.g., JWT) passed in the request.
*   **Cacheable Responses:** The AI MUST configure responses to be explicitly cacheable or non-cacheable to optimize network bandwidth, reduce latency, and hide network failures.
*   **Layered System:** The AI MUST design architectures that support intermediaries (proxies, gateways) for security enforcement, load balancing, and data translation without exposing the layering to the client.
*   **Uniform Interface:** The AI MUST map operations strictly to standard HTTP methods: `GET` (retrieve state), `PUT` (update/provide state), `POST` (provide state/create), `DELETE` (remove), `HEAD` (metadata), and `OPTIONS` (metadata).

**Resource and Data Representation**
*   **JSON as Standard:** The AI MUST use JSON as the preferred data model for resources.
*   **Type Declaration:** The AI SHOULD use the special `_type` key-value pair within JSON payloads to explicitly denote the type of the resource.
*   **Self-Descriptive Messages:** The AI MUST ensure representations include both metadata (format, size, media type) and content.

**Best Practices for REST-based Microservices**
*   **Meaningful Names in Headers:** The AI MUST inject logical service names into the `User-Agent` property of request headers (e.g., `User-Agent: EmployeeSearchService`) to allow performance engineers to easily trace the origin of a cascaded request.
*   **Correlate IDs:** The AI MUST mandate the generation of a random UUID at the entry point of a client request and ensure this UUID is passed to all subsequent internal microservice requests to facilitate distributed tracing.
*   **Centralized Log Analytics:** The AI MUST architect services to output logs compatible with centralized log management (specifically referencing the ELK stack) to enable fuzzy searching and machine learning analytics on system behavior.
*   **API Management & Versioning:** The AI MUST design APIs with future demands in mind, utilizing an API facade. The AI MUST NOT change API method signatures arbitrarily, as it breaks dependent microservices.
*   **Overcoming Synchronous Blocking:** When designing interactions between multiple microservices (e.g., updating stock and sending notifications), the AI MUST evaluate the risk of synchronous point-to-point REST calls causing system bottlenecks.
    *   If blocking is a risk, the AI MUST recommend decoupling the services using asynchronous messaging (Event-Driven Architecture via message queues/brokers) or a Pipeline Orchestration pattern.

**API-First Strategy**
*   **Mocking:** The AI MUST instruct the user to define the API contract and create mock endpoints *before* writing business logic, ensuring QA, frontend, and backend teams can work in parallel.

**Application Modernization & Cloud-Native Design**
*   **Containerization:** The AI MUST architect microservices to be container-ready, enabling horizontal scalability (elasticity) and decoupled deployments.
*   **Target Environments:** The AI MUST tailor API designs to their target:
    *   *Public APIs:* Designed for broad omnichannel reach and security.
    *   *Private APIs:* Designed for internal ESB/service reuse.
    *   *IoT APIs:* Designed for D2D/D2C fog and edge clouds, optimizing for poly-structured data.

@Workflow
1.  **API-First Definition:**
    *   Define the resource models and URI structures using ROA principles.
    *   Establish the API contract using self-descriptive messages (JSON with `_type`).
    *   Generate a mock of the API to unblock parallel development teams.
2.  **Architecture & Constraints Validation:**
    *   Verify the design is strictly Client-Server and Stateless.
    *   Ensure proper use of HTTP verbs (GET, POST, PUT, DELETE, HEAD, OPTIONS).
    *   Implement Cache-Control mechanisms.
3.  **Microservice Instrumentation:**
    *   Inject Correlation ID logic into the API gateway/entry point and propagate it through all inter-service HTTP clients.
    *   Configure HTTP clients to send meaningful `User-Agent` headers containing the source microservice name.
    *   Structure log outputs for ELK stack ingestion.
4.  **Resiliency & Coupling Check:**
    *   Analyze the microservice call chain. If a REST call triggers a downstream process that could degrade performance (e.g., mass email notifications), replace the synchronous REST call with an asynchronous event published to a message broker.

@Examples (Do's and Don'ts)

**Meaningful Headers & Tracing**
*   [DO]: Configure service-to-service HTTP requests to include tracing headers:
    ```http
    GET /api/v1/notifications HTTP/1.1
    Host: internal-service
    User-Agent: CheckoutService/v1
    X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
    ```
*   [DON'T]: Make anonymous point-to-point calls between microservices without passing correlation IDs or identifying the calling service, which makes debugging distributed systems impossible.

**JSON Resource Representation**
*   [DO]: Include explicit type definitions in the JSON resource representation.
    ```json
    {
      "_type": "order",
      "id": "12345",
      "status": "shipped"
    }
    ```
*   [DON'T]: Return ambiguous payloads where the consumer must guess the resource type based solely on the endpoint.

**Resiliency and Decoupling**
*   [DO]: Use asynchronous messaging for long-running downstream tasks to avoid REST blocking. (e.g., `CheckoutService` updates the database and publishes an `OrderPlaced` event to a message broker, which the `NotificationService` consumes).
*   [DON'T]: Use a synchronous point-to-point REST call (`CheckoutService` calls `POST /send-emails` and waits for it to finish before returning the checkout response to the user).

**API-First Development**
*   [DO]: Define the API specification and deploy a mock server immediately so the frontend team can begin integration while the backend team implements the database logic.
*   [DON'T]: Wait for the backend development to be completely finished and integrated before providing the API endpoints and documentation to the QA and frontend teams.