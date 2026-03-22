@Domain
These rules MUST be activated when the AI is tasked with designing, refactoring, or implementing data access layers, transaction management, multithreading logic, state management across requests, or any system handling concurrent user data manipulation. Trigger conditions include requests involving database mapping, session state, thread-safety in application servers, optimistic/pessimistic locking, or resolving data conflicts.

@Vocabulary
- **Lost Update**: A concurrency failure where one session's updates are unknowingly overwritten by another session's commit.
- **Inconsistent Read**: A concurrency failure where a session reads two pieces of data that are correct individually but not correct at the same time (e.g., reading data mid-update).
- **Correctness (Safety)**: The degree to which a system prevents concurrency problems (like lost updates and inconsistent reads).
- **Liveness**: The amount of concurrent activity a system allows. Often inversely proportional to Correctness.
- **Request**: A single call from the outside world that the software processes and responds to.
- **Session**: A long-running interaction between a client and a server, often spanning multiple requests (e.g., login to logout).
- **Process**: A heavyweight execution context that provides strict memory isolation for internal data.
- **Thread**: A lightweight execution agent operating within a process. Threads share memory, causing concurrency issues.
- **System Transaction**: A transaction supported directly by an RDBMS or transaction monitor.
- **Business Transaction**: A transaction from the user's perspective (e.g., selecting items and checking out). Often spans multiple requests and system transactions.
- **Long Transaction**: An anti-pattern where a single system transaction is kept open across multiple requests.
- **Isolation**: A technique to avoid concurrency problems by partitioning data so it can only be accessed by one active agent.
- **Immutability**: Data that cannot be modified. It bypasses concurrency problems and can be shared freely.
- **Optimistic Locking (Optimistic Offline Lock)**: A conflict-detection concurrency strategy. Allows concurrent edits but validates for conflicts via version markers immediately before committing.
- **Pessimistic Locking (Pessimistic Offline Lock)**: A conflict-prevention concurrency strategy. Locks data upon read, preventing other sessions from accessing or modifying it until released.
- **Deadlock**: A situation where two or more transactions wait indefinitely for locks held by each other.
- **ACID**: Atomicity, Consistency, Isolation, Durability. The core properties of transactions.
- **Lock Escalation**: When a database replaces many row-level locks with a single table-level lock, drastically reducing concurrency.
- **Serializable**: The highest transaction isolation level. Guarantees results identical to executing transactions sequentially.
- **Repeatable Read**: Isolation level that prevents unrepeatable reads but allows Phantoms.
- **Read Committed**: Isolation level that prevents dirty reads but allows Unrepeatable Reads.
- **Read Uncommitted**: The lowest isolation level. Allows Dirty Reads.
- **Phantom**: A read error where a collection query returns new elements inserted by another transaction during the current transaction.
- **Unrepeatable Read**: A read error where reading the same data twice yields different results because another transaction updated it in between.
- **Dirty Read**: A read error where a transaction reads uncommitted changes from another transaction.
- **Offline Concurrency**: Concurrency management handled by the application (spanning multiple system transactions) rather than the database.
- **Coarse-Grained Lock**: A single lock used to manage the concurrency of a group of related objects (an aggregate).
- **Implicit Lock**: Framework-level or Layer Supertype-level lock management that prevents developers from forgetting to acquire offline locks.

@Objectives
- Maximize system Liveness (throughput and concurrency) without compromising necessary Correctness (data integrity).
- Ensure Business Transactions strictly adhere to ACID properties even when spanning multiple System Transactions.
- Prevent Lost Updates and Inconsistent Reads using the least restrictive locking strategy appropriate for the business case.
- Eliminate manual thread synchronization and explicit multithreaded programming in application servers by relying on process isolation or strict object creation per request.

@Guidelines

**1. Transaction Management Constraints**
- The AI MUST NOT design or implement System Transactions that span multiple user requests (Long Transactions). System Transactions MUST be kept as short as possible.
- The AI MUST align System Transactions to begin and end within the lifespan of a single Request (Request Transaction).
- If late transactions are used (opening the transaction only when updating), the AI MUST implement manual checks to prevent Inconsistent Reads.
- The AI MUST NOT place database locks on tables corresponding to a Domain Layer Supertype, to aggressively prevent database Lock Escalation that would freeze the entire system.

**2. Optimistic vs. Pessimistic Concurrency Control**
- The AI MUST default to Optimistic Offline Lock for business transactions unless the requirements explicitly state that conflicts are highly probable or the cost of a user losing work is strictly unacceptable.
- When implementing Optimistic Offline Locks, the AI MUST use a sequential integer version counter. The AI MUST NOT use system timestamps for version checks due to inherent server clock unreliability.
- When implementing Optimistic Offline Locks to prevent Inconsistent Reads, the AI MUST only check versions of data actively relied upon for calculations, rather than all data read, to avoid unnecessary transaction failures.
- When implementing Pessimistic Offline Locks, the AI MUST mitigate Deadlocks using highly conservative, automated schemes: either enforcing a strict order of lock acquisition (e.g., alphabetical), acquiring all needed locks at the very start of the transaction, or implementing strict time limits (Timeouts).

**3. Application Server Concurrency & Multithreading**
- The AI MUST avoid explicit synchronization blocks or explicit thread locks (`synchronized`, `lock()`) in business application code.
- If Thread-per-Request is used, the AI MUST enforce isolated zones by creating fresh, new objects for each request session. 
- The AI MUST NOT use static variables, class-based mutables, or Singleton patterns for mutable data in a multi-threaded application server. 
- If global memory is strictly required, the AI MUST use a thread-scoped Registry (e.g., `ThreadLocal`) rather than a static Singleton.
- Database connections MUST be pooled and acquired explicitly, as they are too expensive to instantiate fresh per request.

**4. Offline Lock Implementation Rules**
- The AI MUST encapsulate Offline Concurrency control logic within Framework classes or Layer Supertypes (Implicit Lock). Business logic developers MUST NOT be forced to explicitly call lock acquisition methods.
- The AI MUST use Coarse-Grained Locks for aggregate object clusters. Lock the root of the aggregate or share a version object across the aggregate to prevent locking overhead.
- In Pessimistic Offline Lock, the AI MUST release all locks immediately if a session is abandoned, utilizing HTTP session timeout listeners or timestamp expiration.

@Workflow
When architecting or modifying a system requiring concurrency management, the AI MUST execute the following steps:

1. **Execution Context Mapping:** Identify the boundaries of Requests, Sessions, and System Transactions. Map out where Business Transactions span multiple System Transactions.
2. **Immutability Extraction:** Identify all read-only or immutable data. Isolate this data from concurrency mechanisms to instantly improve Liveness.
3. **Isolation Level Tuning:** Determine the exact transaction isolation level required for the operation. Start at Serializable for safety, and downgrade to Repeatable Read or Read Committed *only* if Liveness/performance benchmarks demand it, accepting the specific read errors (Phantoms, Unrepeatable Reads) associated with the downgrade.
4. **Lock Strategy Selection:** Default to Optimistic Offline Lock. If the business context dictates that conflict resolution is impossible or unacceptable, switch to Pessimistic Offline Lock.
5. **Lock Granularity Definition:** If the operation edits an aggregate (e.g., a Customer and their Addresses), design a Coarse-Grained Lock via a Shared Version or a Root Lock to minimize lock acquisition calls.
6. **Implicit Framework Integration:** Embed the chosen locking strategy into a Layer Supertype or a Data Mapper so that the acquisition and verification of locks occur automatically on `load()`, `update()`, or `commit()`.
7. **Thread-Safety Review:** Ensure the application server code contains no mutable static fields. Verify that the request handler instantiates entirely isolated object graphs.

@Examples (Do's and Don'ts)

**[DO] Use integer version counters for Optimistic Locking in SQL.**
```sql
-- Correct Implementation of Optimistic Lock Check
UPDATE customer 
SET name = ?, modified = ?, version = version + 1 
WHERE id = ? AND version = ?;
```

**[DON'T] Use timestamps for Optimistic Locking.**
```sql
-- Anti-pattern: Clocks across clustered servers can be out of sync
UPDATE customer 
SET name = ?, modified = ? 
WHERE id = ? AND modified = ?; 
```

**[DO] Create fresh objects per request to avoid multithreading issues.**
```java
// Correct: Creating a new isolated object graph per request
public void handleRequest(HttpServletRequest request) {
    CustomerService service = new CustomerService(); 
    service.process(request.getParameter("id"));
}
```

**[DON'T] Use singletons or static variables for mutable data in a Web Server.**
```java
// Anti-pattern: Threads will clash over this shared mutable state
public class CustomerService {
    private static Customer currentCustomer; // FATAL: Thread collision
    
    public static void process(String id) {
        currentCustomer = db.find(id);
        currentCustomer.calculate();
    }
}
```

**[DO] Use Coarse-Grained Locks for Aggregates.**
```java
// Correct: Modifying a child implicitly increments the parent's version lock
public class Address extends DomainObject {
    public void updateCity(String newCity) {
        this.city = newCity;
        this.getCustomer().getVersion().increment(); // Coarse-Grained Lock
    }
}
```

**[DON'T] Leave business transaction state locked indefinitely.**
```java
// Anti-pattern: No timeout or session listener to release locks if user abandons browser
public class EditCustomerCommand {
    public void process() {
        // Locks the record, but never releases if the user navigates away
        PessimisticLockManager.acquireLock(customerId, session.getId());
        forward("/editCustomer.jsp"); 
    }
}
```

**[DO] Use Implicit Locks within Mapper or Repository logic.**
```java
// Correct: The framework acquires the lock, the developer doesn't have to remember
public class LockingMapper implements Mapper {
    public DomainObject find(Long id) {
        ExclusiveReadLockManager.INSTANCE.acquireLock(id, AppSessionManager.getSession().getId());
        return impl.find(id);
    }
}
```