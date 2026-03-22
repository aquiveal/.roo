# @Domain
These rules MUST be triggered when the AI is tasked with designing, implementing, refactoring, or reviewing RESTful APIs, specifically involving API versioning, security/authorization implementation, downstream service communication (resiliency), data modification of single or multiple records, endpoint deprecation/migration, or building APIs that serve heterogeneous client devices (e.g., mobile vs. desktop).

# @Vocabulary
- **API Facade**: A pattern that abstracts a complex subsystem or multiple backend service calls from the caller, exposing only necessary details via a single, simplified interface to improve scalability and performance.
- **Backend for Frontend (BFF)**: A pattern that introduces a dedicated interface layer tailored to a specific user experience or device (e.g., one for mobile, one for desktop) to optimize payload formatting and network trips, avoiding the customization of a single general-purpose backend.
- **Basic Authentication**: A standard HTTP header authorization scheme where user credentials (`username:password`) are encoded in Base64.
- **Bulk Operation**: A pattern that groups multiple items in a single API request (usually via `PATCH`) to reduce network round-trips, utilizing custom headers to identify the bulk action intent.
- **Circuit Breaker**: A resilience pattern that prevents cascading system failures when downstream services fail. It operates in three states: Closed (normal), Open (failing, returning graceful errors/fallback), and Half-open (periodically checking if failure is resolved).
- **Content-Negotiation Versioning**: Providing API version information through the HTTP `Accept` header along with the content-type (media), considered the most REST-compliant versioning method.
- **Endpoint Redirection**: A pattern to handle changed/deprecated service endpoints by returning standard HTTP `3xx` codes (301, 307) and providing the new URI in the `Location` header.
- **Entity Endpoints**: Exposing specific entities as individual, lightweight endpoints (e.g., `/investors/{investorId}`) rather than requiring consumers to manage compound identifiers.
- **Idempotent**: An operation that produces the same result on the server regardless of how many times it is executed (e.g., `PUT`, `PATCH`, `DELETE`).
- **Uniform Contract**: Standardizing service contracts across endpoints by abstracting endpoints from individual capabilities and strictly using standard HTTP verbs for execution.

# @Objectives
- Ensure API changes do not break existing clients by implementing structured, REST-compliant versioning strategies.
- Prevent cascading system failures across distributed services by enforcing resilient communication patterns (Circuit Breaker combined with Retry).
- Optimize network performance and reduce round-trips by implementing Bulk Operations and API Facades.
- Tailor API responses to specific client form factors (mobile vs. web) without polluting core backend services using the Backend for Frontend (BFF) pattern.
- Guarantee safe, repeatable data operations by strictly enforcing HTTP idempotency and concurrency controls.
- Secure API endpoints using encrypted transport and proper separation of authentication and authorization.

# @Guidelines

## API Versioning Rules
- The AI MUST increment the MAJOR version when introducing breaking changes (e.g., response data changes, response type changes, removing parts of the API).
- The AI MUST increment the MINOR version when introducing backward-compatible enhancements or bug fixes.
- The AI MUST prefer **Content-Negotiation Versioning** (using the `Accept` header) or **Custom Headers** (e.g., `x-resource-version`) to maintain URI consistency.
- The AI MAY use **URI Path Versioning** (e.g., `/v1/resource`) or **Query Parameter Versioning** (e.g., `?version=1.1`) ONLY IF explicitly requested by the user, while acknowledging that URI versioning violates strict RESTful URI representation principles.

## Security and Authorization
- The AI MUST enforce Basic Authentication over HTTPS/SSL ONLY, as Base64 encoding is not encryption and is vulnerable to packet sniffing.
- The AI MUST clearly separate Authentication (verifying who the user is) from Authorization (verifying what the user is allowed to do, usually via roles like `ADMIN` or `USER`).
- The AI MUST NOT store stateful authentication/authorization sessions on the server; the REST API must remain stateless, requiring credentials/tokens with every request.

## Service Contract and Endpoint Design
- The AI MUST implement a **Uniform Contract** using standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) to express underlying actions.
- The AI MUST NOT use action-based URIs (e.g., `/deleteUser`).
- The AI MUST use **Entity Endpoints** to expose reusable, lightweight resources (e.g., `/users/{id}/orders/{orderId}`).
- When migrating or deprecating an endpoint, the AI MUST implement **Endpoint Redirection** by returning an HTTP `301 Moved Permanently` or `307 Temporary Redirect` status code and providing the new URI inside the HTTP `Location` response header.

## Idempotency and Concurrency
- The AI MUST ensure that `PUT`, `PATCH`, and `DELETE` endpoints are fully idempotent. Repeatedly executing them due to intermittent network failures MUST NOT produce unintended side effects.
- For concurrency control in idempotent updates, the AI MUST utilize the `E-Tag` header. If a resource is in an inconsistent state during an update, the AI MUST return an HTTP `409 Conflict` status code.

## Bulk Operations
- The AI MUST NOT create separate, non-RESTful URIs for bulk operations (e.g., `/users/bulk-update`).
- The AI MUST reuse the existing resource endpoint (e.g., a `PATCH` request to `/users`) but accept an array/list of objects in the request body.
- The AI MUST require a custom HTTP header (e.g., `x-bulk-patch: true`) to explicitly identify the client's intent to perform a bulk operation.

## Resilience (Circuit Breaker & Retry)
- When writing code that calls external or downstream microservices, the AI MUST wrap the call in a **Circuit Breaker** pattern (e.g., using Hystrix or an equivalent resilience library).
- The AI MUST provide a graceful `fallbackMethod` to return default data or a safe error message when the downstream service is unavailable (Circuit Breaker is Open).
- The AI MUST implement an intelligent **Retry Pattern** alongside the Circuit Breaker. The Retry logic MUST abandon retries immediately if the Circuit Breaker indicates a non-transient failure (to prevent Denial of Service attacks on failing services).

## API Facade and Backend for Frontend (BFF)
- If a client workflow requires calling multiple fine-grained APIs to achieve a single business goal, the AI MUST create an **API Facade** to orchestrate these calls on the server side, exposing a single endpoint to the client.
- If an API must serve highly heterogeneous clients (e.g., a resource-constrained mobile app vs. a data-heavy desktop web app), the AI MUST implement the **Backend for Frontend (BFF)** pattern.
- The AI MUST create distinct interface layers for each client type to format payload size and structure individually, preventing a single backend from becoming bloated with client-specific conditional logic.
- The AI MUST acknowledge and account for the drawback of BFF by ensuring shared logic is pushed down to the core microservices to prevent defect leaks and security lapses in the BFF layers.

# @Workflow
When tasked with creating or refactoring a RESTful API endpoint, the AI MUST execute the following algorithmic process:

1. **Contract Definition**: Define the resource URI as an Entity Endpoint. Map the required action strictly to the appropriate HTTP verb (GET, POST, PUT, PATCH, DELETE).
2. **Versioning Strategy**: Determine the API version. Define the `Accept` header or custom version header requirements. Do not embed the version in the URI path unless strictly constrained by legacy architecture.
3. **Payload & Bulk Assessment**: Determine if the endpoint needs to modify single or multiple items. If multiple, design a Bulk Operation leveraging a list/array payload and a custom `x-bulk-operation` header applied to the standard endpoint.
4. **Idempotency & Concurrency Check**: If the method is PUT, PATCH, or DELETE, implement E-Tag validation. Write logic to return `409 Conflict` if states mismatch. Ensure duplicate requests process safely.
5. **Security Verification**: Wrap the endpoint in stateless Authorization checks. Ensure transport requires HTTPS.
6. **Downstream Integration (Resiliency)**: If the endpoint calls other microservices, wrap the HTTP client call in a Circuit Breaker. Define and implement the fallback method.
7. **Client Formatting (BFF/Facade)**: Check the target clients. If mobile and web require drastically different payloads, split the endpoint into distinct BFF controllers. If the endpoint requires aggregating 3+ downstream services, wrap the logic in a Facade interface.

# @Examples (Do's and Don'ts)

## Versioning
- **[DO]**: Use Content-Negotiation for versioning.
  ```java
  @GetMapping(value = "/investors", headers = "Accept=application/investors-v1.1+json")
  public List<Investor> fetchAllInvestors() { ... }
  ```
- **[DON'T]**: Hardcode versions in the URI path unnecessarily, violating resource representation.
  ```java
  @GetMapping("/v2/investors")
  public List<Investor> fetchAllInvestors() { ... }
  ```

## Bulk Operations
- **[DO]**: Use a custom header and an array payload on the standard resource path.
  ```java
  @PatchMapping("/investors/{id}/stocks")
  public ResponseEntity<Void> updateStocks(
      @PathVariable String id,
      @RequestHeader(value = "x-bulk-patch") boolean isBulk,
      @RequestBody List<Stock> stocks) { ... }
  ```
- **[DON'T]**: Create action-based URIs for bulk operations.
  ```java
  @PostMapping("/investors/{id}/stocks/bulkUpdate")
  public ResponseEntity<Void> updateStocks(@RequestBody List<Stock> stocks) { ... }
  ```

## Endpoint Redirection
- **[DO]**: Return a 301/307 status code and a Location header when an endpoint moves.
  ```http
  HTTP/1.1 301 Moved Permanently
  Location: /api/new-resource-endpoint
  ```
- **[DON'T]**: Return a 404 or a 200 with a custom JSON error message stating the endpoint has moved.

## Circuit Breaker
- **[DO]**: Implement a fallback method for downstream calls.
  ```java
  @HystrixCommand(fallbackMethod="downstreamFailureFallback")
  public String callDownstreamService() {
      return restTemplate.getForObject(URI, String.class);
  }
  public String downstreamFailureFallback() {
      return "Service temporarily unavailable. Please try again later.";
  }
  ```
- **[DON'T]**: Call downstream microservices without wrapping them in failure detection, risking thread exhaustion and cascading system crashes.