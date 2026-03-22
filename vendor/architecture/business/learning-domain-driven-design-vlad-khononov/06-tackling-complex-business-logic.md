# @Domain

These rules MUST trigger when the AI is tasked with designing, modeling, or implementing complex business logic, core subdomains, or tactical Domain-Driven Design (DDD) patterns. Activation conditions include user requests involving "aggregates," "entities," "value objects," "domain events," "domain services," "business rules," "invariants," or refactoring from an anemic domain model / transaction script into a rich domain model.

# @Vocabulary

- **Domain Model**: An object model of the domain that incorporates both behavior and data, completely devoid of infrastructural or technological concerns (e.g., POCOs/POJOs).
- **Primitive Obsession**: An anti-pattern where a language's standard primitive data types (strings, integers) are exclusively used to represent complex business domain concepts, leading to duplicated validation and scattered logic.
- **Value Object**: An immutable object that is identified exclusively by the composition of its values, lacking an explicit identification field.
- **Entity**: An object with an explicit, unique, and immutable identification field, used to distinguish instances even if all other properties are identical. Its state is mutable and expected to change over time.
- **Aggregate**: A hierarchy of Entities and Value Objects that share a strict transactional consistency boundary. 
- **Aggregate Root**: The single specific Entity within an Aggregate designated as the sole entry point and public interface for modifying the Aggregate's state.
- **Command**: A state-modifying method exposed by the Aggregate Root (can be a plain method or a dedicated parameter object) formulated in the imperative.
- **Domain Event**: A message describing a significant business event that has already occurred within the Aggregate's lifecycle, formulated in the past tense.
- **Domain Service**: A stateless object used to host complex business logic or calculations that require reading from multiple Aggregates or do not naturally fit within a single Aggregate or Value Object.
- **Optimistic Concurrency**: A data-protection mechanism utilizing a version field on the Aggregate to prevent concurrent modifications from overwriting one another.
- **Degrees of Freedom**: The number of data points needed to describe a system's state. Aggregates and Value Objects reduce degrees of freedom by encapsulating invariants, making the system more predictable.

# @Objectives

- **Tackle Business Complexity**: The AI MUST encapsulate complex business rules, state transitions, and invariants within self-contained, highly cohesive domain objects to reduce the system's "degrees of freedom."
- **Enforce Transactional Consistency**: The AI MUST design models where data integrity is mathematically guaranteed within boundaries, strictly adhering to the one-aggregate-per-transaction rule.
- **Eradicate Accidental Complexity**: The AI MUST keep the Domain Model strictly decoupled from databases, ORMs, message buses, and other infrastructure.
- **Speak the Ubiquitous Language**: The AI MUST name every class, property, and method using the exact terminology of the business domain experts, rejecting purely technical naming conventions.

# @Guidelines

## Domain Model Purity
- The AI MUST implement Domain Model objects as plain objects (POCOs/POJOs).
- The AI MUST NOT inject or reference database contexts, repositories, or external service clients inside Entities or Value Objects.

## Value Objects
- When encountering business concepts identifiable solely by their values (e.g., money, measurements, colors, phone numbers), the AI MUST model them as Value Objects.
- The AI MUST implement Value Objects as strictly immutable. Any business logic that manipulates the data MUST return a completely new instance of the Value Object rather than modifying the existing one.
- The AI MUST override equality operators (`Equals`, `GetHashCode`, `==`, `!=`) to compare Value Objects based strictly on the composition of their properties, NOT by memory reference.
- The AI MUST encapsulate all validation for the values within the Value Object's constructor or factory method.

## Entities
- When modeling a domain concept with a lifecycle and distinct identity, the AI MUST model it as an Entity.
- The AI MUST provide every Entity with a unique identification field (e.g., `UserId`, `TicketId`).
- The AI MUST make the Entity's identification field strictly immutable throughout the object's lifecycle.
- The AI MUST NOT use Entities as independent, top-level architectural patterns; they MUST only exist as building blocks within an Aggregate.

## Aggregates and Transactional Boundaries
- The AI MUST group a hierarchy of Entities and Value Objects that require strong data consistency into an Aggregate.
- The AI MUST ensure that a single database transaction modifies ONE and ONLY ONE instance of an Aggregate. 
- If a business rule seemingly requires modifying multiple Aggregates simultaneously, the AI MUST recognize this as a design flaw and re-evaluate the Aggregate boundaries or use eventual consistency (Sagas/Domain Events).
- The AI MUST keep Aggregates as small as possible, including only the objects that are absolutely required to be in a strongly consistent state to protect business invariants.
- **Aggregate Referencing**: When an Aggregate needs to associate with another Aggregate, the AI MUST reference the external Aggregate exclusively by its ID (e.g., `Guid CustomerId`), NEVER by holding a direct object reference (e.g., `Customer Customer`).

## Aggregate Root and Encapsulation
- The AI MUST designate exactly one Entity per Aggregate as the Aggregate Root.
- The AI MUST restrict all external state modifications. External components MUST NOT be allowed to directly set properties on the Aggregate or its inner Entities (e.g., all property setters MUST be `private` or `init`).
- The AI MUST expose state-modifying logic exclusively through public methods ("Commands") on the Aggregate Root.
- The AI MUST ensure the Aggregate Root validates all inputs and enforces all business rules before altering internal state.

## Concurrency Management
- The AI MUST include a `Version` field (e.g., `int _version`) on the Aggregate Root to support optimistic concurrency control.
- The AI MUST increment the version field upon any state mutation.
- The AI MUST instruct the persistence layer to verify the expected version during database commits, throwing a Concurrency Exception if a mismatch occurs.

## Domain Events
- The AI MUST formulate Domain Event names strictly in the past tense (e.g., `TicketEscalated`, `MessageAppended`).
- The AI MUST include all necessary data related to the event within the event object payload.
- The AI MUST append Domain Events to an internal collection within the Aggregate Root during command execution, to be dispatched by the Application Layer after the transaction commits.

## Domain Services
- When business logic requires coordinating data from multiple Aggregates or performing calculations that do not naturally belong to a single Entity/Value Object, the AI MUST implement a Domain Service.
- The AI MUST implement Domain Services as completely stateless objects.
- The AI MUST NOT use Domain Services as a loophole to bypass the "one aggregate per transaction" rule. Domain Services may read from multiple Aggregates but must not commit modifications to multiple Aggregates.

## Application Layer Orchestration
- When implementing the Application Layer (Service Layer) that interacts with the Domain Model, the AI MUST follow a strict transaction script:
  1. Load the Aggregate's current state via a Repository.
  2. Execute the required Command (method) on the Aggregate.
  3. Persist the modified Aggregate state via the Repository.
  4. Return the operation's result (or catch concurrency exceptions).

# @Workflow

When requested to implement complex business logic, the AI MUST execute the following algorithmic steps:

1. **Analyze the Ubiquitous Language**: Identify all nouns and verbs from the provided business rules.
2. **Eradicate Primitive Obsession**: Identify properties currently modeled as strings, ints, or decimals that contain implicit domain rules (e.g., Email, Phone, Currency, Measurements). Extract these into immutable **Value Objects** with value-based equality.
3. **Define Entities**: Identify objects with a distinct identity and a mutable lifecycle. Assign them strongly-typed ID Value Objects (e.g., `TicketId`).
4. **Draw Aggregate Boundaries**: Group Entities and Value Objects that must change together in a strongly consistent, atomic database transaction. Keep the boundary as small as possible.
5. **Establish the Aggregate Root**: Pick the top-level Entity in the boundary. Make all setters private. Expose public "Command" methods that enforce business rules.
6. **Decouple External Aggregates**: Scan the Aggregate for direct object references to other Aggregates. Replace them with ID references.
7. **Implement Domain Events**: Inside the Command methods, instantiate past-tense Domain Events when significant state changes occur, adding them to an internal event collection.
8. **Enforce Concurrency**: Add a Version integer to the Aggregate Root.
9. **Extract Domain Services**: If a business algorithm requires inputs from external policies or multiple aggregates, extract it into a stateless Domain Service.
10. **Write the Application Layer**: Create the orchestrating method that loads the Aggregate, calls the Command, and saves it in a single transaction while handling concurrency exceptions.

# @Examples (Do's and Don'ts)

## 1. Value Objects vs. Primitive Obsession

**[DON'T]** Use primitive types with implicit rules scattered across the codebase.
```csharp
public class Person 
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string MobilePhone { get; set; } // Implicit rule: must be a valid phone format
    public int HeightMetric { get; set; } // Implicit rule: metric units
}
```

**[DO]** Encapsulate attributes into immutable Value Objects with value-based equality.
```csharp
public class Person 
{
    private PersonId _id;
    private Name _name;
    private PhoneNumber _mobile;
    private Height _height;

    public Person(PersonId id, Name name, PhoneNumber mobile, Height height) 
    {
        _id = id;
        _name = name;
        _mobile = mobile;
        _height = height;
    }
}

// Value Object Example
public class Height 
{
    public readonly int Centimeters;

    private Height(int centimeters) => Centimeters = centimeters;

    public static Height FromMetric(int cm) => new Height(cm);
    public static Height FromImperial(int feet, int inches) => new Height((feet * 30) + (inches * 2));
    
    // Value-based equality overrides omitted for brevity, but REQUIRED by AI.
}
```

## 2. Aggregate Referencing and Transaction Boundaries

**[DON'T]** Reference other Aggregates by object reference, creating massive, unscalable transaction boundaries.
```csharp
public class Ticket // Aggregate Root
{
    public Guid Id { get; set; }
    public Customer Customer { get; set; } // BAD: Direct reference to another Aggregate
    public Agent AssignedAgent { get; set; } // BAD: Direct reference
    
    public void Reassign(Agent newAgent) 
    {
        this.AssignedAgent = newAgent;
        newAgent.ActiveTickets.Add(this); // BAD: Modifying two aggregates in one operation
    }
}
```

**[DO]** Reference other Aggregates by ID only, maintaining small, strictly enforced consistency boundaries.
```csharp
public class Ticket // Aggregate Root
{
    private TicketId _id;
    private CustomerId _customerId; // GOOD: Referenced by ID
    private AgentId _assignedAgentId; // GOOD: Referenced by ID
    private int _version; // GOOD: Concurrency management

    public void Execute(ReassignTicketCommand cmd) 
    {
        // Enforce invariants
        if (this.IsClosed) throw new InvalidOperationException("Cannot reassign a closed ticket.");
        
        _assignedAgentId = cmd.NewAgentId;
        _version++;
        
        // Emitting a Domain Event (Past tense)
        _domainEvents.Add(new TicketReassignedEvent(_id, cmd.NewAgentId));
    }
}
```

## 3. Application Layer Orchestration

**[DON'T]** Implement business logic inside the Application layer (Transaction Script / Anemic Domain Model).
```csharp
public class TicketService 
{
    public void EscalateTicket(Guid ticketId, string reason) 
    {
        var ticket = _db.Tickets.Find(ticketId);
        
        // BAD: Business rules leaked into the application service
        if (ticket.IsEscalated) return;
        if (ticket.RemainingTime > 0) return;

        ticket.IsEscalated = true;
        ticket.EscalationReason = reason;
        
        _db.SaveChanges();
    }
}
```

**[DO]** Use the Application layer purely to load, delegate to the Aggregate Root, and save (handling concurrency).
```csharp
public class TicketService 
{
    public ExecutionResult Escalate(TicketId id, EscalationReason reason) 
    {
        try 
        {
            // 1. Load the Aggregate's current state
            var ticket = _ticketRepository.Load(id);
            
            // 2. Execute the required action (Aggregate enforces its own rules)
            var cmd = new EscalateCommand(reason);
            ticket.Execute(cmd);
            
            // 3. Persist the modified state
            _ticketRepository.Save(ticket);
            
            return ExecutionResult.Success();
        } 
        catch (ConcurrencyException ex) 
        {
            // 4. Handle concurrent modification failures
            return ExecutionResult.Error(ex);
        }
    }
}
```