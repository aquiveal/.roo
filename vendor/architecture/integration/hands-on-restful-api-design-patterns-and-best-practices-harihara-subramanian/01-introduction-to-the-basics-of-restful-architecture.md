# @Domain

These rules MUST be triggered whenever the AI is tasked with designing, implementing, refactoring, evaluating, or documenting web services, Web APIs, software architectures, or specifically RESTful service communications. The rules apply to all tasks involving client-server interactions, data exchange over the World Wide Web (WWW), resource modeling, and HTTP-based network communications.

# @Vocabulary

- **Web 3.0**: The executing semantic web or read-write-execute web, characterized by decentralized services, data-driven behaviors, and combining semantic and web services.
- **Web Services Architecture (WSA)**: A method of standardized communication consisting of a Service Provider, Service Consumer, and Service Broker, traditionally using XML/JSON, SOAP, WSDL, and UDDI.
- **Service-Oriented Architecture (SOA)**: An architectural style consisting of well-defined, self-contained collections of services that are independent of other service contexts and states.
- **Resource-Oriented Architecture (ROA)**: A structural design foundation for the semantic web utilizing basic web technologies (HTTP, URI, XML/JSON) to expose business entities as addressable resources.
- **Resource**: An explicit reference to an entity that can be identified, assigned, and referenced via a URI (e.g., servers, devices, datasets).
- **Addressability**: The practice of exposing datasets or functionalities as a resource accessible through URIs.
- **Representational State Transfer (REST)**: An architectural style providing guidelines for distributed hypermedia systems to communicate directly using existing web protocols (HTTP), revolving around the concept of resources.
- **Application State**: Data stored on the server side that helps identify incoming client requests using previous interaction details. (Statelessness dictates the server MUST NOT store this).
- **Resource State**: The current state of the server/resource at any given point in time; also referred to as a resource representation.
- **Session Stickiness (Session Affinity)**: A process of creating an affinity between a client and a specific server; strictly prohibited in RESTful design.
- **Richardson Maturity Model (RMM)**: A model developed by Leonard Richardson breaking down REST into levels. An API must achieve Level-3 (Hypermedia Controls) to be fully qualified as RESTful.
- **HATEOAS**: Hypermedia as the Engine of Application State. Application state representations that include links to related resources, allowing clients to programmatically navigate the API.
- **Intermediaries**: Event-driven middleware components, proxies, or gateways situated between the client and server to provide data translation, security, and performance enhancements.
- **Code on Demand (COD)**: An optional REST constraint enabling servers to send software code (e.g., JavaScript) to clients to be executed locally.

# @Objectives

- Ensure all web services strictly adhere to the five mandatory REST constraints: Client-Server, Statelessness, Cacheable, Uniform Interface, and Layered Systems.
- Attain the architectural goals of REST: Performance, Scalability, Simplicity, Modifiability, Visibility, Portability, Reliability, and Testability.
- Decouple the user interface (client) from data storage (server) to improve portability and independent scalability.
- Enforce Level-3 of the Richardson Maturity Model (RMM) for all RESTful APIs by implementing HATEOAS.
- Design self-descriptive messages that do not rely on server-side stored contexts or sessions.

# @Guidelines

## General Architecture & Web APIs
- When developing Web APIs, the AI MUST expose server-side interfaces through standard web representations (JSON/XML) without requiring complex web service protocols like SOAP/WSDL, unless explicitly requested.
- The AI MUST model every business entity as a "Resource" accessible through a unique URI.

## ROA & HTTP Operations
- When implementing operations in a Resource-Oriented Architecture, the AI MUST map HTTP methods precisely as defined by the text's ROA guidelines:
  - `GET`: Read the resource representations.
  - `PUT`: Create a new resource.
  - `DELETE`: Delete the resource (and optionally linked resources).
  - `POST`: Modify the resource.
  - `HEAD`: Retrieve Meta information of the resource.
- The AI MUST ensure that resource identification is completely independent of its values (two distinct resources may point to the same data at a given time but remain separate resources).

## Constraint 1: Client-Server
- The AI MUST enforce a strict separation of concerns. The server provides services (data storage/processing), and the client handles the user interface and requests. Both MUST be standalone, independent, testable components.

## Constraint 2: Statelessness
- The AI MUST NOT implement session stickiness or session affinity on the server.
- The AI MUST enforce that every client request is completely self-contained, carrying all explicit application state information required for the server to understand and process the request independently.
- The AI MUST ensure the server includes any necessary information in its response that the client may need to create or maintain a state on the client side.

## Constraint 3: Cacheable
- The AI MUST implicitly or explicitly label all responses as cacheable or non-cacheable.
- The AI MUST utilize HTTP cache control headers to fine-tune caching behaviors. Required headers to consider include:
  - `Expires`: To represent the date/time after which a response is stale.
  - `Cache-control`: To define caching directives (`max-age`, extensions).
  - `ETag`: As a unique identifier for server resource states.
  - `Last-modified`: To identify the time the response was generated.

## Constraint 4: Uniform Interface
- **Identification of Resources**: The AI MUST assign stable URIs. The semantics of the mapping of a URI to a resource MUST NOT change.
- **Manipulation of Resources**: The AI MUST decouple the resource's representation from the URI. The API MUST support dynamic media types (e.g., JSON, XML) dictated by the client's `Accept` HTTP header.
- **Self-Descriptive Messages**: The AI MUST utilize constrained message types (GET, HEAD, OPTIONS, PUT, POST, DELETE). Messages MUST include metadata detailing resource state, representation format, and size.
- **HATEOAS**: The AI MUST embed hypermedia links within the response representation to inform the client of possible ways to change its application state. A REST API without HATEOAS MUST be treated as incomplete.

## Constraint 5: Layered Systems
- The AI MUST design the architecture such that a specific layer only communicates with the layer immediately above or below it.
- The AI MUST NOT allow request and response messages to divulge details to the recipients about which underlying layer the message originated from.
- The AI MUST allow for the insertion of intermediaries (proxies, gateways, load balancers) without requiring any changes to the service consumers.

## Constraint 6: Code on Demand (Optional)
- The AI MAY defer some portions of logic execution to the client by returning executable scripts (Code on Demand) IF flexibility is required, while acknowledging this reduces the visibility of the underlying API.

# @Workflow

When instructed to design or implement a RESTful API, the AI MUST execute the following algorithmic process:

1. **Resource Identification & Modeling**: 
   - Identify all business entities.
   - Define a unique, stable URI for every entity (Resource).
2. **Determine Representations**: 
   - Define the supported media types (JSON, XML).
   - Implement logic to read the client's `Accept` header to serve the appropriate format.
3. **Map HTTP Methods**:
   - Assign the appropriate ROA HTTP verbs (`GET` for read, `PUT` for create, `POST` for modify, `DELETE` for removal, `HEAD` for meta-info).
4. **Enforce Statelessness**:
   - Strip any server-side session management.
   - Ensure the request schema forces the client to pass all necessary application state context.
5. **Implement Caching**:
   - Evaluate the volatility of each resource.
   - Inject `Cache-control`, `ETag`, `Expires`, and `Last-modified` headers into the response payload logic.
6. **Implement HATEOAS (RMM Level-3)**:
   - For every response payload, append a hypermedia block (e.g., a `links` array) that provides URIs and HTTP methods for the next available application state transitions.
7. **Architect Layering**:
   - Separate the API facade/controller from the underlying data and authentication servers, ensuring no cross-layer contamination of knowledge.

# @Examples (Do's and Don'ts)

## Statelessness
- **[DO]**: Pass complete context in every request.
  ```http
  GET /api/v1/direct_messages.json?since_id=12345&count=100 HTTP/1.1
  Authorization: Bearer <token>
  ```
- **[DON'T]**: Rely on the server remembering the client's position from a previous request.
  ```http
  GET /api/v1/direct_messages/next_page HTTP/1.1
  Cookie: session_id=abcxyz
  ```

## Uniform Interface (Manipulation of Resources via Accept Header)
- **[DO]**: Serve dynamic representations based on headers.
  ```http
  // Request
  GET /api/v1/resources/1 HTTP/1.1
  Accept: application/xml

  // Response
  Content-Type: application/xml
  <resource><id>1</id></resource>
  ```
- **[DON'T]**: Hardcode representations into the URI scheme.
  ```http
  GET /api/v1/resources/1/get_xml HTTP/1.1
  ```

## HATEOAS (Hypermedia as the Engine of Application State)
- **[DO]**: Provide hypermedia links to the next available application states.
  ```json
  {
    "accountId": "12345",
    "balance": 100.00,
    "links": [
      {
        "rel": "deposit",
        "href": "/accounts/12345/deposit",
        "method": "POST"
      },
      {
        "rel": "withdraw",
        "href": "/accounts/12345/withdraw",
        "method": "POST"
      }
    ]
  }
  ```
- **[DON'T]**: Return dead-end data requiring the client to guess or hardcode the next URIs.
  ```json
  {
    "accountId": "12345",
    "balance": 100.00
  }
  ```

## Caching
- **[DO]**: Include explicit cache directives in the self-descriptive message.
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/json
  Cache-Control: max-age=4500, must-revalidate
  ETag: "uqv2309u324klm"
  Last-Modified: Fri, 12 Jan 2018 18:00:09 GMT
  ```
- **[DON'T]**: Leave caching ambiguous, forcing the client to continuously re-fetch static data.
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/json
  // Missing Cache-Control, ETag, and Last-Modified
  ```

## HTTP Verbs (ROA text definitions)
- **[DO]**: Use `PUT` to create a new resource, and `POST` to modify an existing one, strictly according to the text's ROA definitions.
  ```http
  PUT /booktitles.com/resources HTTP/1.1
  // Creates a new collection

  POST /booktitles.com/resources/title18 HTTP/1.1
  // Modifies title 18
  ```
- **[DON'T]**: Rely on arbitrary or custom verbs for actions.
  ```http
  GET /booktitles.com/resources/title18/update?name=newtitle HTTP/1.1
  ```