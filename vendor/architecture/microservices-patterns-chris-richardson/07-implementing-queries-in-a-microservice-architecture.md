@Domain
This rule file is activated when the AI is tasked with designing, implementing, refactoring, or evaluating query operations and data retrieval mechanisms within a microservice architecture. This includes requests to fetch data distributed across multiple services, aggregate service data, design view databases, implement API composition, or build Command Query Responsibility Segregation (CQRS) modules.

@Vocabulary
- **API Composition Pattern**: A query implementation pattern where an API composer invokes multiple provider services and performs an in-memory join of the results.
- **API Composer**: The component (Client, API Gateway, or Standalone Service) responsible for querying provider services and aggregating their responses.
- **Provider Service**: A backend microservice that owns a subset of the data required by the API composer.
- **CQRS (Command Query Responsibility Segregation) Pattern**: A pattern that strictly separates command operations (Create, Update, Delete) from query operations (Read) by maintaining one or more read-only view databases optimized for specific queries.
- **Command Side**: The module and data model in CQRS responsible for implementing business rules, executing CUD operations, and publishing domain events upon state changes.
- **Query Side**: The module and data model in CQRS responsible for subscribing to domain events, updating a view database, and serving query requests.
- **Query-Only Service**: A standalone service that implements CQRS views by subscribing to events from multiple other services, without owning any command-side business logic.
- **Replication Lag**: The inevitable delay between a command updating the primary database and the corresponding domain event updating the CQRS view database (eventual consistency).
- **Idempotent Event Handler**: An event handler that correctly handles the redelivery of duplicate events, typically by tracking the maximum processed `eventId` per aggregate.
- **Upcasting**: The process of transforming old versions of events into the latest schema version when they are loaded from an event store.

@Objectives
- Determine the most efficient and scalable pattern (API Composition vs. CQRS) for retrieving distributed data based on query complexity and filtering requirements.
- Minimize network latency and avoid inefficient in-memory joins of large datasets.
- Prevent synchronous communication failures from causing cascading outages by implementing robust fallbacks and reactive concurrency.
- Enforce strict separation of concerns by ensuring services are not burdened with queries outside their primary domain responsibilities.
- Ensure CQRS read-models remain eventually consistent while correctly handling concurrent updates, duplicate events, and replication lag.

@Guidelines
- **Query Pattern Selection**:
  - The AI MUST use the **API Composition Pattern** as the default choice for simple, primary-key-based queries that require assembling data from multiple services without complex filtering or sorting.
  - The AI MUST use the **CQRS Pattern** when a query requires joining, filtering, or sorting large datasets across multiple services, which would result in expensive in-memory joins if API Composition were used.
  - The AI MUST use the **CQRS Pattern** if the service owning the data uses a database that does not efficiently support the required query type (e.g., geospatial queries on a standard key-value store).
  - The AI MUST use the **CQRS Pattern** (via a Query-Only Service) to enforce separation of concerns, ensuring a service is not burdened with high-volume queries that do not align with its primary business capability.

- **API Composition Rules**:
  - **Composer Placement**: The AI MUST place the API Composer in a frontend client ONLY if the client is on a high-bandwidth, low-latency LAN. For clients over the internet/mobile, the AI MUST place the API Composer in an API Gateway or a Standalone Service.
  - **Reactive Execution**: The AI MUST implement API Composition using a reactive programming model (e.g., Java `CompletableFuture`, Project Reactor `Mono`, RxJava). The AI MUST NOT invoke provider services sequentially unless one service explicitly depends on the output of another.
  - **High Availability**: The AI MUST mitigate reduced availability in API Composers by implementing caching for provider responses and designing the composer to return incomplete data (graceful degradation) if a non-critical provider service fails.

- **CQRS Architecture Rules**:
  - **Segregation**: The AI MUST ensure the Command Side data model is completely separated from the Query Side data model.
  - **Event-Driven Updates**: The AI MUST ensure the Query Side is updated EXCLUSIVELY by subscribing to domain events published by the Command Side.
  - **Handling Concurrency**: If a CQRS view subscribes to events from multiple aggregate types, the AI MUST implement concurrency controls (e.g., pessimistic/optimistic locking, or atomic attribute updates) in the Data Access Object (DAO) to prevent concurrent event handlers from overwriting each other.
  - **Idempotency**: The AI MUST ensure CQRS event handlers are idempotent. The handler MUST track the `max(eventId)` processed for each aggregate instance within the view datastore and ignore events with IDs less than or equal to the tracked ID.
  - **Replication Lag Mitigation**: When generating API responses, the AI MUST provide mechanisms for the client to handle eventual consistency (e.g., the command API returns a token/event ID, and the query API validates if the view has processed that token).
  - **View Rebuilding**: The AI MUST support adding or updating CQRS views by designing mechanisms to process archived events (e.g., from AWS S3 using Apache Spark) and incrementally calculating snapshots.

- **NoSQL CQRS Implementation (e.g., DynamoDB) Rules**:
  - **Schema Design**: The AI MUST structure the view table schema based on the query access patterns. For queries requiring sorting/filtering, the AI MUST utilize composite primary keys (Partition Key + Sort Key) and Secondary Indexes.
  - **Efficient Updates**: The AI MUST favor granular attribute update operations (e.g., DynamoDB `UpdateItem`) over full-item replacements (e.g., `PutItem`) to avoid lost updates during concurrent event processing.
  - **Idempotent Updates via Conditionals**: The AI MUST utilize the database's conditional expression capabilities (e.g., DynamoDB `attribute_not_exists(aggregateTracker) OR aggregateTracker < :eventId`) to automatically reject duplicate events at the database level.
  - **Pagination**: The AI MUST implement pagination for queries returning lists, returning an opaque pagination token to the client rather than relying on position-based offsets.

@Workflow
1. **Query Analysis**: Analyze the requested query operation. Identify which services hold the required data, what the filtering/sorting criteria are, and the expected payload size.
2. **Select Pattern**: 
   - IF the query is a simple primary-key lookup across services without cross-service filtering/sorting, proceed to **Step 3 (API Composition)**.
   - IF the query requires cross-service filtering, sorting, or uses unsupported database indexing, proceed to **Step 4 (CQRS)**.
3. **Implement API Composition**:
   - Determine the location of the API Composer (API Gateway vs. Standalone Service).
   - Write declarative, reactive code to invoke provider services concurrently.
   - Implement error handling to return cached or partial data when a provider fails.
4. **Implement CQRS**:
   - Define the Query Side data model optimized specifically for the required query (e.g., document store, text search engine).
   - Map domain events from the Command Side to update operations on the Query Side.
   - Implement the DAO layer with strict idempotency (tracking `eventId`) and concurrency controls (attribute-level updates or optimistic locking).
   - Expose the Query API, implementing pagination and client-side tokens for replication lag detection.

@Examples (Do's and Don'ts)

- **API Composition Concurrency**
  - [DO]: Use reactive wrappers to fetch data concurrently.
    ```java
    Mono<OrderInfo> orderInfo = orderService.findOrderById(orderId);
    Mono<Optional<TicketInfo>> ticketInfo = kitchenService.findTicketByOrderId(orderId).map(Optional::of).onErrorReturn(Optional.empty());
    Mono<Tuple2<OrderInfo, Optional<TicketInfo>>> combined = Mono.when(orderInfo, ticketInfo);
    ```
  - [DON'T]: Block and wait for each service sequentially.
    ```java
    // Anti-pattern: Synchronous sequential blocking
    OrderInfo orderInfo = orderService.findOrderById(orderId);
    TicketInfo ticketInfo = kitchenService.findTicketByOrderId(orderId); 
    ```

- **Query Pattern Selection**
  - [DO]: Implement a CQRS view if you need to find an order history filtered by a keyword that exists in the `KitchenService` but sorted by a date that exists in the `OrderService`.
  - [DON'T]: Pull 10,000 orders from `OrderService` and 10,000 tickets from `KitchenService` into the API Gateway to perform an in-memory join and filter.

- **CQRS Event Idempotency in NoSQL**
  - [DO]: Use conditional expressions to enforce idempotency directly in the database update.
    ```java
    UpdateItemSpec spec = new UpdateItemSpec()
        .withPrimaryKey("orderId", orderId)
        .withUpdateExpression("SET deliveryStatus = :status, DeliveryAggregateTracker = :eventId")
        .withConditionExpression("attribute_not_exists(DeliveryAggregateTracker) OR DeliveryAggregateTracker < :eventId");
    ```
  - [DON'T]: Read the record into memory, check the event ID, and write the record back without locks, as this causes race conditions and lost updates.

- **Handling Partial Failures in API Composition**
  - [DO]: Design the composer to return a partial response if a non-essential backend service is unreachable.
    ```java
    // Graceful degradation
    Mono<Optional<DeliveryInfo>> deliveryInfo = deliveryService.findDeliveryByOrderId(orderId)
        .map(Optional::of)
        .onErrorReturn(Optional.empty());
    ```
  - [DON'T]: Fail the entire query and return an HTTP 500 to the user just because a supplementary service (like delivery tracking) is temporarily down.