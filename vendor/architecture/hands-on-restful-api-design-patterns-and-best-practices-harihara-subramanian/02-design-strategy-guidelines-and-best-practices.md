@Domain
Trigger these rules whenever tasked with designing, reviewing, refactoring, or implementing RESTful APIs, web service architectures, URI routing, API payloads, HTTP interactions, or API documentation.

@Vocabulary
- **Affordance**: The design quality where an API's properties intuitively provide clues about its operation and capabilities to the consumer.
- **Resource Archetypes**: The structural classification of REST resources, specifically into four categories: Document, Collection, Store, and Controller.
- **Document**: A base resource representing a single entity with a field and link-based structure (e.g., a specific customer profile).
- **Collection**: A server-managed directory of resources where the server decides the URIs of newly added resources.
- **Store**: A client-managed resource repository where the client chooses the URIs for the resources it adds.
- **Controller**: An executable method with parameters and return values, representing application-specific actions that do not fit standard CRUD methods.
- **Coarse-grained API**: APIs that return combined or extensive datasets in a single call to minimize network trips (typically used for Read operations).
- **Fine-grained API**: APIs broken down into small, specific actions or datasets (typically used for Write operations).
- **HATEOAS (Hypermedia as the Engine of Application State)**: A REST constraint where responses include hypermedia links allowing the client to programmatically navigate to the next application state.
- **Content-Negotiation**: The mechanism of serving different representation formats (e.g., JSON vs. XML) at the same URI based on the client's `Accept` HTTP header or a query parameter format selection.
- **Opaque URIs**: URIs where the client relies on hypermedia and media types rather than hardcoding or parsing the URI string structure itself.
- **JSONP (JSON with Padding)**: A method used to support multi-origin read access from JavaScript, circumventing same-origin policies.
- **CORS (Cross-Origin Resource Sharing)**: A mechanism supporting multi-origin read/write access from JavaScript clients.

@Objectives
- Design APIs prioritizing the Application Developer (App Developer) experience through extreme simplicity, consistency, and intuitive interfaces.
- Maximize the leverage of existing web architecture (HTTP verbs, headers, status codes) rather than reinventing transport wrappers.
- Ensure APIs are entirely platform-independent and loosely coupled, abstracting all backend service internals and domain models from the exposed interfaces.
- Enforce strict adherence to RESTful uniform interfaces and URI formatting rules based on RFC 3986.

@Guidelines

# 1. URI Design Syntax and Formatting
- The AI MUST use a forward slash (`/`) to indicate hierarchical relationships.
- The AI MUST NOT use a trailing forward slash (`/`) in URIs or include them in links provided to clients.
- The AI MUST use hyphens (`-`) to improve the readability of URI names, paths, and segments.
- The AI MUST NOT use underscores (`_`) anywhere in a URI path.
- The AI MUST use entirely lowercase letters in URI paths.
- The AI MUST NOT include file extensions (e.g., `.json`, `.xml`) in URIs. Rely on media types communicated via the `Content-Type` and `Accept` headers or format query parameters instead.

# 2. URI Naming and Resource Archetypes
- The AI MUST use singular nouns for Document names.
- The AI MUST use plural nouns for Collections and Stores.
- The AI MUST use verbs or verb phrases for Controller resources.
- Controllers MUST ALWAYS appear as the last segment in a URI path, with absolutely no child resources following them.
- The AI MUST NOT use CRUD function names (Create, Read, Update, Delete) in URIs.
- The AI MUST define consistent sub-domain authorities (e.g., `api.domain.com` for endpoints, `developer.domain.com` for API portals).

# 3. HTTP Interaction and Method Mapping
- The AI MUST NOT tunnel other requests through GET or POST methods.
- The AI MUST map methods strictly as follows:
  - `GET`: Retrieve a representation of a resource.
  - `HEAD`: Retrieve response headers only.
  - `PUT`: Update a mutable resource OR insert into a Store. MUST be idempotent.
  - `POST`: Create a new resource in a Collection OR execute a Controller action.
  - `DELETE`: Remove a resource from its parent.
  - `OPTIONS`: Retrieve metadata about available methods.

# 4. Query Parameters
- The AI MUST use URI queries for filtering Collections or Stores.
- The AI MUST use URI queries to paginate Collection or Store results (e.g., `limit` and `offset`).
- The AI MUST use URI queries to support partial response (returning only requested fields).
- The AI MUST use URI queries to support embedding linked/nested resources dynamically.

# 5. Status Code Rules
- The AI MUST NOT use a `200 OK` status code to communicate an error in the response body.
- The AI MUST use `201 Created` for successful resource creation.
- The AI MUST use `202 Accepted` for successful asynchronous actions.
- The AI MUST use `204 No Content` when sending an empty response body.
- The AI MUST NOT use `302 Found`. It causes client confusion regarding automatic redirections.
- The AI MUST use `303 See Other` to refer the client to a different URI instead of `302`.
- The AI MUST use `405 Method Not Allowed` when a client uses an unsupported HTTP method, and MUST include the `Allow` header in the response.
- The AI MUST use `406 Not Acceptable` when the server cannot serve the requested media type.
- The AI MUST use `412 Precondition Failed` to support conditional operations when a required condition is not met.
- The AI MUST use `415 Unsupported Media Type` when the payload's media type cannot be processed.

# 6. Metadata and HTTP Headers
- The AI MUST use `Content-Type` to specify media types.
- The AI MUST use `Content-Length` so clients know the message body size.
- The AI MUST include `Last-Modified` and `ETag` (typically a hash/digest of resource contents) in responses to enable conditional caching.
- The AI MUST support conditional `PUT` requests using `If-Unmodified-Since` and/or `If-Match`.
- The AI MUST use the `Location` header to specify the URI of newly created resources (for `201` or `202` responses).
- The AI MUST leverage HTTP cache headers (`Cache-Control`, `Expires`, `Date`) for `200 OK` responses to encourage caching. Use shorter durations instead of `no-cache` directives where possible.
- The AI MAY use expiration caching headers (negative caching) for `3xx` and `4xx` responses.
- The AI MUST NOT use custom HTTP headers unless strictly necessary. Essential interpretation data must go in the payload body or URI.

# 7. Representations and Payload Formats
- The AI MUST design representations primarily in JSON (or XML).
- The AI MUST NOT create additional custom transport envelopes or wrappers; leverage the native HTTP envelope exclusively.
- The AI MUST ensure error responses follow a consistent schema, generic error types, and provide human-readable diagnostic information.
- The AI MUST implement HATEOAS using consistent forms to represent links, self-linking representations, and links that advertise state-sensitive actions.

# 8. Versioning, Security, and Cross-Origin Rules
- The AI MUST version the API when making breaking changes (response data changes, type changes, endpoint removals).
- Minor, non-breaking modifications (adding parameters) SHOULD also increment the minor version.
- The AI MUST support CORS for multi-origin read/write access and JSONP for multi-origin read-only access for JavaScript clients.
- The AI MUST abstract service internals; RESTful API payloads MUST NOT contain traces of SOAP payloads or internal database domain models.

@Workflow
When tasked with designing or implementing a RESTful API endpoint, the AI MUST follow this exact sequence:

1. **Resource Modeling**: Determine the business entity and classify it into the correct Resource Archetype (Document, Collection, Store, or Controller).
2. **URI Path Definition**: Construct the URI path strictly applying the lowercase, hyphen-separated, extension-less, trailing-slash-free rules. Ensure collections are plural and documents are singular.
3. **HTTP Method Selection**: Assign the correct HTTP method based on the action (e.g., `POST` for creating in a Collection, `PUT` for adding to a Store).
4. **Query Parameter Design**: Add standardized query parameters for pagination (`limit`, `offset`), filtering, partial responses, and format selection.
5. **Header Configuration**: Specify the necessary standard headers (`Content-Type`, `Accept`, `ETag`, `Last-Modified`, `Location`, `Cache-Control`). Ensure no custom headers are used inappropriately.
6. **Payload & Error Schema Design**: Design the JSON representation. Ensure no custom envelopes are used. Define explicit, standard HTTP status codes (avoiding `302` and using `200` only for actual success).
7. **HATEOAS Integration**: Inject state-aware hypermedia links into the response representation to guide the client to the next possible actions.

@Examples

[DO] **Collection and Document URIs**
```text
https://api.airlines.com/v1/profiles/customers
https://api.airlines.com/v1/profiles/customers/member-status
```

[DON'T] **Trailing Slashes and Underscores**
```text
https://api.airlines.com/v1/profiles/customers/
https://api.airlines.com/v1/profiles/member_status
```

[DO] **Controller Resource URIs**
```http
POST /v1/alerts/245245/resend HTTP/1.1
```

[DON'T] **CRUD terms in URIs**
```http
POST /v1/users/1234/delete HTTP/1.1
GET /v1/user-delete?id=1234 HTTP/1.1
```

[DO] **Query Parameters for Pagination and Formatting**
```text
GET /v1/operations/flight-status/arrivals/zrh/2018-05-21?limit=40&offset=10&format=json
```

[DON'T] **File Extensions in URIs**
```text
GET /v1/operations/flight-status.json
```

[DO] **Proper Redirects**
```http
HTTP/1.1 303 See Other
Location: https://api.example.com/v2/new-resource
```

[DON'T] **Using 302 for Redirects**
```http
HTTP/1.1 302 Found
Location: https://api.example.com/v2/new-resource
```

[DO] **Conditional Updates via HTTP Headers**
```http
PUT /v1/customers/1234/preferences HTTP/1.1
If-Match: "uqv2309u324klm"
Content-Type: application/json
```

[DON'T] **Returning errors inside a 200 OK response**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "error",
  "message": "User not found"
}
```