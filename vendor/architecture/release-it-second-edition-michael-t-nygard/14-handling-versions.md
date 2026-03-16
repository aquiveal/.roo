# @Domain

This rule file activates whenever the AI is instructed to perform tasks related to:
- Designing, modifying, or deprecating API routes and endpoints.
- Structuring request/response message payloads, schemas, or DTOs.
- Writing or modifying integration tests, contract tests, or API functional tests.
- Implementing inter-service communication and client SDKs.
- Executing or preparing deployments of services that have upstream consumers or downstream dependencies.
- Documenting APIs using tools like Swagger/OpenAPI.

# @Vocabulary

- **Postel's Robustness Principle**: "Be conservative in what you do, be liberal in what you accept from others." The foundational philosophy for handling versions and API evolution.
- **Layered Agreements**: The concept that APIs are a stack of agreements (Protocol, Framing, Encoding, Syntax, Semantics, Authorization). Changing any established agreement constitutes a breaking change.
- **Covariant Requests / Contravariant Responses**: The rule governing safe API evolution: A service can safely accept more (or require less) input than before, and return more (never less) output than before.
- **De Facto Specification**: The actual, observable behavior of the running implementation, regardless of what the written documentation or intended design states.
- **Inbound Testing**: Generative (fuzz) testing applied to a service's own API to find gaps between the documented specification and the actual implementation.
- **Outbound Testing**: Generative testing applied to dependencies (downstream services) using their specifications but your own tests to ensure accurate understanding of their contract.
- **Contract Tests (FIT tests)**: Tests owned by the calling service that verify both sides of the contract without over-specifying a fragile end-to-end integration loop.
- **Coordinated Deployment**: An anti-pattern where a service provider and its consumers must be deployed simultaneously to avoid system breakage.

# @Objectives

- Ensure that consuming applications are never broken by API or service updates.
- Decouple the deployment schedules of service providers from their consumers to enable autonomous, zero-downtime deployments.
- Strictly adhere to Postel's Robustness Principle in all message formatting and API route definitions.
- Treat the live implementation's behavior—including its flaws and lack of validation—as the immutable specification for existing API versions.
- Implement breaking changes exclusively through explicit URL versioning and side-by-side controller translation, avoiding business logic duplication.
- Validate API contracts using isolated, generative inbound and outbound testing rather than brittle end-to-end tests.

# @Guidelines

## Identifying and Avoiding Breaking Changes
- The AI MUST NOT introduce any of the following breaking changes to an existing API version:
  - Rejecting a network protocol, request framing, content encoding, request syntax, or request routing that previously worked.
  - Adding new required fields to a request.
  - Forbidding optional information in the request that was previously allowed.
  - Removing information from the response that was previously guaranteed.
  - Requiring an increased level of authorization for an existing route.
- The AI MUST classify the following as SAFE, non-breaking changes:
  - Requiring a subset of previously required parameters.
  - Accepting a superset of previously accepted parameters (adding optional fields).
  - Returning a superset of previously returned values (adding new response fields).
  - Enforcing a subset of the previously required constraints on parameters.

## Handling Undefined Behavior and De Facto Specifications
- The AI MUST treat existing implementation behavior as the immutable contract. If an existing API endpoint receives unvalidated input (e.g., accepts any string instead of validating a URL format) and that behavior is already in production, the AI MUST NOT add validation that rejects previously accepted input in the current version.
- The AI MUST NOT "fix" unintended behaviors or edge cases if callers might be relying on those behaviors, unless deploying an explicitly new API version.

## Implementing Breaking Changes (When Unavoidable)
- The AI MUST include a version number in the request and reply message formats (payloads) to assist with debugging.
- The AI MUST implement API versioning via the URL (e.g., `/v2/applications`). Do NOT use custom headers or media types (`Accept`/`Content-Type`) for versioning, as they complicate intermediary routing (caches, proxies, load balancers).
- The AI MUST bump ALL routes in the API simultaneously when a new version is created. Do not force consumers to track mixed version numbers across different endpoints.
- The AI MUST support both the old and new API versions side-by-side to allow consumers to upgrade at their own pace.

## Controller-Level Version Translation
- The AI MUST NOT duplicate business logic to support multiple API versions.
- The AI MUST route new API requests directly to the current version of the business logic.
- The AI MUST update old API controllers to act as translators: converting old request objects into current objects for the business logic, and converting current response objects back into old API responses.

## Defensive Consumption (Handling Others' Versions)
- The AI MUST assume downstream services can change at any time. Client code MUST accept any combination of newly added optional fields (missing, present, null) without crashing.
- The AI MUST gracefully handle unrecognized fields in responses by ignoring them, not by throwing parsing errors.

## Contract and Integration Testing
- The AI MUST NOT write brittle end-to-end integration tests that over-specify the call to the provider (e.g., asserting specific data values based on a specific test request).
- The AI MUST split integration tests into two distinct phases:
  1. Verify that outbound requests are generated strictly according to the provider's specification requirements.
  2. Verify that the consuming code is prepared to gracefully handle ANY response the provider is allowed to send (including errors and omitted optional fields).
- The AI MUST use generative testing (fuzzing) driven by Swagger/OpenAPI specifications to test the boundaries of inbound APIs and outbound dependencies.
- The AI MUST test side-by-side API versions by mixing calls to the old and new API versions on the exact same entities to ensure cross-version compatibility.

# @Workflow

When tasked with modifying an API, adding a feature, or integrating a service, the AI MUST follow this algorithmic process:

1. **Change Impact Assessment**:
   - Analyze the proposed change against the "Identifying and Avoiding Breaking Changes" guidelines.
   - Determine if the change adds validation to previously unvalidated fields, removes response data, or adds required request fields.
   - If the change is SAFE (Covariant Request/Contravariant Response), proceed to Step 2.
   - If the change is BREAKING, proceed to Step 3.

2. **Safe Implementation**:
   - Implement the change in the current API version.
   - Add generative tests to ensure the API still accepts all previous inputs.
   - Update the Swagger/OpenAPI documentation.
   - Stop.

3. **Breaking Change Implementation (URL Versioning)**:
   - Create a new version identifier in the URL route (e.g., copy `/v1/` to `/v2/`).
   - Bump ALL routes in the service to the new version namespace.

4. **Controller Translation Pattern**:
   - Point the `/v2/` controller directly to the updated business logic.
   - Rewrite the `/v1/` controller to act as an adapter.
   - Implement mapping functions in the `/v1/` controller to transform `v1_Request` -> `v2_BusinessModel` and `v2_BusinessModel` -> `v1_Response`.

5. **Test Side-by-Side Compatibility**:
   - Write tests that create an entity using the `/v2/` API, and then read/update it using the `/v1/` API (and vice versa). Ensure no internal server errors occur due to missing fields.

6. **Contract Testing Update**:
   - Write or update outbound tests to ensure the client generates requests matching the new spec.
   - Write inbound tests feeding generative, randomized payloads matching the spec to ensure the service handles all optional permutations.

# @Examples (Do's and Don'ts)

## API Versioning Strategy

- **[DO]** Use URL-based versioning and bump all routes simultaneously.
```text
GET /v2/applications
POST /v2/applications
GET /v2/borrower
PUT /v2/borrower
```

- **[DON'T]** Mix versions across routes or rely on custom headers that break caching intermediaries.
```text
// Anti-pattern: Mixed routing
GET /v1/applications
POST /v2/applications

// Anti-pattern: Custom headers
GET /applications
api-version: 2.0
```

## Controller Translation Pattern

- **[DO]** Route legacy controllers to new business logic via translation adapters.
```javascript
// V2 Controller (Current)
async function createApplicationV2(req, res) {
    const v2Data = req.body; // Contains new required fields
    const result = await BusinessLogic.createApplication(v2Data);
    res.json(result);
}

// V1 Controller (Legacy Adapter)
async function createApplicationV1(req, res) {
    const v1Data = req.body;
    // Translate v1 to v2: Provide defaults for new required fields to prevent breakage
    const v2Data = {
        ...v1Data,
        creditScore: v1Data.creditScore || DEFAULT_CREDIT_SCORE,
        collateralCategory: v1Data.collateralCategory || 'UNKNOWN'
    };
    
    const result = await BusinessLogic.createApplication(v2Data);
    
    // Translate v2 back to v1: Strip new fields the old client doesn't understand
    const v1Response = mapToV1Response(result);
    res.json(v1Response);
}
```

- **[DON'T]** Duplicate business logic to support multiple API versions.
```javascript
// Anti-pattern: Duplicated database/business logic
async function createApplicationV1(req, res) {
    const v1Data = req.body;
    // Duplicating the actual insertion logic just for V1
    const dbResult = await db.insert('applications_v1', v1Data); 
    res.json(dbResult);
}
```

## De Facto Specifications & Input Validation

- **[DO]** Maintain backwards compatibility even if original input validation was missing or flawed.
```java
// V1 was documented as requiring a URL, but the code originally just accepted a String.
// We MUST continue accepting generic strings in V1 to avoid breaking existing callers.
public Response handleV1Request(String urlOrString) {
    // Process as string, do not throw validation error
}

// Validation can be enforced in V2
public Response handleV2Request(URL strictUrl) {
    // Strict URL validation applied here
}
```

- **[DON'T]** Retroactively apply strict validation to an existing API endpoint.
```java
// Anti-pattern: Breaking change on an existing route
public Response handleV1Request(String input) {
    if (!isValidUrl(input)) {
        throw new BadRequestException("Strict URL required"); // BREAKS existing clients!
    }
}
```

## Contract Testing

- **[DO]** Split tests into strict generation checks and broad consumption checks.
```python
# Test 1: Verify we generate requests exactly to the provider's spec
def test_outbound_request_conforms_to_spec():
    request = build_provider_request(data)
    assert schema_validator.is_valid(request, provider_openapi_spec)

# Test 2: Verify we can handle any valid response from the provider, including missing optional fields
def test_inbound_response_handling():
    # Use generative testing (fuzzing) to create valid variations of provider responses
    for generated_response in generate_valid_responses(provider_openapi_spec):
        result = process_provider_response(generated_response)
        assert result.is_successful() # Should not crash on missing optional fields
```

- **[DON'T]** Write brittle end-to-end integration tests that assume exact provider data.
```python
# Anti-pattern: Fragile E2E test that breaks if the provider adds a new optional field
def test_integration_tight_coupling():
    response = call_real_provider_service(request)
    # Fails if the provider adds a new field we didn't expect
    assert response.keys() == ["id", "status"] 
```