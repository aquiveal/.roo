@Domain
These rules apply whenever the AI is tasked with designing, implementing, refactoring, or testing the instantiation logic of complex objects, Aggregates, or when translating objects across Bounded Contexts. This is specifically triggered when addressing object creation patterns in a Domain-Driven Design (DDD) architecture.

@Vocabulary
- **Factory**: An object or method that shifts the responsibility of complex object or Aggregate creation away from the client, encapsulating assembly and enforcing invariants.
- **Factory Method**: A specific method placed on an Aggregate Root used to produce instances of another Aggregate type or its inner parts, expressing the Ubiquitous Language.
- **Factory on Service**: A Domain Service acting as a Factory, typically used during Bounded Context integration to translate foreign objects into local domain types.
- **Abstract Factory**: A Factory pattern utilized when creating objects of different types within a class hierarchy, allowing the client to pass basic parameters while the Factory determines the concrete type.
- **Separated Interface**: A pattern where the Factory interface is defined in the Domain layer, but its technical implementation (especially for cross-context translations) is housed in the Infrastructure layer.
- **Ubiquitous Language**: The shared, domain-specific language spoken by the team, which must dictate the naming of Factory Methods.

@Objectives
- **Encapsulate Complexity**: Shift the responsibility for creating complex objects and Aggregates to separate Factory objects or Factory Methods.
- **Enforce Invariants**: Create entire Aggregates as a single, consistent piece, ensuring all business rules and invariants are strictly enforced at the moment of creation.
- **Unburden Clients**: Reduce the number of parameters the client must provide by injecting contextual boundaries (e.g., `TenantId`, parent Aggregate IDs) internally within the Factory.
- **Safeguard Contextual Data**: Prevent the production of wrong state (e.g., creating an Aggregate under the wrong tenant) by strictly controlling identity associations within the Factory.
- **Express Ubiquitous Language**: Reject generic `create` or `new` prefixes in favor of expressive, domain-driven verbs (e.g., `scheduleCalendarEntry`, `startDiscussion`).

@Guidelines
- **Aggregate Root Factory Methods**: If an Aggregate creates instances of another Aggregate type, implement this creation as a Factory Method on the parent Aggregate Root. 
- **Constructor Hiding**: When a Factory Method is the designated way to create an object, you MUST hide the target object's constructor from clients (e.g., declare it with `protected` scope).
- **Context Injection**: The Factory Method MUST automatically supply contextual state (like `TenantId` or the parent's unique identifier) to the new object. Do NOT require the client to pass these parameters.
- **Guard Clauses**: You MUST protect the creation process using guard clauses. These can exist inside the Factory Method itself (e.g., `if (this.isClosed()) throw new IllegalStateException();`) and/or rely on the self-delegating guards within the target object's constructor.
- **Domain Event Publishing**: If the creation of the Aggregate represents a significant business occurrence, the Factory Method MUST publish a Domain Event prior to returning the newly created instance.
- **Performance Trade-offs**: Accept the performance overhead of retrieving an Aggregate Root from the persistence store purely to invoke its Factory Method; the benefits of invariant enforcement and invariant protection outweigh the cost.
- **Services as Factories (Integration)**: When integrating Bounded Contexts, use a Domain Service as a Factory to translate foreign models (e.g., a generic `User In Role` REST representation) into local, specific Value Objects (e.g., `Author`, `Moderator`).
- **Separated Interfaces for Services**: If a Factory on a Service requires technical implementation (e.g., REST adapters, JSON translation), place the interface in the Domain Model and the implementation in the Infrastructure Layer.
- **Abstract Factories for Hierarchies**: Use Abstract Factories when the domain dictates a class hierarchy, allowing the client to remain completely unaware of the specific concrete subclass being instantiated.
- **Testing Factories**: You MUST test Factory Methods by asserting that the returned instance is not null, verifying the structural integrity of the returned object, and verifying that the expected Domain Event was published.

@Workflow
1. **Identify Creation Needs**: Determine if the object being created is an Aggregate or complex Value Object requiring invariant enforcement.
2. **Determine the Host**: Decide if the creation belongs on an existing Aggregate Root (as a Factory Method) or on a Domain Service (for cross-context translation).
3. **Define the Ubiquitous Language**: Consult domain terminology to name the Factory Method (e.g., `planBacklogItem` instead of `createBacklogItem`).
4. **Design the Signature**: Define the method parameters. Require only what the client must provide. Exclude contextual identities (Tenant, Parent ID) that the host Aggregate already possesses.
5. **Implement Guards**: Add business logic checks that validate whether the creation is currently allowed (e.g., checking if a parent entity is active/open).
6. **Instantiate and Emit**: Call the hidden constructor of the target object, publish the relevant Domain Event, and return the newly created instance.
7. **Restrict Access**: Change the visibility of the target object's constructor to `protected` (or package-private) to force clients to use the Factory.

@Examples (Do's and Don'ts)

[DO] Implement a Factory Method on an Aggregate Root with an expressive name, context injection, and Domain Event publishing.
```java
public class Forum extends Entity {
    // Contextual data held by the parent Aggregate
    private TenantId tenantId;
    private ForumId forumId;
    private boolean closed;

    // Expressive Factory Method
    public Discussion startDiscussion(
            DiscussionId aDiscussionId,
            Author anAuthor,
            String aSubject) {
        
        // Guard clause enforcing business invariant
        if (this.isClosed()) {
            throw new IllegalStateException("Forum is closed.");
        }

        // Instantiation utilizing injected context (tenantId, forumId)
        Discussion discussion = new Discussion(
                this.tenantId(),
                this.forumId(),
                aDiscussionId,
                anAuthor,
                aSubject);

        // Emit Domain Event
        DomainEventPublisher.instance().publish(new DiscussionStarted(...));

        return discussion;
    }
}

public class Discussion extends Entity {
    // Constructor is protected to force usage of Forum.startDiscussion()
    protected Discussion(
            TenantId aTenantId, 
            ForumId aForumId, 
            DiscussionId aDiscussionId, 
            Author anAuthor, 
            String aSubject) {
        // Initialization logic
    }
}
```

[DON'T] Leave constructors public for complex Aggregates, rely on anemic `create` naming, or force the client to manage contextual mappings.
```java
// ANTI-PATTERN: Client bears the burden of ensuring correct tenancy and parent associations.
public class DiscussionService {
    public Discussion createDiscussion(
            TenantId tenantId, 
            ForumId forumId, 
            DiscussionId discussionId, 
            Author author, 
            String subject) {
        
        // No checks to see if the Forum is actually open!
        
        // Public constructor allows bypassing business rules
        Discussion discussion = new Discussion(tenantId, forumId, discussionId, author, subject);
        return discussion;
    }
}
```

[DO] Use a Domain Service as a Factory with a Separated Interface when translating foreign concepts into local models.
```java
// Interface in Domain Layer
public interface CollaboratorService {
    public Author authorFrom(Tenant aTenant, String anIdentity);
}

// Implementation in Infrastructure Layer
public class TranslatingCollaboratorService implements CollaboratorService {
    private UserInRoleAdapter userInRoleAdapter;

    @Override
    public Author authorFrom(Tenant aTenant, String anIdentity) {
        // Technical translation from remote REST resource to local Value Object
        return (Author) this.userInRoleAdapter.toCollaborator(
                aTenant, anIdentity, "Author", Author.class);
    }
}
```