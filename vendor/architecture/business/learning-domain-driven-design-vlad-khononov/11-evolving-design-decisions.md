# @Domain
Trigger these rules when the user requests assistance with system refactoring, architectural modernization, migrating legacy code, adapting systems to organizational or business strategy changes, scaling existing bounded contexts, or addressing technical debt and "big ball of mud" codebases. 

# @Vocabulary
- **Vectors of Change**: The four common catalysts that invalidate existing design decisions: Business Domain evolution, Organizational Structure changes, Domain Knowledge discovery, and System Growth.
- **Accidental Complexity**: Complexity caused by outdated design decisions, unregulated growth, and lack of re-evaluation, rather than the inherent difficulty of the business problem.
- **Essential Complexity**: The inherent, unavoidable complexity of the business domain itself.
- **Coherent Use Cases**: Sets of use cases that work on the same set of data and share a strong functional relationship, used to identify finer-grained subdomains during growth.
- **Migration Event**: An explicit domain event (e.g., `migrated-from-legacy`) used when transitioning to an Event-Sourced Domain Model to acknowledge the lack of granular historical state transition data.
- **Chatty Bounded Contexts**: Bounded contexts that are unable to complete operations without making synchronous calls to other bounded contexts, indicating ineffective model boundaries.

# @Objectives
- The AI MUST continuously align software architecture and tactical design patterns with the evolving realities of the business strategy and organizational structure.
- The AI MUST treat "pain" in implementing new features as a strict signal to re-evaluate subdomain classification and refactor the underlying design pattern.
- The AI MUST eliminate accidental complexity caused by software growth by relentlessly distilling core subdomains, splitting "jack of all trades" bounded contexts, and shrinking aggregate boundaries to the bare minimum required for strong consistency.
- The AI MUST enforce proper strategic integration adjustments when team topologies or collaboration dynamics change over time.

# @Guidelines

## Subdomain Evolution and Strategic Reclassification
- When an in-house Core Subdomain can be replaced by a newly available off-the-shelf product that competitors also use, the AI MUST reclassify it as a Generic Subdomain and recommend adopting the external solution.
- When an organization decides to replace a Generic off-the-shelf solution with a custom in-house implementation to gain a competitive edge, the AI MUST reclassify it as a Core Subdomain.
- When a custom CRUD-like application (Supporting) can be replaced by an open-source or SaaS product, the AI MUST reclassify it as Generic.
- When the business logic of a Supporting Subdomain becomes increasingly complex to optimize costs or generate profit, the AI MUST reclassify it as a Core Subdomain and mandate in-house development.
- When a Core Subdomain's complexity is no longer profitable or justified, the AI MUST reclassify it as a Supporting Subdomain and recommend cutting extraneous complexity or outsourcing.
- When a Subdomain becomes Core, the AI MUST eliminate `Separate Ways` integrations and enforce `Customer-Supplier` relationships (since a Core Subdomain must have a single source of truth/implementation).
- When a Subdomain becomes Core, the AI MUST implement Anticorruption Layers (ACL) to protect it from upstream dependencies, and Open-Host Services (OHS) with Published Languages to protect downstream consumers.

## Tactical Design Refactoring
- **Transaction Script to Active Record**: When a Transaction Script struggles with complex data structures, the AI MUST refactor the data mapping into Active Record objects while keeping procedural business logic in the script.
- **Active Record to Domain Model**: When Active Record logic suffers from duplication or inconsistency due to complex business rules, the AI MUST execute a 4-step refactoring process:
  1. Extract immutable data structures and their related logic into Value Objects.
  2. Make all Active Record setters `private` to surface where state-modifying logic resides, then move that logic inside the object's boundary.
  3. Identify the smallest possible transactional boundaries required for strong consistency and group objects into Aggregates.
  4. Identify the Aggregate Root for each group, making all methods of internal objects accessible only via the Root.
- **Domain Model to Event-Sourced Domain Model (ESDM)**: When history, auditability, or deep analytics become required, the AI MUST refactor state-based aggregates to ESDM using one of two historical data strategies:
  - *Generating Past Transitions*: Reverse-engineer approximate past events based on the current state (best-effort). The AI MUST warn that skipped historical events will be lost.
  - *Modeling Migration Events*: Create a single, explicit `migrated-from-legacy` event containing a snapshot of the current state to explicitly acknowledge the lack of historical transitions.

## Adapting to Organizational Changes
- **Partnership to Customer-Supplier**: When teams shift to different geographical locations or collaboration degrades, the AI MUST decouple their integration from Partnership to Customer-Supplier (using ACL or Conformist).
- **Customer-Supplier to Separate Ways**: When severe communication problems occur over non-core functionality, the AI MUST recommend duplicating the functionality (`Separate Ways`) to eliminate team friction.
- **Growing Teams**: When engineering teams grow, the AI MUST propose splitting wide bounded context boundaries into smaller ones so that each team exclusively owns its own bounded context.

## Managing Growth and Knowledge Discovery
- When domain knowledge is low or requirements change rapidly, the AI MUST define broad bounded context boundaries. As domain knowledge stabilizes, the AI MUST decompose them into narrower boundaries.
- When system functionality expands, the AI MUST identify finer-grained subdomains by grouping Coherent Use Cases to ensure Core subdomains remain distilled.
- When bounded contexts accumulate logic for multiple unrelated problems ("jack of all trades"), the AI MUST extract the unrelated logic into laser-focused, dedicated bounded contexts.
- When aggregates grow to include data that does not strictly require strong consistency for business invariants, the AI MUST extract that data into separate aggregates to maintain minimal transactional boundaries.

# @Workflow
1. **Analyze Symptoms of Change**: Identify the primary pain point. Is it difficult to add new features (Tactical)? Is there team friction (Organizational)? Have business goals shifted (Strategic)? Are contexts too "chatty" (Growth)?
2. **Re-evaluate Subdomain Types**: Map the current functionality against the business strategy to determine if the Subdomain has shifted between Core, Generic, or Supporting.
3. **Adjust Strategic Integrations**: 
   - Ensure Core domains are built in-house and protected by ACL/OHS.
   - Adjust team integration patterns (Partnership, Customer-Supplier, Separate Ways) to match current organizational realities.
4. **Execute Tactical Refactoring**: 
   - If business logic complexity has outgrown the pattern, elevate the pattern (TS -> AR -> DM -> ESDM).
   - Apply strict boundary rules (private setters, Value Objects, explicit Aggregate Roots).
5. **Optimize Boundaries for Growth**: Shrink aggregate boundaries to strong-consistency requirements only. Decompose broad bounded contexts into narrower ones based on Coherent Use Cases.

# @Examples (Do's and Don'ts)

## Active Record to Domain Model Refactoring
- **[DO]** Make state modification explicit and protected when elevating to a Domain Model.
```csharp
// DO: State modifications happen exclusively through explicit behavioral methods.
public class Player 
{
    public PlayerId Id { get; private set; } // Value Object
    public Points Points { get; private set; } // Value Object

    public void ApplyBonus(int percentage) 
    {
        this.Points = this.Points.MultiplyBy(1 + percentage / 100.0);
    }
}
```
- **[DON'T]** Leave public setters open when complex invariants exist, simulating an anemic domain model.
```csharp
// DON'T: External services modify state directly, scattering business logic.
public class Player 
{
    public Guid Id { get; set; }
    public int Points { get; set; }
}

public class ApplyBonusService 
{
    public void Execute(Guid playerId, int percentage) {
        var player = repository.Load(playerId);
        player.Points *= 1 + percentage / 100.0; // Logic leaked outside the entity
        repository.Save(player);
    }
}
```

## Transitioning to Event-Sourced Domain Models
- **[DO]** Use an explicit migration event if you cannot accurately reconstruct the complete historical event stream.
```json
// DO: Acknowledge missing history explicitly using a migration event.
{
  "lead-id": 12,
  "event-id": 0,
  "event-type": "migrated-from-legacy",
  "first-name": "Shauna",
  "status": "converted",
  "last-contacted-on": "2020-05-27T12:02:12.51Z",
  "followup-on": null
}
```
- **[DON'T]** Fabricate fake historical events that imply a perfect audit log when intermediate states (e.g., failed contact attempts) are permanently lost.

## Aggregate Growth Management
- **[DO]** Split aggregates when new data requirements do not dictate strong transactional consistency with existing data. Reference external entities by ID.
```csharp
// DO: Keep aggregates small. Reference the agent by ID because agent schedules/data don't require strong consistency with the Ticket state.
public class Ticket 
{
    private TicketId _id;
    private AgentId _assignedAgentId; 
    private List<Message> _messages;
}
```
- **[DON'T]** Add entire entity graphs into an existing aggregate just because they are queried together, causing bloated transactional boundaries.
```csharp
// DON'T: Nesting Agent object directly inside Ticket forces them into the same database transaction unnecessarily.
public class Ticket 
{
    private Guid _id;
    private Agent _assignedAgent; // Entire agent entity pulled into the boundary
    private List<Message> _messages;
}
```