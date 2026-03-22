@Domain
This rule file is triggered when the AI is tasked with designing, refactoring, or evaluating Domain-Driven Design (DDD) domain models, establishing transactional boundaries, defining business logic execution limits, creating Entities/Value Objects that cluster together, or addressing concurrency, performance, and scalability bottlenecks within business logic layers.

@Vocabulary
- **Aggregate**: A cluster of associated Entities and Value Objects treated as a single unit for data changes, defined by a carefully crafted transactional consistency boundary.
- **Root Entity (Aggregate Root)**: The single, specific Entity contained within an Aggregate that acts as the gateway for all external access and state modifications.
- **Invariant**: A true business rule or constraint that must always be kept transactionally consistent throughout the lifetime of the Aggregate.
- **Transactional Consistency**: Immediate, atomic consistency achieved within a single database transaction.
- **Eventual Consistency**: Consistency achieved over time (usually via Domain Events and asynchronous subscribers) across multiple disconnected Aggregates.
- **Optimistic Concurrency**: A versioning strategy (e.g., incrementing a version number) used to prevent simultaneous, overlapping modifications by different clients from corrupting Aggregate state.
- **Law of Demeter**: The principle of least knowledge; an object should invoke methods only on itself, its parameters, instantiated objects, or its direct parts.
- **Tell, Don't Ask**: A design principle where client objects tell a server object what to do via command methods, rather than asking for its state to make decisions externally.

@Objectives
- Establish strict transactional consistency boundaries around the smallest possible cluster of domain objects.
- Prevent concurrency contention and transactional failures in multi-user environments by eliminating false invariants.
- Ensure high performance, fast load times, and massive scalability by avoiding large object graphs and deep relational loading.
- Promote distributed architectures and system autonomy by aggressively decoupling Aggregates.
- Enforce strict information hiding so that internal Aggregate state cannot be manipulated outside the Root Entity's control.

@Guidelines

### 1. Invariants and Consistency Boundaries
- The AI MUST define Aggregate boundaries strictly based on true business invariants (rules that MUST instantly be up-to-date), not on UI convenience or false assumptions of object graph composition.
- The AI MUST strictly enforce the golden rule of Aggregate design: **Modify only ONE Aggregate instance per transaction.**
- If a use case demands the modification of multiple Aggregates, the AI MUST reject atomic transactions and utilize **Eventual Consistency** instead.

### 2. Sizing and Composition (Design Small Aggregates)
- The AI MUST design small Aggregates, ideally limiting them to a single Root Entity and a minimal number of attributes or Value-typed properties.
- When evaluating whether a child object should be an Entity or a Value Object, the AI MUST favor Value Objects. If the child part can be completely replaced when it changes rather than continuously modified over a long life cycle, it MUST be modeled as a Value Object.
- The AI MUST NOT design large-cluster Aggregates (e.g., a `Product` Aggregate holding thousands of `BacklogItem` instances).

### 3. Referencing Other Aggregates
- The AI MUST NOT use direct object references (pointers) to other Aggregates.
- The AI MUST reference external Aggregates exclusively by their **Globally Unique Identity** (e.g., using `ProductId` instead of a `Product` object reference).
- This constraint ensures Aggregates remain small, avoids unintended cross-Aggregate mutations, and enables seamless distribution across NoSQL stores or remote network boundaries.

### 4. Eventual Consistency
- The AI MUST implement Eventual Consistency when business rules span multiple Aggregates. 
- The AI MUST facilitate this by having the modified Aggregate publish a Domain Event. Asynchronous subscribers (in separate transactions) MUST listen to this event and update the other necessary Aggregates.
- To determine if Eventual Consistency is appropriate, the AI MUST ask "Whose job is it?" If it is the current user's job to make the data consistent, use transactional consistency. If it is another user's job or the system's job, use eventual consistency.

### 5. Breaking the Rules
- The AI MAY break the rules of Aggregates (e.g., modifying multiple Aggregates in one transaction or using direct object references) ONLY under the following strict conditions:
  1. **User Interface Convenience**: When the UI supports batch creation of multiple distinct Aggregate instances at once.
  2. **Lack of Technical Mechanisms**: When the system completely lacks asynchronous messaging, background timers, or threading capabilities.
  3. **Global Transactions**: When legacy enterprise policies strictly mandate two-phase commits (XA/2PC).
  4. **Query Performance**: When direct object references are absolute necessities to satisfy critical query performance SLAs (e.g., theta joins).

### 6. Encapsulation, Navigation, and Dependency Management
- The AI MUST NOT inject Repositories or Domain Services into Aggregate instances.
- To resolve dependencies, the AI MUST use an Application Service to look up required objects (using a Repository or Domain Service) *before* invoking the Aggregate's command method, and pass the resolved objects/data in as parameters.
- The AI MUST apply **Law of Demeter** and **Tell, Don't Ask**. The Root Entity MUST NOT expose internal parts in a way that allows clients to mutate them directly. All state-altering commands MUST be explicitly declared on the Root Entity's interface.

### 7. Optimistic Concurrency
- The AI MUST implement optimistic concurrency (e.g., a `version` attribute) on the Root Entity to protect invariants from concurrent client modifications.

@Workflow
1. **Analyze Invariants**: When given a set of domain requirements, identify the true business invariants. Separate real transactional constraints from mere compositional conveniences.
2. **Define the Root**: Establish the Root Entity. Assign it a globally unique identity (e.g., UUID or DB sequence).
3. **Minimize the Cluster**: Strip the Aggregate down. Retain only properties required to maintain the identified invariants. Convert mutable child Entities to immutable Value Objects where possible.
4. **Sever Object Graph Links**: Replace any direct object references to other Aggregates with ID-based Value Objects (e.g., replace `Customer customer` with `CustomerId customerId`).
5. **Implement Command Methods**: Define explicit, intention-revealing methods on the Root Entity to handle state transitions. Ensure these methods "Tell, Don't Ask" and guard invariants.
6. **Publish Domain Events**: If a command method's success requires a change in another Aggregate, construct the method to mutate the local state and publish a Domain Event.
7. **Manage Dependencies in Application Service**: Write the Application Service to load the Aggregate, load any required dependencies, invoke the Aggregate's command, and save the Aggregate. Do not inject Repositories into the Aggregate.

@Examples (Do's and Don'ts)

### 1. Aggregate Sizing and References
- **[DON'T]** Model large clusters with direct object references.
```java
// ANTI-PATTERN: Large cluster, false invariants, direct object references
public class Product extends Entity {
    private ProductId productId;
    private Set<BacklogItem> backlogItems; // Causes massive lazy-loading & concurrency conflicts
    private Set<Release> releases;
    
    public void planBacklogItem(BacklogItem item) {
        this.backlogItems.add(item);
    }
}
```

- **[DO]** Design small Aggregates referencing parents/partners by identity.
```java
// CORRECT: Small Aggregate, Identity reference
public class BacklogItem extends ConcurrencySafeEntity {
    private BacklogItemId backlogItemId;
    private ProductId productId; // Referenced by ID, not object
    private TenantId tenantId;
    private BacklogItemStatus status;

    public BacklogItem(TenantId tenantId, ProductId productId, BacklogItemId backlogItemId) {
        this.tenantId = tenantId;
        this.productId = productId;
        this.backlogItemId = backlogItemId;
    }
}
```

### 2. Dependency Resolution
- **[DON'T]** Inject Repositories into Aggregates (Disconnected Domain Model).
```java
// ANTI-PATTERN: Injecting Repository into Aggregate
public class BacklogItem extends Entity {
    @Autowired
    private TeamRepository teamRepository; // NEVER do this

    public void assignTeamMember(String memberId) {
        Team team = teamRepository.findTeamFor(this.tenantId);
        // ...
    }
}
```

- **[DO]** Resolve dependencies in the Application Service and pass them to the Aggregate.
```java
// CORRECT: Application Service handles lookups, Aggregate takes parameters
public class ProductBacklogItemService {
    @Transactional
    public void assignTeamMemberToTask(String tenantId, String backlogItemId, String teamMemberId) {
        BacklogItem backlogItem = backlogItemRepo.backlogItemOfId(tenantId, backlogItemId);
        Team team = teamRepo.teamOfId(tenantId, backlogItem.teamId()); // Looked up BEFORE invoking Aggregate
        
        backlogItem.assignTeamMemberToTask(new TeamMemberId(teamMemberId), team);
    }
}
```

### 3. Multi-Aggregate Updates (Eventual Consistency)
- **[DON'T]** Modify multiple Aggregates in a single transaction.
```java
// ANTI-PATTERN: Modifying multiple aggregates in one transaction
@Transactional
public void commitBacklogItemToSprint(String backlogItemId, String sprintId) {
    BacklogItem item = repo.findItem(backlogItemId);
    Sprint sprint = repo.findSprint(sprintId);
    
    item.setStatus(COMMITTED);
    sprint.addCommittedItem(item); // Violates single-aggregate-per-transaction rule
}
```

- **[DO]** Modify one Aggregate and publish a Domain Event for eventual consistency.
```java
// CORRECT: Modify one, publish event
public class BacklogItem extends Entity {
    public void commitTo(SprintId sprintId) {
        this.sprintId = sprintId;
        this.status = BacklogItemStatus.COMMITTED;
        
        DomainEventPublisher.instance().publish(
            new BacklogItemCommitted(this.tenantId, this.backlogItemId, this.sprintId)
        );
    }
}

// Separate asynchronous listener handles the Sprint update
public class BacklogItemCommittedListener {
    public void handleEvent(BacklogItemCommitted event) {
        Sprint sprint = sprintRepo.findSprint(event.sprintId());
        sprint.registerCommittedItem(event.backlogItemId());
    }
}
```

### 4. Encapsulation (Law of Demeter & Tell, Don't Ask)
- **[DON'T]** Expose internal parts for client mutation.
```java
// ANTI-PATTERN: Asking for internal parts and modifying them
Product product = repo.productOfId(productId);
for (ProductBacklogItem item : product.getBacklogItems()) {
    if (item.getId().equals(targetId)) {
        item.setOrdering(newOrdering); // Client manipulates inner parts directly
    }
}
```

- **[DO]** Tell the Root Entity what to do via an explicit command.
```java
// CORRECT: Tell, Don't Ask
Product product = repo.productOfId(productId);
product.reorderBacklogItem(targetId, newOrdering); // Root controls the transition

// Inside Product class:
public void reorderBacklogItem(BacklogItemId id, int newOrdering) {
    for (ProductBacklogItem item : this.backlogItems) {
        item.reorderFrom(id, newOrdering); // Root delegates to inner part safely
    }
}
```