@Domain
Triggered when the user requests tasks related to the design, architecture, integration, refactoring, documentation, or security auditing of RESTful APIs, API management platforms, or microservices integrations.

@Vocabulary
*   **API (Application Programming Interface)**: A set of rules and tools (akin to traffic rules, recipes, or blueprints) that initiate and govern how business workloads and software applications interact.
*   **D2D / D2C / C2C**: Device-to-Device, Device-to-Cloud, and Cloud-to-Cloud integration facilitated by APIs.
*   **RPC (Remote Procedure Call)**: An API type that enables applications to call remote functions, using XML or JSON content types.
*   **SOAP (Simple Object Access Protocol)**: An older, complex XML-based messaging protocol for web services.
*   **REST (Representational State Transfer)**: A lightweight, fully-featured architectural style for networked applications, utilizing HTTP protocols and standard operations (GET, PUT, POST, DELETE).
*   **ROA (Resource-Oriented Architecture)**: An architecture where application state and functionality are divided into distributed resources, accessible via URIs.
*   **NFR / QoS**: Non-Functional Requirements and Quality of Service attributes (Performance, Scalability, Modifiability, Portability, Reliability).
*   **URI (Uniform Resource Identifier)**: The unique name and address used to identify every resource.
*   **Representation**: The current or desired state of a resource (often formatted as JSON or XML) transferred between client and server, containing metadata and content.
*   **Idempotent**: APIs where making multiple identical requests yields the exact same response and server state every time.
*   **Content-Negotiation**: The process where a client requests a suitable presentation/format of a resource, or different representations are handled via different URLs.
*   **HATEOAS (Hypermedia as the Engine of Application State)**: Providing hyperlinks within the response message to help clients dynamically navigate related resources and operations.
*   **JWT (JSON Web Token)**: A standardized, optionally validated/encrypted container format used to securely transfer information and authorization details between parties.
*   **CSRF (Cross-Site Request Forgery)**: A security attack targeting state-changing requests (PUT, POST, DELETE) which must be mitigated using tokens.
*   **XXE**: XML External Entity attacks, a specific vulnerability in XML parsing.

@Objectives
*   Design APIs that serve as the standard for process, data, and application integration across web, mobile, cloud, and IoT environments.
*   Adhere strictly to the REST architectural constraints: Client-Server separation, Stateless communication, Cacheability, Uniform Interface, and Layered Systems.
*   Ensure APIs fulfill essential Non-Functional Requirements (NFRs): Performance, Scalability, Modifiability, Portability, and Reliability.
*   Implement standardized RESTful design patterns including versioning, URI templates, pagination, sorting, filtering, and bulk operations to optimize network bandwidth and developer experience (DX).
*   Enforce rigorous API security through stateless authentication (JWT/OAuth2), method whitelisting, input validation, secure parsing, and cryptography (TLS/Mutually-authenticated certs).

@Guidelines

**Architectural Constraints & Uniform Interface**
*   The AI MUST ensure a clear separation of concerns between clients and servers so they can evolve independently.
*   The AI MUST enforce stateless communication: server machines MUST NOT store client session information. Every request MUST carry all relevant information.
*   The AI MUST design responses to be cacheable by clients to reduce network traffic and latency.
*   The AI MUST use standard HTTP methods for interactions: GET (retrieve), PUT (update/replace), POST (create), DELETE (remove), along with HEAD and OPTIONS for metadata.
*   The AI MUST structure endpoints using nouns for resources/arguments and HTTP verbs for actions.

**Representations & Media Types**
*   The AI MUST specify representation formats using media types (MIME types) in the `Content-Type` header (e.g., `application/json`, `application/xml`).
*   The AI MUST support compression of resource representations to save network bandwidth and storage.
*   The AI MUST implement Content-Negotiation, evaluating the `Accept` header to determine the preferred order of response types.

**Idempotency**
*   The AI MUST design GET, PUT, and DELETE operations to be strictly idempotent.
*   The AI MUST treat POST operations as non-idempotent.

**REST API Design Patterns**
*   **URI Templates**: The AI MUST use URIs with placeholders (named substitution variables) to define where resources reside.
*   **Versioning**: The AI MUST attach version numbers to APIs to ensure backward compatibility and track API evolution.
*   **Bulk Operations**: The AI MUST use coarse-grained methods for bulk operations to minimize multiple requests and conserve network bandwidth.
*   **Pagination**: The AI MUST implement pagination for endpoints returning large datasets to reduce payload size and prevent unnecessary server processing.
*   **Sorting**: The AI MUST implement sorting using a `sort` or `sort_by` URL parameter accepting comma-separated attribute names, supporting ascending and descending order.
*   **Filtering**: The AI MUST implement filtering via URL parameters (e.g., `?state=active`). For advanced filtering, the AI MUST encode property name, operator, and filter value.
*   **Unicode**: The AI MUST ensure APIs and URLs support Unicode characters for internationalization.
*   **HATEOAS**: The AI MUST embed hyperlinks in GET responses to provide clients with metadata regarding related resources and available operations.
*   **Swagger Documentation**: The AI MUST use automated tools like Swagger to document API usage, inputs, outputs, and metadata.
*   **HTTP Status Codes**: The AI MUST return accurate HTTP status codes to communicate the success or failure states of the server.
*   **Error Logging**: The AI MUST implement detailed error logging for both client request errors and API internal errors to facilitate error analytics.

**API Security Design Patterns**
*   **Stateless Authentication & Authorization**: The AI MUST use JWT with OAuth2 for user authentication and encrypted API keys in headers for service-to-service communication.
*   **Method Whitelisting**: The AI MUST restrict endpoints to accept only correct, explicitly allowed HTTP methods and reject others with appropriate error messages.
*   **CSRF Protection**: The AI MUST protect PUT, POST, and DELETE requests from CSRF using token-based approaches and XSS prevention.
*   **Input Validation**: The AI MUST validate input on both client and server sides. The AI MUST log validation failures and implement rate-limiting if failures surge.
*   **URL Validation**: The AI MUST validate the URL, query strings, headers, cookies, and form fields against tampering.
*   **Secure Parsing & Content Verification**: The AI MUST NOT assume the content type. It MUST verify that the incoming content matches the `Content-Type` header and securely parse XML/JSON (e.g., using XML serializers to prevent XML injection, XXE, and signature wrapping).
*   **Cryptography & Integrity**: The AI MUST mandate TLS for all data in transit. The AI MUST use message digest/hashing algorithms to ensure message integrity and prevent tampering.

@Workflow
1.  **Resource Identification & URI Design**: Define the resources (nouns) the API will expose. Group them into homogeneous collections. Define URI templates for addressing specific resources.
2.  **Method Assignment & Idempotency Check**: Assign HTTP verbs (GET, POST, PUT, DELETE) to the resources. Verify that GET, PUT, and DELETE handlers are strictly idempotent.
3.  **Data Representation & Content Negotiation**: Define JSON/XML payloads. Setup `Content-Type` verification and `Accept` header negotiation logic. Implement payload compression capabilities.
4.  **Implement Advanced Design Patterns**: 
    *   Add `sort` / `sort_by` and filtering parameters to collection endpoints.
    *   Implement pagination logic to prevent large data dumps.
    *   Add HATEOAS links to GET responses.
    *   Implement coarse-grained endpoints for bulk operations if applicable.
5.  **Integrate Security Controls**:
    *   Apply JWT/OAuth2 stateless authentication.
    *   Implement strict method whitelisting.
    *   Add server-side input, URL, and payload validation. Ensure XML/JSON parsers are secure.
    *   Add CSRF tokens for state-changing methods.
6.  **Error Handling & Documentation**: Map exceptions to standard HTTP status codes. Set up comprehensive error logging. Generate Swagger documentation for the finished API.

@Examples

**URI Design & HTTP Methods**
*   [DO]: Use nouns and HTTP verbs: `GET /users/123` or `POST /users`.
*   [DON'T]: Use verbs in the URI or violate idempotency: `POST /getUser/123` or `GET /users/123/delete`.

**Filtering, Sorting, and Pagination**
*   [DO]: Implement query parameters for collection manipulation: `GET /products?state=active&sort=-price&limit=50&offset=100`.
*   [DON'T]: Create separate endpoints for different views or return millions of records at once: `GET /getActiveProductsSortedByPriceDescending`.

**Content Verification and Security**
*   [DO]: Validate that the payload matches the declared type before parsing.
    ```python
    if request.headers['Content-Type'] != 'application/json':
        return HTTP_415_UNSUPPORTED_MEDIA_TYPE
    # Proceed with secure JSON parsing
    ```
*   [DON'T]: Blindly parse incoming payloads without checking the `Content-Type` header, exposing the server to injection or parsing vulnerabilities.

**Authentication**
*   [DO]: Use JWT tokens in the `Authorization` header for stateless validation across distributed microservices.
*   [DON'T]: Rely on server-side stored session IDs/cookies for authentication, as it breaks the stateless architectural constraint and hinders horizontal scalability.

**HATEOAS Implementation**
*   [DO]: Include navigational links in the response.
    ```json
    {
      "id": 1234,
      "name": "Sample Product",
      "links": [
        { "rel": "self", "href": "/products/1234" },
        { "rel": "update", "href": "/products/1234", "method": "PUT" }
      ]
    }
    ```
*   [DON'T]: Return isolated data that forces the client to hardcode or guess the URIs for subsequent operations.