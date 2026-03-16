# @Domain
These rules MUST trigger when the AI is tasked with designing, architecting, documenting, refactoring, or implementing Application Programming Interfaces (APIs), including making architectural decisions about API paradigms (REST, RPC, GraphQL, WebHooks, WebSockets, HTTP Streaming), endpoint naming, defining HTTP methods, designing payload structures, or transitioning from polling mechanisms to event-driven architectures.

# @Vocabulary
*   **API Paradigm**: The foundational interface standard and structural pattern defining how backend data is exposed to other applications.
*   **Request-Response API**: An API architecture where a client explicitly makes an HTTP request to a server endpoint, and the server returns a finite JSON or XML response.
*   **REST (Representational State Transfer)**: A resource-oriented request-response paradigm using standard HTTP methods to execute CRUD operations on distinct entities.
*   **Resource**: In REST, an entity that can be identified, named, addressed, or handled on the web (typically represented as a noun).
*   **RPC (Remote Procedure Call)**: An action-oriented request-response paradigm where a client passes a method name and arguments to execute a block of code on a server.
*   **GraphQL**: A single-endpoint request-response query language allowing clients to explicitly define the exact structure and nested relationships of the data they require.
*   **Event-Driven API**: An API architecture designed to push data to clients asynchronously when state changes occur, negating the need for continuous polling.
*   **Polling**: The anti-pattern of clients repeatedly querying an API endpoint at a predetermined frequency to check for new data.
*   **WebHook**: An event-driven URL endpoint configured by a client that accepts HTTP requests (usually POST) triggered by the API provider when specific events occur.
*   **WebSocket**: A two-way, full-duplex streaming communication protocol over a single, long-lived TCP connection.
*   **HTTP Streaming**: An event-driven mechanism where the server pushes new data to the client over a single indefinite HTTP connection using `Transfer-Encoding: chunked` or Server-Sent Events (SSE).
*   **Idempotent**: An operation (like HTTP GET) that produces the same result regardless of how many times it is executed, having absolutely no side effects.

# @Objectives
*   Evaluate client needs and backend constraints to select the optimal API paradigm rather than defaulting to REST.
*   Strictly enforce the architectural conventions, naming rules, and HTTP verb mappings inherent to the chosen API paradigm.
*   Eliminate polling by designing robust Event-Driven APIs when clients require real-time state updates.
*   Prevent "payload creep" (over-fetching) and excessive round-trips (under-fetching) by identifying when to transition from REST/RPC to GraphQL.
*   Design APIs for future extensibility and correct relationship mapping without compromising simplicity.

# @Guidelines

### REST API Rules
*   The AI MUST map APIs to resources (nouns), NOT actions (verbs).
*   The AI MUST define two URLs per resource: a collection URL (e.g., `/users`) and a specific element URL (e.g., `/users/U123`).
*   The AI MUST strictly enforce CRUD to HTTP verb mapping:
    *   **Create**: `POST`
    *   **Read**: `GET` (MUST NEVER change state, MUST have no side effects, MUST be idempotent, and MUST be perfectly cacheable).
    *   **Update**: `PUT` (total replacement) or `PATCH` (partial update).
    *   **Delete**: `DELETE`
*   The AI MUST use standard HTTP status codes: 2XX (Success), 3XX (Moved), 4XX (Client-side error), 5XX (Server-side error).
*   The AI MUST represent nested resource relationships as subresources in the URL path (e.g., `/repos/:owner/:repo/issues`).
*   When representing Non-CRUD operations in REST, the AI MUST use one of three fallback patterns:
    1.  Render the action as a field update in the resource payload (e.g., `PATCH` with `{"archived": true}`).
    2.  Treat the action as a subresource (e.g., `PUT /repos/:owner/:repo/issues/:number/lock`).
    3.  For search operations ONLY, use the action verb in the URL (e.g., `GET /search/code?q=:query`).

### RPC API Rules
*   The AI MUST use RPC when the API requires complex actions, operations with multiple side-effects, or functions that do not cleanly map to CRUD resources.
*   The AI MUST include the name of the operation directly in the endpoint URL (e.g., `/api/conversations.archive`).
*   The AI MUST use `GET` for read-only requests and `POST` for all other requests.

### GraphQL API Rules
*   The AI MUST use GraphQL when clients suffer from payload creep (too much unused data) or multiple round-trip bottlenecks.
*   The AI MUST define only a single URL endpoint for the entire API.
*   The AI MUST specify operations as either a `query` or a `mutation` within the JSON body.
*   The AI MUST utilize GraphQL's strong typing to validate query syntax at development time.
*   The AI MUST explicitly account for backend parsing complexity and performance optimization bottlenecks when designing a GraphQL schema.

### Event-Driven API Rules (Real-Time Data)
*   The AI MUST NEVER recommend polling for real-time data updates. (Assume 98%+ of polling calls return no new data).
*   **WebHooks**:
    *   Use for server-to-server real-time notifications.
    *   The AI MUST design a robust retry mechanism (e.g., immediate, 1 min, 5 min) and an automatic disablement threshold (e.g., 95% failure rate).
    *   The AI MUST account for inbound firewall restrictions (which block WebHooks) and design security verification methods.
*   **WebSockets**:
    *   Use for high-frequency, two-way, full-duplex communication between a web browser and a server.
    *   The AI MUST utilize ports 80 or 443 to bypass firewall restrictions.
    *   The AI MUST account for scalability constraints, as the server must maintain a persistent active connection per client/workspace.
    *   The AI MUST design client-side logic to handle dropped connections and re-initiation.
*   **HTTP Streaming**:
    *   Use for one-way server-to-client continuous data feeds over simple HTTP.
    *   The AI MUST use `Transfer-Encoding: chunked` (newline-delimited strings) or Server-Sent Events (SSE / `EventSource` API).
    *   The AI MUST account for client/proxy buffering limits that might delay data rendering, and connection drops when switching event subscriptions.

# @Workflow
1.  **Requirement Analysis**: Analyze the core functionality the API needs to expose. Determine if it is resource-centric (CRUD), action-centric, querying-flexible, or requires real-time updates.
2.  **Paradigm Selection**:
    *   If exposing distinct entities with basic CRUD operations, initialize a **REST** architecture.
    *   If exposing complex actions, multi-resource side-effects, or commands, initialize an **RPC** architecture.
    *   If clients require maximum flexibility, nested data fetching, and minimal payloads, initialize a **GraphQL** architecture.
    *   If the data changes frequently and clients need real-time updates, skip to Step 5 (Event-Driven).
3.  **Endpoint Definition**:
    *   *For REST*: Map resources to noun-based URLs, define subresources for relationships, and strictly map functionality to GET, POST, PUT, PATCH, and DELETE.
    *   *For RPC*: Map operations to verb/action-based endpoints.
    *   *For GraphQL*: Define the single endpoint, Schema, Queries, and Mutations.
4.  **Non-CRUD Resolution (REST)**: If REST was selected and edge-case actions exist, explicitly map them to resource state fields (`{"archived": true}`), subresource endpoints (`/lock`), or search endpoints.
5.  **Event-Driven Integration**: If real-time updates are needed, evaluate the consumer:
    *   If server-to-server, implement **WebHooks** (include retry and security architecture).
    *   If browser-to-server requiring two-way communication, implement **WebSockets**.
    *   If one-way continuous feed over simple HTTP, implement **HTTP Streaming** (SSE).
6.  **Validation**: Review the designed architecture to ensure no paradigm rules are violated (e.g., verbs in REST paths, state-changes in GET requests, missing retry logic in WebHooks).

# @Examples (Do's and Don'ts)

### REST Resource Naming
*   [DO] `GET /users/U123` (Retrieves user element)
*   [DO] `POST /users` (Creates a new user in the collection)
*   [DON'T] `GET /getUserInfo/U123` (Violates REST nouns-only rule)
*   [DON'T] `POST /users/U123/update` (Violates REST standard HTTP verb usage; use PUT or PATCH instead)

### REST Relationships and Subresources
*   [DO] `GET /repos/:owner/:repo/issues/:number` (Shows clear relationship between repos and issues)
*   [DON'T] `GET /issues?repo_id=123` (When the issue strictly belongs to a specific repository resource tree)

### REST Non-CRUD Operations
*   [DO] `PATCH /repos/:owner/:repo` with body `{"archived": true}` (Renders action as a field)
*   [DO] `PUT /repos/:owner/:repo/issues/:number/lock` (Treats action as a subresource)
*   [DO] `GET /search/code?q=:query` (Permitted use of action verb for search)
*   [DON'T] `POST /repos/:owner/:repo/archive` (Creates a non-resource endpoint)

### RPC Endpoint Naming
*   [DO] `POST /api/conversations.archive` with body `channel=C01234`
*   [DO] `POST /api/chat.postMessage`
*   [DON'T] `POST /api/conversations/C01234` (Looks like REST but executes a complex action; in RPC, specify the operation in the URL)

### GraphQL Implementation
*   [DO] `POST /graphql` with body `{"query": "query { viewer { login }}"}`
*   [DON'T] `POST /graphql/viewer` (GraphQL MUST use a single endpoint for all operations)

### Real-Time Data (Polling vs. Event-Driven)
*   [DO] Provide a WebHook registration endpoint so the server can `POST` to the client's URL when a new channel is created.
*   [DON'T] Instruct the client to run a cron job executing `GET /channels` every 60 seconds to check for new channels.

### WebHook Architecture
*   [DO] Implement a delivery retry queue: retry immediately on failure, then at 1 minute, then at 5 minutes, and notify the developer if 95% of requests fail.
*   [DON'T] Send a WebHook once and drop the payload if the client server responds with a `500` error or network timeout.