# @Domain
These rules MUST trigger whenever the AI is tasked with designing, architecting, refactoring, or implementing client-to-service communication, external APIs, API Gateways, Backends for Frontends (BFF), or API composition logic within a microservice architecture. 

# @Vocabulary
*   **API Gateway**: A service that acts as the single entry point into the application from outside the firewall, responsible for request routing, API composition, and protocol translation.
*   **Backends for Frontends (BFF)**: An architectural pattern that defines a separate, standalone API gateway for each specific type of client (e.g., mobile, web, third-party).
*   **API Composition**: A pattern where a gateway or composer service handles a client request by invoking multiple backend services and aggregating the results into a single response.
*   **Edge Functions**: Request-processing functions implemented at the edge of an application (e.g., Authentication, Authorization, Rate Limiting, Caching, Metrics Collection, Request Logging).
*   **Protocol Translation**: The process of translating between client-friendly protocols (e.g., HTTP, WebSockets) and internal, client-unfriendly microservice protocols (e.g., gRPC, AMQP).
*   **Reactive Programming**: A declarative programming paradigm used to handle asynchronous data streams and concurrent operations cleanly, utilizing abstractions like `CompletableFuture` (Java), `Mono`/`Flux` (Project Reactor), or `Promise` (JavaScript).
*   **Callback Hell**: An anti-pattern occurring when asynchronous callbacks are heavily nested, leading to unmaintainable and error-prone code.
*   **GraphQL Schema**: A definition of the server-side data model (nodes/types) and the queries/mutations a client can execute.
*   **Resolver**: A function in a GraphQL server that fetches the data for a specific field in the schema by invoking backend services.
*   **DataLoader**: A utility (especially in NodeJS/GraphQL) used to implement server-side batching and caching to optimize loading and prevent N+1 query performance issues.
*   **Spring Cloud Gateway**: A Spring-based API Gateway framework utilizing Spring 5, Spring Boot 2, and Spring WebFlux (Project Reactor) to define routing and composition reactively.

# @Objectives
*   **Encapsulate Architecture**: Hide the internal microservice decomposition from external clients to allow the architecture to evolve without breaking clients.
*   **Optimize Client Interactions**: Provide client-specific APIs that minimize network round-trips over high-latency networks (internet/mobile) using API composition.
*   **Decentralize API Ownership**: Empower client-facing teams to own, deploy, and manage their specific API gateways (BFF pattern) to prevent organizational bottlenecks.
*   **Ensure High Performance & Resilience**: Implement asynchronous/non-blocking I/O, reactive concurrent service invocations, and circuit breakers to handle partial backend failures safely.
*   **Centralize Edge Security**: Authenticate external requests at the edge before they reach internal services, ensuring unauthenticated traffic never penetrates the firewall.

# @Guidelines

### 1. Client-to-Service Communication Rules
*   The AI MUST NOT allow external clients (web, mobile, third-party) to directly invoke backend microservices.
*   The AI MUST introduce an API Gateway or BFF layer to mediate all external requests.
*   The AI MUST design coarse-grained APIs for clients that return all data required for a specific view or interaction in a single network request via API composition.

### 2. API Gateway Architecture & Edge Functions
*   The AI MUST implement Edge Functions (Authentication, Authorization, Rate Limiting, Request Logging) inside the API Gateway, NOT scattered across internal backend services.
*   The AI MUST separate the API Gateway into two distinct layers: an API layer (client-specific routing/composition) and a Common layer (shared edge functions).
*   The AI MUST apply the Backends for Frontends (BFF) pattern when dealing with multiple distinct clients (e.g., iOS, Android, Web, Public API) to prevent a single monolithic gateway from becoming a development bottleneck.
*   When defining ownership in a BFF architecture, the AI MUST assign the ownership of each BFF module to the respective client team (e.g., the mobile team owns the mobile BFF).

### 3. API Composition & Concurrency
*   When a gateway endpoint requires data from multiple backend services, the AI MUST implement API composition within the gateway.
*   The AI MUST invoke backend services concurrently whenever there are no dependencies between the service calls.
*   The AI MUST NOT invoke independent backend services sequentially, as this causes the total response time to equal the sum of all service response times.
*   The AI MUST use Reactive Programming abstractions (e.g., `Mono.when()`, `Promise.all()`) to manage concurrent invocations.
*   The AI MUST NOT use nested asynchronous callbacks (callback hell) or blocking abstractions (`Future.get()`) to aggregate data.

### 4. Handling Partial Failures
*   The AI MUST apply the Circuit Breaker pattern to all remote service invocations within the API Gateway to prevent the gateway from running out of threads or resources when a backend service fails or exhibits high latency.
*   The AI MUST implement fallback logic (e.g., returning cached data, omitting non-critical data, or returning a default value) when a non-critical backend service is unavailable.

### 5. Implementation with Spring Cloud Gateway
*   When implementing a Java-based API Gateway, the AI MUST use Spring Cloud Gateway with Spring WebFlux.
*   The AI MUST use `RouteLocator` to define standard proxy routes (e.g., matching paths and routing to service URLs).
*   The AI MUST use `RouterFunction` to route to custom handler methods (e.g., `OrderHandlers::getOrderDetails`) when API composition or protocol translation is required.

### 6. Implementation with GraphQL
*   When designing an API Gateway for highly diverse client data requirements, the AI MUST consider using GraphQL.
*   The AI MUST define a strictly typed GraphQL schema containing `Query` types and related object types.
*   The AI MUST attach Resolver functions to schema fields to fetch data from the backend REST/gRPC services.
*   The AI MUST implement the `DataLoader` pattern (batching and caching) inside GraphQL resolvers to coalesce multiple independent downstream requests into a single batch request, preventing the N+1 query problem.

# @Workflow
When tasked with designing or implementing an external API layer in a microservices architecture, the AI MUST follow this exact step-by-step process:

1.  **Client Analysis**: Identify all external clients (mobile, single-page app, third-party API consumers). Determine their network constraints and specific data requirements.
2.  **Pattern Selection**:
    *   If there is only one client type or a very simple application, select the standard **API Gateway pattern**.
    *   If there are multiple client types with varying deployment cycles and team structures, select the **Backends for Frontends (BFF) pattern**.
3.  **Endpoint Definition**: Define coarse-grained API endpoints tailored exactly to the needs of the client UI/UX, explicitly mapping out which internal services own the necessary underlying data.
4.  **Edge Function Centralization**: Specify and implement authentication, authorization, and rate limiting at the gateway level.
5.  **Technology Selection**: Choose the implementation framework based on the ecosystem (e.g., Spring Cloud Gateway for Java/Spring, Apollo GraphQL + Express for NodeJS).
6.  **Reactive Composition Implementation**: Write the API composition logic. For every endpoint requiring data from multiple services:
    *   Identify independent backend calls.
    *   Wrap backend invocations in reactive abstractions (`Mono`, `Promise`).
    *   Execute independent calls in parallel.
    *   Map and aggregate the reactive results into a single client-facing response object.
7.  **Resilience Implementation**: Wrap all outgoing network calls from the Gateway with Circuit Breakers and configure appropriate timeouts and fallback behaviors.
8.  **Performance Optimization**: If using GraphQL, explicitly wrap backend invocations in a `DataLoader` to batch requests and eliminate N+1 latency issues.

# @Examples (Do's and Don'ts)

### 1. Client-to-Service Communication
**[DON'T]** Allow a mobile client to compose data by calling services directly over the internet:
```javascript
// BAD: Client performing API composition over high-latency network
async function getOrderDetails(orderId) {
    const order = await fetch(`https://api.example.com/orders/${orderId}`);
    const ticket = await fetch(`https://api.example.com/kitchen/ticket/${orderId}`);
    const delivery = await fetch(`https://api.example.com/delivery/${orderId}`);
    return { ...order, ticket, delivery };
}
```

**[DO]** Route through an API Gateway that returns a coarse-grained response:
```javascript
// GOOD: Client makes a single request to the API Gateway/BFF
async function getOrderDetails(orderId) {
    // The Gateway handles the composition internally over the high-speed LAN
    return await fetch(`https://gateway.example.com/api/mobile/v1/order-details/${orderId}`);
}
```

### 2. API Composition Concurrency (Spring Cloud Gateway / Project Reactor)
**[DON'T]** Invoke independent backend services sequentially, blocking or summing response times:
```java
// BAD: Sequential blocking calls increase latency
public OrderDetails getOrderDetails(String orderId) {
    OrderInfo orderInfo = orderService.findOrderById(orderId).block(); // Blocks!
    TicketInfo ticketInfo = kitchenService.findTicketByOrderId(orderId).block(); // Waits for order!
    DeliveryInfo deliveryInfo = deliveryService.findDeliveryByOrderId(orderId).block(); // Waits for ticket!
    return new OrderDetails(orderInfo, ticketInfo, deliveryInfo);
}
```

**[DO]** Use reactive abstractions to fetch independent data concurrently and handle partial failures:
```java
// GOOD: Concurrent reactive composition
public Mono<ServerResponse> getOrderDetails(ServerRequest serverRequest) {
    String orderId = serverRequest.pathVariable("orderId");

    Mono<OrderInfo> orderInfo = orderService.findOrderById(orderId);
    
    // Treat non-critical data as Optional and provide a fallback on error
    Mono<Optional<TicketInfo>> ticketInfo = kitchenService.findTicketByOrderId(orderId)
        .map(Optional::of)
        .onErrorReturn(Optional.empty());

    Mono<Optional<DeliveryInfo>> deliveryInfo = deliveryService.findDeliveryByOrderId(orderId)
        .map(Optional::of)
        .onErrorReturn(Optional.empty());

    // Execute concurrently using Mono.when / Mono.zip
    Mono<Tuple3<OrderInfo, Optional<TicketInfo>, Optional<DeliveryInfo>>> combined = 
        Mono.zip(orderInfo, ticketInfo, deliveryInfo);

    Mono<OrderDetails> orderDetails = combined.map(tuple -> 
        OrderDetails.makeOrderDetails(tuple.getT1(), tuple.getT2(), tuple.getT3())
    );

    return orderDetails.flatMap(details -> ServerResponse.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .body(fromObject(details)));
}
```

### 3. GraphQL Resolvers & Batching
**[DON'T]** Write GraphQL resolvers that trigger N+1 backend network requests sequentially:
```javascript
// BAD: Triggers N network calls if 10 orders are queried
function resolveOrderRestaurant({ restaurantId }, args, context) {
    // Makes a distinct HTTP request for EVERY order in the array
    return context.restaurantServiceProxy.findRestaurant(restaurantId); 
}
```

**[DO]** Use `DataLoader` in the API Gateway to batch and cache backend requests:
```javascript
// GOOD: Uses DataLoader to coalesce requests
const DataLoader = require('dataloader');

class RestaurantServiceProxy {
    constructor() {
        // Initializes DataLoader with a batch fetching function
        this.dataLoader = new DataLoader(restaurantIds => this.batchFindRestaurants(restaurantIds));
    }

    findRestaurant(restaurantId) {
        // Defers the load to be batched with other simultaneous requests
        return this.dataLoader.load(restaurantId);
    }

    batchFindRestaurants(restaurantIds) {
        // Makes a SINGLE network request for N IDs
        return fetch(`http://restaurant-service/restaurants?ids=${restaurantIds.join(',')}`);
    }
}

function resolveOrderRestaurant({ restaurantId }, args, context) {
    return context.restaurantServiceProxy.findRestaurant(restaurantId);
}
```