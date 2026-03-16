@Domain
This rule set is activated when the AI is tasked with architecting, designing, refactoring, or writing business logic for a microservices-based application. Triggering contexts include domain modeling, defining database schemas/entities, implementing service classes, defining event-driven architectures, handling data consistency within services, and utilizing Domain-Driven Design (DDD) patterns (such as Aggregates, Entities, Value Objects, and Domain Events).

@Vocabulary
- **Hexagonal Architecture**: An architectural style where business logic is at the core, surrounded by inbound adapters (handling external requests) and outbound adapters (invoking external applications/databases).
- **Transaction Script Pattern**: A procedural business logic organization pattern where classes that implement behavior (scripts) are separate from those that store state (pure data classes).
- **Domain Model Pattern**: An object-oriented business logic organization pattern consisting of a network of relatively small classes (an object model) that contain both state and behavior.
- **Domain-Driven Design (DDD)**: An approach for building complex software centered on the development of an object-oriented domain model.
- **Entity**: A DDD building block representing an object with persistent identity (e.g., mapped via JPA `@Entity`).
- **Value Object**: A DDD building block representing an immutable object that is a collection of values, where instances with identical attributes are interchangeable.
- **Repository**: A DDD building block that encapsulates the database access mechanism for persistent entities.
- **Domain Service**: A class that implements business logic that does not naturally belong in an Entity or Value Object.
- **Aggregate**: A cluster of domain objects (entities and value objects) within an explicit boundary that can be treated as a single unit.
- **Aggregate Root**: The single root entity of an Aggregate, which serves as the only entry point for external classes to reference or update the Aggregate.
- **Invariants**: Business rules within an aggregate that must be enforced at all times.
- **Domain Event**: A class representing a state change or a notable happening to an aggregate, named using a past-participle verb (e.g., `OrderCreated`).
- **Event Enrichment**: The practice of including additional data in a domain event beyond the aggregate ID, providing consumers with necessary data to avoid callback queries.
- **Event Storming**: An event-centric workshop format used to quickly understand a complex domain by brainstorming events, triggers (commands/time/external), and aggregates.

@Objectives
- Structure business logic correctly based on complexity (Procedural for simple, Object-Oriented/DDD for complex).
- Enforce explicit boundaries around business objects using the DDD Aggregate pattern to prevent invariant violations.
- Eliminate object references that span microservice boundaries, utilizing primary keys for inter-aggregate relationships.
- Strictly align transaction scopes to the boundaries of a single Aggregate to adhere to the constraints of a microservice architecture.
- Ensure state changes are reliably communicated across the system by systematically generating and publishing Domain Events.
- Decouple infrastructure concerns (like messaging APIs) from core domain logic (Aggregates).

@Guidelines

**1. Choosing a Business Logic Organization Pattern**
- When business logic is simple, the AI MUST use the Transaction Script pattern (procedural services with data-only objects).
- When business logic is complex, the AI MUST use the Domain Model pattern applying DDD tactical patterns (Entities, Value Objects, Aggregates).

**2. Designing Aggregates and Boundaries**
- The AI MUST define explicit Aggregate boundaries to clarify the scope of load, update, and delete operations.
- The AI MUST ensure that every Aggregate has a single Aggregate Root entity.
- The AI MUST enforce Aggregate Rule #1: External classes MUST ONLY reference the Aggregate Root. Child entities or value objects inside the Aggregate MUST NOT be referenced or updated directly by external clients.
- The AI MUST define Aggregate granularity to be as small/fine-grained as possible to increase scalability and reduce concurrent update collisions, while remaining large enough to atomically enforce business invariants.

**3. Handling Inter-Aggregate References**
- The AI MUST enforce Aggregate Rule #2: Aggregates MUST reference other Aggregates by identity (primary key, e.g., `Long consumerId`) rather than by object references (e.g., `Consumer consumer`).
- This rule MUST be applied indiscriminately, even if the referenced Aggregate currently resides in the same microservice, to facilitate future decomposition and simplify NoSQL/sharded persistence.

**4. Managing Transaction Boundaries**
- The AI MUST enforce Aggregate Rule #3: A single ACID transaction MUST ONLY create or update a single Aggregate.
- If a use case requires updating multiple Aggregates, the AI MUST NOT wrap them in a single local transaction. Instead, the AI MUST implement a Saga (a sequence of local transactions coordinated via asynchronous messaging).

**5. Designing and Generating Domain Events**
- When an Aggregate is created or undergoes a significant state transition, the AI MUST define a Domain Event.
- The AI MUST name Domain Events using past-participle verbs (e.g., `TicketAcceptedEvent`).
- The AI MUST apply Event Enrichment where appropriate, adding necessary state details to the event payload to prevent consumers from needing to perform synchronous callbacks to fetch data.
- The AI MUST separate event generation from event publishing. Aggregates MUST NOT be injected with messaging APIs.
- To return events from an Aggregate to a Domain Service, the AI MUST use one of two patterns:
  1. The aggregate method returns a list of events (e.g., `List<DomainEvent>`).
  2. The aggregate accumulates events in an internal list, accessed via a superclass method (e.g., `registerDomainEvent()`).

**6. Publishing Domain Events**
- The AI MUST ensure that Domain Services execute local database updates and event publishing within the same ACID transaction.
- The AI MUST utilize a transactional messaging mechanism (e.g., Transactional Outbox pattern) to prevent data inconsistencies if the application crashes between updating the DB and sending the event.
- The AI MUST implement a type-safe domain event publisher (e.g., `AbstractAggregateDomainEventPublisher`) to guarantee that a service only publishes events valid for its specific Aggregate.

**7. Structuring Inbound and Outbound Adapters**
- The AI MUST encapsulate external interaction using the Hexagonal Architecture pattern.
- Inbound adapters (e.g., REST Controllers, Command Handlers, Event Consumers) MUST only invoke Domain Services.
- Outbound adapters MUST implement Repositories (for DB access) or Event Publishers (for message brokers).

@Workflow
When tasked with designing or modifying the business logic for a microservice, the AI MUST follow this step-by-step algorithm:

1. **Assess Complexity**: Evaluate if the logic is simple CRUD (use Transaction Script) or complex state-driven rules (use Domain Model). If Domain Model, proceed to step 2.
2. **Identify Aggregates**: Analyze the nouns/domain concepts. Group related entities and value objects into an Aggregate. Select the Aggregate Root.
3. **Refactor Relationships**: Scan the domain model for inter-aggregate object references. Replace all object references to other aggregates with identity fields (primary keys).
4. **Define State Machine & Invariants**: Determine the states the Aggregate can hold and the business rules (invariants) it must enforce. Define operations on the Aggregate Root to handle these transitions.
5. **Define Domain Events**: Create event classes (past-participle named) for each state change. Enrich the payload with data necessary for downstream consumers.
6. **Implement Aggregate Behavior**: Write methods on the Aggregate Root that validate invariants, mutate local state, and output a `List<DomainEvent>`. Do not inject messaging or repository services into the Aggregate.
7. **Implement Domain Services**: Write service classes that are called by Inbound Adapters. For each method:
    a. Retrieve the Aggregate via a Repository (or instantiate it).
    b. Invoke the Aggregate Root's business method.
    c. Persist the Aggregate via the Repository.
    d. Publish the returned `List<DomainEvent>` via a transactional event publisher.
8. **Verify Transaction Scope**: Check the Domain Service method. Ensure only ONE aggregate is mutated per transaction. If multiple require mutation, outline a Saga definition.

@Examples (Do's and Don'ts)

**Principle: Inter-Aggregate References**
- [DO] 
```java
@Entity
public class Order {
    @Id
    private Long id;
    private Long consumerId; // Primary key reference
    private Long restaurantId; // Primary key reference
    @Embedded
    private OrderLineItems orderLineItems; // Value Object inside Aggregate
}
```
- [DON'T] 
```java
@Entity
public class Order {
    @Id
    private Long id;
    @ManyToOne
    private Consumer consumer; // ANTI-PATTERN: Object reference to another Aggregate
    @ManyToOne
    private Restaurant restaurant; // ANTI-PATTERN: Object reference to another Aggregate
}
```

**Principle: Aggregate Event Generation**
- [DO]
```java
public class Ticket {
    public List<DomainEvent> accept(ZonedDateTime readyBy) {
        this.acceptTime = ZonedDateTime.now();
        this.readyBy = readyBy;
        return Collections.singletonList(new TicketAcceptedEvent(readyBy));
    }
}
```
- [DON'T]
```java
public class Ticket {
    @Autowired
    private DomainEventPublisher publisher; // ANTI-PATTERN: Infrastructure injected into Domain

    public void accept(ZonedDateTime readyBy) {
        this.acceptTime = ZonedDateTime.now();
        this.readyBy = readyBy;
        publisher.publish(new TicketAcceptedEvent(readyBy)); // ANTI-PATTERN
    }
}
```

**Principle: Domain Service Transaction and Publishing Boundaries**
- [DO]
```java
@Transactional
public class KitchenService {
    @Autowired
    private TicketRepository ticketRepository;
    @Autowired
    private TicketDomainEventPublisher domainEventPublisher;

    public void accept(long ticketId, ZonedDateTime readyBy) {
        Ticket ticket = ticketRepository.findById(ticketId)
            .orElseThrow(() -> new TicketNotFoundException(ticketId));
        List<TicketDomainEvent> events = ticket.accept(readyBy);
        domainEventPublisher.publish(ticket, events); // Published transactionally alongside DB commit
    }
}
```
- [DON'T]
```java
@Transactional
public class KitchenService {
    @Autowired
    private TicketRepository ticketRepository;
    @Autowired
    private OrderRepository orderRepository; 

    public void acceptAndApprove(long ticketId, long orderId) {
        Ticket ticket = ticketRepository.findById(ticketId).get();
        ticket.accept();
        Order order = orderRepository.findById(orderId).get();
        order.approve(); // ANTI-PATTERN: Modifying multiple aggregates in one transaction. MUST use a Saga.
    }
}
```

**Principle: Event Naming and Enrichment**
- [DO]
```java
// Past-participle, contains aggregate ID and enriched data
public class OrderCreatedEvent implements DomainEvent {
    private List<OrderLineItem> lineItems;
    private long restaurantId;
    private String restaurantName;
    // Getters and constructors...
}
```
- [DON'T]
```java
// Ambiguous name, forces downstream consumers to immediately make a REST call to fetch data
public class CreateOrderEvent implements DomainEvent {
    private long orderId;
}
```