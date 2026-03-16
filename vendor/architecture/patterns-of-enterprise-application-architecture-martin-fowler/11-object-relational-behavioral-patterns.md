# @Domain
Trigger this rule file when the task involves object-relational behavioral mapping, specifically coordinating database reads and writes across business transactions, managing in-memory object identity and consistency, optimizing database reads for related objects, and resolving offline concurrency tracking. 

# @Vocabulary
*   **Unit of Work**: An object that maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems.
*   **Identity Map**: A map that keeps a record of all objects that have been read from the database in a single business transaction to ensure each object gets loaded only once.
*   **Lazy Load**: An object that does not contain all of the data you need but contains a marker or reference to know how to get it from the database when accessed.
*   **Caller Registration**: A Unit of Work strategy where the client code manually registers changed objects with the Unit of Work.
*   **Object Registration**: A Unit of Work strategy where domain objects automatically register themselves (e.g., as dirty, new, or removed) with the Unit of Work during their normal execution.
*   **Unit of Work Controller**: A strategy where the Unit of Work intercepts all database reads, takes a copy of the read object, and compares the object state at commit time to determine what changed.
*   **System Transaction**: A transaction enforced directly by the underlying database or transaction monitor.
*   **Business Transaction**: A logical sequence of work from the user's perspective, often spanning multiple requests and multiple system transactions.
*   **Explicit Identity Map**: An Identity Map utilizing distinct, strongly-typed methods for each object type (e.g., `findPerson(1)`).
*   **Generic Identity Map**: An Identity Map utilizing a single, untyped method for all objects (e.g., `find("Person", 1)`).
*   **Lazy Initialization**: A Lazy Load implementation where a field access first checks if the field is null, and if so, loads the data before returning it.
*   **Virtual Proxy**: A Lazy Load implementation where an empty object perfectly mimics the target object's interface, loading the real data from the database only when one of its methods is invoked.
*   **Value Holder**: A Lazy Load implementation where a wrapper object explicitly holds the lazy value, requiring the client to call a `getValue()` method to trigger the load.
*   **Ghost**: A Lazy Load implementation where the real object is instantiated in a partial state (typically just its ID) and triggers a full load of its fields the first time any property is accessed.
*   **Ripple Loading**: A severe performance anti-pattern where iterating over a collection of Lazy Load objects triggers a separate database query for every single object.

# @Objectives
*   Defer and batch database updates to the end of a business transaction to minimize database calls and keep system transactions short.
*   Ensure that multiple queries for the same database row within a session always return the exact same in-memory object instance to avoid update conflicts and inconsistent reads.
*   Prevent loading massive graphs of objects from the database by deferring the retrieval of related objects until they are explicitly accessed by the application.
*   Abstract the tracking of database insertions, updates, and deletions away from business logic.

# @Guidelines
### Unit of Work
*   **Track State Changes**: Track all new, dirty, and removed objects inside the Unit of Work. Do not execute database updates immediately when object state changes.
*   **Centralized Commit**: The Unit of Work must dictate what to do at commit time. It must open a system transaction, perform concurrency checking (e.g., Optimistic Offline Lock), execute the required inserts, updates, and deletes, and then commit.
*   **Object Registration Preference**: Prefer Object Registration over Caller Registration. Domain objects should notify the Unit of Work when they are altered to prevent developers from forgetting to register changes.
*   **Thread Safety**: A Unit of Work must be scoped to the session or request. Ensure multiple threads cannot access the same Unit of Work (e.g., store it in a thread-scoped Registry like Java's `ThreadLocal`).
*   **Referential Integrity Ordering**: Use the Unit of Work to sequence database writes correctly to satisfy database foreign-key constraints (e.g., insert parent before child, delete child before parent).
*   **Batch Updates**: Whenever supported by the platform, the Unit of Work should utilize batched SQL statements to minimize remote calls.

### Identity Map
*   **Check Before Loading**: Always check the Identity Map before issuing a database query for an object by its ID. If present, return the mapped object.
*   **Register on Load**: Whenever an object is newly instantiated from database data, immediately place it into the Identity Map to break cyclic references during complex object graph loads.
*   **Key Selection**: Use the database primary key as the map key. If using compound keys, create a generic Key class with fast equality operations.
*   **Map Scoping**: Usually scope the Identity Map to a single session/Unit of Work. For strictly immutable objects, you may use a process-scoped (global) Identity Map to maximize caching performance.
*   **Interface Explicitness**: Prefer Explicit Identity Maps (strongly typed methods) over Generic Identity Maps to preserve compile-time checking and explicit interfaces.
*   **Inheritance Handling**: Use a single Identity Map for an entire inheritance tree rather than splitting maps per subclass, which complicates polymorphic lookups.

### Lazy Load
*   **Target Selection**: Apply Lazy Load to related objects that require an extra database call to access and are not always needed when the primary object is used.
*   **Avoid LOB Laziness**: Do not use Lazy Load on fields stored in the same database row (like Serialized LOBs) because the database has already paid the cost to retrieve the data.
*   **Prevent Ripple Loading**: Do not populate a collection with individual Lazy Load proxies. Instead, make the collection itself a Lazy Load (e.g., a Ghost List) so that the first access loads all collection elements in a single query.
*   **Proxy Identity Warning**: If using Virtual Proxies, be aware that the proxy has a different object identity than the real object. Override equality methods, or restrict Virtual Proxies strictly to collections where identity issues are less prevalent.
*   **Null Semantics**: If using Lazy Initialization, be careful if `null` is a valid domain value. If `null` is valid, use a Special Case object to represent an unloaded state.

# @Workflow
1.  **Session Start**: Upon beginning a business transaction/request, instantiate a Unit of Work and bind it to the current thread or session context. Initialize empty Identity Maps within this Unit of Work.
2.  **Object Retrieval**: When the application requests an object by ID, the Data Mapper queries the Identity Map. 
    *   If found, return the in-memory instance. 
    *   If not found, issue the `SELECT` statement, instantiate the object (or Ghost), register it as "clean" with the Unit of Work, put it in the Identity Map, and return it.
3.  **Graph Traversal**: If the application accesses a related object that is not yet loaded, trigger the Lazy Load mechanism (e.g., Virtual Proxy invokes the loader interface). Retrieve the data and place the new object into the Identity Map.
4.  **State Modification**: As the application mutates domain objects or adds/removes relationships, the domain objects call `UnitOfWork.getCurrent().registerDirty(this)` or `registerNew(this)`.
5.  **Commit Phase**: When the business transaction completes, the application calls `commit()` on the Unit of Work.
6.  **Database Sync**: The Unit of Work opens a database transaction, checks version stamps for optimistic locking, executes `INSERT` for new objects, `UPDATE` for dirty objects, and `DELETE` for removed objects (ordered by referential integrity), and commits the transaction.
7.  **Cleanup**: Unbind and destroy the Unit of Work from the thread/session context.

# @Examples (Do's and Don'ts)

### Unit of Work: Object Registration
*   **[DO]** Encapsulate Unit of Work registration within the domain object's mutator methods so the caller doesn't have to manage state tracking.
```java
class Album extends DomainObject {
    public void setTitle(String title) {
        this.title = title;
        UnitOfWork.getCurrent().registerDirty(this);
    }
}
```
*   **[DON'T]** Require the client code to manually track changes and invoke explicit update methods during a complex business transaction.
```java
// Anti-pattern: Caller Registration forces the client to remember to save
album.setTitle("New Title");
albumMapper.update(album); // Unnecessary DB call right now
```

### Identity Map: Breaking Cycles and Avoiding Duplicates
*   **[DO]** Check the Identity Map before fetching, and immediately insert the object into the Identity Map upon creation, *before* loading its relationships.
```java
protected DomainObject abstractFind(Long id) {
    DomainObject result = (DomainObject) loadedMap.get(id);
    if (result != null) return result;
    
    ResultSet rs = executeQuery(id);
    result = createEmptyObject(id);
    loadedMap.put(id, result); // Put before loading children to avoid cycles
    doLoad(result, rs); 
    return result;
}
```
*   **[DON'T]** Issue a query without checking the map, returning a second instance of a database row that will overwrite or conflict with the first instance.
```java
// Anti-pattern: Blindly loading without checking Identity Map
public DomainObject find(Long id) {
    ResultSet rs = executeQuery(id);
    return load(rs); // May create duplicate in-memory object for same ID
}
```

### Lazy Load: Collections and Ripple Loading
*   **[DO]** Create a lazy collection wrapper (Ghost List) that loads all related items in a single query when the collection is first accessed.
```java
class VirtualList implements List {
    private List source;
    private VirtualListLoader loader;
    
    private List getSource() {
        if (source == null) source = loader.load(); // Loads all elements in one query
        return source;
    }
    public int size() { return getSource().size(); }
    // ... delegate other methods
}
```
*   **[DON'T]** Query a list of IDs and create a Lazy Load proxy for each individual item, which causes a new query to fire on every iteration step.
```java
// Anti-pattern: Ripple Loading
for (ProxyItem item : lazyItems) {
    item.getName(); // Triggers a separate SELECT query for every single item
}
```