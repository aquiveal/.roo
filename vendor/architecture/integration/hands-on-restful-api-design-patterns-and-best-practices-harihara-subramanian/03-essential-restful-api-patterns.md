@Domain
When the user requests to design, implement, review, or refactor RESTful API endpoints, particularly using Java and Spring Boot, or when evaluating REST API architecture, routing patterns, response formatting, and error handling.

@Vocabulary
- **Statelessness**: The property of a server being completely free from storing client application states; all requests must be independent and self-contained with necessary context and credentials.
- **Content Negotiation**: The mechanism allowing services and clients to select the resource representation format (e.g., JSON, XML, GIF, PNG) for their communication, primarily using HTTP headers.
- **Agent-driven Negotiation (Reactive Negotiation)**: Client-side selection of content representation using the `Accept` request header (the preferred REST API approach).
- **Server-driven Negotiation (Proactive Negotiation)**: Server-side determination of content representation (considered complex and less preferred).
- **URI Templates**: The practice of describing a set of resources as variables within a URI using curly braces (e.g., `{resource_id}`).
- **Design for Intent**: A design strategy where changes to one object automatically propagate changes to related objects (cascading effect) to satisfy use cases without exposing internal business objects.
- **Pagination**: A resource representation mechanism for serving subsets of massive data responses using URI queries, preventing server performance degradation.
- **Offset-based Pagination**: Pagination relying on a starting point and maximum count (e.g., `offset` and `limit`).
- **Time-based Pagination**: Pagination relying on a specific timeframe (e.g., `since` and `until`).
- **Cursor-based Pagination**: Pagination relying on a pointer or bookmark reference (e.g., `cursor` or `token`) for remaining data.
- **Discoverability**: The descriptive capability of a server to instruct the client on how to use the API via HTTP status codes, `Allow` headers, `Location` headers, and `Link` headers.
- **Unicode**: An encoding standard (e.g., UTF-8) allowing APIs to seamlessly support international character sets and multiple languages.

@Objectives
- Guarantee strictly stateless server-client communication for maximum scalability and traceability.
- Implement robust agent-driven content negotiation to serve varied media types based on explicit client preference.
- Design clear, dynamic, and predictable endpoints using URI templates.
- Abstract internal business complexities by using "Design for Intent" cascading logic in the service layer.
- Optimize data retrieval and prevent server overload using standard query-based pagination techniques.
- Maximize API discoverability by strictly adhering to HTTP protocol standards for creations, invalid methods, and navigation links.

@Guidelines

### 1. Statelessness
- The AI MUST NOT maintain session affinity or stickiness on the server.
- The AI MUST NOT use server-side sessions (e.g., `HttpSession`) to store authentication or authorization information. 
- The AI MUST require the client to provide all necessary context and credentials with every single request.

### 2. Content Negotiation
- The AI MUST implement agent-driven content negotiation using the `Accept` HTTP header.
- The AI MUST provide a pre-configured default representation (e.g., `application/json`) if no `Accept` header is present in the client request.
- The AI MUST return a `406 Not Acceptable` HTTP status code if the client's requested media type cannot be served.
- The AI MAY support content negotiation via specific URI extensions (e.g., `/courses.json`, `/courses.xml`) or query parameters (e.g., `?format=xml`) if header-based negotiation is not feasible.

### 3. URI Templates
- The AI MUST use curly braces `{}` to define variables or resource identifiers within URIs (e.g., `/api/{resource_id}`).
- When using Spring Boot, the AI MUST bind these URI template variables to method parameters using the `@PathVariable` annotation.

### 4. Design for Intent
- The AI MUST NOT expose internal business objects directly to the API consumer.
- The AI MUST encapsulate cascading effects within the service layer (e.g., if a client adds a stock, the API automatically updates the overall investor portfolio calculations in the background without requiring explicit client commands).

### 5. Pagination
- The AI MUST treat pagination as a resource *representation*, NOT as a distinct resource.
- The AI MUST implement pagination parameters strictly as URI **queries** (e.g., `?page=2`), NEVER as URI **paths** (e.g., `/page/2`).
- The AI MUST implement one of the three standard pagination variants:
  1. Offset-based: Use `offset` and `limit` parameters.
  2. Time-based: Use `since` and `until` parameters (can be combined with `limit`).
  3. Cursor-based: Use a `cursor` or `token` parameter along with a `limit`.

### 6. Discoverability
- The AI MUST implement discoverability for invalid requests by returning `405 Method Not Allowed` accompanied by an `Allow` header detailing the supported HTTP methods.
- The AI MUST implement discoverability for resource creation (POST) by returning a `201 Created` status code accompanied by a `Location` header containing the exact URI of the newly created resource.
- The AI SHOULD utilize `Link` headers to provide clues and valid URLs for next possible actions (HATEOAS).

### 7. Error and Exception Logging
- The AI MUST use existing, standard HTTP status codes (e.g., `401`, `404`, `405`) to communicate execution errors and resource leaks.
- The AI MUST provide customized, human-readable JSON error messages explaining the context of the failure.
- The AI MUST map application-specific exceptions (e.g., `ResourceNotFoundException`) to appropriate HTTP status codes using framework-specific error handling.

### 8. Unicode
- The AI MUST explicitly support internationalization by applying the `charset=UTF-8` directive in HTTP headers (e.g., `Accept-Encoding`, `Content-Type`).

@Workflow
1. **Endpoint Definition**: Define the API URI utilizing URI templates with `{}` for dynamic segments. Map these using `@PathVariable`.
2. **Statelessness Check**: Validate that the endpoint relies entirely on incoming request parameters, headers, and payloads, without accessing server-side session context.
3. **Content Negotiation Setup**: Configure the controller to produce specific media types (e.g., `produces = {MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE}`). Ensure a `406 Not Acceptable` handler is active for unsupported types.
4. **Pagination Integration**: If the endpoint returns a collection, inject `@RequestParam` variables for offset/limit, since/until, or cursor/token.
5. **Intent Implementation**: Delegate the business logic to a service class that handles any cascading updates required by the transaction (Design for Intent) before returning the final representation.
6. **Discoverability Enforcement**: 
   - If it is a POST method, construct the URI of the newly created resource using `ServletUriComponentsBuilder`, inject it into the `Location` header, and return HTTP `201`.
   - Ensure generic exception handlers catch unsupported methods and return HTTP `405` with the `Allow` header.
7. **Error Formatting & Unicode**: Ensure all custom exceptions return standard HTTP codes with descriptive JSON bodies. Append `charset=UTF-8` to text/JSON responses.

@Examples (Do's and Don'ts)

### Statelessness
- [DO]: Require authorization tokens and context in every request header/body.
- [DON'T]: Store user login state in `HttpSession` or rely on server-side memory to track the client's current workflow step.

### Content Negotiation
- [DO]: 
  ```java
  @GetMapping(path="/investors/{id}", produces={MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE})
  ```
- [DON'T]: Hardcode the response generation to a single format while ignoring the client's `Accept` header without returning a `406 Not Acceptable`.

### URI Templates
- [DO]: `/investors/{investorId}/stocks/{symbol}` mapped with `@PathVariable String investorId, @PathVariable String symbol`.
- [DON'T]: `/investors/stocks?investorId=123&symbol=AAPL` (Do not use query parameters to identify a specific, hierarchical resource).

### Pagination
- [DO]: `/stocks?offset=10&limit=5` using `@RequestParam(value="offset", defaultValue="0") int offset`.
- [DON'T]: `/stocks/page/2` (Do not treat a page as a distinct REST resource path).

### Discoverability (Valid HTTP Methods)
- [DO]: Return `405 Method Not Allowed` with the header `Allow: GET, POST` when a client attempts a `DELETE` on a read-only endpoint.
- [DON'T]: Return `500 Internal Server Error` when a client uses the wrong HTTP verb.

### Discoverability (Resource Creation)
- [DO]: 
  ```java
  URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(newId).toUri();
  return ResponseEntity.created(location).build();
  ```
- [DON'T]: Return `200 OK` with a simple success message and no `Location` header when a new resource is successfully inserted via POST.

### Error Handling
- [DO]: Return a `404 Not Found` with a custom JSON body `{"Status": 404, "error": "Investor Not Found"}` by utilizing a custom `InvestorNotFoundException`.
- [DON'T]: Let the application crash and return a generic Tomcat/Spring `500 Internal Server Error` stack trace to the API consumer.

### Unicode
- [DO]: `@GetMapping(value="/welcome", produces="application/json;charset=UTF-8")`
- [DON'T]: Send internationalized text (like Japanese characters) using the default system charset, risking garbled text on the client side.