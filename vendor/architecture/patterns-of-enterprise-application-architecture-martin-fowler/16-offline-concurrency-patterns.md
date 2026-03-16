@Domain
Trigger these rules when the user requests help designing, implementing, refactoring, or debugging long-running business transactions, systems spanning multiple HTTP requests or database transactions, or offline concurrency control mechanisms (optimistic locking, pessimistic locking, aggregate locking, or implicit locking frameworks).

@Vocabulary
- **Offline Concurrency**: Concurrency control for data manipulated across multiple underlying system/database transactions (a business transaction).
- **System Transaction**: A single, short-lived transaction managed by the database or transaction monitor.
- **Business Transaction**: A logical sequence of work from the user's perspective that spans multiple requests and multiple system transactions.
- **Optimistic Offline Lock**: A strategy that prevents conflicts by detecting concurrent modifications at commit time and rolling back the transaction if a conflict occurred.
- **Pessimistic Offline Lock**: A strategy that prevents conflicts by forcing a business transaction to acquire a lock on data before loading or modifying it.
- **Exclusive Write Lock**: A pessimistic lock required only to edit data (allows concurrent reads).
- **Exclusive Read Lock**: A pessimistic lock required to read or edit data (severely restricts concurrency).
- **Read/Write Lock**: A pessimistic lock combination where read and write locks are mutually exclusive, but concurrent read locks are permitted.
- **Coarse-Grained Lock**: A single lock that covers a group of related objects (an aggregate), eliminating the need to lock each object individually.
- **Shared Lock**: A type of Coarse-Grained Lock where all items in a group share the same lockable token (e.g., a shared version object).
- **Root Lock**: A type of Coarse-Grained Lock where locking the root object of an aggregate implicitly locks all members of that aggregate.
- **Implicit Lock**: A framework or layer supertype mechanism that automatically acquires offline locks, preventing developers from forgetting to apply locking mechanics.
- **Lock Manager**: An infrastructure component (often a database table or a pinned singleton) responsible for granting, denying, and releasing pessimistic locks.
- **Inconsistent Read**: A concurrency failure where a transaction reads data that has been modified by another concurrent transaction, leading to logic executing on stale data.

@Objectives
- Ensure data integrity and consistency across long-running business transactions without relying on long-running database transactions.
- Maximize system liveness and concurrency by defaulting to Optimistic Offline Locks unless conflict probability or cost is prohibitively high.
- Prevent lost updates and inconsistent reads across spanning requests.
- Protect system concurrency by eliminating the risk of deadlocks in offline locking schemes (e.g., fail immediately rather than waiting for pessimistic locks).
- Remove the burden of manual lock management from domain logic developers by implementing Implicit Locks.
- Reduce database contention and locking overhead by clustering associated objects under a single Coarse-Grained Lock.

@Guidelines

**Optimistic Offline Lock Rules**
- ALWAYS use Optimistic Offline Lock as the default offline concurrency strategy, assuming the chance of conflict is low.
- MUST use a numeric version field or counter for optimistic checks. NEVER use system timestamps for concurrency checks, as system clocks are unreliable across distributed servers.
- MUST execute the validation (version check) and the data update within the *same* final system transaction.
- Implement updates by placing the version number in the SQL `WHERE` clause (e.g., `UPDATE ... WHERE id = ? AND version = ?`).
- MUST inspect the database row count returned by the `UPDATE` or `DELETE` statement. If the row count is `0`, the AI MUST throw a Concurrency/Conflict Exception and roll back the system transaction.
- MUST increment the version number upon any successful update.
- To prevent inconsistent reads, MUST track objects that are read but not modified, and verify their versions haven't changed at commit time (or increment their versions if the system transaction isolation level is weaker than repeatable read).
- Provide a `checkCurrent` method if the business transaction is complex, allowing the system to fail early before the final commit, but never rely on it as a substitute for the final commit-time check.

**Pessimistic Offline Lock Rules**
- ONLY use Pessimistic Offline Lock when the chance of conflict is high or the business cost of throwing away user work is unacceptable.
- MUST acquire the lock *before* loading the data to guarantee the data loaded is the most current version.
- NEVER wait or block for a pessimistic lock. The Lock Manager MUST throw an exception immediately if a lock is unavailable, thereby completely eliminating the risk of deadlocks.
- MUST store locks in a centralized Lock Manager (a database table for clustered application servers; an in-memory singleton ONLY for single-server setups).
- MUST bind lock ownership to a specific session (e.g., HTTP Session ID or Application Session ID).
- MUST implement a timeout or session-binding listener (e.g., `HttpSessionBindingListener`) to automatically clear locks if a user abandons the session or the client crashes.
- All lock acquisitions and database loads MUST be grouped within a single system transaction.

**Coarse-Grained Lock Rules**
- MUST apply a Coarse-Grained Lock to an Aggregate (a cluster of associated objects treated as a unit for data changes).
- For a Shared Lock, MUST ensure all objects in the group map to the exact same version instance in the Identity Map.
- For a Root Lock, MUST implement child-to-parent navigation so that saving/locking a child object navigates to and locks the root object.
- MUST use Lazy Load when navigating from child to root to prevent infinite loops and avoid unnecessary performance hits.

**Implicit Lock Rules**
- NEVER require application developers to explicitly write lock acquisition or version incrementing code in their domain logic or Transaction Scripts.
- MUST factor locking mechanics into the application framework, Layer Supertype, Data Mapper, or Decorator.
- For Optimistic Locks, the Unit of Work MUST automatically handle version checking and incrementing during the commit phase.
- For Pessimistic Locks, MUST use a Decorator (e.g., a `LockingMapper` that wraps a standard `Mapper`) to automatically intercept `find()` calls and invoke `LockManager.acquireLock()` before executing the query.

@Workflow
1. **Context Assessment**: Determine if the requested transaction spans multiple HTTP requests or user think-time. If yes, an offline concurrency pattern is required.
2. **Strategy Selection**: Assess the conflict probability.
   - Low probability -> Select Optimistic Offline Lock.
   - High probability / strict business rules -> Select Pessimistic Offline Lock.
3. **Granularity Definition**: Identify if the objects form an Aggregate. If multiple related objects are edited together (e.g., Order and LineItems), apply a Coarse-Grained Lock (Root or Shared).
4. **Optimistic Implementation**:
   - Add a `version` integer to the target tables and Layer Supertype.
   - Modify the Data Mapper's `UPDATE` and `DELETE` SQL to include `AND version = ?`.
   - Implement row count validation (if `0`, throw `ConcurrencyException`).
5. **Pessimistic Implementation**:
   - Create a Lock Manager using a database `lock` table (columns: `lockable_id`, `owner_id`).
   - Implement `acquireLock` (insert row) and `releaseLock` (delete row).
   - Hook lock release to the HTTP session expiration.
6. **Implicit Factoring**: Hide the chosen locking mechanism behind a `UnitOfWork` (for optimistic commit checks) or a `LockingMapper` decorator (for pessimistic read locks).

@Examples (Do's and Don'ts)

**Optimistic Offline Lock**
[DO] Implement updates checking the version and verifying the row count:
```java
public void update(DomainObject object) {
    PreparedStatement stmt = conn.prepareStatement(
        "UPDATE customer SET name = ?, version = ? WHERE id = ? AND version = ?"
    );
    stmt.setString(1, object.getName());
    stmt.setInt(2, object.getVersion() + 1);
    stmt.setLong(3, object.getId());
    stmt.setInt(4, object.getVersion());
    
    int rowCount = stmt.executeUpdate();
    if (rowCount == 0) {
        throw new ConcurrencyException("Record modified by another user.");
    }
    object.setVersion(object.getVersion() + 1);
}
```
[DON'T] Use timestamps for concurrency checks:
```java
// ANTI-PATTERN: Timestamps are unreliable across clustered nodes
UPDATE customer SET name = ? WHERE id = ? AND modified_timestamp = ? 
```

**Pessimistic Offline Lock**
[DO] Fail immediately if a lock is unavailable to avoid deadlocks:
```java
public void acquireLock(Long lockable, String owner) {
    if (!hasLock(lockable, owner)) {
        try {
            // Attempt to insert lock record
            pstmt = conn.prepareStatement("INSERT INTO lock (lockableid, ownerid) VALUES (?, ?)");
            pstmt.setLong(1, lockable);
            pstmt.setString(2, owner);
            pstmt.executeUpdate();
        } catch (SQLException ex) {
            // Throw exception IMMEDIATELY if insert fails due to unique constraint
            throw new ConcurrencyException("Unable to lock " + lockable + ", already in use.");
        }
    }
}
```
[DON'T] Wait for locks across offline business transactions using `SELECT ... FOR UPDATE` that blocks indefinitely.

**Coarse-Grained Lock**
[DO] Increment the root object's version when saving the aggregate:
```java
public void commit() {
    for (DomainObject object : modifiedObjects) {
        // Navigate to the root of the aggregate and increment its version
        for (DomainObject owner = object; owner != null; owner = owner.getParent()) {
            owner.getVersion().increment();
        }
    }
}
```
[DON'T] Lock every child object individually, causing massive lock table contention or massive version-check queries.

**Implicit Lock**
[DO] Use a decorator to abstract pessimistic lock acquisition away from the business logic:
```java
class LockingMapper implements Mapper {
    private Mapper impl;
    
    public DomainObject find(Long id) {
        // Framework implicitly acquires lock before the developer's logic proceeds
        LockManager.INSTANCE.acquireLock(id, AppSessionManager.getSession().getId());
        return impl.find(id);
    }
}
```
[DON'T] Require the developer to manually write `LockManager.acquireLock()` inside their UI controllers or domain models.