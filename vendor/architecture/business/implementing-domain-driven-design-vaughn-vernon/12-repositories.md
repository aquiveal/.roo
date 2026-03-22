@Domain
Trigger these rules when the user requests to create, modify, or test data storage, data access layers, persistence mechanisms, or Repositories for Domain-Driven Design (DDD) entities and Aggregates.

@Vocabulary
- **Repository**: A mechanism that provides the illusion of an in-memory collection of all objects of a specific Aggregate type. It abstracts away the underlying persistence mechanism.
- **Aggregate Root**: The single Entity within an Aggregate boundary that external objects are allowed to hold references to. Repositories are provided ONLY for Aggregate Roots.
- **Collection-Oriented Repository**: A repository design that strictly mimics a standard `Set` collection. Objects are added once, and subsequent modifications to the retrieved objects are automatically tracked and saved by the persistence mechanism (e.g., Hibernate).
- **Persistence-Oriented Repository**: A repository design used for data stores that do not implicitly track changes (e.g., NoSQL, Data Fabrics, MongoDB, Riak, Coherence). Requires explicit `save()` or `put()` operations for both new and modified objects.
- **Implicit Copy-on-Read / Copy-on-Write**: Persistence mechanism behaviors (like Hibernate) that automatically track changes to objects, enabling Collection-Oriented Repositories.
- **Explicit Copy-before-Write**: A persistence behavior (like TopLink's UnitOfWork) where the client must explicitly register an object for modification to get an editable clone.
- **Data Access Object (DAO)**: A pattern that wraps database tables and provides fine-grained CRUD operations. Distinct from a Repository, which has domain object (Aggregate) affinity. DAOs should be avoided in DDD in favor of Repositories.
- **Use Case Optimal Query**: A specific Repository finder method that executes a complex query to dynamically compose and return a custom Value Object (instead of a full Aggregate) tailored strictly for a specific UI view/use case.
- **In-Memory Repository**: A testing implementation of a Repository interface backed by a `HashMap` to facilitate fast testing of Application Services without requiring a database.

@Objectives
- The AI MUST restrict the creation of Repositories strictly to Aggregate Roots.
- The AI MUST hide all infrastructural persistence details (SQL, ORM annotations, DB exceptions) behind a clean, collection-like domain interface.
- The AI MUST strictly separate the Repository Interface (placed in the Domain Layer) from the Repository Implementation (placed in the Infrastructure Layer).
- The AI MUST ensure that transaction management is exclusively handled in the Application Layer, never inside the Domain Layer or the Repository itself.

@Guidelines
- **Aggregate Restriction**: The AI MUST NOT create a Repository for inner Entities or Value Objects. A Repository MUST ONLY be created for an Aggregate Root.
- **1:1 Mapping**: The AI MUST generally maintain a one-to-one relationship between an Aggregate type and a Repository.
- **Orientation Selection**:
  - If the project uses an ORM with implicit change tracking (e.g., Hibernate/JPA), the AI MUST default to a **Collection-Oriented Repository** using methods like `add()` and `remove()`. Do NOT include a `save()` method for updates.
  - If the project uses NoSQL, Key-Value stores, Data Fabrics, or aims to decouple completely from ORM mechanics, the AI MUST default to a **Persistence-Oriented Repository** using methods like `save()` (for both insert and update) and `remove()`.
- **Method Return Types**: The AI MUST use `void` return types for `add()`, `save()`, and `remove()` methods. Do not return `boolean` like standard Java collections, because true success is deferred until the database transaction commits.
- **Identity Generation**: The AI MUST provide a `nextIdentity()` method on the Repository interface to generate globally unique identifiers (e.g., UUIDs or DB sequences) before or during Aggregate instantiation.
- **Exception Wrapping**: The AI MUST catch infrastructure-specific exceptions (e.g., `ConstraintViolationException`) inside the Repository implementation and throw domain-friendly or standard language exceptions (e.g., `IllegalStateException` or `IllegalArgumentException`).
- **Additional Behavior**: The AI MAY add a `size()` method to mimic collection behaviors.
- **Use Case Optimal Queries**: The AI MAY add finder methods that return a custom Value Object (instead of an Aggregate) to optimize read performance for specific UI views. However, the AI MUST flag excessive use of this pattern as a code smell ("Repository masks Aggregate mis-design"), which may indicate the need for CQRS.
- **Transaction Management**: The AI MUST NOT place transaction annotations (e.g., `@Transactional`), commits, or rollbacks inside the Repository or Domain Model. Transactions MUST be managed in the Application Service Facade.
- **Type Hierarchies**: If Aggregates form a class hierarchy, the AI MUST use a single shared Repository ONLY if the subclasses obey the Liskov Substitution Principle (LSP) and clients use them interchangeably. Otherwise, prefer explicit Standard Types (Value Objects) over subclassing.
- **Anti-DAO Pattern**: The AI MUST NOT create methods in the Repository that perform CRUD operations on the internal parts of an Aggregate.

@Workflow
1. **Analyze the Target**: Verify that the domain concept requiring storage is an Aggregate Root. If it is an internal Entity, halt Repository creation and instruct the user to access it via its Aggregate Root.
2. **Determine Persistence Orientation**: Assess the underlying data store. Select Collection-Oriented (`add`/`remove`) for state-tracking ORMs. Select Persistence-Oriented (`save`/`remove`) for NoSQL, document stores, or abstract safety.
3. **Define the Interface**: Create the Repository interface in the Domain Layer (e.g., `com.project.domain.model.calendar.CalendarEntryRepository`). Define `nextIdentity()`, `add()` or `save()`, `remove()`, and domain-specific finder methods (e.g., `calendarEntryOfId()`).
4. **Implement the Repository**: Create the implementation class in the Infrastructure Layer (e.g., `com.project.infrastructure.persistence.HibernateCalendarEntryRepository`).
5. **Handle Exceptions**: Implement the methods, ensuring all ORM/DB exceptions are caught and rethrown as standard/domain exceptions.
6. **Manage Transactions**: Ensure the Application Service (the client of the Repository) initiates and commits the transaction, passing the context (Session/UnitOfWork) implicitly to the Repository.
7. **Create Testing Mocks**: Generate an In-Memory implementation of the Repository backed by a `HashMap` for fast Application Service unit testing.

@Examples (Do's and Don'ts)

[DO] Define a Collection-Oriented Repository interface in the Domain Layer.
```java
package com.saasovation.collaboration.domain.model.calendar;

public interface CalendarEntryRepository {
    public CalendarEntryId nextIdentity();
    public void add(CalendarEntry aCalendarEntry);
    public void remove(CalendarEntry aCalendarEntry);
    public CalendarEntry calendarEntryOfId(Tenant aTenant, CalendarEntryId aCalendarEntryId);
    public Collection<CalendarEntry> calendarEntriesOfCalendar(Tenant aTenant, CalendarId aCalendarId);
}
```

[DON'T] Define a DAO-style interface that leaks DB concepts, returns booleans for saves, or updates internal Aggregate parts.
```java
public interface CalendarEntryDAO {
    public boolean insertCalendarEntry(CalendarEntry entry);
    public boolean updateCalendarEntry(CalendarEntry entry);
    // Anti-pattern: Updating an internal part of an Aggregate directly
    public void updateCalendarEntryLocation(CalendarEntryId id, String newLocation); 
}
```

[DO] Define a Persistence-Oriented Repository interface when using NoSQL or Data Fabrics (e.g., MongoDB, Coherence).
```java
package com.saasovation.agilepm.domain.model.product;

public interface ProductRepository {
    public ProductId nextIdentity();
    public void save(Product aProduct); // Handles both creation and update
    public void remove(Product aProduct);
    public Product productOfId(Tenant aTenant, ProductId aProductId);
}
```

[DO] Implement the Repository in the Infrastructure Layer and wrap framework exceptions.
```java
package com.saasovation.collaboration.infrastructure.persistence;

public class HibernateCalendarEntryRepository implements CalendarEntryRepository {
    private SessionProvider sessionProvider;

    @Override
    public void add(CalendarEntry aCalendarEntry) {
        try {
            this.session().saveOrUpdate(aCalendarEntry);
        } catch (ConstraintViolationException e) {
            throw new IllegalStateException("CalendarEntry is not unique.", e);
        }
    }
    
    private org.hibernate.Session session() {
        return this.sessionProvider.session();
    }
    // ...
}
```

[DON'T] Manage transactions inside the Repository or Domain Model.
```java
// Anti-pattern: Transaction management inside the Repository
public class BadProductRepository implements ProductRepository {
    @Override
    public void save(Product aProduct) {
        Transaction tx = this.session().beginTransaction();
        this.session().save(aProduct);
        tx.commit(); // NO! Transactions belong in the Application Service.
    }
}
```

[DO] Manage transactions in the Application Layer (Application Service).
```java
package com.saasovation.agilepm.application;

public class ProductBacklogItemService {
    @Autowired
    private BacklogItemRepository backlogItemRepository;

    @Transactional // Transaction is managed here
    public void planProductBacklogItem(String aTenantId, String aProductId, String aSummary) {
        Product product = productRepository.productOfId(new TenantId(aTenantId), new ProductId(aProductId));
        BacklogItem plannedItem = product.planBacklogItem(aSummary);
        
        backlogItemRepository.add(plannedItem);
    }
}
```

[DO] Create an In-Memory Repository implementation for testing Application Services.
```java
package com.saasovation.agilepm.domain.model.product.impl;

public class InMemoryProductRepository implements ProductRepository {
    private Map<ProductId, Product> store = new HashMap<ProductId, Product>();

    @Override
    public void save(Product aProduct) {
        this.store.put(aProduct.productId(), aProduct);
    }

    @Override
    public Product productOfId(Tenant aTenant, ProductId aProductId) {
        Product product = this.store.get(aProductId);
        if (product != null && !product.tenant().equals(aTenant)) {
            return null;
        }
        return product;
    }
    // ...
}
```