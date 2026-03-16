@Domain
Trigger these rules when the user requests architectural design, system modeling, refactoring, or implementation of microservices architecture (MSA), RESTful API service compositions, Internet of Things (IoT) backend integrations, event-driven architectures, or decentralized data management strategies.

@Vocabulary
- **Smart Objects / Digitized Elements**: Physical, mechanical, and electrical systems in personal/professional environments that are computationally sensitive, perceptive, and responsive.
- **D2D (Device-to-Device) / D2C (Device-to-Cloud)**: Integration and data-transmission protocols linking embedded systems to one another or to remote cloud applications.
- **MSA (Microservices Architecture)**: An architectural style consisting of fine-grained, horizontally-scalable, independently-deployable, API-driven, technology-agnostic, and loosely-coupled services.
- **Service Composition**: The act of combining multiple distributed microservices to realize composite, process-aware, and business-critical applications.
- **Orchestration**: A centralized service composition method where a central coordinator/engine guides and guarantees control flows, calling participating services sequentially or synchronously.
- **Choreography**: A decentralized, peer-to-peer service composition method relying on an event-driven architecture (EDA) where services react to events asynchronously via an event bus.
- **Smart Endpoints and Dumb Pipes**: The choreography principle where the routing mechanism (event bus) contains no logic, and all business logic is embedded within the participating microservices.
- **Event-Command-Transformation Pattern**: A pattern used in choreography to separate a service from its consumers by using an intermediate component that transforms an event into a specific command.
- **Polyglot Persistence**: The practice of using different types of data storage technologies to handle varying data requirements across decoupled microservices.
- **Eventual Consistency**: A consistency model used in decentralized data management where data changes are propagated across microservices asynchronously, requiring race condition handling.

@Objectives
- The AI MUST enforce the Single Responsibility Principle for all microservices, ensuring they are modular, loosely coupled, and highly cohesive.
- The AI MUST design system interactions using RESTful interfaces separated strictly into client-server boundaries, ensuring technology-agnostic implementations.
- The AI MUST evaluate and select the correct service composition method (Orchestration, Choreography, or Hybrid) based on the business process requirements (synchronous vs. asynchronous, centralized vs. parallel).
- The AI MUST enforce decentralized data management by assigning a distinct, isolated data store to every microservice.
- The AI MUST eliminate distributed SQL joins across microservice boundaries and substitute them with API-level aggregations or composite microservices.

@Guidelines

**1. Microservice Architecture & RESTful API Principles**
- The AI MUST design microservices to run in their own process space and deploy independently via containers.
- The AI MUST enforce a strict Client-Server constraint: Client and server applications must evolve independently with zero dependencies other than resource URIs.
- The AI MUST implement cache-ability: Responses must provide caching metadata so clients/proxies can store frequently-accessed data to reduce server load and latency.

**2. Service Composition Selection & Implementation**
- **When to use Orchestration**: The AI MUST apply orchestration when processes are sequential (zero possibility for parallel execution), require tight flow control, involve long-running stateful transactions, or when centralizing the business rules is strictly mandated.
- **Orchestration Fault Tolerance**: The AI MUST implement failure-handling mechanisms, such as compensations, retries, and repair activities within the orchestrator to prevent a single point of failure from crashing the business process.
- **When to use Choreography**: The AI MUST apply choreography for event-driven applications requiring parallel processing, shared-nothing architecture, and asynchronous communication without blocking.
- **Event Bus Utilization**: The AI MUST utilize an event bus (a "dumb pipe") to route events between "smart" microservices in choreographed architectures.
- **Decoupling Producers and Consumers**: The AI MUST employ the Event-Command-Transformation pattern if a consuming service requires specific logic filtering (e.g., filtering VIP customers for a payment service based on an order-placed event).

**3. Hybrid Composition Architectures**
- The AI MUST utilize Hybrid Patterns when a single architectural style does not fit the complexity of the application.
- **Hybrid Pattern 1 (Choreography between, Orchestration within)**: The AI MUST design services to react to an event bus externally, but internally orchestrate synchronous/asynchronous calls to sub-services.
- **Hybrid Pattern 2 (Reactive Orchestrator)**: The AI MUST use a reactive coordinator that listens to an event stream, processes business rules, and issues commands back to the stream for decoupled services to consume.
- **Hybrid Pattern 3 (Event-Driven Orchestration)**: The AI MUST integrate a workflow engine (e.g., BPMN) with REST APIs and an asynchronous message broker (e.g., AMQP) to replace tight point-to-point service adapters.

**4. Decentralized Data Management**
- The AI MUST map one exclusive database/data store to each microservice.
- The AI MUST utilize Polyglot Persistence, choosing the optimal database type (e.g., NoSQL document store, key-value store, relational, in-memory) based on the specific microservice's read/write volume, data structure, querying, and lifecycle needs.
- The AI MUST explicitly prohibit the use of SQL JOIN operations across different microservice databases.
- The AI MUST implement a top-level aggregation/composite microservice (e.g., a "Timeline Service") that fetches data from underlying microservices via REST APIs to combine data, utilizing bulk fetch endpoints to reduce network round-trips.
- The AI MUST implement conditional handling in the application logic to account for Eventual Consistency, resolving race conditions where underlying decentralized data may change between requests.
- The AI MUST apply a two-phase commit mechanism ONLY if strong consistency is a strict, unavoidable requirement for related distributed data.

@Workflow
1. **Domain Decomposition**: Analyze the business requirement and break it down into autonomous, fine-grained microservices following the Single Responsibility Principle.
2. **Data Modeling**: Assign an isolated, optimal database technology to each microservice (Polyglot Persistence). 
3. **API Definition**: Expose the capabilities of each microservice via stateless, cacheable RESTful APIs.
4. **Composition Strategy Assessment**: 
   - If the flow is strictly sequential and requires centralized state management, apply Orchestration.
   - If the flow requires parallel, non-blocking, asynchronous reactions, apply Choreography via an Event Bus.
   - If the flow requires both, implement a Hybrid pattern (e.g., Reactive Orchestrator).
5. **Data Aggregation Design**: If a client requires joined data across domains, create a composite microservice. Expose bulk-fetch APIs on the underlying services and have the composite service perform API-level data aggregation.
6. **Resiliency Planning**: Embed retry logic, compensation transactions, and race-condition handling to account for network latency, service failures, and eventual consistency.

@Examples

**[DO] - Decentralized Data Aggregation (Avoiding SQL Joins)**
```javascript
// Composite Microservice: Timeline Service
// The AI creates a top-level service to aggregate data instead of using database-level SQL joins.

async function getUserTimeline(userId) {
    // 1. Fetch friend IDs from Friend Service
    const friends = await fetch(`http://friend-service/api/friends/${userId}`);
    const friendIds = friends.map(f => f.id);

    // 2. Use a bulk-fetch endpoint on the User Service to get all friend details in one network call
    const users = await fetch(`http://user-service/api/users/bulk?ids=${friendIds.join(',')}`);

    // 3. Fetch recent messages from the Message Service
    const messages = await fetch(`http://message-service/api/messages/recent?userIds=${friendIds.join(',')}`);

    // 4. Aggregate data in memory and return to client
    return aggregateTimelineData(users, messages);
}
```

**[DON'T] - Distributed SQL Joins**
```sql
/* The AI MUST NEVER generate monolithic SQL queries that span across microservice boundaries or directly access another service's database. */
SELECT u.name, m.content 
FROM UserService.Users u
JOIN MessageService.Messages m ON u.id = m.userId
JOIN FriendService.Friends f ON u.id = f.friendId
WHERE f.userId = 123;
```

**[DO] - Event-Command-Transformation Pattern in Choreography**
```java
// Intermediate transformer service decouples the producer from the consumer
public class OrderEventTransformer {
    public void onOrderPlaced(OrderEvent event) {
        // Business rule injected as a transformation, keeping PaymentService agnostic
        if (event.getCustomerType().equals("VIP")) {
            eventBus.publish(new InvoiceCommand(event.getOrderId()));
        } else {
            eventBus.publish(new ProcessPaymentCommand(event.getOrderId(), event.getAmount()));
        }
    }
}
```

**[DON'T] - Tight Coupling in Choreography**
```java
// The AI MUST NEVER hardcode consumer-specific business rules into the producing service or the consuming service.
public class PaymentService {
    public void handleOrderPlacedEvent(OrderEvent event) {
        // Anti-pattern: Payment service now has to know about "VIP" business rules
        if (event.getCustomerType().equals("VIP")) {
            ignorePayment();
        } else {
            processPayment();
        }
    }
}
```