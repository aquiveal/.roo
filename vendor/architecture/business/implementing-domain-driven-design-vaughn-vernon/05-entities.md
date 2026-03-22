@Domain
These rules are triggered whenever the AI is requested to design, implement, review, or refactor Domain Model classes, specifically focusing on Entities, their life cycles, unique identities, construction, validation, and domain-specific behaviors.

@Vocabulary
- **Entity**: A domain concept whose individuality and identity must be tracked across time and distinct states, regardless of how its attributes change.
- **Value Object**: A domain concept that describes, measures, or quantifies something, possessing no unique identity.
- **Anemic Domain Model**: An anti-pattern where domain objects are mere data holders (heavy on getters and setters) devoid of domain behavior.
- **Ubiquitous Language**: The shared language developed by the team (domain experts and developers) that must be explicitly reflected in the code (class names, method names).
- **Domain Identity**: The unique, business-meaningful identifier of an Entity.
- **Surrogate Identity**: A technical, framework-specific identifier (e.g., ORM database primary key) used solely for persistence mechanisms.
- **Self-Encapsulation**: The practice of accessing an object's own data strictly through its private/protected accessor methods, even from within its own constructors or behavior methods.
- **Guard / Precondition**: An assertion inside a setter or behavior method that ensures an invariant is maintained (e.g., throwing an `IllegalArgumentException` on null).
- **Deferred Validation**: A complex validation check performed on a whole Entity or composition of Entities, decoupled from the Entity's internal state modifiers.
- **Intention-Revealing Interface**: Methods named according to the business intent (e.g., `activate()`, `changePassword()`) rather than technical operations (e.g., `setActive()`, `setPassword()`).
- **Layer Supertype**: An abstract base class used to centralize and hide infrastructural/surrogate persistence attributes (e.g., `IdentifiedDomainObject`).

@Objectives
- Model domain concepts as Entities ONLY when identity and life cycle continuity are absolute requirements; otherwise, favor Value Objects.
- Eradicate CRUD-based, Anemic Domain Models by enforcing Intention-Revealing Interfaces that mirror the Ubiquitous Language.
- Ensure strict stability, uniqueness, and early generation of Entity identity.
- Prevent infrastructure and persistence leakages (like ORM surrogate keys) from polluting the domain model interface.
- Guarantee that an Entity is always in a valid state upon construction and after any behavioral mutation via self-encapsulation and guards.
- Decouple complex, whole-object validation logic from the Entity itself by using dedicated Validator classes.

@Guidelines
- **Entity vs. Value Object Selection**: The AI MUST analyze requirements using the concepts of "change" versus "replace". If a concept's attributes change over time but it remains the same "thing", model it as an Entity. If it is completely replaceable, model it as a Value Object.
- **Identity Representation**: The AI MUST model Domain Identity as a strongly typed Value Object (e.g., `TenantId`, `ProductId`) rather than a primitive `String` or `Long` to prevent accidental misuse and enhance expressiveness.
- **Identity Generation & Timing**: 
  - The AI MUST favor early identity generation (e.g., using `UUID` or querying the Repository for a sequence *before* instantiation). 
  - The AI MUST NOT rely on late identity generation (e.g., DB auto-increment on save) for Entities that will be placed in a `java.util.Set` or that publish Domain Events upon creation, as a null/default ID will break equality checks and Event contracts.
- **Surrogate Identity Isolation**: If an ORM (like Hibernate) requires a database primary key, the AI MUST create a Surrogate Identity separate from the Domain Identity. The AI MUST hide this surrogate key in a Layer Supertype (e.g., `IdentifiedDomainObject`) using private or protected visibility.
- **Identity Stability**: The AI MUST make Domain Identity immutable. The AI MUST implement guards in identity setters that throw an `IllegalStateException` if the identity is already set.
- **Self-Encapsulation**: The AI MUST use private or protected setters for all attributes. Constructors and public behavior methods MUST delegate to these setters to ensure all Guards and Preconditions are universally enforced.
- **Intention-Revealing Behaviors**: The AI MUST NOT generate generic CRUD setters (e.g., `setStatus()`) for domain operations. The AI MUST generate methods named after business actions (e.g., `commitTo()`, `deactivate()`).
- **Object Construction**: The AI MUST ensure constructors take all required parameters to satisfy the Entity's invariants. A protected/private zero-argument constructor MAY be provided ONLY if required by an ORM.
- **Guards and Preconditions**: The AI MUST validate attributes immediately within their respective setter methods (e.g., checking for null, empty strings, length limits, formats) and throw an `IllegalArgumentException` on failure.
- **Deferred Validation (Whole Object)**: For complex validation requiring the inspection of the entire Entity state, the AI MUST NOT embed this logic in the Entity's domain behaviors. The AI MUST define a separate `Validator` class (using the Specification or Strategy pattern) that gathers all errors via a `ValidationNotificationHandler`.
- **Role Interfaces**: If an Entity plays multiple roles, the AI SHOULD consider using fine-grained role interfaces (e.g., `IAddOrdersToCustomer`) to prevent object schizophrenia and explicitly define client capabilities.

@Workflow
When requested to design or implement an Entity, the AI MUST execute the following steps strictly in order:
1. **Analyze the Ubiquitous Language**: Extract nouns and verbs from the provided requirements to identify the Entity name and its explicit business behaviors.
2. **Design the Domain Identity**: Create a custom Value Object for the Identity. Determine the generation strategy (UUID, DB Sequence, User-provided, Bounded Context integration). Ensure the timing of generation is "early".
3. **Define the Surrogate Identity (if applicable)**: If using an ORM, implement a Layer Supertype to abstract and hide the DB primary key.
4. **Implement State and Self-Encapsulation**: Define the internal state attributes. Implement private/protected setters with strict Guards/Preconditions for every attribute. Ensure identity setters throw exceptions if modification is attempted after initialization.
5. **Implement Constructors**: Create a primary constructor that accepts all properties required for a valid initial state. Have the constructor invoke the private/protected setters (Self-Encapsulation) to populate the state. Add a hidden no-arg constructor if required by the ORM.
6. **Implement Intention-Revealing Behaviors**: Create public methods using domain terminology to handle state mutations. Avoid public property setters. If state changes, consider tracking via Domain Events.
7. **Implement Deferred Validation (Optional)**: If complex whole-object validation is required, create an accompanying `Validator` and `ValidationNotificationHandler` in the same module. Define a `validate(ValidationNotificationHandler)` method on the Entity that delegates to the `Validator`.

@Examples (Do's and Don'ts)

[DO] Implement Identity Stability and Self-Encapsulation
```java
public class User extends Entity {
    private TenantId tenantId;
    private String username;

    protected User(TenantId aTenantId, String aUsername) {
        super();
        this.setTenantId(aTenantId);
        this.setUsername(aUsername);
    }

    protected void setUsername(String aUsername) {
        if (this.username != null) {
            throw new IllegalStateException("The username may not be changed.");
        }
        if (aUsername == null || aUsername.trim().isEmpty()) {
            throw new IllegalArgumentException("The username must be provided.");
        }
        this.username = aUsername;
    }

    protected void setTenantId(TenantId aTenantId) {
        if (aTenantId == null) {
            throw new IllegalArgumentException("The tenantId may not be null.");
        }
        this.tenantId = aTenantId;
    }
}
```

[DON'T] Leave Identity mutable or expose generic CRUD setters
```java
public class User {
    public String username;
    
    // BAD: Identity is mutable, no guards, no self-encapsulation
    public void setUsername(String username) {
        this.username = username; 
    }
}
```

[DO] Hide Surrogate ORM Identity in a Layer Supertype
```java
public abstract class IdentifiedDomainObject implements Serializable {
    private long id = -1; // Surrogate key

    protected IdentifiedDomainObject() {
        super();
    }

    protected long id() {
        return this.id;
    }

    protected void setId(long anId) {
        this.id = anId;
    }
}

public class User extends IdentifiedDomainObject {
    private TenantId tenantId; // Actual Domain Identity
    // ...
}
```

[DON'T] Mix Surrogate Identity with Domain Identity in the public interface
```java
public class User {
    public long id; // BAD: Exposes DB primary key to domain clients
    public TenantId tenantId; 
}
```

[DO] Implement Intention-Revealing Interfaces for behaviors
```java
public class Tenant extends Entity {
    private boolean active;

    // GOOD: Mirrors Ubiquitous Language, hides internal state representation
    public void activate() {
        if (!this.isActive()) {
            this.setActive(true);
            // publish TenantActivated event
        }
    }

    public void deactivate() {
        if (this.isActive()) {
            this.setActive(false);
            // publish TenantDeactivated event
        }
    }

    protected void setActive(boolean anActive) {
        this.active = anActive;
    }
}
```

[DON'T] Use generic status setters for business operations
```java
public class Tenant extends Entity {
    private boolean active;

    // BAD: Forces client to understand internal state logic, no explicit business intent
    public void setActive(boolean active) {
        this.active = active;
    }
}
```

[DO] Use separate Validator classes for complex Deferred Validation
```java
public class WarbleValidator extends Validator {
    private Warble warble;

    public WarbleValidator(Warble aWarble, ValidationNotificationHandler aHandler) {
        super(aHandler);
        this.warble = aWarble;
    }

    @Override
    public void validate() {
        if (this.warble.hasWarpedCondition()) {
            this.notificationHandler().handleError("The warble is warped.");
        }
        if (this.warble.hasWackyState()) {
            this.notificationHandler().handleError("The warble has a wacky state.");
        }
    }
}

public class Warble extends Entity {
    public void validate(ValidationNotificationHandler aHandler) {
        new WarbleValidator(this, aHandler).validate();
    }
}
```

[DON'T] Embed complex whole-object validation and throw immediate exceptions inside the Entity
```java
public class Warble extends Entity {
    // BAD: Fails fast on the first error, clutters the domain object with validation logic
    public void validate() {
        if (this.hasWarpedCondition()) {
            throw new RuntimeException("The warble is warped."); 
        }
        if (this.hasWackyState()) {
            throw new RuntimeException("The warble has a wacky state.");
        }
    }
}
```