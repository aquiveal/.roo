# @Domain
These rules MUST trigger when the AI is tasked with designing, implementing, or refactoring business logic for a core subdomain that requires deep data insights, rigorous audit logs, historical state reconstruction (time traveling), or when the user explicitly requests an "Event-Sourced Domain Model," "Event Sourcing," or an "Event Store." 

# @Vocabulary
- **Event Sourcing**: A pattern that introduces the dimension of time into the data model by persisting events documenting every change in an aggregate’s lifecycle, rather than reflecting only the current state.
- **Event Store**: An append-only database used for persisting events. It serves as the system's strongly consistent source of truth and only supports fetching events by business entity ID and appending new events.
- **Domain Event**: A message describing a significant state transition or business action that has already happened, serving as the building block of the event-sourced domain model.
- **State Projection (Reconstitution/Rehydration)**: The process of iterating over an aggregate's historical events and sequentially applying transformation logic to generate an in-memory representation of its current state.
- **Time Traveling**: The ability to project an entity's state at any specific point in its past lifecycle by applying only a subset of its events up to that desired point.
- **Event-Sourced Domain Model**: An architectural pattern combining the Domain Model pattern (aggregates, commands) with Event Sourcing. All state changes are exclusively expressed and persisted as domain events.
- **Snapshot Pattern**: An optimization technique where an aggregate's projected state is periodically cached to prevent performance degradation when the event stream exceeds a large threshold (e.g., 10,000+ events).
- **Forgettable Payload Pattern**: A data deletion technique (often for GDPR compliance) where sensitive information inside immutable events is encrypted, and the encryption key is stored externally. Deleting the key effectively "deletes" the data.

# @Objectives
- Treat the dimension of time as a first-class modeling construct by capturing all state transitions as immutable events.
- Establish the event stream as the absolute, single source of truth for the system's state.
- Strictly separate the execution of business logic (commands) from the mutation of data (state projections).
- Enable flexible, polyglot data analysis by supporting multiple specialized read models (projections) derived from the same event stream.
- Ensure high resilience and correct concurrency handling when appending events to the Event Store.

# @Guidelines

### Event Modeling & Structure
- The AI MUST formulate all domain event names in the past tense (e.g., `OrderSubmitted`, `LeadInitialized`, `ContactDetailsUpdated`).
- The AI MUST ensure each event payload contains all the necessary data related to the specific state transition it describes.
- The AI MUST treat events as strictly immutable. Events MUST NOT be updated, modified, or deleted once appended to the Event Store.

### Aggregate Implementation
- The AI MUST NOT directly mutate aggregate state fields within command execution methods.
- The AI MUST implement command execution logic (e.g., `Execute(Command)`) such that it validates invariants against the current projected state, instantiates the relevant domain event(s), and appends them to the aggregate's internal uncommitted event collection.
- The AI MUST separate the aggregate's state representation into a dedicated projection class (e.g., `TicketState`) containing `Apply(SpecificEvent)` methods.
- The AI MUST sequentially route all newly created events and all historically loaded events through the state projection's `Apply` methods to mutate the in-memory state.
- The AI MUST include an incrementing `Version` field in the aggregate's state, tracking the total number of applied modifications.

### Event Store Integration
- The AI MUST implement the Event Store interface with a minimum of two operations: `Fetch(Guid instanceId)` and `Append(Guid instanceId, Event[] newEvents, int expectedVersion)`.
- The AI MUST implement optimistic concurrency management by passing the aggregate's pre-modification `Version` as the `expectedVersion` when appending new events.
- The AI MUST shard the event store by aggregate IDs when scaling the database to ensure all events belonging to a single aggregate instance reside in the same shard.

### Projections & Querying
- The AI MUST assume the use of the CQRS (Command-Query Responsibility Segregation) pattern alongside Event Sourcing, as the Event Store cannot be queried by anything other than aggregate ID.
- The AI MUST allow the creation of multiple projection models (e.g., Search Model, Analysis Model) derived from the same event stream, utilizing only the specific events relevant to that projection's purpose.

### Performance & Data Management
- The AI MUST NOT preemptively implement the Snapshot Pattern. The AI MUST only suggest or implement snapshots if the aggregate's expected lifespan exceeds 10,000 events.
- The AI MUST use the Forgettable Payload Pattern if the user requires the ability to physically delete data (e.g., for GDPR) from the append-only event store.

### Anti-Patterns to Avoid
- The AI MUST NOT use a text file or application logging framework as a substitute for an event-sourced audit log.
- The AI MUST NOT use a dual-write approach (modifying a state-based table and writing to a "logs" table in the same transaction) due to the risk of developer error and schema degradation.
- The AI MUST NOT use database triggers copying state into a "history" table to replace Event Sourcing, as this captures the "what" but loses the business context ("why").

# @Workflow
When tasked with implementing an operation within an Event-Sourced Domain Model, the AI MUST follow this exact algorithmic script:

1. **Load**: Fetch the aggregate's domain events from the Event Store using the aggregate's unique ID.
2. **Reconstitute**:
    a. Instantiate the aggregate's internal state projection object.
    b. Iterate sequentially through the fetched events.
    c. Dynamically invoke the correct `Apply(SpecificEvent)` overload on the state object for each event.
    d. Capture the current `Version` of the aggregate.
3. **Execute**:
    a. Accept the incoming command.
    b. Validate the command against the reconstituted in-memory state.
    c. Instantiate the appropriate new Domain Event(s) (named in past tense).
    d. Append the new event(s) to the aggregate's uncommitted event list and immediately run them through the state's `Apply` method to update the in-memory state.
4. **Commit**:
    a. Send the uncommitted events to the Event Store.
    b. Provide the captured pre-modification `Version` to enforce optimistic concurrency control.
5. **(Optional) Specialized Needs**:
    a. If querying is required, generate separate CQRS read models by applying the events to targeted projection logic.
    b. If GDPR compliance is requested, wrap sensitive event payload fields in an encryption/decryption envelope tied to an external Key-Value store.

# @Examples (Do's and Don'ts)

### Command Execution and State Mutation
**[DO]** Separate command logic from state mutation by emitting events:
```csharp
public class Ticket
{
    private List<DomainEvent> _uncommittedEvents = new List<DomainEvent>();
    private TicketState _state;

    public Ticket(IEnumerable<IDomainEvent> history)
    {
        _state = new TicketState();
        foreach (var e in history) { AppendEvent(e); }
    }

    private void AppendEvent(IDomainEvent @event)
    {
        _uncommittedEvents.Add(@event);
        ((dynamic)_state).Apply((dynamic)@event);
    }

    public void Execute(RequestEscalation cmd)
    {
        // Validation relies strictly on _state
        if (!_state.IsEscalated && _state.RemainingTimePercentage <= 0)
        {
            var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
            AppendEvent(escalatedEvent); // Emits event, does not set fields directly
        }
    }
}

public class TicketState
{
    public bool IsEscalated { get; private set; }
    public int Version { get; private set; }

    public void Apply(TicketEscalated @event)
    {
        IsEscalated = true; // State is only mutated inside Apply methods
        Version += 1;
    }
}
```

**[DON'T]** Modify aggregate state directly inside the command method in an event-sourced model:
```csharp
public void Execute(RequestEscalation cmd)
{
    if (!this.IsEscalated && this.RemainingTimePercentage <= 0)
    {
        // Anti-pattern: Mutating state directly without going through an event
        this.IsEscalated = true;
        this.Version += 1;
        
        var escalatedEvent = new TicketEscalated(_id, cmd.Reason);
        _domainEvents.Add(escalatedEvent);
    }
}
```

### Application Service Flow
**[DO]** Follow the Load-Reconstitute-Execute-Commit script with concurrency checking:
```csharp
public void RequestEscalation(TicketId id, EscalationReason reason)
{
    var events = _eventStore.Fetch(id);
    var ticket = new Ticket(events);
    var originalVersion = ticket.Version; // Capture version for concurrency
    
    var cmd = new RequestEscalation(reason);
    ticket.Execute(cmd);
    
    _eventStore.Append(id, ticket.GetUncommittedEvents(), originalVersion);
}
```

**[DON'T]** Attempt to load and save a state-based object when the domain requires an audit log:
```csharp
public void RequestEscalation(TicketId id, EscalationReason reason)
{
    // Anti-pattern: Relying on state-based representation and separate log tables
    var ticket = _database.GetTicket(id);
    ticket.IsEscalated = true;
    _database.Save(ticket);
    _database.Execute("INSERT INTO Logs (id, action) VALUES (@id, 'Escalated')", id);
}
```

### Multiple Projections
**[DO]** Create tailored projections that ignore irrelevant events for specific analysis needs:
```csharp
public class AnalysisModelProjection
{
    public int Followups { get; private set; }
    public LeadStatus Status { get; private set; }

    public void Apply(FollowupSet @event)
    {
        Status = LeadStatus.FOLLOWUP_SET;
        Followups += 1;
    }

    public void Apply(ContactDetailsChanged @event)
    {
        // Ignored for this specific projection as it doesn't affect status or followups
    }
}
```