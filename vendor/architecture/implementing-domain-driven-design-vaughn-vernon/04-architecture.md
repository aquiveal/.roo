@Domain
Software architecture design, refactoring, and implementation tasks involving enterprise applications. These rules activate specifically when applying Domain-Driven Design (DDD) to structure systems, define architectural layers, establish system interfaces (REST, SOA), manage distributed processing (Events, Sagas), and persist domain state (CQRS, Event Sourcing, Data Fabrics).

@Vocabulary
- **Risk-Driven Architecture**: The practice of allowing real, genuine quality demands (functional requirements) to drive the use of architectural styles, preventing unjustified "cool" technology choices.
- **Layers Architecture**: Partitioning a program into cohesive layers (User Interface, Application, Domain, Infrastructure) where dependencies strictly flow downward.
- **Strict Layers**: A layer couples only to the layer directly below it.
- **Relaxed Layers**: A layer can couple to any layer below it (e.g., UI and Application both accessing Infrastructure).
- **Dependency Inversion Principle (DIP)**: High-level modules must not depend on low-level modules; both must depend on abstractions. Details depend upon abstractions.
- **Hexagonal Architecture (Ports and Adapters)**: A symmetrical architecture defining the application's core API (the "inside") wrapped by ports, with external clients, persistence, and messaging interacting via adapters (the "outside").
- **SOA (Service-Oriented Architecture)**: Interoperable services designed to prioritize business value and strategic goals over technical capabilities.
- **REST (Representational State Transfer)**: An architectural style for distributed systems utilizing uniquely addressable resources, stateless communication, standard HTTP methods (verbs), and HATEOAS.
- **CQRS (Command-Query Responsibility Segregation)**: An architecture pattern strictly separating methods that mutate state (Commands) from methods that return state (Queries), often backing them with entirely separate data models (Write Model vs. Read Model).
- **Event-Driven Architecture (EDA)**: Software architecture promoting the production, detection, consumption of, and reaction to Domain Events.
- **Pipes and Filters**: Breaking a distributed process into sequential message-based steps where each handler filters or transforms an event and publishes a new one.
- **Long-Running Process (Saga)**: An event-driven, distributed parallel processing pattern requiring a state tracker (executive) object to manage completion, timeouts, and retries across multiple bounded contexts.
- **Event Sourcing**: Representing the entire state of an Aggregate as an append-only sequence of historical Events.
- **Data Fabric / Grid Computing**: High-performance, elastic, distributed in-memory caches or key-value stores (e.g., Coherence, GemFire) used for storing Aggregates and continuous querying.

@Objectives
- Ensure the Domain Model remains entirely pure, architecturally neutral, and completely ignorant of infrastructure, database, and UI concerns.
- Select and apply architectural styles strictly to mitigate risks and satisfy explicit functional requirements, avoiding accidental complexity.
- Facilitate loose coupling, scalability, and high testability using Ports and Adapters or Dependency Inversion.
- Implement highly scalable reads and writes using CQRS and Event-Driven techniques when domain complexity or view sophistication demands it.
- Embrace eventual consistency across system boundaries and aggregates, eschewing global distributed transactions (two-phase commits) whenever possible.

@Guidelines
- **Risk-Driven Selection**: The AI MUST justify the selection of any architectural pattern (CQRS, REST, EDA) against specific use cases or user stories. The AI MUST NOT apply complex patterns (like Event Sourcing) by default.
- **Layering and DIP Enforcement**: 
  - The AI MUST NOT allow the Domain Layer to depend on the Infrastructure Layer. 
  - The AI MUST place interface abstractions in the Domain Layer (e.g., `Repository` interfaces) and place their implementations in the Infrastructure Layer.
- **Hexagonal (Ports and Adapters) Adherence**: 
  - The AI MUST design the application core (inner hexagon) to be completely agnostic of external clients. 
  - The AI MUST create explicit Adapters for specific input Ports (HTTP, AMQP, UI) and output Ports (SQL, NoSQL, message brokers).
- **RESTful Design Constraints**: 
  - The AI MUST NOT expose the domain model directly via REST. Changes to the core domain model MUST NOT arbitrarily break external system interfaces.
  - The AI MUST create a separate representation layer, decoupling the Core Domain from the system's REST interface.
  - The AI MUST use HTTP GET strictly for safe, side-effect-free query operations.
- **CQRS Implementation Rules**: 
  - The AI MUST strictly divide methods: Commands MUST NOT return a value (must be `void`), and Queries MUST NOT mutate state.
  - The AI MUST strip the Command/Write model of all query methods (other than retrieving an aggregate by its unique identity).
  - The AI MUST define a separate Read Model (e.g., denormalized database tables or views) optimized specifically for UI presentation.
  - The AI MUST synchronize the Read Model by subscribing to Domain Events published by the Write Model.
- **Eventual Consistency in UI**: When using CQRS or EDA, the AI MUST account for eventual consistency in the User Interface (e.g., by displaying the date/time of the read model data or simulating the update locally).
- **Long-Running Processes (Sagas)**: 
  - When a process requires modifying multiple aggregates or communicating across distributed systems, the AI MUST use an asynchronous Long-Running Process.
  - The AI MUST implement an "executive" state tracker (which can be an Aggregate) to track the steps, handle retries, manage active/passive timeouts, and execute compensation logic if necessary.
- **Event Sourcing**: If tracking historical change is required by the business, the AI MUST implement Event Sourcing. The AI MUST define an Aggregate's current state strictly as the chronological playback of its historical Events.
- **Data Fabrics/Grids**: When interacting with a Data Fabric, the AI MUST treat the storage as an Aggregate-oriented key-value pair map, utilizing unique identities as keys and serialized representations as values.

@Workflow
1. **Requirement & Risk Analysis**: Analyze the functional requirements (use cases/stories) to determine the necessary software qualities. Identify high-contention areas requiring CQRS or multi-aggregate updates requiring EDA.
2. **Core Architecture Initialization**: Establish the overarching architectural style. Default to Hexagonal (Ports and Adapters) to ensure the domain model forms an isolated, architecturally neutral core.
3. **Dependency Inversion Setup**: Define all persistence and messaging contracts (interfaces) inside the Domain or Application layers. Implement these contracts strictly within the Infrastructure layer.
4. **Interface Segregation & REST Planning**: If exposing an API, define RESTful resources based on client use cases, not internal Aggregate shapes. Create translation adapters to map REST representations to/from Domain objects.
5. **CQRS / Read Model Configuration**: If the UI requires complex, cross-aggregate views, partition the system into a Write Model (Aggregates) and a Read Model (denormalized tables). Wire up Event Subscribers to update the Read Model asynchronously.
6. **Distributed Processing Design**: For complex workflows, design an Event-Driven pipeline (Pipes and Filters) or a Long-Running Process (Saga). Define the State Tracker object to orchestrate parallel tasks and manage timeouts.
7. **Implementation & Testing**: Implement the core application API using Application Services. Test the domain and application layers entirely in isolation by stubbing/mocking output adapters (in-memory repositories) without needing a UI or Database.

@Examples (Do's and Don'ts)

- **Dependency Inversion Principle**
  - [DO]: Define `public interface CustomerRepository` in the `domain.model` package, and implement `public class HibernateCustomerRepository implements CustomerRepository` in the `infrastructure.persistence` package.
  - [DON'T]: Place JDBC or Hibernate specific annotations/logic directly inside the Domain Layer objects.

- **RESTful Interfaces**
  - [DO]: Map HTTP GET `/tenants/{id}/users` to a representation object specifically crafted for the API, decoupled from the internal `User` aggregate.
  - [DON'T]: Use the `User` aggregate class directly as the parameter for JAX-RS resource methods (e.g., automatically serializing the domain object to the client).

- **CQRS (Command-Query Separation)**
  - [DO]: Write a command method as `public void commitTo(Sprint sprint) { ... }` that mutates state and returns nothing.
  - [DON'T]: Write a command method as `public Sprint commitTo(Sprint sprint)` that mutates state and also returns the updated state to the caller.

- **Distributed Transactions vs. Eventual Consistency**
  - [DO]: Modify one Aggregate, publish a `ProductCreated` Domain Event, and use an asynchronous subscriber to create the corresponding `Discussion` Aggregate in a separate transaction.
  - [DON'T]: Use a global two-phase commit (XA transaction) to modify the `Product` Aggregate and the `Discussion` Aggregate simultaneously in the same synchronous thread.

- **Long-Running Processes (Sagas)**
  - [DO]: Create a `ProcessStateTracker` aggregate that records `isCompleted()`, tracks a `startTime()`, and listens for parallel completion events before finalizing a multi-step workflow.
  - [DON'T]: Attempt to block the main application thread waiting for remote RPC calls from 3 different bounded contexts to complete sequentially.