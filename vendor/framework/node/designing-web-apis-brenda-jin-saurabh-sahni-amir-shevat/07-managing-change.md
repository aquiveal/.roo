@Domain
Trigger these rules when tasked with designing, modifying, updating, or versioning Web APIs. This includes modifying request/response payloads, adding or removing API endpoints, writing API schema definitions (e.g., JSON Schema, OpenAPI), structuring API routing, or implementing API deprecation and versioning strategies.

@Vocabulary
- **Consistency**: The practice of utilizing uniform naming conventions, data types, request patterns, and error formats across all API endpoints so developers can build a reliable mental model.
- **CI Pipeline (Continuous Integration)**: An automated workflow where code changes are merged, and automated tests (like schema validation) are run to prevent backward-incompatible changes from reaching production.
- **API Description Languages (IDL/JSON Schema/OpenAPI)**: Structured formats used to define, validate, and document JSON requests and responses, utilizing reusable object definitions to enforce consistency.
- **Backward Compatibility**: The strict requirement that an API change must not break existing client integrations (e.g., by not removing fields, changing data types, or unexpectedly altering core behavior).
- **Additive-Change Strategy**: A versioning approach where all updates are backward-compatible (e.g., adding fields, adding endpoints, adding optional request parameters) without changing existing behavior or fault contracts.
- **Explicit-Version Strategy**: A versioning approach where breaking changes are grouped into explicit versions accessible via URI components, HTTP headers, or request parameters.
- **Transformation Layer**: A code architecture pattern where older API versions are supported by silently translating/transforming the new data model back into the older schema before returning the response.
- **SemVer (Semantic Versioning)**: A versioning standard (MAJOR.MINOR.PATCH) where MAJOR indicates backward-incompatible changes, MINOR indicates backward-compatible feature additions, and PATCH indicates backward-compatible bug fixes.
- **Deprecation**: The process of phasing out an endpoint or field by providing adequate notice, documentation, and an incentive (a "carrot") to migrate to a new feature, before actually removing the functionality.

@Objectives
- Ensure absolute consistency across all API endpoints in terms of naming, request parameters, and response payload structures.
- Prevent backward-incompatible changes that could break third-party integrations and client applications.
- Enforce the use of API description languages to validate requests and responses automatically.
- Manage unavoidable breaking changes through structured, explicit versioning and transformation layers rather than destroying existing implementations.
- Provide clear communication and migration paths for developers when deprecating features.

@Guidelines
- **Enforce Consistency**: The AI MUST use the exact same nomenclature, type definitions, and structural hierarchy across all endpoints. If an entity is called a `repository` in one endpoint, it MUST NOT be called `repo` in another.
- **Never Break Existing Clients (Default to Additive)**: The AI MUST prefer an additive-change strategy. Adding new endpoints, new optional request parameters, and new response fields is permitted.
- **No Destructive Modifications**: The AI MUST NOT remove existing response fields, change the data type of an existing field, rename request parameters, or alter existing error codes on an active API version.
- **Validate via Schema**: The AI MUST define JSON requests and responses using JSON Schema or OpenAPI. 
- **Modularize Schemas**: The AI MUST utilize reusable definitions (e.g., `$ref`) for common objects in schema files to ensure payload consistency across different endpoints.
- **Handle Missing Fields Carefully**: When setting a previously undocumented or unset field to a consistent value (e.g., adding a boolean flag), the AI MUST evaluate if existing clients might rely on the absence of that key for their business logic.
- **Implement Explicit Versioning for Breaking Changes**: If a breaking change is strictly required, the AI MUST implement an explicit-version strategy. The version MUST be specified via a URI component (e.g., `/v2/`), an HTTP custom header/Accept header, or a query parameter.
- **Isolate Version Logic**: The AI MUST NOT litter core business logic with `if version == X` statements. Instead, the AI MUST use versioned controllers, forked functions, or a dedicated transformation layer to convert new data structures into legacy schemas.
- **Use SemVer**: When labeling versions, the AI MUST follow MAJOR.MINOR.PATCH conventions. Roll additive changes into MINOR versions and breaking changes into MAJOR versions.
- **Deprecate with Notice and Incentives**: When tasked with removing an API feature, the AI MUST draft response metadata, headers, or documentation warning of the deprecation, and MUST provide a new, improved endpoint (the "carrot") to incentivize migration.

@Workflow
1. **Analyze the Request**: Determine if the requested API change modifies an existing endpoint or creates a new one.
2. **Assess Compatibility**: Evaluate if the change is Additive (adding a field/endpoint) or Breaking (removing a field, changing a type, altering logic).
3. **Design the Schema**: 
   - Write or update the JSON Schema / OpenAPI specification for the endpoint.
   - Extract any shared entities into reusable `$ref` definitions to maintain consistency.
4. **Implement Additive Changes**:
   - Add the new field or optional query parameter.
   - Ensure default behavior mimics the legacy behavior if the new parameter is absent.
5. **Implement Breaking Changes (If unavoidable)**:
   - Create a new MAJOR version namespace (e.g., `v2`).
   - Implement the new logic in a distinct controller or function.
   - Write a transformation layer that translates the new backend data model into the `v1` schema to keep the old endpoint fully functional.
6. **Implement Communication/Deprecation**: If an endpoint is marked for deprecation, inject warning metadata or headers into the response payload of the deprecated endpoint and draft the documentation updates.

@Examples (Do's and Don'ts)

**Principle: Ensuring Backward Compatibility (Additive Changes)**

[DO] Add an optional parameter to control new behavior, keeping the default response exactly as clients expect.
```json
// Request: GET /users/1234
// Response remains identical to previous versions
{
  "id": 1234,
  "name": "Chen Hong",
  "friends": [2341, 3449]
}

// Request: GET /users/1234?exclude_friends=true
// Response utilizes the new additive feature
{
  "id": 1234,
  "name": "Chen Hong"
}
```

[DON'T] Suddenly remove a field or change its structure to optimize payload size, breaking existing clients.
```json
// DON'T change the response for GET /users/1234 from an object to an array or drop the friends array without warning.
[
  { "1234": { "name": "Chen Hong" } }
]
```

**Principle: Modularizing API Description Schemas**

[DO] Define reusable objects in JSON Schema to guarantee consistency across multiple endpoints.
```json
// common_objects_schema.json
{
  "repository": {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
      "id": { "type": "integer" },
      "name": { "type": "string" }
    }
  }
}

// endpoint_schema.json
{
  "properties": {
    "repositories": {
      "type": "array",
      "items": { "$ref": "../common_objects_schema.json#/repository" }
    }
  }
}
```

[DON'T] Inline schemas independently for every endpoint, leading to structural inconsistencies (e.g., one endpoint returns `id` as an integer, another as a string).

**Principle: Code Architecture for Versioning**

[DO] Use a transformation layer to adapt new data models for older API versions.
```javascript
// Data model returns new V2 structure
const data = getRepositoriesFromDB(); 

// V2 Controller
function getRepositoriesV2(req, res) {
    res.json(data); // Returns new array format
}

// V1 Controller (Maintains Backward Compatibility)
function getRepositoriesV1(req, res) {
    // Transform V2 data back into the V1 dictionary schema
    const transformedData = transformToV1Schema(data);
    res.json(transformedData);
}
```

[DON'T] Clutter the core business logic with inline version checks.
```javascript
function getRepositories(req, res) {
    const data = getRepositoriesFromDB();
    // DON'T do this:
    if (req.version === 'v1') {
        res.json({ repositories: data });
    } else {
        res.json(data);
    }
}
```

**Principle: Communicating Deprecation**

[DO] Inject response metadata to inform active developers of an upcoming deprecation or schema change.
```json
{
  "data": { ... },
  "response_metadata": {
    "response_change": {
      "date": "January 1, 2021",
      "severity": "major",
      "details": "Starting January 1, 2021, the 'friends' array will be removed. Please migrate to the /v2/users endpoint."
    }
  }
}
```

[DON'T] Silently delete endpoints or rename fields without providing a timeline, communication strategy, and an alternative solution.