# @Domain
These rules MUST trigger when the AI is tasked with designing, refactoring, or implementing simple business logic, specifically operating within supporting subdomains, generic subdomain integrations, ETL (extract-transform-load) processes, or basic CRUD (create, read, update, delete) operations. These rules govern the application of the `Transaction Script` and `Active Record` architectural patterns. Do NOT apply these rules to Core Subdomains or complex business logic featuring intricate state transitions, complex invariants, or rich business rules.

# @Vocabulary
- **Transaction Script**: A business logic implementation pattern organized by procedures, where each procedure handles a single, complete request from the presentation layer and acts as an encapsulation boundary.
- **Active Record**: An object that wraps a row in a database table or view, encapsulates the database access (CRUD), and adds basic domain logic (e.g., validation) on that data.
- **Distributed Transaction**: A transaction spanning multiple independent storage mechanisms or communication channels (e.g., updating a database and publishing to a message bus).
- **Implicit Distributed Transaction**: An operation that updates a local database but also communicates a success/failure state to an external caller or process, creating a vulnerability where the caller's state and the database state can easily desynchronize (e.g., a caller retries a successful increment operation because the network response failed).
- **Idempotency**: A characteristic of an operation ensuring that multiple identical requests yield the exact same result as a single request, preventing data corruption on retries.
- **Optimistic Concurrency Control**: A strategy to protect data consistency by verifying that the data has not been altered by another process before applying an update (e.g., passing an expected current value as a condition for the update).
- **Anemic Domain Model**: A term historically used as an anti-pattern when Active Records are mistakenly used to model complex business domains; within this domain, it is recognized as a valid tool solely for simple business logic.

# @Objectives
- Implement simple business logic with minimal abstraction and maximum efficiency, avoiding the accidental complexity of over-engineered domain models.
- Guarantee strict transactional behavior for all operations: procedures MUST entirely succeed or entirely fail without leaving the system in an invalid state.
- Prevent data corruption caused by incomplete multi-record updates, network timeouts, or unhandled distributed transactions.
- Bridge the gap between in-memory data structures and database schemas efficiently using Active Records when data structures are complex but behavior remains simple.

# @Guidelines
- **Strict Transactional Enforcement**: Every transaction script or Active Record orchestration MUST be wrapped in an explicit transaction block. If an operation fails, all changes up to the failure point MUST be rolled back or reversed via compensating actions.
- **Avoid Blind Multi-Record Updates**: NEVER issue multiple database updates (e.g., updating a user record and inserting a log record) sequentially without an overarching database transaction.
- **Mitigate Implicit Distributed Transactions**: When implementing operations that modify data and return a success/failure response to a caller over a network, you MUST protect against network failures that trigger blind retries.
- **Apply Idempotency**: Convert blind increment or append operations (e.g., `visits = visits + 1`) into idempotent operations by requiring the caller to supply the calculated target value.
- **Apply Optimistic Concurrency**: Alternatively, require the caller to supply the currently known state, and strictly condition the database update on that state matching the database's current state (e.g., `WHERE expected_value = @val`).
- **Avoid Distributed Transactions Across Mechanisms**: Do NOT mix database commits and message bus publishing within a simple transaction script. If an operation requires updating a database and publishing a message, recognize it as a distributed transaction and halt to recommend CQRS or Outbox patterns (outside the scope of simple Transaction Scripts).
- **Use Transaction Script for Flat Data**: Apply the Transaction Script pattern for ETL processes, data conversions, or straightforward integrations where data structures are relatively flat.
- **Use Active Record for Complex Structures**: Apply the Active Record pattern when the business logic is simple (CRUD/validation) but the data structures are complex trees or hierarchies. Separate the data structure from behavior (e.g., expose public getters and setters) but encapsulate the database mapping.
- **Limit Active Record Responsibilities**: Active Records MAY contain basic business logic (like validating input fields) but MUST NOT contain complex workflow orchestration. Orchestration MUST reside in the calling Transaction Script.
- **Pragmatic Consistency Exception**: Data consistency guarantees MAY only be relaxed in high-scale, massive-throughput environments (e.g., ingesting billions of IoT events) where the business explicitly accepts a minimal error rate (e.g., 0.001% duplication) to preserve performance.

# @Workflow
1. **Analyze Business Logic Complexity**: Evaluate the requested feature. If it involves complex business rules, intricate state transitions, or is a Core Subdomain, halt and recommend the Domain Model pattern. If it is simple CRUD, ETL, or supporting functionality, proceed.
2. **Evaluate Data Structure**:
   - If the data is flat and the operation is strictly procedural (e.g., read file, transform, write to DB), select the **Transaction Script** pattern.
   - If the data involves complex relationships (one-to-many, object trees) but logic is just CRUD, select the **Active Record** pattern.
3. **Define Transactional Boundaries**: Identify all state modifications that belong to the single operation.
4. **Draft the Implementation**:
   - Initialize an explicit transaction (`StartTransaction`).
   - Perform the database queries, Active Record manipulations, or external API calls.
   - Commit the transaction (`Commit`).
   - Catch any exceptions, roll back the transaction (`Rollback`), and rethrow or return an error response.
5. **Audit for Distributed Vulnerabilities**: Review the operation for "Implicit Distributed Transactions". If the operation performs relative updates (e.g., +1, append) and is called over a network, refactor the parameters to enforce Idempotency or Optimistic Concurrency Control.

# @Examples (Do's and Don'ts)

## Transactional Behavior
**[DO]** Wrap multiple database updates in a strict transaction block to prevent partial updates.
```csharp
public class LogVisit 
{
    public void Execute(Guid userId, DateTime visitedOn) 
    {
        try 
        {
            _db.StartTransaction();
            _db.Execute("UPDATE Users SET last_visit=@p1 WHERE user_id=@p2", visitedOn, userId);
            _db.Execute("INSERT INTO VisitsLog(user_id, visit_date) VALUES(@p1, @p2)", userId, visitedOn);
            _db.Commit();
        } 
        catch 
        {
            _db.Rollback();
            throw;
        }
    }
}
```

**[DON'T]** Execute multiple database operations sequentially without an overarching transaction, risking data corruption on failure.
```csharp
public class LogVisit 
{
    public void Execute(Guid userId, DateTime visitedOn) 
    {
        // ANTI-PATTERN: If the second query fails, the first query is committed, leaving inconsistent state.
        _db.Execute("UPDATE Users SET last_visit=@p1 WHERE user_id=@p2", visitedOn, userId);
        _db.Execute("INSERT INTO VisitsLog(user_id, visit_date) VALUES(@p1, @p2)", userId, visitedOn);
    }
}
```

## Handling Implicit Distributed Transactions
**[DO]** Use Optimistic Concurrency Control (or Idempotency) to protect against network retries causing duplicate data modification.
```csharp
public class LogVisit 
{
    // Optimistic Concurrency: Caller must provide the expected current visits count
    public void Execute(Guid userId, long expectedVisits) 
    {
        _db.Execute(
            "UPDATE Users SET visits=visits+1 WHERE user_id=@p1 AND visits=@p2", 
            userId, expectedVisits
        );
    }
}
```

**[DON'T]** Use blind relative updates in endpoints that might be retried due to network timeouts.
```csharp
public class LogVisit 
{
    public void Execute(Guid userId) 
    {
        // ANTI-PATTERN: If network drops after DB commit, caller retries, adding +2 visits incorrectly.
        _db.Execute("UPDATE Users SET visits=visits+1 WHERE user_id=@p1", userId);
    }
}
```

## Active Record Orchestration
**[DO]** Use a Transaction Script to orchestrate the instantiation, mapping, and saving of Active Record objects within an explicit database transaction.
```csharp
public class CreateUser 
{
    public void Execute(UserDetails userDetails) 
    {
        try 
        {
            _db.StartTransaction();
            
            var user = new User();
            user.Name = userDetails.Name;
            user.Email = userDetails.Email;
            user.Save(); // Active Record handles its own persistence mapping
            
            _db.Commit();
        } 
        catch 
        {
            _db.Rollback();
            throw;
        }
    }
}
```

**[DON'T]** Attempt to embed complex, multi-aggregate business workflows or distributed message publishing directly inside the `Save()` method of an Active Record. Keep the Active Record focused purely on data structure mapping and simple row-level validation.