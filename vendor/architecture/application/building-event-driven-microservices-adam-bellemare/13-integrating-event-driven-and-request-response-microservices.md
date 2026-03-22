# @Domain
These rules are activated when the AI is tasked with designing, implementing, or debugging integrations between asynchronous event-driven microservices (EDMs) and synchronous Request-Response APIs. This includes handling external analytical events, querying third-party APIs, serving real-time stateful data via REST endpoints, designing user interfaces (UIs) backed by event-driven architectures, or structuring micro-frontend applications.

# @Vocabulary
- **Request-Response Services**: Services that communicate directly and synchronously, typically via HTTP/REST APIs.
- **Autonomously Generated Events (Analytical Events)**: Metrics, measurements, or statements of fact sent independently from external client applications (e.g., mobile apps, IoT devices) to the backend.
- **Reactively Generated Events**: Events generated strictly from the response payload of a third-party API call initiated by the microservice.
- **Event-First Solution**: A design pattern where incoming synchronous requests are first parsed and published directly to an event stream before any business logic is applied or database writes occur.
- **Smart Load Balancer**: A routing layer that applies a partitioner algorithm to incoming request keys to forward real-time state queries directly to the specific microservice instance hosting that partition's internal state.
- **Asynchronous UI**: A user interface designed to handle the eventual consistency of event-driven backends, managing user expectations via loading indicators and input blocking.
- **Micro-Frontend**: A frontend architecture that splits a monolithic UI into independent, composition-based components aligned strictly to business bounded contexts.

# @Objectives
- Merge asynchronous event-driven workflows with synchronous request-response communication without violating event-driven principles.
- Enforce the "Single Source of Truth" by schematizing external events at the ingestion point.
- Protect external third-party APIs from being flooded during event stream reprocessing or scaling events.
- Optimize real-time state querying by intelligently routing requests based on partition ownership or leveraging decoupled external state stores.
- Align human interactions and UI architectures (Micro-Frontends) directly with backend event-driven bounded contexts.

# @Guidelines

## Handling External Events
- When ingesting Autonomously Generated Events, the AI MUST implement an event receiver service that routes events to distinct streams based on their schemas and business definitions.
- The AI MUST enforce schema validation upon reception of analytical events to prevent downstream consumers from dealing with malformed or unparsed text.
- The AI MUST account for multiple concurrent versions of analytical events, as external clients (like mobile apps) will run older versions of schemas.
- When generating Reactively Generated Events from third-party APIs, the AI MUST extract the response payload (e.g., payment success/failure, external ID) and convert it into a schematized event for downstream reconciliation.

## Integrating Third-Party Request-Response APIs
- When a microservice calls a third-party API, the AI MUST execute the request, wait for the response, parse the result into a locally understood object, apply business logic, and ONLY THEN produce the result to the output event stream.
- The AI MUST commit consumer offsets ONLY after the API request-response cycle is fully complete and successful.
- The AI MUST implement strict throttling and rate-limiting (quotas) for third-party API calls to prevent flooding remote services, especially during the reprocessing of historical event streams.
- The AI MUST account for the nondeterministic nature of external API calls; the AI MUST add comments or architectural warnings indicating that reprocessing events may yield different results from the external API than the initial processing.

## Serving Real-Time Requests with Internal State Stores
- When an API requests data materialized in an internal state store, the AI MUST NOT use basic round-robin load balancing.
- The AI MUST implement a Smart Load Balancer or routing logic that applies the partitioner algorithm to the request's key to identify the specific microservice instance holding the requested data.
- The AI MUST implement fallback redirect logic within each microservice instance so that if a request is incorrectly routed (due to consumer group rebalancing or race conditions), the instance can redirect the request to the correct peer.

## Serving Real-Time Requests with External State Stores
- The AI MUST NOT allow external services to directly query the external state store. All access MUST go through the microservice's Request-Response API.
- The AI MUST structure the solution using one of two patterns:
  1. **All-in-One Microservice**: A single microservice consumes events, materializes them to the external store, and hosts the API to serve requests.
  2. **Separate Microservices (Composite Service)**: One executable processes events and writes to the store; a separate executable hosts the REST API to serve requests. The AI MUST enforce that both executables share the exact same codebase, bounded context, and deployment pipeline.

## Handling Requests Within an Event-Driven Workflow (Event-First)
- When capturing user input that drives core business state, the AI MUST implement the "Event-First" pattern: the request is parsed, converted into a schematized event, and published to the event broker BEFORE the application consumes it to update the database.
- To mitigate the read-after-write latency of the Event-First pattern, the AI MAY cache the value in the application's memory immediately after publishing to the broker, but MUST NOT bypass the event stream for database writes.

## Processing Events for User Interfaces
- The AI MUST implement Asynchronous UI techniques when handling user inputs as events (e.g., displaying a spinning wheel, disabling submit buttons, showing "please wait") to manage latency expectations.
- When designing human approval workflows (e.g., Editor and Advertiser publishing approvals), the AI MUST translate human decisions into distinct, canonical events (e.g., `EditorApprovalEvent`, `AdvertiserApprovalEvent`) rather than updating a monolithic database state.
- The AI MUST encapsulate specific UI gating logic (e.g., withholding a document from advertisers until editors approve) within dedicated microservices, utilizing isolated event streams (e.g., `editor-approved-stream`) to enforce the workflow.

## Micro-Frontends
- When architecting UIs for event-driven backends, the AI MUST use a Micro-Frontend approach, composing the UI out of independent frontend components that align strictly 1:1 with backend bounded contexts.
- The AI MUST recommend a shared, business-logic-free UI element library and strict style guide to prevent visual inconsistencies across decoupled micro-frontends.
- The AI MUST design a composite aggregation layer that stitches the micro-frontends together and gracefully handles varying load times or partial failures of individual UI components.

# @Workflow
When tasked with integrating request-response mechanics with an event-driven microservice, the AI MUST follow this step-by-step process:

1. **Identify the Integration Vector**: Determine if the task involves ingesting external analytical events, querying a 3rd-party API, serving state via REST, or capturing UI interactions.
2. **Establish the Ingestion/Contract Boundary**:
   - If ingesting, define strict schemas for the incoming data and configure routing logic based on event type. Account for legacy client versions.
   - If UI-driven, implement the "Event-First" pattern by defining the event schema that the UI request will immediately be mapped to.
3. **Design the Processing & External API Logic**:
   - If calling external APIs, implement non-blocking/blocking calls, strict error handling, and throttle/quota mechanisms. 
   - Ensure consumer offsets are only committed after the API response is successfully handled and downstream events are emitted.
4. **Design the Real-Time Serving Layer**:
   - If using *Internal State*, implement partition-key routing logic in the load balancer and redirect logic in the microservice.
   - If using *External State*, define whether the API and event processor share an executable or are split into a composite service. Ensure the database is hidden behind the API.
5. **Architect the Frontend Experience**:
   - For UIs, design Asynchronous UI flow states (loading, disabled).
   - Divide the UI into Micro-Frontends aligned to the backend bounded contexts, utilizing a compositional UI layer to stitch them together.

# @Examples (Do's and Don'ts)

## Event-First UI Processing
- **[DO]** Parse an incoming HTTP POST request into an `OrderSubmittedEvent`, publish it to Apache Kafka, return an HTTP 202 Accepted to the client, and consume the event asynchronously to update the local database.
- **[DON'T]** Accept an HTTP POST request, write it directly to the local MySQL database, and then emit a "Semaphore Event" simply signaling that the database has been updated.

## Serving Internal State
- **[DO]** Configure the API Gateway/Load Balancer to extract the `userId` from the REST request, hash it using the exact same partitioner algorithm used by the event broker, and forward the HTTP request directly to the specific container assigned to `Partition 4`.
- **[DON'T]** Use a generic Round-Robin load balancer to distribute REST queries across internal-state microservices, resulting in cache misses and excessive inter-node redirect hops.

## External API Integration
- **[DO]** Wrap third-party API calls in a rate-limiter, implement exponential backoff, and explicitly pause consumer polling if the external API returns HTTP 429 (Too Many Requests), especially when rewinding consumer offsets to reprocess historical data.
- **[DON'T]** Reset an event stream to offset 0 and allow the microservice to blindly fire thousands of synchronous HTTP requests per second at a paid third-party vendor.

## Micro-Frontend Alignment
- **[DO]** Create an `ExperienceSearch` micro-frontend backed by a geolocation search microservice, and an independent `ExperienceReview` micro-frontend backed by a review event-processor, stitching them together visually in the client browser.
- **[DON'T]** Build a monolithic React application that queries a single GraphQL aggregation layer which contains blended business logic for both search and reviews.