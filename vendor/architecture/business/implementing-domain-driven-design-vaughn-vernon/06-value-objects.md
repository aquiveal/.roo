@Domain
These rules are triggered when the AI is tasked with designing, implementing, refactoring, testing, or persisting Domain-Driven Design (DDD) models, specifically when analyzing domain concepts to determine if they should be Entities or Value Objects, and when authoring classes that measure, quantify, or describe concepts in the domain.

@Vocabulary
- **Value Object**: A domain concept that measures, quantifies, or describes a thing in the domain. It is characterized by immutability, value equality, and replaceability.
- **Conceptual Whole (Meaningful Whole)**: A Value Object composed of multiple related attributes that only provide cohesive meaning when grouped together as an integral unit (e.g., `amount` + `currency` = `MonetaryValue`).
- **Replaceability**: The characteristic of changing a Value Object's state by completely replacing the object reference with a new instance, rather than mutating the existing instance.
- **Value Equality**: Determining object equality by comparing the types and all corresponding attributes of two instances, rather than relying on a unique identity.
- **Side-Effect-Free Function**: An operation (CQS Query) that produces output or derives a new state without modifying the object's own internal state.
- **Standard Type (Type Code / Lookup)**: Descriptive objects that indicate the types of things (e.g., Currency, Phone Number Type). Modeled as Enums or Value Objects.
- **Enum-as-State**: A pattern utilizing language enums to implement the State pattern elegantly, embedding state-specific behaviors directly within enum constants.
- **Data Model Leakage**: An anti-pattern where the requirements of the persistence mechanism (e.g., relational databases requiring primary keys for collections) inappropriately force a domain concept to be modeled as an Entity instead of a Value Object.
- **Surrogate Identity**: A database-only primary key used to persist a Value Object collection as database entities. It must be strictly hidden from the domain model.
- **Layer Supertype**: An abstract base class (e.g., `IdentifiedValueObject`) used to encapsulate and hide infrastructural or surrogate identity details from the pure domain model.

@Objectives
- Strive to model domain concepts as Value Objects instead of Entities wherever logically possible.
- Guarantee strict immutability, value equality, and side-effect-free behaviors for all Value Object implementations.
- Prevent data model and ORM requirements from polluting the domain model; maintain the conceptual purity of Value Objects even if they are backed by database entities.
- Reduce integration complexity between Bounded Contexts by translating complex upstream Aggregates into simple, immutable downstream Value Objects (Integration with Minimalism).
- Express the Ubiquitous Language through fluent, business-centric method names, explicitly rejecting mechanical JavaBean-style getters/setters.

@Guidelines

**1. Modeling Choices: Value Object vs. Entity**
- The AI MUST evaluate every domain concept to see if it measures, quantifies, or describes a thing in the domain. If it does, and it does not require a continuous lifecycle with unique identity tracking, it MUST be modeled as a Value Object.
- The AI MUST challenge any assumption that an object must be an Entity simply because its attributes change. Instead, employ the **Replaceability** principle (swap the old Value Object with a new one).

**2. Conceptual Wholeness**
- The AI MUST NOT leave related attributes scattered across an Entity (e.g., `amount` and `currency`).
- The AI MUST group related attributes into a single strongly typed Value Object (e.g., `MonetaryValue`).
- If an Entity contains multiple attributes that naturally form a descriptive concept, the AI MUST extract them into a Value Object.

**3. Immutability and State Encapsulation**
- Value Objects MUST be completely immutable.
- The AI MUST use a primary constructor that initializes all state atomically.
- The AI MUST NOT implement public setter methods.
- The AI MUST use private, self-encapsulating setter methods called ONLY by the primary constructor to initialize state. These private setters MUST contain all Guard assertions (e.g., null checks, length checks, format validation).
- The AI MUST provide a protected or private zero-argument constructor strictly for ORM/framework reflection mechanisms.

**4. Side-Effect-Free Behavior**
- Methods on a Value Object MUST NOT mutate its internal state.
- If a domain behavior requires altering the value, the AI MUST implement a method that returns a *newly instantiated* Value Object with the updated state (e.g., `name.withMiddleInitial("L")`).
- The AI MUST avoid passing Entity references into Value Object methods if doing so risks mutating the Entity's state. Value Object methods should ideally accept and return only other Value Objects or primitives.

**5. Expressive, Fluent Interfaces**
- The AI MUST name methods according to the Ubiquitous Language.
- The AI MUST NOT use the `get` prefix for property accessors (e.g., use `valuePercentage()` instead of `getValuePercentage()`).

**6. Value Equality**
- The AI MUST override `equals()` and `hashCode()` for every Value Object.
- The `equals()` method MUST compare the types and *all* attributes of the two objects.

**7. Integrating Bounded Contexts**
- When integrating with an upstream Bounded Context, the AI MUST NOT blindly replicate upstream Aggregates as downstream Aggregates.
- The AI MUST favor translating upstream Aggregates into minimal, immutable Value Objects in the downstream Context.

**8. Standard Types**
- The AI MUST model Standard Types (e.g., type codes) as Value Objects or Enums.
- When types dictate different behaviors, the AI MUST leverage the Enum-as-State pattern, declaring abstract methods on the Enum and overriding them in the specific Enum constants.

**9. Persistence and Defeating Data Model Leakage**
- The AI MUST NOT model a concept as an Entity merely because a relational database requires it to be stored in its own table with a primary key.
- **Single Value Objects**: The AI MUST persist these by denormalizing their attributes into the parent Entity's table (e.g., Hibernate `<component>`). Column names should reflect the object navigation path using underscores (e.g., `business_priority_ratings_benefit`).
- **Collections of Value Objects**: 
  - If serialized text is acceptable and querying individual attributes is unnecessary, serialize the entire collection into a single database column.
  - If a separate table is required, the AI MUST use a **Layer Supertype** (e.g., `IdentifiedValueObject` extending `IdentifiedDomainObject`) to hold a private/protected surrogate identity (`id`). The domain model MUST NOT expose this identity.
  - When replacing a collection of Value Objects in an Entity, the AI MUST call `clear()` on the existing collection before adding new items to ensure the ORM correctly deletes orphaned records.

@Workflow
When tasked with modeling or implementing a domain concept:
1. **Assess Characteristics**: Ask if the concept measures, quantifies, or describes. If yes, classify it as a Value Object.
2. **Define the Conceptual Whole**: Identify all attributes that cohesively belong together.
3. **Construct the Class**: 
   - Declare the class as `final`.
   - Implement a private zero-argument constructor for the ORM.
   - Implement a primary constructor containing all attributes.
   - Implement private setters with Guard assertions. Call these setters from the primary constructor.
4. **Implement Equality**: Override `equals()` and `hashCode()` to compare all domain attributes.
5. **Implement Behaviors**: Define fluent, Ubiquitous Language-based methods. Ensure all methods are Side-Effect-Free (returning new instances if state changes are simulated).
6. **Implement Copy Constructor**: Provide a constructor that takes an instance of its own type to facilitate shallow copying (crucial for testing).
7. **Write Tests**: Write tests demonstrating client usage. Tests MUST verify immutability by creating a copy of the Value Object, executing a behavior on the original, and asserting that the original and copy are still equal.
8. **Map Persistence**: Define the ORM mapping. Use denormalized components for single Values, or a Layer Supertype with a surrogate key for collections of Values. Ensure no database IDs are exposed to the public API.

@Examples (Do's and Don'ts)

**[DO] Create a Conceptual Whole with Fluent Accessors and Side-Effect-Free Behaviors**
```java
public final class FullName implements Serializable {
    private String firstName;
    private String lastName;

    protected FullName() { super(); } // For ORM

    public FullName(String aFirstName, String aLastName) {
        this();
        this.setFirstName(aFirstName);
        this.setLastName(aLastName);
    }

    public FullName(FullName aFullName) { // Copy constructor for testing
        this(aFullName.firstName(), aFullName.lastName());
    }

    public String firstName() { return this.firstName; }
    public String lastName() { return this.lastName; }

    // Side-Effect-Free Function
    public FullName withMiddleInitial(String aMiddleInitial) {
        // Validation omitted for brevity
        return new FullName(this.firstName() + " " + aMiddleInitial, this.lastName());
    }

    private void setFirstName(String aFirstName) {
        if (aFirstName == null || aFirstName.trim().isEmpty()) {
            throw new IllegalArgumentException("First name is required.");
        }
        this.firstName = aFirstName;
    }

    private void setLastName(String aLastName) {
        if (aLastName == null || aLastName.trim().isEmpty()) {
            throw new IllegalArgumentException("Last name is required.");
        }
        this.lastName = aLastName;
    }

    @Override
    public boolean equals(Object anObject) {
        boolean equalObjects = false;
        if (anObject != null && this.getClass() == anObject.getClass()) {
            FullName typedObject = (FullName) anObject;
            equalObjects = this.firstName().equals(typedObject.firstName()) &&
                           this.lastName().equals(typedObject.lastName());
        }
        return equalObjects;
    }

    @Override
    public int hashCode() {
        return (151513 * 229) + this.firstName().hashCode() + this.lastName().hashCode();
    }
}
```

**[DON'T] Scatter attributes in an Entity or use mutable JavaBean setters**
```java
public class Customer extends Entity {
    // DON'T: Scattered attributes failing to form a Conceptual Whole
    private String firstName; 
    private String lastName;
    private BigDecimal amount;
    private String currency;

    // DON'T: Mechanical getters and mutating setters
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getFirstName() { return this.firstName; }
}
```

**[DO] Hide Data Model Leakage using a Layer Supertype for Value Object Collections**
```java
public abstract class IdentifiedDomainObject implements Serializable {
    private long id = -1; // Surrogate key for ORM
    protected IdentifiedDomainObject() { super(); }
    protected long id() { return this.id; }
    protected void setId(long anId) { this.id = anId; }
}

public abstract class IdentifiedValueObject extends IdentifiedDomainObject {
    public IdentifiedValueObject() { super(); }
}

// The domain concept remains a Value Object, but the ORM can store it in a table
public final class GroupMember extends IdentifiedValueObject {
    private String name;
    private TenantId tenantId;
    
    // Domain methods...
}
```

**[DON'T] Promote a Value Object to an Entity just to satisfy an ORM**
```java
// DON'T: Exposing database IDs on a concept that is structurally a Value Object
public class GroupMember {
    public long databaseId; // Leaking persistence into the domain model!
    private String name;
    
    public long getDatabaseId() { return this.databaseId; }
}
```

**[DO] Implement Standard Types using Enum-as-State**
```java
public enum GroupMemberType {
    GROUP {
        @Override
        public boolean isGroup() { return true; }
    },
    USER {
        @Override
        public boolean isUser() { return true; }
    };

    public boolean isGroup() { return false; }
    public boolean isUser() { return false; }
}
```

**[DO] Test Value Objects for Immutability**
```java
public void testValuePercentageCalculation() throws Exception {
    BusinessPriority businessPriority = new BusinessPriority(new BusinessPriorityRatings(2, 4, 1, 1));
    BusinessPriority businessPriorityCopy = new BusinessPriority(businessPriority); // Copy constructor
    
    assertEquals(businessPriority, businessPriorityCopy); // Assert initial equality
    
    BusinessPriorityTotals totals = new BusinessPriorityTotals(53, 49, 102, 37, 33);
    float valuePercentage = businessPriority.valuePercentage(totals); // Execute behavior
    
    assertEquals("5.9", this.oneDecimal().format(valuePercentage));
    
    // Assert the original object was NOT mutated by the behavior
    assertEquals(businessPriorityCopy, businessPriority); 
}
```