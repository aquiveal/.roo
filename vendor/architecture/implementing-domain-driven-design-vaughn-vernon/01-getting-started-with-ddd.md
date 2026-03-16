# @Domain
These rules MUST be activated when the user requests tasks involving software modeling, system architecture, refactoring of legacy or data-centric code (CRUD/Anemic Domain Models), API design, or the creation/modification of core business logic, domain objects (Entities, Value Objects), or Application Services.

# @Vocabulary
- **Domain-Driven Design (DDD)**: An approach to developing software that focuses on bringing domain experts and software developers together to reflect the mental model of the business experts in the code.
- **Domain Model**: A specific software model of the exact business domain being worked in, typically implemented as an object model where objects contain both data and literal, accurate business behavior.
- **Domain Expert**: Individuals who know the specific line of business intimately (e.g., product designers, sales, business leaders), regardless of their formal job title.
- **Ubiquitous Language**: A pervasive, shared team language (domain experts + developers) representing business concepts and terms. It is strictly bounded to a single context and directly captured in the software model and its tests.
- **Bounded Context**: A conceptual boundary around a whole application or finite system where every term, phrase, or sentence of the Ubiquitous Language has a specific, unambiguous contextual meaning.
- **Core Domain**: A part of the business domain of primary importance to the success of the organization. It requires the highest priority and investment in tactical/strategic DDD patterns.
- **Supporting Subdomain**: A less critical area of the business that supports the Core Domain but does not warrant the highest design investment.
- **Anemic Domain Model**: An anti-pattern where domain objects are weak, lack business behaviors, and consist entirely of data accessors (public getters/setters), effectively serving as dumb data holders.
- **Transaction Script**: A procedural code design where business logic resides in services rather than in the domain objects themselves, often utilizing Anemic Domain Models.
- **Strategic Design**: The higher-level DDD patterns including Bounded Contexts, Context Maps, and the Ubiquitous Language.
- **Tactical Design**: The lower-level modeling building blocks of DDD, such as Aggregates, Entities, Value Objects, Services, and Domain Events.

# @Objectives
- The AI MUST bridge the gap between technical implementation and business intent by ensuring code design is literally exactly how the software works.
- The AI MUST eliminate translations between business requirements and technical jargon; the code must speak the Ubiquitous Language.
- The AI MUST actively identify and refactor Anemic Domain Models into behavior-rich, explicitly intention-revealing Domain Models.
- The AI MUST isolate complexity by strictly enforcing Bounded Contexts, rejecting any attempt to create a single universal model for an entire enterprise.
- The AI MUST centralize business knowledge inside the domain model rather than leaking it into user interfaces, application services, or persistence layers.

# @Guidelines
- **Enforce Ubiquitous Language**:
  - The AI MUST meticulously extract nouns, verbs, and adjectives from business requirements to name classes, methods, and variables.
  - The AI MUST NEVER use arbitrary technical jargon (e.g., `ObjectManager`, `DataProcessor`) when a precise business term exists.
- **Eradicate Anemic Domain Models**:
  - The AI MUST NOT generate domain classes consisting solely of public getters and setters (JavaBeans/property-bag style).
  - The AI MUST encapsulate data completely and expose only intention-revealing behavioral methods.
- **Bounded Context Integrity**:
  - The AI MUST NOT share the same domain object definitions across different Bounded Contexts. Concepts must be unique to their specific context.
- **Intention-Revealing Interfaces**:
  - The AI MUST design methods that reflect specific business scenarios and use cases rather than generic CRUD operations (e.g., use `relocateTo(Address)` instead of `setAddress(Address)`).
- **Application Service Constraints**:
  - Application Services MUST act ONLY as task coordinators, transaction managers, or security enforcers.
  - Application Services MUST NOT contain business rules, calculations, or domain logic. They must delegate entirely to the domain objects.
- **Complexity Justification**:
  - The AI MUST NOT use complex DDD tactical patterns for simple CRUD or data-entry subsystems. DDD MUST be reserved for the Core Domain where business rules are highly complex.
- **Test-First Discovery**:
  - When designing a new domain object, the AI MUST first write client-like test code that demonstrates how the object should be used according to the Ubiquitous Language before implementing the object itself.

# @Workflow
1. **Complexity Assessment**: Evaluate the user's request. If the domain logic is simple (CRUD), advise the user that heavy DDD tactical patterns may be overkill. If the logic is complex or part of the Core Domain, proceed with strict DDD rules.
2. **Language Extraction**: Analyze the prompt for business terminology. Formulate a Ubiquitous Language glossary (nouns for Entities/Value Objects, verbs for behaviors).
3. **Contextualization**: Identify the explicit Bounded Context for the current feature. Reject requirements that attempt to force universal concepts across contexts.
4. **Behavioral Test Design**: Write a brief, demonstrative test showing how a client (e.g., an Application Service) will interact with the domain object using the Ubiquitous Language.
5. **Model Implementation**: 
   - Define the domain object (Entity or Value Object).
   - Make all internal state private.
   - Implement the explicit behaviors discovered in step 2.
   - Add invariant guards to protect business rules.
6. **Application Service Orchestration**: Create a thin Application Service method. This method MUST ONLY:
   - Retrieve necessary domain objects from a Repository.
   - Invoke the specific, intention-revealing behavior on the domain object.
   - Save the object back to the Repository (or rely on transaction commits).
7. **Refactoring Review**: Scan the generated code for "anemia-induced memory loss" indicators (e.g., generic `save` methods, chained setters). Refactor into explicit business behaviors if found.

# @Examples (Do's and Don'ts)

## Anemic vs. Behavior-Rich Domain Objects
[DON'T]: Design objects as dumb data holders managed by procedural scripts.
```java
// Anti-Pattern: Anemic Domain Model
public class BacklogItem {
    private String sprintId;
    private String status;
    
    public void setSprintId(String sprintId) { this.sprintId = sprintId; }
    public void setStatus(String status) { this.status = status; }
}

// Client code (leaks business logic):
backlogItem.setSprintId(sprintId);
backlogItem.setStatus("COMMITTED");
```

[DO]: Design objects that encapsulate their state and expose business behaviors reflecting the Ubiquitous Language.
```java
// Correct: Behavior-Rich Domain Model
public class BacklogItem extends Entity {
    private SprintId sprintId;
    private BacklogItemStatusType status;
    
    public void commitTo(Sprint aSprint) {
        if (!this.isScheduledForRelease()) {
            throw new IllegalStateException("Must be scheduled for release to commit to sprint.");
        }
        if (this.isCommittedToSprint()) {
            if (!aSprint.sprintId().equals(this.sprintId())) {
                this.uncommitFromSprint();
            }
        }
        this.elevateStatusWith(BacklogItemStatus.COMMITTED);
        this.sprintId = aSprint.sprintId();
        
        DomainEventPublisher.instance().publish(new BacklogItemCommitted(...));
    }
}

// Client code (explicit intent):
backlogItem.commitTo(sprint);
```

## Intention-Revealing Interfaces
[DON'T]: Use a single, generic update method that handles multiple divergent business scenarios using optional parameters or null checks.
```java
// Anti-Pattern: Procedural Transaction Script
public void saveCustomer(
    String customerId, String firstName, String lastName, 
    String street, String city, String phone, String email) {
    
    Customer customer = customerDao.readCustomer(customerId);
    if (firstName != null) customer.setFirstName(firstName);
    if (street != null) customer.setStreet(street);
    // ... cognitive overload and hidden complexity
    customerDao.saveCustomer(customer);
}
```

[DO]: Break down interfaces to explicitly reflect specific business goals.
```java
// Correct: Explicit Domain Interface
public interface Customer {
    public void changePersonalName(String firstName, String lastName);
    public void relocateTo(PostalAddress changedPostalAddress);
    public void changeHomeTelephone(Telephone telephone);
    public void disconnectHomeTelephone();
    public void primaryEmailAddress(EmailAddress emailAddress);
}
```

## Application Service Orchestration
[DON'T]: Place business logic or validation inside the Application Service.
```java
// Anti-Pattern: Business logic in Application Service
@Transactional
public void changeCustomerName(String id, String first, String last) {
    Customer customer = repo.findById(id);
    if (first == null || last == null) {
        throw new Exception("Name cannot be null"); // Domain rule leaked
    }
    customer.setFirstName(first);
    customer.setLastName(last);
    repo.save(customer);
}
```

[DO]: Use the Application Service strictly for fetching, delegating to the domain object, and managing the transaction.
```java
// Correct: Thin Application Service
@Transactional
public void changeCustomerPersonalName(String customerId, String firstName, String lastName) {
    Customer customer = customerRepository.customerOfId(customerId);
    if (customer == null) {
        throw new IllegalStateException("Customer does not exist.");
    }
    
    // Delegation of business logic to the domain model
    customer.changePersonalName(firstName, lastName);
}
```