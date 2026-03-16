# @Domain
These rules MUST trigger when the AI is tasked with designing, implementing, refactoring, documenting, or reviewing Web APIs, API endpoints, payload structures, API error handling mechanisms, API versioning strategies, or developer onboarding documentation (SDKs, tutorials, guides).

# @Vocabulary
- **Developer Experience (DX)**: The overarching usability, speed, and intuitiveness experienced by a human developer integrating with the API.
- **Tutorial**: An interactive interface or step-by-step document designed to teach developers about the API (e.g., answering questions or filling in code).
- **Guide**: A contextual document providing information for developers at a specific point in time (e.g., getting started, updating, or converting versions).
- **Sandbox**: An interactive online documentation interface where developers can test code and preview API results without needing to implement authentication or write backend code.
- **Machine-Readable Error**: A specific, unambiguous, snake_case string returned programmatically so client code can handle errors without parsing text.
- **Human-Readable Error**: A verbose, personalized error message intended for the developer to read, explaining the exact context of the failure and how to fix it.
- **Translation Layer**: Additional backend infrastructure designed to silently translate internal data models (which may have changed) into the historical format expected by external developers to maintain backward compatibility.
- **Primitive**: A core API building block or access level that enables new, unforeseen workflows without simply mirroring the internal workflows of the host application.
- **Breaking Change**: Any API modification that would cause an existing, previously functioning integration to fail.

# @Objectives
- **Real-Life Utility**: Ground all API design decisions in explicit, real-life third-party developer use cases rather than internal application architecture.
- **Frictionless Onboarding**: Minimize the "Time to Hello World" (TTHW) by designing intuitive structures, recommending sandboxes, and simplifying authentication.
- **Strict Consistency**: Enforce rigid consistency in naming conventions, access patterns, and data types across the entire API surface area.
- **Effortless Troubleshooting**: Create categorized, multi-layered error handling systems (HTTP status, headers, machine-readable codes, human-readable messages) that make debugging immediate and actionable.
- **Future-Proof Extensibility**: Architect APIs to withstand inevitable product changes through early versioning, translation layers, and strategic primitive exposure.

# @Guidelines

## 1. Use Case & Focus Constraints
- The AI MUST NOT design APIs that simply expose internal database schemas or microservice architectures. The design MUST reflect the external developer's required workflow.
- The AI MUST force focus: when designing an endpoint or API suite, the AI MUST explicitly define what the API is *not* going to do. Attempting to solve too many "what-ifs" in a single endpoint is strictly prohibited.
- The AI MUST balance access levels: Do not provide access so low-level that the integration experience is confusing, nor so high-level that integrations can only mirror the host application's exact UI/workflows. Provide "primitives."

## 2. Onboarding & Documentation Constraints
- When generating API documentation, the AI MUST include or recommend a "Getting Started" guide or interactive tutorial.
- The AI MUST recommend frictionless initial access, such as unauthenticated sandbox endpoints, mock data testers, or simple UI-based OAuth token generators.

## 3. Consistency & Naming Constraints
- The AI MUST prioritize consistency over technical "correctness." If an existing system uses a specific term (e.g., `users`), the AI MUST NOT rename it in new endpoints (e.g., `members`) just because the product changed internally.
- The AI MUST strictly enforce data type consistency. A field (e.g., `user`) MUST NOT be an integer ID in one endpoint and an object in another endpoint. If the payload must change, create a newly named field or explicitly version the endpoint.
- The AI MUST enforce consistent error payload formatting. If a successful request returns JSON, an error request MUST return JSON, never HTML or plain text.

## 4. Error Handling Constraints
- The AI MUST categorize all potential API errors into four specific categories: System-level, Business logic, API request formatting, and Authorization.
- The AI MUST define a matrix for all errors containing: HTTP Status Code, HTTP Headers (where applicable), Machine-readable error code, and Human-readable error message.
- The AI MUST NOT leak backend architecture, database connection strings, or internal stack traces to the API response. System-level errors must be occluded behind generic 500-level responses.
- The AI MUST use highly specific, actionable machine-readable codes (e.g., `charge_already_refunded`) instead of generic codes (e.g., `cannot_refund`).
- The AI MUST recommend formatting errors following RFC 7807 (Problem Details for HTTP APIs) when structuring complex error responses.
- The AI MUST generate verbose human-readable error messages that personalize the context (e.g., pointing out exactly which parameter was missing or if a test key was used in a live environment).

## 5. Tooling & Logging Constraints
- The AI MUST integrate or recommend request logging and analytics tagging (HTTP statuses, error frequencies, request metadata) for the API backend.
- The AI MUST explicitly implement PII (Personally Identifiable Information) redaction rules in any logging code it generates.

## 6. Extensibility, Versioning, & Backward Compatibility Constraints
- The AI MUST build a versioning system (e.g., `/v1/`) into the API URI or Header structure from the very beginning, even if no major changes are anticipated.
- The AI MUST maintain backward compatibility for existing endpoints at all costs. If the internal data model changes (e.g., transitioning from single-workspace to federated multi-workspace), the AI MUST design a "Translation Layer" to convert the new internal state into the legacy API payload structure.
- The AI MUST recommend a beta testing or early-adopter access strategy for major API changes to gather real-world developer feedback before public release.

# @Workflow
When tasked with designing or implementing an API, the AI MUST execute the following algorithmic steps:

1. **Define the Target:**
   - Identify the specific external developer use case.
   - Output an explicit statement of the API's primary goal and a list of explicit non-goals (what the API will avoid doing).
2. **Establish the Contract:**
   - Define the endpoint URLs, ensuring consistency with any existing API surface.
   - Define request parameters and response payloads.
   - Validate that no payload fields are polymorphic (e.g., a field is always an array, or always an object, never both).
3. **Design the Error Matrix:**
   - Map out the code path from request to response.
   - Identify potential failures at the System, Business Logic, Request Formatting, and Authorization layers.
   - Generate the explicit JSON error schema including `status`, `error_code` (machine-readable), and `message` (human-readable).
4. **Implement Versioning & Extensibility:**
   - Wrap the endpoint in a versioning schema (e.g., `/v1/`).
   - If refactoring an existing API to accommodate new internal architecture, write the Translation Layer logic to preserve the exact historical output.
5. **Draft Onboarding Assets:**
   - Output a stub for the Getting Started tutorial.
   - Output recommendations for SDK abstractions or Sandbox testability.

# @Examples (Do's and Don'ts)

## Error Code Specificity
- **[DO]**: `"error_code": "token_revoked"`
- **[DON'T]**: `"error_code": "invalid_auth"` (Too vague, does not tell the developer *why* the auth failed).

- **[DO]**: `"error_code": "name_too_long"`
- **[DON'T]**: `"error_code": "invalid_name"`

- **[DO]**: `"error_code": "expired_card"`
- **[DON'T]**: `"error_code": "invalid_card"`

## Type Consistency
- **[DO]**: 
  Endpoint A: `{"user_id": 123}`
  Endpoint B: `{"user_id": 123, "user_details": {"name": "Jane"}}`
- **[DON'T]**: 
  Endpoint A returns `{"user": 123}` (integer) and Endpoint B returns `{"user": {"id": 123, "name": "Jane"}}` (object). This creates code bloat as developers must check the type of `user` on every request.

## Error Response Formatting
- **[DO]**: 
  ```json
  {
    "ok": false,
    "error": "missing_required_parameter",
    "message": "Your request was missing the {user_id} parameter."
  }
  ```
- **[DON'T]**: Returning an HTML Nginx or Apache default 400 Bad Request error page when the API client is expecting a `Content-Type: application/json` response.

## Backend Error Occlusion
- **[DO]**: Return HTTP `500` with `"error": "internal_system_error", "message": "An unexpected error occurred while processing the request. Please try again later."`
- **[DON'T]**: Return HTTP `500` with `"error": "db_connection_timeout", "message": "Failed to connect to pgsql://admin:pass@10.0.0.5/prod_db"` (Leaks internal architecture and security vectors).

## Rate Limiting Errors
- **[DO]**: Return HTTP `429` with header `Retry-After: 3600`, and payload: `{"error": "rate_limit_exceeded", "message": "You have been rate-limited. See Retry-After header and try again."}`
- **[DON'T]**: Return HTTP `400` with payload: `{"error": "too_many_requests"}` (Missing the standard 429 status code and the actionable Retry-After header).