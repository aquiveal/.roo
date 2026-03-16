# @Domain

This rule file is triggered when the AI is tasked with designing, modifying, implementing, or testing Application Programming Interfaces (APIs), remote procedure calls (RPCs), message queues, or service-to-service communication architectures. It applies whenever the AI handles data format specifications (JSON, XML, etc.), backward compatibility, API versioning, integration testing, and contract testing between consumer and provider services.

# @Vocabulary

*   **Robustness Principle (Postel's Law)**: "Be conservative in what you do, be liberal in what you accept from others." The foundational rule for building robust distributed systems.
*   **Layered Agreements**: The stack of implicit and explicit contracts between services, including connection handshaking, request framing, content encoding, message syntax, message semantics, and authorization.
*   **Breaking Change**: Any unilateral break from a prior agreement, such as adding a required field, forbidding optional information, or removing guaranteed response data.
*   **Nonbreaking Change**: Safe modifications, characterized by covariant requests and contravariant responses (e.g., accepting a superset of inputs or returning a superset of outputs).
*   **Implementation Gap**: The disparity between a published specification and what the implementation actually accepts. Once public, the implementation becomes the de facto specification.
*   **Version Discriminator**: A mechanism (URL prefix, query parameter, HTTP header, or request body field) used to explicitly declare the version of an API protocol being used.
*   **Inbound Testing**: Using generative testing to exercise your own API to uncover gaps between the specification and the implementation.
*   **Outbound Testing**: Using randomized, generative tests against the specifications of external services to verify your system's assumptions about those dependencies.
*   **Contract Testing**: Tests owned by the calling service that verify conformance to specific edges of a provider's specification without invoking the live provider.

# @Objectives

*   Prevent consumers of a service from being forced to coordinate their deployments with the provider's deployment schedule.
*   Preserve backward compatibility ruthlessly to minimize the migration cost pushed onto other development teams.
*   Design APIs and service boundaries that safely handle unpredictable, malformed, or partially updated inputs from consumers or providers.
*   Isolate the testing of integration points so that tests verify contract conformance rather than over-specifying responses from live remote systems.

# @Guidelines

*   **Applying the Robustness Principle**: When parsing or handling input from external consumers or providers, the AI MUST accept any structurally valid input that can be safely processed, even if it contains unexpected or undocumented fields.
*   **Evaluating API Changes**: Before modifying an endpoint, the AI MUST classify the change against the Layered Agreements. 
    *   The AI MUST NEVER implement the following as they are Breaking Changes: rejecting a previously working network protocol/framing/routing, adding required fields to a request, forbidding previously allowed optional information, removing previously guaranteed information from a response, or requiring an increased level of authorization.
    *   The AI MAY implement the following as they are Nonbreaking Changes: requiring a strict subset of previously required parameters, accepting a superset of previously accepted parameters, returning a superset of previously returned values, and enforcing a subset of previously required constraints.
*   **Handling Specification vs. Implementation Gaps**: When discovering that a public-facing API accepts inputs outside of its documented specification, the AI MUST NOT "tighten" the implementation to reject those inputs. The AI MUST preserve the existing liberal behavior to avoid breaking existing consumers.
*   **Implementing API Versioning**: When a Breaking Change is absolutely required, the AI MUST implement a Version Discriminator.
    *   The AI MUST prefer placing the version discriminator in the URL (e.g., `/v2/`) as it requires no special intermediary configuration and allows easy log analysis.
    *   If the URL method is rejected by the user, the AI MAY use the `Accept`/`Content-Type` headers, a custom header (e.g., `api-version`), or a specific field in the request body.
    *   The AI MUST bump all route versions simultaneously. Do not force consumers to track mixed version numbers for different parts of the same API.
*   **Managing Controller Logic for Versions**: The AI MUST support both old and new API versions side-by-side during a rollout. The AI MUST NOT duplicate the entire business logic for the new version. Instead, the AI MUST update old API controllers to convert old objects to current objects on request, and convert new objects to old objects on response, passing the converted data to the single, current business logic layer.
*   **Publishing Specifications**: The AI MUST define and maintain machine-readable specifications for message formats (e.g., Swagger/OpenAPI) to facilitate contract testing and consumer development.
*   **Defensive Parsing**: When adding new fields to an existing API (e.g., new partner integration requirements), the AI MUST ensure the handler safely processes requests where the new fields are entirely missing, partially provided, or combined unpredictably.
*   **Contract Testing Constraints**: When writing tests for integration points, the AI MUST split the test into two distinct parts:
    1.  Verify that the request generated by the caller strictly conforms to the provider's specification.
    2.  Verify that the caller can safely handle any valid response the provider is permitted to send.
    *   The AI MUST NOT invoke the live external service in these tests. The AI MUST NOT assert against exact data matches that rely on the live state of the remote provider.

# @Workflow

When tasked with modifying an existing API, integrating a new service, or writing tests for service-to-service communication, the AI MUST follow this exact sequence:

1.  **Change Analysis**: Analyze the requested modification. List all added, removed, or modified request/response fields, headers, and routing rules.
2.  **Classification**: Check the change against the Nonbreaking vs. Breaking rules. 
    *   If the change only relaxes constraints, adds optional inputs, or adds outputs, proceed to step 3. 
    *   If the change tightens constraints, adds required inputs, or removes outputs, proceed to Step 4.
3.  **Implement Nonbreaking Change**: Apply the code modifications. Update the OpenAPI/Swagger specification. Ensure no existing loose input handling is restricted. Proceed to Step 6.
4.  **Implement Versioning (Breaking Change)**: 
    *   Create a new versioned route (e.g., `/v2/resource`). 
    *   Keep the `/v1/resource` route intact.
    *   Refactor the underlying business logic to accept the `v2` data model.
    *   Refactor the `v1` controller to translate incoming `v1` requests into `v2` models, call the shared business logic, and translate the `v2` response back into the `v1` format.
5.  **Cross-Version Testing**: Generate tests that mix calls to the old API version and the new API version on the same underlying entities to ensure entities created by the new API do not cause internal server errors when accessed via the old API.
6.  **Contract Testing**: Write or update Contract Tests for the integration point. Write one suite asserting the outgoing request strictly matches the OpenAPI spec. Write a second suite asserting the service safely handles boundary-condition responses (including missing optional fields) dictated by the specification. Do not use live network calls.

# @Examples (Do's and Don'ts)

**Principle: Adding Data to APIs**
*   [DO]: Add a new field to a JSON payload but make it completely optional in the parsing logic, providing a safe default or `null` fallback if the consumer omits it.
*   [DON'T]: Add a new validation rule to an existing public API that rejects requests missing a newly introduced `creditScore` field, immediately breaking all legacy consumers.

**Principle: Fixing Implementation Gaps**
*   [DO]: Update the API documentation to reflect that the `url` field currently accepts any string, effectively documenting the actual permissive behavior of the live system.
*   [DON'T]: Add a strict Regex URL validator to an existing endpoint because the documentation said it should be a URL, thereby causing existing clients sending malformed strings to suddenly receive `400 Bad Request` errors.

**Principle: Implementing Breaking Changes**
*   [DO]: Create `/v2/borrower` that requires the new fields, while maintaining `/v1/borrower` which populates the new required fields with default values before passing the request to the business logic.
*   [DON'T]: Modify the `/borrower` endpoint directly to require the new fields and tell the consuming teams they must deploy their updates at the exact same time as your release.

**Principle: Contract Testing**
*   [DO]: Write a test that validates your `OrderService` generates a JSON payload that conforms to the JSON Schema published by `BillingService`, and a separate test feeding mock JSON responses into `OrderService` to ensure it parses them safely.
*   [DON'T]: Write an integration test that makes an HTTP call to the staging environment of `BillingService`, creates a real billing record, and asserts that the returned ID is `12345`.