## @Domain
These rules are triggered whenever the AI is requested to design, implement, refactor, or test Domain-Driven Design (DDD) Aggregates using Event Sourcing (A+ES). This includes working on Event Stores, Command Handlers, Domain Events, Event Streams, Aggregate state reconstitution, CQRS Read Model Projections, Event serializers, or Given-When-Expect unit tests.

## @Vocabulary
*   **A+ES**: Aggregates + Event Sourcing. The overarching architectural and tactical pattern of representing the entire state of an Aggregate as a sequence of Events.
*   **Event Stream**: An append-only sequence of serialized Domain Events associated with a specific Aggregate identity. 
*   **Event Store**: The persistence mechanism that stores Event Streams. It is strictly append-only and provides strong consistency guarantees.
*   **IEventStore / IAppendOnlyStore**: The high-level (strongly typed) and low-level (byte array/string) abstractions used to interface with the Event Store.
*   **Apply**: An Aggregate method responsible for appending a newly generated Event to a tracking collection (e.g., `Changes`) AND delegating to `Mutate` to update the Aggregate's internal state.
*   **Mutate (or Replay)**: An Aggregate method responsible strictly for applying an Event's data to the Aggregate's internal state. It routes the Event to a specific `When` handler.
*   **When**: Type-specific handlers inside an Aggregate or Projection that contain the actual state-transition logic for a specific Event type.
*   **Command**: A serialized representation of a method name and its parameters, representing a client's intent to perform a business operation.
*   **Command Handler / Application Service**: The component responsible for orchestrating A+ES: loading the Event Stream, reconstituting the Aggregate, executing the Command, and appending new Events.
*   **Snapshot**: A serialized copy of an Aggregate's full state taken at a specific version in the Event Stream, used to optimize loading performance.
*   **Read Model Projection**: A component that subscribes to Domain Events and generates/updates a persistent Read Model (DTO) optimized for queries (CQRS).
*   **Event Enrichment**: The practice of adding data to an Event that isn't strictly required to reconstitute the Aggregate, but significantly simplifies the logic of Read Model Projections.
*   **Given-When-Expect**: A unit testing specification pattern for A+ES where past Events setup state (Given), a Command is executed (When), and resulting Events are asserted (Expect).
*   **Memoization**: The functional programming equivalent of Snapshots in an Event Store.

## @Objectives
*   Represent the entire state of an Aggregate solely as an append-only sequence of historical Domain Events.
*   Decouple the declaration of business intent (Commands) from the mutation of state (Events).
*   Ensure absolute immutability of Domain Events once instantiated.
*   Optimize persistence by using append-only data structures (RDBMS, NoSQL, or BLOBs) completely bypassing Object-Relational Mapping (ORM) impedance mismatches.
*   Facilitate temporal decoupling, load balancing, and high availability through the use of messaging queues and Command Handlers.
*   Protect against concurrency conflicts using Stream versions and type-based conflict resolution.
*   Enable fast querying by decoupling read operations into completely disposable, event-driven Read Model Projections (CQRS).

## @Guidelines

### Aggregate Design & State Mutation
*   The AI MUST separate Aggregate behavior from state mutation. Business methods validate rules and produce Events. They MUST NOT mutate state directly.
*   The AI MUST pass newly created Events to an `Apply(IEvent e)` method.
*   The `Apply` method MUST append the Event to an uncommitted `Changes` collection and then call `Mutate(e)`.
*   The `Mutate(IEvent e)` method MUST route the Event to a strongly typed `When(SpecificEvent e)` method that updates the internal state.
*   The Aggregate constructor used for reconstitution MUST accept an `IEnumerable<IEvent>` (the historical stream) and loop through them, calling ONLY `Mutate(e)` (NOT `Apply`, to prevent re-adding historical events to uncommitted changes).
*   To reduce cognitive load, the AI MAY split the Aggregate implementation into two distinct classes: one for State and one for Behavior, collaborating exclusively through the `Apply` method.

### Command Handlers & Application Services
*   The AI MUST implement Application Services / Command Handlers using the following strict sequence:
    1. Load the Event Stream using the Aggregate Identity.
    2. Reconstitute the Aggregate from the loaded Events.
    3. Execute the requested business behavior on the Aggregate.
    4. Append the new Events (the `Changes` collection) to the Event Store, passing the original Stream Version to ensure concurrency control.
*   The AI SHOULD use Lambda syntax or delegates to abstract the repetitive load/execute/append boilerplate (e.g., `Update(id, agg => agg.DoSomething())`).
*   The AI MUST design Command objects to be serializable, allowing them to be dispatched asynchronously via message queues for temporal decoupling and load balancing.
*   The AI SHOULD implement generic wrappers/decorators (e.g., `LoggingWrapper`) around a standard `IApplicationService` interface to handle cross-cutting concerns (logging, auditing, retries).

### Event Design & Immutability
*   The AI MUST implement Domain Events and Commands as 100% immutable objects. Fields MUST be read-only and initialized strictly via the constructor.
*   The AI MUST use Value Objects for identifiers (e.g., `ProjectId` instead of `long`) inside Events and Commands to leverage static type checking and prevent parameter-ordering bugs.
*   The AI MUST group flat, highly-parameterized Event contracts into cohesive Value Objects (e.g., `InvoiceHeader`, `InvoiceFooter`) to improve readability and model richness.
*   The AI SHOULD enrich Events with additional display data (e.g., `CustomerName` alongside `CustomerId`) if it simplifies Read Model Projections, adhering to the rule of thumb to satisfy 80% of subscribers natively.

### Persistence & Event Stores
*   The AI MUST divide Event Store implementation into a high-level `IEventStore` (handles serialization and strong typing) and a low-level `IAppendOnlyStore` (handles raw byte arrays, stream names, and database/BLOB I/O).
*   The AI MUST support two distinct read operations in the `IAppendOnlyStore`: reading a specific stream by name/identity (for Aggregate reconstitution) and reading all records globally (for projections and replication).
*   If using BLOB storage (file system, Azure, etc.), the AI MUST prefix variable-length fields with a byte count length and append a hash/CRC to verify data integrity upon read.

### Concurrency Control
*   The AI MUST implement Optimistic Concurrency by throwing an `EventStoreConcurrencyException` if the Expected Version passed during `Append` does not match the current database version.
*   The AI SHOULD implement automatic retry logic for concurrency exceptions by reloading the stream and re-executing the Command delegate.
*   If behavior re-execution is too expensive, the AI MUST implement Event Conflict Resolution. Compare the uncommitted Events against the concurrently saved Events (e.g., `ConflictsWith` method). If the event types do not logically conflict, the AI MAY force the append.

### Performance & Snapshots
*   If an Aggregate's Event Stream is expected to grow exceptionally large, the AI MUST implement an `ISnapshotRepository`.
*   When loading via snapshot, the AI MUST load the snapshot, load ONLY the Events that occurred *after* the snapshot version, and apply them using a `ReplayEvents` method.
*   Snapshots MUST be generated asynchronously on a background thread after a tunable, predefined threshold of new Events.

### Serialization
*   The AI MUST favor serializers that track contract members by integral tags rather than property names (e.g., Protocol Buffers) to allow safe renaming of Event properties as the ubiquitous language evolves without breaking historic streams.

### CQRS & Read Model Projections
*   The AI MUST implement queries using Read Model Projections. Aggregates MUST NOT be used for querying data.
*   Projections MUST be classes that subscribe to Domain Events, update a simple DTO (Read Model), and persist it to a document/relational store using an `IDocumentWriter`.
*   Projections MUST be treated as completely disposable. The AI MUST ensure the system can wipe Read Models and completely rebuild them by replaying the global Event Stream.

### Functional Language Implementation
*   If implementing in a functional language (e.g., F#, Clojure), the AI MUST represent Aggregate state as a simple immutable record.
*   The AI MUST represent `Mutate` as pure functions `Func<State, Event, State>`.
*   The AI MUST calculate current state as a left fold of all past Events over the mutating functions.
*   The AI MUST represent business behaviors as stateless functions `Func<Command, State, Event[]>`.

## @Workflow
1.  **Define Contracts**: Identify the business need. Define the required `Command` and `Event` classes using immutable structures and Value Objects. Consider using a DSL for contract generation.
2.  **Define State Mutators**: In the Aggregate, create the internal state fields. Write the `When(SpecificEvent e)` methods to mutate this state.
3.  **Implement Business Logic**: Write the business methods on the Aggregate. Validate domain rules based on current state. Instantiate new Events. Pass them to `Apply(e)`.
4.  **Wire the Application Service**: Create or update the Command Handler. Use the boilerplate lambda `Update(id, agg => agg.BusinessMethod(cmd.Data))` to load the stream, execute the method, and append to the store.
5.  **Build the Projection**: If the data needs to be queried, create a Projection class. Define `When` methods that catch the Events and write optimized DTOs to the Read Model storage.
6.  **Write Tests**: Write a `Given-When-Expect` unit test specifying the exact required historical events, the command to execute, and the expected resulting events.

## @Examples (Do's and Don'ts)

### Aggregate State Mutation
**[DO]** Separate the appending of an event from the mutation of internal state so historical events don't get accidentally saved as new changes.
```csharp
public partial class Customer
{
    public List<IEvent> Changes = new List<IEvent>();
    public bool ConsumptionLocked { get; private set; }

    // Used by Application Service to load history
    public Customer(IEnumerable<IEvent> events)
    {
        foreach (var @event in events)
        {
            Mutate(@event); // Only mutate state, do not add to Changes
        }
    }

    // Business Method
    public void LockCustomer(string reason)
    {
        if (!ConsumptionLocked)
        {
            Apply(new CustomerLocked(Id, reason));
        }
    }

    // Append and apply
    private void Apply(IEvent e)
    {
        Changes.Add(e);
        Mutate(e);
    }

    // Route to specific state mutator
    private void Mutate(IEvent e)
    {
        ((dynamic)this).When((dynamic)e);
    }

    private void When(CustomerLocked e)
    {
        ConsumptionLocked = true;
    }
}
```

**[DON'T]** Mix business logic, event generation, and state mutation in a single method, or add historical events to the uncommitted changes list during reconstitution.
```csharp
// ANTI-PATTERN: State mutation mixed with logic, breaking reconstitution
public void LockCustomer(string reason)
{
    if (!ConsumptionLocked)
    {
        ConsumptionLocked = true; // State mutated directly! Event Sourcing broken.
        Changes.Add(new CustomerLocked(Id, reason));
    }
}
```

### Event and Command Definitions
**[DO]** Use fully immutable contracts and Value Objects for identifiers.
```csharp
[DataContract]
public sealed class ProjectAssignedToCustomer : IEvent
{
    [DataMember(Order=1)] public CustomerId Customer { get; private set; }
    [DataMember(Order=2)] public ProjectId Project { get; private set; }

    public ProjectAssignedToCustomer(CustomerId customer, ProjectId project)
    {
        Customer = customer;
        Project = project;
    }
}
```

**[DON'T]** Use mutable properties or primitive obsession for identifiers, which allows compiler-invisible bugs.
```csharp
// ANTI-PATTERN: Mutable properties and primitive obsession
public class ProjectAssignedToCustomer
{
    public long CustomerId { get; set; }
    public long ProjectId { get; set; }
}
// Easy to introduce bug: new ProjectAssignedToCustomer { CustomerId = projectId, ProjectId = customerId }
```

### Application Service / Command Handler Boilerplate
**[DO]** Use lambda syntax to abstract stream loading, aggregate execution, and appending.
```csharp
public class CustomerApplicationService
{
    private readonly IEventStore _eventStore;

    public void Update(CustomerId id, Action<Customer> execute)
    {
        EventStream stream = _eventStore.LoadEventStream(id);
        var customer = new Customer(stream.Events);
        
        execute(customer);
        
        _eventStore.AppendToStream(id, stream.Version, customer.Changes);
    }

    public void When(LockCustomerCommand c)
    {
        Update(c.Id, customer => customer.LockCustomer(c.Reason));
    }
}
```

**[DON'T]** Repeat the load/instantiate/execute/append/version-check logic manually inside every single command handler method.

### Concurrency Conflict Resolution
**[DO]** Catch concurrency exceptions and attempt automatic resolution by checking if the specific event types logically collide.
```csharp
catch (EventStoreConcurrencyException ex)
{
    foreach (var failedEvent in customer.Changes)
    {
        foreach (var succeededEvent in ex.ActualEvents)
        {
            if (ConflictsWith(failedEvent, succeededEvent))
            {
                throw new RealConcurrencyException("Conflict detected", ex);
            }
        }
    }
    // No logical conflict, force append
    _eventStore.AppendToStream(id, ex.ActualVersion, customer.Changes);
}

bool ConflictsWith(IEvent event1, IEvent event2)
{
    return event1.GetType() == event2.GetType();
}
```

**[DON'T]** Immediately fail the user request on an optimistic concurrency exception without attempting a retry or evaluating if the concurrent events actually modify overlapping business concerns.