@Domain
These rules apply when the AI is tasked with designing, implementing, refactoring, or integrating components related to Domain Events, Event-Driven Architecture (EDA), Publish-Subscribe mechanisms, Event Stores, message-based integrations, or eventual consistency patterns within a Domain-Driven Design (DDD) ecosystem.

@Vocabulary
- **Domain Event**: A full-fledged part of the domain model representing something of significance that happened in the domain (e.g., a state change or command execution), named in the past tense.
- **Eventual Consistency**: A consistency model where changes in one Aggregate or Bounded Context are asynchronously propagated to other Aggregates or systems via Domain Events, rather than utilizing atomic, two-phase commit (XA) global transactions.
- **DomainEventPublisher**: A lightweight, local Publish-Subscribe component (often implemented using ThreadLocal) that executes in the same process space and thread, used by Aggregates to publish events synchronously to registered subscribers.
- **DomainEventSubscriber**: A component (typically registered by an Application Service) that listens for specific Domain Events published during a single transaction.
- **Event Store**: A specialized storage area (e.g., database table) residing in the same persistence store as the domain model, used to transactionally save serialized Domain Events alongside Aggregate state changes.
- **StoredEvent**: A database entity wrapping a serialized Domain Event, containing an auto-incrementing ID, the event body (JSON), occurred-on timestamp, and event type name.
- **NotificationLog**: A RESTful resource representing a sequence of Events. 
- **Current Log**: A mutable NotificationLog containing the most recent notifications (up to a predefined limit, e.g., 20).
- **Archived Log**: An immutable NotificationLog containing older events that have reached the size limit.
- **PublishedMessageTracker**: A persistent application component used by a background publisher to track the highest `eventId` that has been successfully published to a messaging middleware.
- **Idempotent Receiver**: A message subscriber designed to safely handle duplicate message deliveries either by intrinsic domain logic or by tracking processed message IDs.
- **Event Enrichment**: The practice of adding extra data properties to an Event so that subscribers do not need to perform callbacks (reverse queries) to the originating system to fetch required context.

@Objectives
- Accurately capture and model significant occurrences in the business domain as explicit, immutable Domain Event objects.
- Eliminate two-phase commits (XA transactions) by decoupling Aggregate state changes using eventual consistency.
- Enforce the DDD rule of thumb: Modify exactly *one* Aggregate instance per database transaction.
- Guarantee consistency between domain model updates and event publishing by using an Event Store that shares the domain's datastore.
- Securely and reliably forward stored events to remote Bounded Contexts using RESTful Notification Logs or Messaging Middleware.
- Protect downstream subscribers from duplicate message delivery by enforcing idempotency and explicit message de-duplication tracking.

@Guidelines

# Event Modeling
- The AI MUST name Domain Events according to the Ubiquitous Language, explicitly using past tense verbs (e.g., `BacklogItemCommitted`, NOT `CommitBacklogItem` or `BacklogItemEvent`).
- The AI MUST design Domain Events to be immutable. State MUST be fully initialized via the constructor.
- The AI MUST implement a common interface for all Domain Events (e.g., `DomainEvent`) that guarantees an `occurredOn()` method returning a timestamp (e.g., `java.util.Date`).
- The AI MUST include the identity of the Aggregate on which the event occurred, any associated parameters/Aggregate identities involved in the command, and the Tenant Identity (in multitenant systems).
- The AI MUST apply "Event Enrichment" by including supplemental descriptive data in the event if it prevents remote subscribers from having to execute expensive callback queries to the originating Bounded Context.
- The AI MUST NOT embed full Aggregate object graphs or Entity instances inside a Domain Event. Use basic types, identity Value Objects, and simple descriptive Value Objects.
- The AI MUST assign a unique identity to a Domain Event ONLY IF it is modeled as an Aggregate itself (created directly by a client rather than as a side-effect of another Aggregate) or if required for deduplication over middleware.

# Local Publishing and Subscribing
- The AI MUST use a lightweight, thread-local `DomainEventPublisher` to publish events synchronously within the same process and thread.
- The AI MUST ensure that the `DomainEventPublisher` clears/resets its subscriber list at the beginning of every request (e.g., via a Web Filter) to prevent thread-pooling memory leaks or cross-request pollution.
- The AI MUST place the `DomainEventPublisher.instance().publish(...)` call inside the Aggregate's behavior method immediately after the state mutation occurs.
- The AI MUST register `DomainEventSubscriber` instances within Application Services or Domain Services *before* retrieving the Aggregate and executing its behavior.
- The AI MUST strictly forbid a `DomainEventSubscriber` from modifying a second Aggregate instance within the same transaction. Subscribers in the same transaction may only queue events, save to an Event Store, or send emails.

# Event Store and Infrastructure Consistency
- To prevent message loss or ghost messages, the AI MUST NOT directly publish to external messaging middleware from within the Aggregate or the primary Application Service transaction if the middleware does not share the same database.
- The AI MUST implement an Event Store within the same persistence mechanism as the domain model to guarantee atomic commits (e.g., persisting the Aggregate and the `StoredEvent` in the same SQL transaction).
- The AI MUST use Aspect-Oriented Programming (AOP) or equivalent interception on Application Services to universally subscribe to all `DomainEvent` types and append them to the Event Store (e.g., serializing the event to JSON).

# Publishing via RESTful Resources (Pull Model)
- If designing a RESTful event feed, the AI MUST group events into a `NotificationLog` object.
- The AI MUST implement a pagination strategy dividing logs into an active "Current Log" and immutable "Archived Logs".
- The AI MUST constrain the size of each NotificationLog (e.g., 20 notifications maximum).
- The AI MUST apply HTTP Caching headers: `Cache-Control: max-age=60` for Current Logs (short cache) and `Cache-Control: max-age=3600` (or greater) for Archived Logs.
- The AI MUST include hypermedia links (`rel=self`, `rel=previous`, `rel=next`) in the representations to allow clients to navigate the log chain.

# Publishing via Messaging Middleware (Push Model)
- The AI MUST decouple the actual message broker dispatching from the Application Service transaction.
- The AI MUST implement a background timer/thread (e.g., Quartz, JMX Timer) to periodically poll the Event Store for unpublished events.
- The AI MUST track the ID of the last successfully published event using a persistent `PublishedMessageTracker` object.
- The AI MUST include the event type, unique message ID, and timestamp as message headers/parameters so subscribers can route and deduplicate without parsing the entire JSON body.

# Consuming and Deduplication
- The AI MUST design client message listeners to parse the incoming message, translate remote concepts into the local Bounded Context, and dispatch to a local Application Service.
- The AI MUST design the receiving Application Service or the Aggregate behavior to be idempotent OR implement explicit deduplication tracking by recording handled message IDs in the subscriber's database.

@Workflow
1. **Discover**: Analyze the domain requirements for phrases like "When [X] happens" to identify the Domain Event.
2. **Model Event**: Create the Domain Event class. Name it in the past tense. Add `occurredOn`, identities of involved Aggregates, and enriching properties. Make it immutable.
3. **Publish Locally**: Inside the mutating Aggregate method, instantiate the Event and pass it to `DomainEventPublisher.instance().publish()`.
4. **Setup Event Store**: Configure an AOP interceptor around the Application Service to subscribe to all events and atomically persist them to an `EventStore` table as JSON alongside the Aggregate transaction.
5. **Configure Forwarding**: 
    - *If REST:* Expose `/notifications` URIs delivering `NotificationLog` resources with HATEOAS navigation.
    - *If Messaging:* Create a background polling service that reads from `EventStore` > `PublishedMessageTracker.lastId`, pushes to RabbitMQ/MoM, and updates the tracker.
6. **Implement Subscriber**: In the remote/downstream Bounded Context, implement an `ExchangeListener` or HTTP Poller. 
7. **Translate and Deduplicate**: In the subscriber, read the payload, deduplicate using the message ID or idempotent business logic, and dispatch a Command to the local Application Service.
8. **Process Eventual Consistency**: The local Application Service retrieves the target local Aggregate and invokes the corresponding local state mutation.

@Examples

[DO] Model a Domain Event named in the past tense, fully initialized via constructor, utilizing Value Objects for identities.
```java
public class BacklogItemCommitted implements DomainEvent {
    private final Date occurredOn;
    private final TenantId tenantId;
    private final BacklogItemId backlogItemId;
    private final SprintId committedToSprintId;

    public BacklogItemCommitted(TenantId aTenantId, BacklogItemId aBacklogItemId, SprintId aSprintId) {
        this.occurredOn = new Date();
        this.tenantId = aTenantId;
        this.backlogItemId = aBacklogItemId;
        this.committedToSprintId = aSprintId;
    }
    
    @Override
    public Date occurredOn() { return this.occurredOn; }
    // ... getters
}
```

[DON'T] Name events as commands, use setters, or embed full ORM Entity objects inside the event.
```java
public class CommitBacklogItemEvent implements DomainEvent {
    public Product product; // Anti-pattern: full aggregate embedded
    public Date date;
    
    public void setDate(Date date) { this.date = date; } // Anti-pattern: mutability
}
```

[DO] Publish an event directly from the Aggregate behavior method.
```java
public class BacklogItem extends ConcurrencySafeEntity {
    public void commitTo(Sprint aSprint) {
        // ... business logic ...
        this.setSprintId(aSprint.sprintId());

        DomainEventPublisher.instance().publish(
            new BacklogItemCommitted(this.tenantId(), this.backlogItemId(), aSprint.sprintId())
        );
    }
}
```

[DON'T] Modify two Aggregates in the same transaction from an event subscriber.
```java
// Anti-pattern: Modifying two aggregates in one transaction
DomainEventPublisher.instance().subscribe(new DomainEventSubscriber<BacklogItemCommitted>() {
    public void handleEvent(BacklogItemCommitted event) {
        Sprint sprint = sprintRepository.sprintOfId(event.sprintId());
        sprint.addBacklogItem(event.backlogItemId()); // VIOLATES AGGREGATE RULE
    }
});
```

[DO] Use an Event Store and AOP to capture all events transparently within the Application Service transaction.
```java
@Aspect
public class EventStoreProcessor {
    @Before("execution(* com.myapp.application.*.*(..))")
    public void listen() {
        DomainEventPublisher.instance().subscribe(new DomainEventSubscriber<DomainEvent>() {
            public void handleEvent(DomainEvent event) {
                EventStore.instance().append(event); // Persists to same DB
            }
            public Class<DomainEvent> subscribedToEventType() { return DomainEvent.class; }
        });
    }
}
```

[DO] Design RESTful Notification logs with hypermedia linking and appropriate cache controls.
```http
HTTP/1.1 200 OK
Content-Type: application/vnd.myapp.notification+json
Cache-Control: max-age=3600

{
    "Link": [
        {"href": "/notifications/61,80", "rel": "next"},
        {"href": "/notifications/41,60", "rel": "self"},
        {"href": "/notifications/21,40", "rel": "previous"}
    ],
    "notifications": [ ... ]
}
```